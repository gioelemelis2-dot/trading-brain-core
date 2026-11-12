"""Schema dei valori del Guardian G0 (governance/MODELLO-EPISTEMICO.md).

Ogni numero mostrato dal G0 è un `Valore` con tipo, operazione, condizioni, incertezza, fonte e stato di verifica.
Un numero senza tipo non si può costruire. Le combinazioni applicano le regole del §4 del modello:
tipo = il più debole fra gli input (con un tetto dato dall'operazione), condizioni = unione,
stato di verifica = il più debole, NON STIMABILE contagioso, incertezza da dichiarare se un input non è esatto.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable, Optional

ORDINE_TIPO = {"IPOTESI": 1, "STIMA": 2, "DERIVATO": 3, "MISURA": 4}
TIPI = set(ORDINE_TIPO) | {"REGOLA"}
TETTO_OPERAZIONE = {"osservazione": "MISURA", "calcolo deterministico": "DERIVATO", "inferenza": "STIMA",
                    "assunzione": "IPOTESI", "norma": "REGOLA"}
ORDINE_VERIFICA = {"X": 0, "C": 1, "V-sec": 2, "V-parziale": 2, "V": 3}
ESATTO = "esatto"
NON_STIMABILE = "NON STIMABILE"


@dataclass(frozen=True)
class Valore:
    valore: Optional[Decimal]
    unita: str
    tipo: str
    operazione: str
    fonte: str
    condizioni: frozenset = field(default_factory=frozenset)
    incertezza: str = ESATTO
    stato_verifica: str = "V"
    nota: str = ""

    def __post_init__(self):
        if self.tipo not in TIPI:
            raise ValueError(f"tipo non valido: {self.tipo!r} (ammessi: {sorted(TIPI)})")
        if self.operazione not in TETTO_OPERAZIONE:
            raise ValueError(f"operazione non valida: {self.operazione!r}")
        if self.stato_verifica not in ORDINE_VERIFICA:
            raise ValueError(f"stato di verifica non valido: {self.stato_verifica!r}")
        if not self.fonte:
            raise ValueError("ogni valore deve dichiarare la fonte")
        if (self.valore is None) != (self.incertezza == NON_STIMABILE):
            raise ValueError("valore assente se e solo se l'incertezza è NON STIMABILE")
        if self.valore is not None and not isinstance(self.valore, Decimal):
            raise TypeError("il valore deve essere un Decimal (niente float nei calcoli monetari)")
        if self.tipo == "STIMA" and self.incertezza == ESATTO:
            raise ValueError("una STIMA deve dichiarare la propria incertezza (intervallo o NON STIMABILE)")
        object.__setattr__(self, "condizioni", frozenset(self.condizioni))

    @property
    def stimabile(self) -> bool:
        return self.incertezza != NON_STIMABILE


def misura(valore, unita, fonte, qualita="", stato="V") -> Valore:
    return Valore(Decimal(str(valore)), unita, "MISURA", "osservazione", fonte, stato_verifica=stato, nota=qualita)


def regola(valore, unita, fonte, stato="V", nota="") -> Valore:
    return Valore(Decimal(str(valore)), unita, "REGOLA", "norma", fonte, stato_verifica=stato, nota=nota)


def ipotesi(valore, unita, fonte, ident, nota="") -> Valore:
    """Valore assunto (per esempio una riserva prudenziale per i gap). `ident` entra nelle condizioni."""
    v = None if valore is None else Decimal(str(valore))
    return Valore(v, unita, "IPOTESI", "assunzione", fonte, condizioni=frozenset({ident}),
                  incertezza=NON_STIMABILE if v is None else ESATTO, stato_verifica="C", nota=nota)


def combina(input_: Iterable[Valore], valore, unita: str, operazione: str, fonte: str,
            condizioni_aggiunte: Iterable[str] = (), incertezza: Optional[str] = None, nota: str = "") -> Valore:
    """Crea il risultato di un'operazione applicando le regole di propagazione."""
    ins = list(input_)
    if not ins:
        raise ValueError("un risultato combinato richiede almeno un input")
    tetto = TETTO_OPERAZIONE[operazione]
    non_regole = [v.tipo for v in ins if v.tipo != "REGOLA"]
    candidati = non_regole + ([tetto] if tetto != "REGOLA" else [])
    tipo = min(candidati, key=ORDINE_TIPO.__getitem__) if candidati else "DERIVATO"
    condizioni = frozenset().union(*(v.condizioni for v in ins)) | frozenset(condizioni_aggiunte)
    stato = min((v.stato_verifica for v in ins), key=ORDINE_VERIFICA.__getitem__)
    if any(not v.stimabile for v in ins):
        return Valore(None, unita, tipo, operazione, fonte, condizioni, NON_STIMABILE, stato,
                      "almeno un input è NON STIMABILE")
    if incertezza is None:
        if any(v.incertezza != ESATTO for v in ins):
            raise ValueError("un input non è esatto: dichiarare l'incertezza propagata del risultato")
        incertezza = ESATTO
    if tipo == "STIMA" and incertezza == ESATTO:
        raise ValueError("il risultato è una STIMA: dichiarare l'incertezza")
    return Valore(Decimal(valore), unita, tipo, operazione, fonte, condizioni, incertezza, stato, nota)


def restringi(limite: Valore, candidato: Valore) -> Valore:
    """Regola aurea: una stima o un'ipotesi può solo RESTRINGERE un limite di perdita ammessa, mai allargarlo.
    `limite` e `candidato` esprimono la perdita massima ammessa (stessa unità). Restituisce il più stretto."""
    if limite.unita != candidato.unita:
        raise ValueError("unità diverse")
    if not candidato.stimabile or candidato.valore >= limite.valore:
        return limite
    return combina([limite, candidato], candidato.valore, limite.unita, "calcolo deterministico",
                   fonte=f"restringi({limite.fonte}; {candidato.fonte})",
                   incertezza=candidato.incertezza if candidato.incertezza != ESATTO else None,
                   nota="limite ristretto da una stima o ipotesi")
