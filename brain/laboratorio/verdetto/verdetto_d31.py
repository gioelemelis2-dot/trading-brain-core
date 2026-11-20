"""Verdetto della verifica secondo D-31, D-35, D-36 e D-37 (19/11/2026). Modulo nuovo fuori dal perimetro sigillato
(D-34): ha i suoi due giri di revisione.

- Metro: l'implementazione di riferimento collaudata (`studi/pilota_ia02.intervallo_bootstrap`), cioè bootstrap circolare
  a blocchi da 10, B = 3.999, intervallo basic, quota 2,5% per coda. Il modulo si rifiuta di calcolare se l'impronta
  del pilota non è quella congelata nell'impegno del collaudo (IMPEGNO-PROTOCOLLO-IA02.md).
- Segnale (D-31): favorevole se L > +0,20 R, sfavorevole se U < +0,10 R, altrimenti inconclusivo; un intervallo
  mancante, non finito, invertito o più stretto di 1e-9 R (#119, D-44) è invalido. L'uguaglianza non attraversa la soglia.
- Esiti (D-35, DGS-10 §4 opzione 2), nell'ordine: veto accertato → bocciata; dati inidonei, minimi mancanti o intervallo
  invalido → non decidibile; U < +0,10 → bocciata; L > +0,20 e requisiti superati → promossa; altrimenti non decidibile.
- Screening sullo sviluppo (D-36): media > +0,25 R, L > 0 e potenza stimata ≥ 50%.
- Veto per blocchi (D-37): soglia e minimo di trade per blocco li fissa la scheda prima del sigillo.

Vale solo per la prima apertura con una variante (quota 2,5%): una quota diversa richiede un collaudo (D-31).
"""
import hashlib
import math
import random
from pathlib import Path

from ..esecuzione import sigillo as S
from ..studi import pilota_ia02 as P

SOGLIA_PROMOZIONE = 0.20
SOGLIA_BOCCIATURA = 0.10
D_COLLAUDATO = 1000
MIN_TRADE = 300
MIN_SEDUTE_ATTIVE = 200
SCREENING_MEDIA = 0.25
SCREENING_POTENZA = 0.50
B = 3999
BLOCCO = 10
VICINANZA = 1e-9
AMPIEZZA_MINIMA = 1e-9           # #119, D-44: più stretto è un intervallo degenere (arrotondamento)
ESITI = ("promossa", "bocciata", "non decidibile")
ESITI_REQUISITO = ("superato", "fallito", "non valutabile")
IMPRONTA_PILOTA = "717e55996b23a4954d69c97722458e30c2499000b5055fdcca4cba29f864b0ee"
QUOTA = 0.025                   # D-31: la sola quota collaudata (prima apertura, una variante)
REGISTRI_EREDITATI = ("trial_registry.json", "trial_registry_xauusd.json")   # Binario B: non valgono (D-34)


def segnale(iv) -> str:
    if iv is None or P.intervallo_valido(iv[0], iv[1]) is None or iv[1] - iv[0] < AMPIEZZA_MINIMA:
        return "invalido"
    if iv[0] > SOGLIA_PROMOZIONE:
        return "favorevole"
    if iv[1] < SOGLIA_BOCCIATURA:
        return "sfavorevole"
    return "inconclusivo"


def vicini(lo: float, hi: float) -> list:
    """Estremi a meno di 1e-9 R dalla propria soglia: si riportano, non cambiano il segnale (DGS-10 testo I)."""
    out = []
    if abs(lo - SOGLIA_PROMOZIONE) < VICINANZA:
        out.append("L")
    if abs(hi - SOGLIA_BOCCIATURA) < VICINANZA:
        out.append("U")
    return out


def controlla_coppie(coppie) -> None:
    if not coppie:
        raise ValueError("nessuna seduta")
    for i, c in enumerate(coppie):
        if len(c) != 2:
            raise ValueError(f"seduta {i}: serve la coppia (S, K)")
        s, k = c
        if type(k) is not int or k < 0:
            raise ValueError(f"seduta {i}: K = {k!r} non è un intero ≥ 0")
        if type(s) not in (int, float) or not math.isfinite(s):
            raise ValueError(f"seduta {i}: S = {s!r} non è un numero finito")
        if k == 0 and s != 0:
            raise ValueError(f"seduta {i}: risultato {s} senza trade")


