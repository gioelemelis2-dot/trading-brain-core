"""Verdetto della verifica secondo D-31, D-35, D-36 e D-37 (19/11/2026). Modulo nuovo fuori dal perimetro sigillato
(D-34): ha i suoi due giri di revisione.

- Metro: l'implementazione di riferimento collaudata (`studi/pilota_ia02.intervallo_bootstrap`), cioè bootstrap circolare
  a blocchi da 10, B = 3.999, intervallo basic, quota 2,5% per coda. Il modulo si rifiuta di calcolare se l'impronta
  del pilota non è quella congelata nell'impegno del collaudo (IMPEGNO-PROTOCOLLO-IA02.md).
- Segnale (D-31): favorevole se L > +0,20 R, sfavorevole se U < +0,10 R, altrimenti inconclusivo; un intervallo
  mancante, non finito, invertito o più stretto di 1e-9 R (#119, D-44) è invalido. L'uguaglianza non attraversa la soglia.
- Esiti (D-35, DGS-10 §4 opzione 2), nell'ordine: veto accertato → bocciata; dati inidonei, minimi mancanti o intervallo
  invalido → non decidibile; U < +0,10 → bocciata; L > +0,20 e requisiti superati → promossa; altrimenti non decidibile.
  Prima di applicare le priorità si misura tutto il possibile: media, minimi e segnale del solo metro si riportano anche
  quando decide un veto (DGS-12 §4).
- Requisiti con ruolo (DGS-12 §3): veto, vincolante per promuovere, descrittivo (riportato, non cambia l'esito).
- Veto per blocchi: un blocco con un esito ignoto (S = None) non può dare il veto; un blocco completo sì, anche se
  manca un esito altrove (DGS-12 §3, caso J).
- Screening sullo sviluppo (D-36): media > +0,25 R, L > 0 e potenza stimata ≥ 50%.
- Veto per blocchi (D-37): soglia e minimo di trade per blocco li fissa la scheda prima del sigillo.

Vale solo per la prima apertura con una variante (quota 2,5%): una quota diversa richiede un collaudo (D-31).
"""
import hashlib
import math
import random
import re
from fractions import Fraction
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
RUOLI = ("veto", "promozione", "descrittivo")   # DGS-12 §3: il descrittivo si riporta e non cambia l'esito
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


def _somma_esatta(valori) -> Fraction:
    """#124: somma in frazioni esatte (nessun arrotondamento, nessuna dipendenza dall'ordine o dalla versione)."""
    return sum((Fraction(x) for x in valori), Fraction(0))


def _media(valori, k: int):
    """(media esatta, media riportata): la riportata è il quoziente esatto arrotondato UNA volta."""
    esatta = _somma_esatta(valori) / k
    return esatta, float(esatta)


def controlla_coppie(coppie, ignote: bool = False) -> None:
    """Con `ignote` (solo per il veto per blocchi) una seduta con trade può avere l'esito ignoto: S = None."""
    if not isinstance(coppie, (list, tuple)):                                     # #134: niente generatori
        raise ValueError(f"le coppie vanno date come lista, non come {type(coppie).__name__}")
    if not coppie:
        raise ValueError("nessuna seduta")
    for i, c in enumerate(coppie):
        if len(c) != 2:
            raise ValueError(f"seduta {i}: serve la coppia (S, K)")
        s, k = c
        if type(k) is not int or k < 0:
            raise ValueError(f"seduta {i}: K = {k!r} non è un intero ≥ 0")
        if ignote and s is None:
            if k == 0:
                raise ValueError(f"seduta {i}: esito ignoto senza trade")
            continue
        if type(s) not in (int, float) or not math.isfinite(s):
            raise ValueError(f"seduta {i}: S = {s!r} non è un numero finito")
        if k == 0 and s != 0:
            raise ValueError(f"seduta {i}: risultato {s} senza trade")
    try:                                   # #134, #124 (V124-06): il pilota somma in qualunque ordine, quindi conta
        finito = math.isfinite(float(_somma_esatta(abs(s) for s, _ in coppie if s is not None)))   # la somma dei |S|
    except OverflowError:
        finito = False
    if not finito:
        raise ValueError("la somma dei risultati non è un numero finito")


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


def _seme(seme) -> None:
    """#132 (Gemini R18-08): con seme None `random.Random` usa l'entropia del sistema: bootstrap non riproducibile."""
    if type(seme) is not int:
        raise ValueError(f"seme {seme!r}: serve un intero, registrato nel rapporto")


def intervallo(coppie, seme: int):
    _seme(seme)
    if P.impronta_modulo() != IMPRONTA_PILOTA:
        raise RuntimeError("il pilota non è la versione collaudata: impronta diversa da IMPEGNO-PROTOCOLLO-IA02")
    return P.intervallo_bootstrap(coppie, random.Random(seme), B, BLOCCO)


