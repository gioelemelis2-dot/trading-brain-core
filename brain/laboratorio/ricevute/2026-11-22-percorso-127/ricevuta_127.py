"""Ricevuta del percorso ordinario di verifica (#127; DGS-15 punti 2–4), 22/11/2026. Solo dati e registri SINTETICI.

Per ogni prova: esito atteso e osservato, candidato (commit e impronte del codice), stato del registro della riserva
prima e dopo, chiamate al caricatore, date e quota consumate, percorso del rapporto. L'oggetto è il mercato sintetico
dei test (regole di H-002 in una scheda di test conforme a H-003).
Uso (dalla radice): python3 -s -B brain/laboratorio/ricevute/2026-11-22-percorso-127/ricevuta_127.py <cartella>
"""
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

RADICE = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RADICE))
from brain.laboratorio.esecuzione import caricatore as C            # noqa: E402
from brain.laboratorio.esecuzione import esegui_verifica as EV      # noqa: E402
from brain.laboratorio.esecuzione import manifesto as MF            # noqa: E402
from brain.laboratorio.esecuzione import riserva as RV              # noqa: E402
from brain.laboratorio.esecuzione import sigillo as S               # noqa: E402
from brain.laboratorio.tests import mercato_sintetico as M           # noqa: E402
from brain.laboratorio.tests.test_esegui_verifica import (           # noqa: E402
    ACCESSORIE, B_FINE, B_INIZIO, FINE, INIZIO, LETTURA, ORA, SVILUPPO, contratto, testo_scheda)

BASE = Path(sys.argv[1]).resolve()
CACHE, CACHE_SV = BASE / "cache", BASE / "cache_sviluppo"
chiamate = []
_vero = C.carica


def _conta(*a, **k):
    chiamate.append(a[4])
    return _vero(*a, **k)


C.carica = _conta
EV.ANCORA_GIT = False   # registri SINTETICI fuori da git; l'ancora e la storia sono provate in TestAncoraEStoria
EV.CONTROLLO_AMBIENTE = False   # stesso processo dello script; lanciatore e ambiente provati in TestLanciatore