def minimi_mancanti(coppie) -> list:
    trade = sum(k for _, k in coppie)
    attive = sum(1 for _, k in coppie if k > 0)
    out = []
    if len(coppie) != D_COLLAUDATO:
        out.append(f"sedute: {len(coppie)} invece di {D_COLLAUDATO}")
    if trade < MIN_TRADE:
        out.append(f"trade: {trade} < {MIN_TRADE}")
    if attive < MIN_SEDUTE_ATTIVE:
        out.append(f"sedute con trade: {attive} < {MIN_SEDUTE_ATTIVE}")
    return out


def intervallo(coppie, seme: int):
    if P.impronta_modulo() != IMPRONTA_PILOTA:
        raise RuntimeError("il pilota non è la versione collaudata: impronta diversa da IMPEGNO-PROTOCOLLO-IA02")
    return P.intervallo_bootstrap(coppie, random.Random(seme), B, BLOCCO)


def contesto_prove(registro) -> dict:
    """N dal registro canonico delle prove (D-34 punto 2), con l'impronta del file letto (DGS-11 §6)."""
    registro = Path(registro)
    if registro.name in REGISTRI_EREDITATI:
        raise ValueError(f"{registro.name}: registro ereditato di Binario B, non vale per il verdetto (D-34, DA-28)")
    if not registro.is_file():
        raise ValueError(f"registro delle prove assente: {registro}")
    prima = hashlib.sha256(registro.read_bytes()).hexdigest()
    dati = S.leggi(registro)
    if hashlib.sha256(registro.read_bytes()).hexdigest() != prima:
        raise ValueError(f"{registro.name}: il registro è cambiato durante la lettura")
    return {"registro": registro.name, "n_prove": S.n_prove(dati), "impronta": prima}


def _requisiti(requisiti) -> list:
    out = []
    for r in requisiti:
        if not isinstance(r, dict) or not isinstance(r.get("id"), str) or type(r.get("veto")) is not bool \
                or r.get("esito") not in ESITI_REQUISITO:
            raise ValueError(f"requisito malformato: {r!r}")
        out.append(r)
    return out


def verdetto(coppie, seme: int, requisiti=(), contesto=None, quota=QUOTA) -> dict:
    if type(quota) is not float or quota != QUOTA:
        raise ValueError(f"quota {quota!r}: solo {QUOTA} è collaudata; un'altra richiede un collaudo (D-31)")
    req = _requisiti(requisiti)
    v = {"esito": None, "causa": None, "L": None, "U": None, "media": None, "sedute": len(coppie), "trade": None,
         "sedute_attive": None, "seme": seme, "impronta_pilota": IMPRONTA_PILOTA, "vicini_soglia": [],
         "contesto_prove": contesto, "quota": quota}

    def fine(esito, causa):
        v["esito"], v["causa"] = esito, causa
        return v

    for r in req:
        if r["veto"] and r["esito"] == "fallito":
            return fine("bocciata", f"veto: {r['id']}")
    try:
        controlla_coppie(coppie)
    except ValueError as e:
        return fine("non decidibile", f"dati inidonei: {e}")
    v["trade"] = sum(k for _, k in coppie)
    v["sedute_attive"] = sum(1 for _, k in coppie if k > 0)
    v["media"] = sum(s for s, _ in coppie) / v["trade"] if v["trade"] else None
    mancano = minimi_mancanti(coppie)
    if mancano:
        return fine("non decidibile", "minimi: " + "; ".join(mancano))
    iv = intervallo(coppie, seme)
    if iv is not None:
        v["L"], v["U"] = iv
        v["vicini_soglia"] = vicini(*iv)
    sg = segnale(iv)
    if sg == "invalido":
        return fine("non decidibile", "intervallo invalido")
    if sg == "sfavorevole":
        return fine("bocciata", "statistica: U < +0,10 R")
    if sg == "favorevole":
        aperti = [r["id"] for r in req if r["esito"] != "superato"]
        if not aperti:
            return fine("promossa", "L > +0,20 R e requisiti superati")
        return fine("non decidibile", "requisito non superato o non valutabile: " + ", ".join(aperti))
    return fine("non decidibile", "inconclusivo: L ≤ +0,20 R e U ≥ +0,10 R")


