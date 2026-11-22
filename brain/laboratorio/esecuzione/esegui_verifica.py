"""Esecutore ORDINARIO della verifica sulla riserva (#127; DGS-14; DGS-15 punti 2–4), 22/11/2026.

Sostituisce, per la verifica, il percorso di `esegui_h002` (che non usa né il registro della riserva né il metro
D-31). La scheda deve essere conforme al modello H-003: un blocco ```json contratto-h003``` con il disegno
dichiarato prima del sigillo. La vecchia scheda di H-002 non ce l'ha ed è rifiutata prima di ogni autorizzazione.

Ordine, con i rifiuti PRIMA di ogni lettura dei dati:
 1. contratto della scheda (SchedaNonConforme);
 2. prenotazione: stessa ipotesi, stessa impronta della scheda. Se l'esito è già registrato, è una RIPRESA: si
    controlla che scheda, codice, variante, seme e finestra siano identici e si rigenera il rapporto dal record,
    senza leggere nulla;
 3. sigillo della scheda e del codice (impronte di tutti i file eseguibili);
 4. finestra: la prenotazione è la finestra di LETTURA; le prime `date_accessorie` sono storia (mediane), la
    verifica è il resto e deve contenere esattamente `sedute` sedute (D-37);
 5. quota: j e α_j previsti dal registro; diversa da 2,5% (la sola collaudata) → rifiuto durevole (D-50);
 6. screening sullo sviluppo (D-36, D-47), registrato nel registro delle prove;
 7. manifesto della finestra (insieme atteso contro registro dello scaricamento): anomalie → nessuna autorizzazione;
 8. autorizzazione con l'impegno (scheda, codice, metro, finestra, registri, elenco con impronte, N, quota,
    variante, seme) e il ricontrollo della quota sotto il blocco: se un'altra apertura è arrivata prima, rifiuto;
 9. lettura con i byte verificati file per file; un file difforme dà un esito tecnico registrato, e il consumo resta;
10. coppie giornaliere (S, K) per seduta, veto per blocchi, verdetto D-31 con N dal registro canonico;
11. esito e record nel registro della riserva, esito nel registro delle prove, rapporto tipizzato dal record.
I criteri di H-002 compaiono solo come descrizione: il verdetto è D-31.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from ..simulatori import orb_londra as O
from ..verdetto import verdetto_d31 as V
from . import caricatore as C
from . import manifesto as MF
from . import riserva as RV
from . import sigillo as S
from .esegui_h002 import RADICE, VARIANTI, moduli_brain

PARTENZA = "brain.laboratorio.esecuzione.esegui_verifica"
BLOCCO = re.compile(r"```json contratto-h003\n(.*?)\n```", re.S)
DESTINAZIONI = ("test", "verifica")
ESITI_TECNICI = ("completata", "rapporto rigenerato", "rifiutata per quota", "file difforme")


class SchedaNonConforme(ValueError):
    """La scheda non ha un contratto H-003 valido: nessuna prenotazione può essere autorizzata con essa."""


def _intero(x, minimo=0) -> bool:
    return type(x) is int and x >= minimo


def leggi_contratto(scheda: Path) -> dict:
    trovati = BLOCCO.findall(Path(scheda).read_text(encoding="utf-8"))
    if len(trovati) != 1:
        raise SchedaNonConforme(f"{Path(scheda).name}: serve un solo blocco «json contratto-h003» (modello H-003)")
    try:
        c = json.loads(trovati[0])
    except ValueError as e:
        raise SchedaNonConforme(f"contratto H-003 illeggibile: {e}") from None
    attese = {"modello", "ipotesi", "destinazione", "simulatore", "variante", "m", "mercato", "metro", "seme",
              "screening_seme", "potenza_stimata", "date_accessorie", "sedute", "veto_blocchi", "sviluppo"}
    if not isinstance(c, dict) or set(c) != attese:
        raise SchedaNonConforme(f"contratto H-003 con campi diversi da quelli del modello: {sorted(c) if isinstance(c, dict) else c!r}")
    problemi = []
    if c["modello"] != "H-003":
        problemi.append("modello diverso da H-003")
    if c["destinazione"] not in DESTINAZIONI:
        problemi.append("destinazione")
    if c["simulatore"] != "orb_londra" or c["variante"] not in VARIANTI:
        problemi.append("simulatore o variante")
    if c["metro"] != "D-31":
        problemi.append("metro diverso da D-31")
    if c["mercato"] != "XAUUSD":
        problemi.append("mercato")
    if not _intero(c["m"], 1) or not _intero(c["seme"]) or not _intero(c["screening_seme"]):
        problemi.append("m o semi")
    if type(c["potenza_stimata"]) not in (int, float) or not 0 <= c["potenza_stimata"] <= 1:
        problemi.append("potenza stimata")
    if not _intero(c["date_accessorie"]) or c["sedute"] != V.D_COLLAUDATO or type(c["sedute"]) is not int:
        problemi.append("date accessorie o sedute (D-37: 1.000)")
    vb = c["veto_blocchi"]
    if not isinstance(vb, dict) or set(vb) != {"soglia", "minimo_trade"} or type(vb["soglia"]) not in (int, float) \
            or not _intero(vb["minimo_trade"], 1):
        problemi.append("veto per blocchi")
    try:
        sv = [date.fromisoformat(x) for x in c["sviluppo"]]
        if len(sv) != 2 or sv[1] < sv[0] or sv[0] < C.INIZIO_SVILUPPO:
            problemi.append("periodo di sviluppo")
    except (TypeError, ValueError):
        problemi.append("periodo di sviluppo")
    if problemi:
        raise SchedaNonConforme(f"contratto H-003 non valido: {', '.join(problemi)}")
    return c


def impronte_codice(radice: Path = RADICE) -> Dict[str, str]:
    radice = Path(radice)
    return {f: hashlib.sha256((radice / f).read_bytes()).hexdigest() for f in moduli_brain(radice, PARTENZA)}


def sedute(inizio: date, fine: date) -> List[date]:
    out, g = [], inizio
    while g <= fine:
        if g.weekday() < 5 and g not in O.esclusi(g.year):
            out.append(g)
        g += timedelta(days=1)
    return out


def coppie(trade: List[dict], giorni: List[date]) -> List[tuple]:
    per_giorno: Dict[date, list] = {}
    for x in trade:
        per_giorno.setdefault(x["data"], []).append(x["r"])
    return [(sum(per_giorno.get(g, [])), len(per_giorno.get(g, []))) for g in giorni]


def _json(x):
    return json.loads(json.dumps(x, default=str, allow_nan=False))


def _scrivi_rapporto(percorso: Path, testo: str) -> None:
    percorso = Path(percorso)
    percorso.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=percorso.parent, prefix=f".{percorso.name}.")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(testo)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, percorso)


def rapporto_da_record(rec: dict) -> str:
    """Il rapporto finale, SOLO dal record scritto nel registro della riserva: rigenerabile senza rileggere i dati."""
    idn = rec["identita"]
    righe = [f"RAPPORTO DI VERIFICA · {idn['ipotesi']} {idn['variante']} · esito {rec['esito']}",
             f"- prenotazione {rec['prenotazione']} · j = {rec['j']} · quota {rec['quota']} [REGOLA] · N globale "
             f"{rec['n_globale']} [MISURA] dal registro canonico",
             f"- impronta dell'impegno: {rec['impronta_impegno']} [MISURA] · scheda {idn['scheda_sha256'][:16]}… · "
             f"seme {idn['seme']}",
             f"- finestra di lettura {idn['finestra']['lettura'][0]} → {idn['finestra']['lettura'][1]}, verifica "
             f"{idn['finestra']['verifica'][0]} → {idn['finestra']['verifica'][1]} [REGOLA]",
             f"- chiamate al caricatore: sviluppo {rec['chiamate_caricatore']['sviluppo']}, verifica "
             f"{rec['chiamate_caricatore']['verifica']} [MISURA]"]
    if rec.get("verdetto") is not None:
        righe.append(V.rapporto(rec["verdetto"]))
    else:
        righe.append(f"ESITO TECNICO · {rec['esito_tecnico']} · {rec['esito']} · causa: {rec['causa']} [MISURA]")
    righe.append(V.rapporto_screening(rec["screening"]))
    d = rec.get("descrizione_h002")
    if d is not None:
        righe.append("- criteri di H-002 (solo descrizione, non cambiano l'esito D-31): "
                     + json.dumps(d, ensure_ascii=False, sort_keys=True) + " [MISURA]")
    return "\n".join(righe) + "\n"


def _registra_una_volta(registro: Path, ipotesi: str, voce: dict, ora: str) -> None:
    gia = [e for e in S.leggi(registro)["esecuzioni"] if e["ipotesi"] == ipotesi and e["ruolo"] == voce["ruolo"]
           and e.get("variante") == voce["variante"]]
    if gia:
        if any(e.get("impronta_impegno") != voce.get("impronta_impegno") for e in gia):
            raise ValueError(f"{voce['ruolo']} di {ipotesi} già registrata con un altro impegno")
        return
    S.registra_esecuzioni(registro, ipotesi, [voce], ora)


def esegui(scheda: Path, registro: Path, riserva: Path, id_: str, cache: Path, cache_sviluppo: Path,
           rapporto: Path, ora: str) -> dict:
    chiamate = {"sviluppo": 0, "verifica": 0}

    def leggi(cartella, inizio, fine, modalita, attese=None):
        chiamate[modalita] += 1
        return C.carica(Path(cartella) / c["mercato"], Path(cartella) / f"{c['mercato']}_ASK", inizio, fine, modalita,
                        registro, c["ipotesi"], scheda, attese=attese)

    def risultato(esito_tecnico, esito, h=None, percorso=None, motivo=""):
        return {"esito_tecnico": esito_tecnico, "esito": esito, "chiamate_caricatore": dict(chiamate),
                "prenotazione": id_, "impronta_impegno": h, "rapporto": str(percorso) if percorso else None,
                "motivo": motivo}

    c = leggi_contratto(scheda)                                                          # 1
    sha_scheda = S.impronta(scheda)
    p = RV.prenotazione(riserva, id_)                                                    # 2
    if p["evento"]["ipotesi"] != c["ipotesi"] or p["evento"]["hash_domanda"] != sha_scheda:
        raise ValueError(f"la prenotazione {id_!r} è di un'altra ipotesi o di un'altra scheda")
    if p["stato"] == "rifiutato":
        raise ValueError(f"la prenotazione {id_!r} è stata rifiutata ({p['rifiuto']['motivo']}): serve una richiesta nuova")
    if p["stato"] not in ("prenotato", "autorizzato"):
        raise ValueError(f"la prenotazione {id_!r} è {p['stato']}")
    lettura = (date.fromisoformat(p["evento"]["inizio"]), date.fromisoformat(p["evento"]["fine"]))
    verifica = (lettura[0] + timedelta(days=c["date_accessorie"]), lettura[1])
    identita = {"ipotesi": c["ipotesi"], "variante": c["variante"], "seme": c["seme"], "scheda_sha256": sha_scheda,
                "codice": impronte_codice(),
                "finestra": {"lettura": [x.isoformat() for x in lettura], "verifica": [x.isoformat() for x in verifica]}}
    if p["record"] is not None:                                                          # ripresa dopo il verdetto
        if p["record"]["identita"] != _json(identita):
            raise ValueError("ripresa non identica: scheda, codice, variante, seme o finestra diversi dal record")
        _scrivi_rapporto(rapporto, rapporto_da_record(p["record"]))
        return risultato("rapporto rigenerato", p["record"]["esito"], p["record"]["impronta_impegno"], rapporto)
    sigillo = S.controlla_sigillo(registro, c["ipotesi"], scheda, codice=identita["codice"])   # 3
    if c["variante"] not in sigillo["varianti"]:                                         # #137: prima di leggere
        raise ValueError(f"variante {c['variante']!r} non dichiarata nel sigillo di {c['ipotesi']}: {sigillo['varianti']}")
    giorni_verifica = sedute(*verifica)                                                  # 4
    if len(giorni_verifica) != c["sedute"]:
        raise ValueError(f"la finestra di verifica ha {len(giorni_verifica)} sedute, la scheda ne dichiara {c['sedute']}")
    autorizzata = p["stato"] == "autorizzato"
    if not autorizzata:                                                                   # 5
        j, q = RV.quota_prevista(riserva, c["m"])
        if q != V.QUOTA:
            RV.rifiuta(riserva, id_, c["m"], V.QUOTA, f"quota {q!r} non collaudata (D-31: solo {V.QUOTA})",
                       "prima dell'autorizzazione", sha_scheda, ora)
            return risultato("rifiutata per quota", None, motivo=f"quota {q!r}")
    else:
        j, q = p["autorizzazione"]["j"], p["autorizzazione"]["alfa_j"]
    par = VARIANTI[c["variante"]]                                                         # 6
    sv = [date.fromisoformat(x) for x in c["sviluppo"]]
    bid, ask, _ = leggi(cache_sviluppo, sv[0], sv[1], "sviluppo")
    giorni_sv = sedute(sv[0] + timedelta(days=c["date_accessorie"]), sv[1])
    scr = V.screening(coppie(O.trade(O.prepara(bid, ask, par), par), giorni_sv), c["screening_seme"],
                      c["potenza_stimata"])
    if not scr["ammessa"]:
        raise ValueError(f"screening non superato: {'; '.join(scr['cause'])}")
    _registra_una_volta(registro, c["ipotesi"], {"ruolo": "sviluppo", "variante": c["variante"],
                                                "screening": _json(scr)}, ora)
    man = MF.manifesto(cache, c["mercato"], lettura[0], lettura[1])                       # 7
    if man["anomalie"]:
        raise ValueError(f"manifesto con anomalie: {'; '.join(man['anomalie'][:10])}")
    ctx = V.contesto_prove(registro)
    impegno = {"scheda_sha256": sha_scheda, "codice": identita["codice"],                    # 8
               "metro": {"modulo": "D-31", "pilota": V.IMPRONTA_PILOTA, "quota": V.QUOTA},
               "finestra": identita["finestra"], "registri": man["registri"], "elenco": man["elenco"],
               "impronta_elenco": man["impronta_elenco"], "n_globale": ctx["n_prove"], "quota": q, "j": j,
               "variante": c["variante"], "seme": c["seme"], "contratto": c,
               "sedute": [g.isoformat() for g in giorni_verifica]}             # DGS-16: fissate prima di aprire
    h = RV.impronta_impegno(impegno)
    try:
        RV.autorizza(riserva, id_, ctx["n_prove"], h, ora, c["m"], impegno=impegno, quota_attesa=q)
    except ValueError as e:
        if not str(e).startswith("quota cambiata"):
            raise
        j2, q2 = RV.quota_prevista(riserva, c["m"])
        RV.rifiuta(riserva, id_, c["m"], V.QUOTA, f"quota {q2!r} non collaudata: {e}", "ricontrollo all'autorizzazione",
                   sha_scheda, ora)
        return risultato("rifiutata per quota", None, motivo=str(e))
    _registra_una_volta(registro, c["ipotesi"], {"ruolo": "verifica", "variante": c["variante"],
                                                "impronta_impegno": h}, ora)
    rec = {"prenotazione": id_, "j": j, "quota": q, "n_globale": ctx["n_prove"], "impronta_impegno": h,
           "identita": identita, "screening": scr, "chiamate_caricatore": None}
    try:                                                                                   # 9
        bid, ask, info = leggi(cache, lettura[0], lettura[1], "verifica", MF.attese(man))
    except C.FileDifforme as e:
        rec.update(esito="non decidibile", esito_tecnico="file difforme", causa=f"file difforme: {e}", verdetto=None,
                   descrizione_h002=None)
    else:
        tr = O.trade(O.prepara(bid, ask, par), par)                                        # 10
        dentro = [x for x in tr if verifica[0] <= x["data"] <= verifica[1]]
        cp = coppie(dentro, giorni_verifica)
        veto = V.veto_blocchi(cp, c["veto_blocchi"]["soglia"], c["veto_blocchi"]["minimo_trade"])
        v = V.verdetto(cp, c["seme"], [veto], contesto=ctx)
        rec.update(esito=v["esito"], esito_tecnico="completata", causa=v["causa"], verdetto=v,
                   descrizione_h002=O.metriche(dentro),
                   coppie=[[g.isoformat(), s, k] for g, (s, k) in zip(giorni_verifica, cp)],   # DGS-16: in ordine
                   feriali_esclusi=[g.isoformat() for g in (verifica[0] + timedelta(days=i)
                                                            for i in range((verifica[1] - verifica[0]).days + 1))
                                    if g.weekday() < 5 and g not in set(giorni_verifica)])
    rec["chiamate_caricatore"] = dict(chiamate)
    rec = _json(rec)
    RV.rendiconta(riserva, id_, rec["esito"], ora, record=rec)                            # 11
    _registra_una_volta(registro, c["ipotesi"], {"ruolo": "esito", "variante": c["variante"], "esito": rec["esito"],
                                                "impronta_impegno": h}, ora)
    _scrivi_rapporto(rapporto, rapporto_da_record(rec))
    return risultato(rec["esito_tecnico"], rec["esito"], h, rapporto)


def main(argv=None) -> int:
    a = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    for nome in ("--scheda", "--registro", "--riserva", "--cache", "--cache-sviluppo", "--rapporto"):
        a.add_argument(nome, required=True, type=Path)
    a.add_argument("--prenotazione", required=True)
    a.add_argument("--ora", required=True)
    x = a.parse_args(argv)
    try:
        r = esegui(x.scheda, x.registro, x.riserva, x.prenotazione, x.cache, x.cache_sviluppo, x.rapporto, x.ora)
    except (ValueError, S.NonSigillata) as e:
        print(f"RIFIUTATA prima dell'autorizzazione o della lettura: {e}", file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r["esito_tecnico"] in ("completata", "rapporto rigenerato") else 3


if __name__ == "__main__":
    sys.exit(main())