def candidato():
    g = subprocess.run(["git", "-C", str(RADICE), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    sporco = subprocess.run(["git", "-C", str(RADICE), "status", "--porcelain", "--", "brain/laboratorio/esecuzione",
                             "brain/laboratorio/verdetto", "brain/laboratorio/simulatori"], capture_output=True,
                            text=True).stdout.strip()
    codice = EV.impronte_codice()
    return {"commit": g, "perimetro_modificato_rispetto_al_commit": bool(sporco),
            "impronta_insieme_codice": hashlib.sha256(json.dumps(codice, sort_keys=True).encode()).hexdigest(),
            "file_di_codice": len(codice), "python": sys.version.split()[0]}


def stato_riserva(riserva):
    s = RV.stato(riserva)
    return {"sha256_file": hashlib.sha256(riserva.read_bytes()).hexdigest(), "giorni": s["giorni"],
            "aperture": [{k: a[k] for k in ("id", "j", "alfa_j", "n_globale", "esito")} for a in s["aperture"]],
            "rifiuti": [{k: r[k] for k in ("id", "j_previsto", "m", "quota_calcolata", "fase")} for r in s["rifiuti"]],
            "alfa_speso": s["alfa_speso"], "prenotazioni_attive": s["prenotazioni_attive"]}


class Prova:
    def __init__(self, nome):
        self.d = BASE / nome
        if self.d.exists():
            shutil.rmtree(self.d)
        self.d.mkdir(parents=True)
        self.registro, self.riserva = self.d / "registro_prove.json", self.d / "riserva.json"
        RV.crea(self.riserva, date(2005, 1, 1), date(2023, 10, 31), 0.05, ORA)

    def scheda(self, ipotesi, inizio, fine, id_, sigilla=True, **k):
        sch = self.d / f"{ipotesi}.md"
        sch.write_text(testo_scheda(contratto(ipotesi, **k)), encoding="utf-8")
        if sigilla:
            S.sigilla(self.registro, ipotesi, sch, ["V-T"], ORA, codice=EV.impronte_codice())
        RV.prenota(self.riserva, id_, ipotesi, inizio, fine, S.impronta(sch), ORA)
        return sch

    def esegui(self, sch, id_):
        return EV.esegui(sch, self.registro, self.riserva, id_, CACHE, CACHE_SV, self.d / f"rapporto_{id_}.txt", ORA)


def prova(nome, atteso, fn):
    p = Prova(nome)
    chiamate.clear()
    voce = {"prova": nome, "atteso": atteso}
    try:
        prima, osservato = fn(p)
        voce["osservato"] = osservato
    except Exception as e:                                                  # noqa: BLE001
        voce["osservato"] = f"ECCEZIONE {type(e).__name__}: {e}"
        prima = voce.get("prima")
    voce["registro_riserva_prima"] = prima
    voce["registro_riserva_dopo"] = stato_riserva(p.riserva)
    voce["chiamate_al_caricatore"] = list(chiamate)
    rapporti = sorted(str(x.relative_to(BASE)) for x in p.d.glob("rapporto_*.txt"))
    voce["rapporti"] = rapporti
    return voce


def _sha(x):
    return hashlib.sha256(x if isinstance(x, bytes) else x.encode("utf-8")).hexdigest()


def a_corsa(p):
    sch = p.scheda("H-T127", LETTURA, FINE, "P1")
    prima = stato_riserva(p.riserva)
    r = p.esegui(sch, "P1")
    rec = RV.record_esito(p.riserva, "P1")
    imp = RV.prenotazione(p.riserva, "P1")["autorizzazione"]["impegno"]
    # DGS-16: rapporto originale, record e rapporto rigenerato confrontabili nello stesso ambiente
    originale = Path(r["rapporto"]).read_bytes()
    rigenerato = EV.rapporto_da_record(rec).encode("utf-8")
    (p.d / "record_P1.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    (p.d / "rapporto_rigenerato_P1.txt").write_bytes(rigenerato)
    (p.d / "sedute_e_coppie_P1.json").write_text(json.dumps(
        {"sedute_nell_impegno": imp["sedute"], "coppie_del_record": rec["coppie"],
         "feriali_esclusi": rec["feriali_esclusi"]}, ensure_ascii=False, indent=1), encoding="utf-8")
    v = rec["verdetto"]
    return prima, {"esito_tecnico": r["esito_tecnico"], "esito": r["esito"], "impronta_impegno": r["impronta_impegno"],
                   "provenienza": {
                       "sigillo": "preparato dal collaudo (S.sigilla nello script), con le impronte del codice",
                       "prenotazione": "preparata dal collaudo (RV.prenota), con l'impronta della scheda",
                       "potenza_stimata": "valore DICHIARATO nel contratto della scheda di test (0,6): input, non calcolato",
                       "screening": "calcolato dall'esecutore sullo sviluppo sintetico",
                       "quota, manifesto, impegno, autorizzazione, lettura, coppie, verdetto, record, rapporto":
                           "generati dall'esecutore ordinario"},
                   "sedute_nell_impegno": len(imp["sedute"]), "coppie_uguali_alle_sedute":
                       [x[0] for x in rec["coppie"]] == imp["sedute"], "feriali_esclusi": len(rec["feriali_esclusi"]),
                   "valori_esadecimali": {"L": float.hex(v["L"]), "U": float.hex(v["U"]), "media": float.hex(v["media"])},
                   "sha256": {"rapporto_originale": _sha(originale), "rapporto_rigenerato": _sha(rigenerato),
                              "record": _sha(json.dumps(rec, sort_keys=True, ensure_ascii=False))},
                   "rapporto_originale_uguale_al_rigenerato": originale == rigenerato,
                   "L_U": [rec["verdetto"]["L"], rec["verdetto"]["U"]], "media": rec["verdetto"]["media"],
                   "sedute_trade_attive": [rec["verdetto"][k] for k in ("sedute", "trade", "sedute_attive")],
                   "screening_ammessa": rec["screening"]["ammessa"],
                   "registro_prove": [e["ruolo"] for e in S.leggi(p.registro)["esecuzioni"]],
                   "rapporto_uguale_al_record": Path(r["rapporto"]).read_text(encoding="utf-8") == EV.rapporto_da_record(rec)}


def b_vecchia(p):
    vecchia = p.d / "H-002-ORB-v3.md"
    shutil.copy(RADICE / "brain" / "laboratorio" / "ipotesi" / "H-002-ORB-v3.md", vecchia)
    RV.prenota(p.riserva, "P1", "H-002", LETTURA, FINE, S.impronta(vecchia), ORA)
    prima = stato_riserva(p.riserva)
    try:
        p.esegui(vecchia, "P1")
        return prima, "ACCETTATA (difetto)"
    except EV.SchedaNonConforme as e:
        return prima, f"rifiutata prima dell'autorizzazione: {e}"


def c_quota(p):
    sch = p.scheda("H-T127", LETTURA, FINE, "P1", m=2)
    prima = stato_riserva(p.riserva)
    r = p.esegui(sch, "P1")
    try:
        p.esegui(sch, "P1")
        secondo = "ACCETTATO (difetto)"
    except ValueError as e:
        secondo = f"rifiutato: {e}"
    return prima, {"esito_tecnico": r["esito_tecnico"], "secondo_tentativo": secondo,
                   "quota_prevista_dopo": RV.quota_prevista(p.riserva, 1),
                   "esecuzioni_nel_registro_prove": len(S.leggi(p.registro)["esecuzioni"])}


def d_concorrenza(p):
    sa = p.scheda("H-TA", LETTURA, FINE, "A")
    sb = p.scheda("H-TB", B_INIZIO, B_FINE, "B")
    prima = stato_riserva(p.riserva)
    vero_m = MF.manifesto
    stato = {"fatto": False}

    def cade(*a, **k):
        if a[4] == "verifica":
            raise RuntimeError("caduta di A durante la lettura")
        return _conta(*a, **k)

    def man(*a, **k):
        if not stato["fatto"] and a[2] == B_INIZIO:
            stato["fatto"] = True
            with mock.patch.object(C, "carica", side_effect=cade):
                try:
                    p.esegui(sa, "A")
                except RuntimeError:
                    pass
        return vero_m(*a, **k)
    with mock.patch.object(MF, "manifesto", side_effect=man):
        r = p.esegui(sb, "B")
    return prima, {"B": r["esito_tecnico"], "B_chiamate": r["chiamate_caricatore"]}


def e_difforme(p):
    sch = p.scheda("H-T127", LETTURA, FINE, "P1")
    prima = stato_riserva(p.riserva)
    f = CACHE / "XAUUSD_ASK" / f"{(INIZIO + timedelta(days=10)).isoformat()}.bi5"
    orig = f.read_bytes()

    def sost(*a, **k):
        if a[4] == "verifica":
            f.write_bytes(orig + b"\x00")
        return _conta(*a, **k)
    try:
        with mock.patch.object(C, "carica", side_effect=sost):
            r = p.esegui(sch, "P1")
    finally:
        f.write_bytes(orig)
    return prima, {"esito_tecnico": r["esito_tecnico"], "esito": r["esito"],
                   "causa": RV.record_esito(p.riserva, "P1")["causa"]}


def f_ripresa(p):
    sch = p.scheda("H-T127", LETTURA, FINE, "P1")
    vero = EV._scrivi_rapporto
    with mock.patch.object(EV, "_scrivi_rapporto", side_effect=RuntimeError("caduta prima del rapporto")):
        try:
            p.esegui(sch, "P1")
        except RuntimeError:
            pass
    prima = stato_riserva(p.riserva)
    letture_prima = list(chiamate)
    chiamate.clear()
    with mock.patch.object(EV, "_scrivi_rapporto", side_effect=vero):
        r = p.esegui(sch, "P1")
    with mock.patch.object(EV, "impronte_codice", return_value={"altro.py": "0" * 64}):
        try:
            p.esegui(sch, "P1")
            diversa = "ACCETTATA (difetto)"
        except ValueError as e:
            diversa = f"rifiutata: {e}"
    return prima, {"letture_della_prima_corsa_caduta": letture_prima, "ripresa": r["esito_tecnico"],
                   "sha256_rapporto_rigenerato": _sha(Path(r["rapporto"]).read_bytes()),
                   "esito": r["esito"], "ripresa_con_codice_diverso": diversa}


def g_omesso(p):
    sch = p.scheda("H-T127", LETTURA, FINE, "P1")
    prima = stato_riserva(p.riserva)
    reg = CACHE / "registro_scaricamento_XAUUSD_ASK.csv"
    orig = reg.read_bytes()
    righe = list(csv.DictReader(orig.decode("utf-8").splitlines()))
    tolta = [x for x in righe if x["giorno"] == INIZIO.isoformat()][0]
    with open(reg, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(righe[0]))
        w.writeheader()
        w.writerows(x for x in righe if x is not tolta)
    try:
        p.esegui(sch, "P1")
        esito = "AUTORIZZATA (difetto)"
    except ValueError as e:
        esito = f"rifiutata prima dell'autorizzazione: {e}"
    finally:
        reg.write_bytes(orig)
    return prima, esito


if __name__ == "__main__":
    BASE.mkdir(parents=True, exist_ok=True)
    if not CACHE.exists():
        M.scrivi(CACHE, LETTURA, FINE, 0.6, 11)
        M.scrivi(CACHE, B_INIZIO, B_FINE, 0.6, 12)
        M.scrivi(CACHE_SV, *SVILUPPO, 0.6, 13)
    voci = [prova("A_corsa_completa", "completata, promossa; letture: sviluppo, verifica; j = 1; quota 0,025", a_corsa),
            prova("B_vecchia_scheda_H002", "rifiutata prima dell'autorizzazione; nessuna lettura; registro invariato",
                  b_vecchia),
            prova("C_quota_non_collaudata", "rifiuto durevole; nessuna lettura; nessun consumo; j e N invariati",
                  c_quota),
            prova("D_concorrenza", "A consuma (j = 1); B rifiutata al ricontrollo (j previsto 2); nessuna lettura della "
                  "finestra di B", d_concorrenza),
            prova("E_file_difforme", "esito tecnico «file difforme», non decidibile; consumo mantenuto", e_difforme),
            prova("F_ripresa_dopo_il_verdetto", "rapporto rigenerato dal record senza letture; codice diverso rifiutato",
                  f_ripresa),
            prova("G_giorno_omesso_nel_registro", "rifiutata prima dell'autorizzazione (manifesto con anomalie)",
                  g_omesso)]
    print(json.dumps({"candidato": candidato(), "finestra": {"lettura": [LETTURA.isoformat(), FINE.isoformat()],
                      "accessorie_giorni": ACCESSORIE, "verifica": [INIZIO.isoformat(), FINE.isoformat()]},
                      "prove": voci}, ensure_ascii=False, indent=1, default=str))