def contesto_prove(registro) -> dict:
    """N dal registro canonico delle prove (D-34 punto 2), con l'impronta del file letto (DGS-11 §6)."""
    registro = Path(registro)
    if registro.is_symlink():                                                     # #133 (Gemini R18-09)
        raise ValueError(f"{registro}: collegamento simbolico, non il registro canonico")
    if registro.name in REGISTRI_EREDITATI:
        raise ValueError(f"{registro.name}: registro ereditato di Binario B, non vale per il verdetto (D-34, DA-28)")
    if not registro.is_file():
        raise ValueError(f"registro delle prove assente: {registro}")
    prima = hashlib.sha256(registro.read_bytes()).hexdigest()
    dati = S.leggi(registro)
    if hashlib.sha256(registro.read_bytes()).hexdigest() != prima:
        raise ValueError(f"{registro.name}: il registro è cambiato durante la lettura")
    return {"registro": registro.name, "n_prove": S.n_prove(dati), "impronta": prima}


IMPRONTA_ESADECIMALE = re.compile(r"[0-9a-f]{64}")


def _contesto(c) -> None:
    """#133 (Gemini R18-09): il contesto di N è quello di `contesto_prove`, non un dizionario qualsiasi."""
    if c is None:
        return
    if not isinstance(c, dict) or set(c) != {"registro", "n_prove", "impronta"} \
            or not isinstance(c["registro"], str) or not c["registro"] \
            or type(c["n_prove"]) is not int or c["n_prove"] < 0 \
            or not isinstance(c["impronta"], str) or not IMPRONTA_ESADECIMALE.fullmatch(c["impronta"]):
        raise ValueError(f"contesto delle prove malformato: {c!r} (usare contesto_prove)")


def _requisiti(requisiti) -> list:
    """Ogni requisito con il suo ruolo: veto, vincolante per promuovere («promozione») o descrittivo."""
    out = []
    for r in requisiti:
        if not isinstance(r, dict) or not isinstance(r.get("id"), str) or type(r.get("veto")) is not bool \
                or r.get("esito") not in ESITI_REQUISITO or type(r.get("descrittivo", False)) is not bool \
                or (r["veto"] and r.get("descrittivo", False)):
            raise ValueError(f"requisito malformato: {r!r}")
        ruolo = "veto" if r["veto"] else "descrittivo" if r.get("descrittivo", False) else "promozione"
        out.append({"id": r["id"], "ruolo": ruolo, "esito": r["esito"]})
    return out


def verdetto(coppie, seme: int, requisiti=(), contesto=None, quota=QUOTA) -> dict:
    if type(quota) is not float or quota != QUOTA:
        raise ValueError(f"quota {quota!r}: solo {QUOTA} è collaudata; un'altra richiede un collaudo (D-31)")
    _seme(seme)
    _contesto(contesto)
    req = _requisiti(requisiti)
    v = {"esito": None, "causa": None, "L": None, "U": None, "media": None,
         "sedute": len(coppie) if isinstance(coppie, (list, tuple)) else None, "trade": None,
         "sedute_attive": None, "seme": seme, "impronta_pilota": IMPRONTA_PILOTA, "vicini_soglia": [],
         "contesto_prove": contesto, "quota": quota, "segnale": None, "requisiti": req, "intervallo_scartato": None}

    def fine(esito, causa):
        v["esito"], v["causa"] = esito, causa
        return v

    # Prima si misura tutto quello che si può (DGS-12 §4: esito contabile, segnale del metro, veto e verdetto
    # restano distinti nel rapporto), poi si applicano le priorità di D-35.
    inidonei, mancano = None, []
    try:
        controlla_coppie(coppie)
    except ValueError as e:
        inidonei = str(e)
    if inidonei is None:
        v["trade"] = sum(k for _, k in coppie)
        v["sedute_attive"] = sum(1 for _, k in coppie if k > 0)
        v["media"] = _media((s for s, _ in coppie), v["trade"])[1] if v["trade"] else None   # #124
        mancano = minimi_mancanti(coppie)
        if not mancano:
            iv = intervallo(coppie, seme)
            v["segnale"] = segnale(iv)
            if v["segnale"] == "invalido":                  # #131: un intervallo invalido non è una stima
                v["intervallo_scartato"] = iv
            else:
                v["L"], v["U"] = iv
                v["vicini_soglia"] = vicini(*iv)
    for r in req:
        if r["ruolo"] == "veto" and r["esito"] == "fallito":
            return fine("bocciata", f"veto: {r['id']}")
    if inidonei is not None:
        return fine("non decidibile", f"dati inidonei: {inidonei}")
    if mancano:
        return fine("non decidibile", "minimi: " + "; ".join(mancano))
    sg = v["segnale"]
    if sg == "invalido":
        return fine("non decidibile", "intervallo invalido")
    if sg == "sfavorevole":
        return fine("bocciata", "statistica: U < +0,10 R")
    if sg == "favorevole":
        aperti = [r["id"] for r in req if r["ruolo"] != "descrittivo" and r["esito"] != "superato"]
        if not aperti and contesto is None:                 # #133: si promuove solo con N dal registro canonico
            return fine("non decidibile", "N non fornito: serve il contesto del registro canonico (D-34 punto 2)")
        if not aperti:
            return fine("promossa", "L > +0,20 R e requisiti superati")
        return fine("non decidibile", "requisito non superato o non valutabile: " + ", ".join(aperti))
    return fine("non decidibile", "inconclusivo: L ≤ +0,20 R e U ≥ +0,10 R")