def screening(coppie, seme: int, potenza_stimata) -> dict:
    if type(potenza_stimata) not in (int, float) or not 0.0 <= potenza_stimata <= 1.0:
        raise ValueError(f"potenza stimata {potenza_stimata!r} fuori da [0, 1]")
    controlla_coppie(coppie)
    trade = sum(k for _, k in coppie)
    s = {"ammessa": False, "cause": [], "media": None, "L": None, "U": None, "seme": seme, "potenza": potenza_stimata}
    if trade == 0:
        s["cause"].append("nessun trade")
        return s
    s["media"] = sum(x for x, _ in coppie) / trade
    if not s["media"] > SCREENING_MEDIA:
        s["cause"].append(f"media {s['media']:.4f} non > +0,25 R")
    iv = intervallo(coppie, seme)
    if segnale(iv) == "invalido":
        s["cause"].append("intervallo invalido")
    else:
        s["L"], s["U"] = iv
        if not iv[0] > 0:
            s["cause"].append("limite inferiore non > 0")
    if not potenza_stimata >= SCREENING_POTENZA:
        s["cause"].append(f"potenza stimata {potenza_stimata:.4f} < 50%")
    s["ammessa"] = not s["cause"]
    return s


def veto_blocchi(coppie, soglia, minimo_trade_blocco, ampiezza: int = 250) -> dict:
    if type(soglia) not in (int, float) or not math.isfinite(soglia):
        raise ValueError(f"soglia {soglia!r} non valida")
    if type(minimo_trade_blocco) is not int or minimo_trade_blocco < 1:
        raise ValueError(f"minimo di trade per blocco {minimo_trade_blocco!r} non valido")
    if type(ampiezza) is not int or ampiezza < 1 or not coppie or len(coppie) % ampiezza:
        raise ValueError(f"{len(coppie)} sedute non divisibili in blocchi da {ampiezza}")
    controlla_coppie(coppie)
    medie, fallito, sottile = [], False, False
    for i in range(0, len(coppie), ampiezza):
        blocco = coppie[i:i + ampiezza]
        k = sum(x for _, x in blocco)
        m = sum(x for x, _ in blocco) / k if k else None
        medie.append(m)
        if k < minimo_trade_blocco:
            sottile = True
        elif m < soglia:
            fallito = True
    esito = "fallito" if fallito else "non valutabile" if sottile else "superato"
    return {"id": "blocchi", "veto": True, "esito": esito, "medie": medie}


# --- Rapporto tipizzato (D-34 punto 4; MODELLO-EPISTEMICO §3-§4; audit I2) ---
TIPI = ("MISURA", "DERIVATO", "STIMA", "IPOTESI", "REGOLA")


def _voce(etichetta, valore, unita, tipo, incertezza, fonte) -> dict:
    return {"etichetta": etichetta, "valore": valore, "unita": unita, "tipo": tipo, "incertezza": incertezza,
            "fonte": fonte}


