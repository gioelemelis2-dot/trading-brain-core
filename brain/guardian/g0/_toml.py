"""Caricatore TOML portabile (Python 3.9 e successivi): `tomllib` (3.11+) → `tomli` (se installato) → parser minimale.

Il parser minimale serve quando nessuno dei due è disponibile (per esempio il Python 3.9 di sistema di macOS). Copre
SOLO il sottoinsieme usato dai file del Guardian:
- commenti `#` (anche a fine riga, fuori dalle stringhe) e righe vuote;
- tabelle `[a.b]` e array di tabelle `[[a]]`, con chiavi semplici (lettere, cifre, `_`, `-`);
- coppie `chiave = valore` con chiave semplice o tra virgolette (`"JPY/EUR" = "162.00"`, `'USD/EUR' = …`), come
  nella sezione [cambi];
- stringhe "base" (con gli escape di TOML) e 'letterali'; interi e decimali in base 10 (anche con `_` ed esponente);
  `true`/`false`; array su una sola riga di questi valori.
Ogni altro costrutto (tabelle inline, stringhe su più righe, date, chiavi puntate o tra virgolette, array su più righe,
numeri esadecimali, inf/nan, chiavi o tabelle duplicate, chiavi tra virgolette nelle intestazioni) è un ERRORE esplicito con il numero di riga: mai
un'interpretazione a metà. Il test `test_compatibilita_e_concorrenza.py` confronta il risultato con `tomllib` su tutti
i file TOML del Guardian.
"""
from __future__ import annotations

import re

try:
    import tomllib as _motore
    MOTORE = "tomllib"
except ModuleNotFoundError:
    try:
        import tomli as _motore
        MOTORE = "tomli"
    except ModuleNotFoundError:
        _motore = None
        MOTORE = "minimale"


class ErroreToml(ValueError):
    pass


def loads(testo: str) -> dict:
    return _motore.loads(testo) if _motore is not None else loads_minimale(testo)


def load(fp) -> dict:
    """Come `tomllib.load`, ma accetta file aperti sia in binario sia in testo."""
    dati = fp.read()
    return loads(dati.decode("utf-8") if isinstance(dati, bytes) else dati)


_CHIAVE = r"[A-Za-z0-9_-]+"
_PERCORSO = rf"{_CHIAVE}(?:[ \t]*\.[ \t]*{_CHIAVE})*"
_TABELLA = re.compile(rf"\[[ \t]*({_PERCORSO})[ \t]*\][ \t]*(?:#.*)?")
_ARRAY_DI_TABELLE = re.compile(rf"\[\[[ \t]*({_PERCORSO})[ \t]*\]\][ \t]*(?:#.*)?")
_COPPIA = re.compile(rf"({_CHIAVE})[ \t]*=[ \t]*")
_UGUALE = re.compile(r"[ \t]*=[ \t]*")
_INTERO = r"[+-]?(?:0|[1-9](?:_?[0-9])*)"
_RE_INTERO = re.compile(_INTERO)
_RE_DECIMALE = re.compile(rf"{_INTERO}(?:\.[0-9](?:_?[0-9])*(?:[eE][+-]?[0-9](?:_?[0-9])*)?|[eE][+-]?[0-9](?:_?[0-9])*)")
_ESCAPE = {'"': '"', "\\": "\\", "b": "\b", "t": "\t", "n": "\n", "f": "\f", "r": "\r"}


def _errore(n: int, msg: str):
    return ErroreToml(f"TOML riga {n}: {msg} (parser minimale: costrutto non gestito o non valido)")


def _controllo(ch: str) -> bool:
    return (ord(ch) < 0x20 and ch != "\t") or ord(ch) == 0x7F


def _stringa_base(s: str, i: int, n: int):
    out, j = [], i + 1
    while j < len(s):
        ch = s[j]
        if ch == '"':
            return "".join(out), j + 1
        if ch == "\\":
            e = s[j + 1:j + 2]
            if e in _ESCAPE:
                out.append(_ESCAPE[e])
                j += 2
                continue
            if e in ("u", "U"):
                k = 4 if e == "u" else 8
                h = s[j + 2:j + 2 + k]
                if not re.fullmatch(rf"[0-9A-Fa-f]{{{k}}}", h):
                    raise _errore(n, f"escape unicode non valido {s[j:j + 2 + k]!r}")
                out.append(chr(int(h, 16)))
                j += 2 + k
                continue
            raise _errore(n, f"escape non valido {s[j:j + 2]!r}")
        if _controllo(ch):
            raise _errore(n, "carattere di controllo in una stringa")
        out.append(ch)
        j += 1
    raise _errore(n, "stringa non chiusa")