def screening(coppie, seme: int, potenza_stimata) -> dict:
    _seme(seme)
    if type(potenza_stimata) not in (int, float) or not 0.0 <= potenza_stimata <= 1.0:
        raise ValueError(f"potenza stimata {potenza_stimata!r} fuori da [0, 1]")
    controlla_coppie(coppie)
    trade = sum(k for _, k in coppie)
    s = {"ammessa": False, "cause": [], "media": None, "L": None, "U": None, "seme": seme, "potenza": potenza_stimata,
         "L_vicino_a_zero": False}
    if trade == 0:
        s["cause"].append("nessun trade")
        return s
    esatta, s["media"] = _media((x for x, _ in coppie), trade)     # #124: decisione in frazioni esatte
    if not esatta > Fraction(SCREENING_MEDIA):
        s["cause"].append(f"media {s['media']:.4f} non > +0,25 R")
    iv = intervallo(coppie, seme)
    if segnale(iv) == "invalido":
        s["cause"].append("intervallo invalido")
    else:
        s["L"], s["U"] = iv
        s["L_vicino_a_zero"] = abs(iv[0]) < VICINANZA                # #124 (N22-A2): si riporta, non cambia l'esito
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
    controlla_coppie(coppie, ignote=True)
    medie, fallito, sottile = [], False, False
    for i in range(0, len(coppie), ampiezza):
        blocco = coppie[i:i + ampiezza]
        if any(x is None for x, _ in blocco):          # DGS-12 §3: l'esito ignoto può cambiare il blocco: non accertato
            medie.append(None)
            sottile = True
            continue
        k = sum(x for _, x in blocco)
        esatta, m = _media((x for x, _ in blocco), k) if k else (None, None)   # #124
        medie.append(m)
        if k < minimo_trade_blocco:
            sottile = True
        elif esatta < Fraction(soglia):
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
        _voce("sedute", v["sedute"], "sedute", "MISURA", misura(v["sedute"]), "coppie giornaliere della prova"),
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


RUOLO_NEL_RAPPORTO = {"veto": "veto", "promozione": "vincolante per promuovere",
                      "descrittivo": "descrittivo, non cambia l'esito"}


def rapporto(v: dict) -> str:
    righe = [f"VERDETTO D-31 · {v['esito']} · causa: {v['causa']}"]
    for x in voci_rapporto(v):
        righe.append(_riga(x))
    righe.append(f"- segnale del solo metro: {v['segnale'] or 'non calcolato (dati inidonei o minimi mancanti)'}")
    if v["intervallo_scartato"] is not None:
        righe.append(f"- intervallo scartato perché invalido (D-44): {_fmt(tuple(v['intervallo_scartato']))} R, "
                     "non è una stima")
    for r in v["requisiti"]:
        righe.append(f"- requisito {r['id']} [{RUOLO_NEL_RAPPORTO[r['ruolo']]}]: {r['esito']}")
    if v["vicini_soglia"]:
        righe.append(f"- estremi a meno di 1e-9 R [REGOLA] dalla soglia: {', '.join(v['vicini_soglia'])} (non cambia l'esito)")
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
        _voce("potenza stimata della verifica", s["potenza"], "probabilità", "IPOTESI",              # #141
              "dichiarata nella scheda, non ricalcolata: la procedura di potenza non esiste ancora (DGS-17 Q9)",
              "scheda dell'ipotesi (D-36)"),
        _voce("intervallo sullo sviluppo", (s["L"], s["U"]) if stimabile else None, "R a trade", "STIMA",
              (f"intervallo bootstrap basic, 2,5% per coda, blocchi da {BLOCCO}, B = {B}, seme {s['seme']}")
              if stimabile else "NON STIMABILE", f"pilota_ia02 sha256 {IMPRONTA_PILOTA[:16]}…"),
    ]


def rapporto_screening(s: dict) -> str:
    esito = "ammessa alla verifica" if s["ammessa"] else "NON ammessa: " + "; ".join(s["cause"])
    righe = [f"SCREENING D-36 · {esito}"]
    for x in voci_screening(s):
        righe.append(_riga(x))
    if s.get("L_vicino_a_zero"):
        righe.append("- limite inferiore a meno di 1e-9 R [REGOLA] da 0 (non cambia l'esito; arrotondamento possibile, #124)")
    righe.append("Lo screening non è una prova: decide solo se spendere la riserva; il giudizio è della verifica (D-36).")
    return "\n".join(righe)