def voci_rapporto(v: dict) -> list:
    """Ogni numero del verdetto con tipo, incertezza e fonte. Misure, derivati e regole prima delle stime."""
    def misura(x):
        return "esatto" if x is not None else "NON DISPONIBILE"
    c = v.get("contesto_prove")
    voci = [
        _voce("sedute", v["sedute"], "sedute", "MISURA", "esatto", "coppie giornaliere della prova"),
        _voce("trade", v["trade"], "trade", "MISURA", misura(v["trade"]), "coppie giornaliere della prova"),
        _voce("sedute con trade", v["sedute_attive"], "sedute", "MISURA", misura(v["sedute_attive"]),
              "coppie giornaliere della prova"),
        _voce("media del campione", v["media"], "R a trade", "DERIVATO",
              "esatto (sul campione)" if v["media"] is not None else "NON DISPONIBILE", "somma di S / somma di K"),
        _voce("prove nel registro (N)", c["n_prove"] if c else None, "prove", "MISURA",
              "esatto" if c else "NON FORNITO",
              f"{c['registro']}, sha256 {c['impronta'][:16]}…" if c else "nessun registro fornito"),
        _voce("soglie del metro", (SOGLIA_PROMOZIONE, SOGLIA_BOCCIATURA), "R a trade", "REGOLA", "esatto",
              "D-31 (Δ = 0,05 R attorno a +0,15 R)"),
        _voce("quota", v["quota"], "per coda", "REGOLA", "esatto", "D-31, D-38"),
    ]
    stimabile = v["L"] is not None and v["U"] is not None
    voci.append(_voce(
        "vantaggio della strategia", (v["L"], v["U"]) if stimabile else None, "R a trade", "STIMA",
        (f"intervallo bootstrap basic, 2,5% per coda, blocchi da {BLOCCO}, B = {B}, seme {v['seme']}; "
         f"valido nel dominio del collaudo IA-02") if stimabile else "NON STIMABILE",
        f"pilota_ia02 sha256 {IMPRONTA_PILOTA[:16]}…"))
    return voci


def _fmt(x) -> str:
    if x is None:
        return "—"
    if isinstance(x, tuple):
        return "[" + "; ".join(_fmt(y) for y in x) + "]"
    if isinstance(x, float):
        return f"{x:.4f}"
    return str(x)


def _riga(x: dict) -> str:
    return (f"- {x['etichetta']}: {_fmt(x['valore'])} {x['unita']} [{x['tipo']}] · incertezza: "
            f"{x['incertezza']} · fonte: {x['fonte']}")


def rapporto(v: dict) -> str:
    righe = [f"VERDETTO D-31 · {v['esito']} · causa: {v['causa']}"]
    for x in voci_rapporto(v):
        righe.append(_riga(x))
    if v["vicini_soglia"]:
        righe.append(f"- estremi a meno di 1e-9 R dalla soglia: {', '.join(v['vicini_soglia'])} (non cambia l'esito)")
    righe.append("Esito della regola, non una raccomandazione a operare: la decisione resta del titolare (D-14).")
    return "\n".join(righe)


def voci_screening(s: dict) -> list:
    """Il rapporto dello screening (D-36) con i tipi. La media dello sviluppo è gonfiata dalla selezione."""
    stimabile = s["L"] is not None and s["U"] is not None
    return [
        _voce("media sullo sviluppo", s["media"], "R a trade", "DERIVATO",
              "esatto sul campione, ma gonfiata dalla selezione fra varianti" if s["media"] is not None
              else "NON DISPONIBILE", "sviluppo dal 15/11/2023 (D-29)"),
        _voce("soglie dello screening", (SCREENING_MEDIA, 0.0, SCREENING_POTENZA), "R, R, probabilità", "REGOLA",
              "esatto", "D-36 (media > +0,25 R; L > 0; potenza ≥ 50%)"),
        _voce("potenza stimata della verifica", s["potenza"], "probabilità", "STIMA",
              "dalla procedura congelata nella scheda prima del sigillo", "scheda dell'ipotesi (D-36)"),
        _voce("intervallo sullo sviluppo", (s["L"], s["U"]) if stimabile else None, "R a trade", "STIMA",
              (f"intervallo bootstrap basic, 2,5% per coda, blocchi da {BLOCCO}, B = {B}, seme {s['seme']}")
              if stimabile else "NON STIMABILE", f"pilota_ia02 sha256 {IMPRONTA_PILOTA[:16]}…"),
    ]


def rapporto_screening(s: dict) -> str:
    esito = "ammessa alla verifica" if s["ammessa"] else "NON ammessa: " + "; ".join(s["cause"])
    righe = [f"SCREENING D-36 · {esito}"]
    for x in voci_screening(s):
        righe.append(_riga(x))
    righe.append("Lo screening non è una prova: decide solo se spendere la riserva; il giudizio è della verifica (D-36).")
    return "\n".join(righe)