def _valore(s: str, i: int, n: int):
    if i >= len(s):
        raise _errore(n, "valore mancante")
    if s.startswith('"""', i) or s.startswith("'''", i):
        raise _errore(n, "stringa su più righe")
    c = s[i]
    if c == '"':
        return _stringa_base(s, i, n)
    if c == "'":
        j = s.find("'", i + 1)
        if j < 0:
            raise _errore(n, "stringa non chiusa")
        if any(_controllo(ch) for ch in s[i + 1:j]):
            raise _errore(n, "carattere di controllo in una stringa")
        return s[i + 1:j], j + 1
    if c == "[":
        elementi, i = [], i + 1
        while True:
            while i < len(s) and s[i] in " \t":
                i += 1
            if i >= len(s) or s[i] == "#":
                raise _errore(n, "array su più righe")
            if s[i] == "]":
                return elementi, i + 1
            v, i = _valore(s, i, n)
            elementi.append(v)
            while i < len(s) and s[i] in " \t":
                i += 1
            if i < len(s) and s[i] == ",":
                i += 1
            elif i < len(s) and s[i] == "]":
                return elementi, i + 1
            else:
                raise _errore(n, "array non chiuso o separatore mancante")
    if c == "{":
        raise _errore(n, "tabella inline")
    m = re.match(r"[^\s,\]#]+", s[i:])
    t = m.group(0) if m else ""
    if t in ("true", "false"):
        return t == "true", i + len(t)
    if _RE_INTERO.fullmatch(t):
        return int(t.replace("_", "")), i + len(t)
    if _RE_DECIMALE.fullmatch(t):
        return float(t.replace("_", "")), i + len(t)
    raise _errore(n, f"valore non supportato {t!r}")


def loads_minimale(testo: str) -> dict:
    radice: dict = {}
    corrente = radice
    definite: set = set()            # id delle tabelle già aperte con [intestazione]
    array_tabelle: set = set()       # id delle liste create con [[intestazione]]

    def naviga(percorso, n):
        nodo = radice
        for k in percorso:
            x = nodo.setdefault(k, {})
            if isinstance(x, list):
                if id(x) not in array_tabelle:
                    raise _errore(n, f"{k!r} è un array di valori, non di tabelle")
                x = x[-1]
            if not isinstance(x, dict):
                raise _errore(n, f"{k!r} è già un valore, non una tabella")
            nodo = x
        return nodo

    for n, riga in enumerate(testo.splitlines(), 1):
        s = riga.strip(" \t")
        if not s or s.startswith("#"):
            continue
        if s.startswith("[["):
            m = _ARRAY_DI_TABELLE.fullmatch(s)
            if not m:
                raise _errore(n, "intestazione di array di tabelle non valida")
            percorso = [p.strip() for p in m.group(1).split(".")]
            padre = naviga(percorso[:-1], n)
            lista = padre.setdefault(percorso[-1], [])
            if not isinstance(lista, list):
                raise _errore(n, f"{percorso[-1]!r} è già definita come tabella o valore")
            if lista and id(lista) not in array_tabelle:
                raise _errore(n, f"{percorso[-1]!r} è un array di valori")
            array_tabelle.add(id(lista))
            corrente = {}
            lista.append(corrente)
            continue
        if s.startswith("["):
            m = _TABELLA.fullmatch(s)
            if not m:
                raise _errore(n, "intestazione di tabella non valida")
            percorso = [p.strip() for p in m.group(1).split(".")]
            padre = naviga(percorso[:-1], n)
            t = padre.setdefault(percorso[-1], {})
            if not isinstance(t, dict):
                raise _errore(n, f"{percorso[-1]!r} è già definita come array o valore")
            if id(t) in definite:
                raise _errore(n, f"tabella [{m.group(1)}] definita due volte")
            definite.add(id(t))
            corrente = t
            continue
        if s[0] in "\"'":                                   # chiave tra virgolette (stringa base o letterale)
            chiave, fine = _valore(s, 0, n)
            u = _UGUALE.match(s, fine)
            if not u:
                raise _errore(n, "dopo una chiave tra virgolette serve «=» (chiavi puntate non gestite)")
            inizio = u.end()
        else:
            m = _COPPIA.match(s)
            if not m:
                raise _errore(n, "riga non riconosciuta (chiave puntata?)")
            chiave, inizio = m.group(1), m.end()
        valore, fine = _valore(s, inizio, n)
        resto = s[fine:].strip(" \t")
        if resto and not resto.startswith("#"):
            raise _errore(n, f"testo dopo il valore: {resto!r}")
        if chiave in corrente:
            raise _errore(n, f"chiave {chiave!r} duplicata")
        corrente[chiave] = valore
    return radice
