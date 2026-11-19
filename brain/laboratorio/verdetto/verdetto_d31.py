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
import math
import random

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


def _requisiti(requisiti) -> list:
    out = []
    for r in requisiti:
        if not isinstance(r, dict) or not isinstance(r.get("id"), str) or type(r.get("veto")) is not bool \
                or r.get("esito") not in ESITI_REQUISITO:
            raise ValueError(f"requisito malformato: {r!r}")
        out.append(r)
    return out


def verdetto(coppie, seme: int, requisiti=()) -> dict:
    req = _requisiti(requisiti)
    v = {"esito": None, "causa": None, "L": None, "U": None, "media": None, "sedute": len(coppie), "trade": None,
         "sedute_attive": None, "seme": seme, "impronta_pilota": IMPRONTA_PILOTA, "vicini_soglia": []}

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
    s = {"ammessa": False, "cause": [], "media": None, "L": None, "U": None, "seme": seme}
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
