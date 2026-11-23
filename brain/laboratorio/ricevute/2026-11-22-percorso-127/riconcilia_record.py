"""Riconciliazione del record di una verifica (DGS-17), 23/11/2026. Non legge dati di mercato: solo i registri e il
rapporto di una prova della ricevuta (cartella `A_corsa_completa` prodotta da ricevuta_127.py).

Controlla:
1. identità: impronta dell'impegno nel registro della riserva = impronta nel record; finestra, scheda, codice, seme;
2. sedute: l'elenco nell'impegno (fissato prima dell'autorizzazione) = le date delle coppie del record, nello stesso
   ordine, senza doppioni; K = 0 solo con S = 0;
3. media = somma degli S / somma dei K, in frazioni esatte, arrotondata una volta;
4. verdetto RICALCOLATO dalle sole coppie del record (stesso seme, veto per blocchi della scheda, contesto N
   registrato) uguale a quello registrato: L, U, segnale, esito, causa, requisiti;
5. rapporto sul disco = rapporto rigenerato dal record, byte per byte (confronto dei byte, non del testo decodificato:
   DGS-18, la lettura come testo può normalizzare le terminazioni di riga).
Uso (dalla radice): python3 -s -B brain/laboratorio/ricevute/2026-11-22-percorso-127/riconcilia_record.py <cartella A>
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from brain.laboratorio.esecuzione import esegui_verifica as EV     # noqa: E402
from brain.laboratorio.esecuzione import riserva as RV             # noqa: E402
from brain.laboratorio.verdetto import verdetto_d31 as V           # noqa: E402

d = Path(sys.argv[1])
p = RV.prenotazione(d / "riserva.json", "P1")
rec, imp = p["record"], p["autorizzazione"]["impegno"]
esiti = {}
esiti["1 identità"] = (rec["impronta_impegno"] == RV.impronta_impegno(imp) == p["autorizzazione"]["hash_dati"]
                       and rec["identita"]["finestra"] == imp["finestra"]
                       and rec["identita"]["scheda_sha256"] == imp["scheda_sha256"]
                       and rec["identita"]["codice"] == imp["codice"] and rec["identita"]["seme"] == imp["seme"])
date = [c[0] for c in rec["coppie"]]
esiti["2 sedute"] = (date == imp["sedute"] and len(set(date)) == len(date) == 1000
                     and all(c[1] == 0 for c in rec["coppie"] if c[2] == 0))
v = rec["verdetto"]
esatta = sum(Fraction(c[1]) for c in rec["coppie"]) / sum(c[2] for c in rec["coppie"])
esiti["3 media"] = v["media"] == float(esatta)
cp = [(c[1], c[2]) for c in rec["coppie"]]
vb = imp["contratto"]["veto_blocchi"]
veto = V.veto_blocchi(cp, vb["soglia"], vb["minimo_trade"])
ctx = {"registro": v["contesto_prove"]["registro"], "n_prove": v["contesto_prove"]["n_prove"],
       "impronta": v["contesto_prove"]["impronta"]}
w = json.loads(json.dumps(V.verdetto(cp, imp["seme"], [veto], contesto=ctx), default=str))
chiavi = ("L", "U", "segnale", "esito", "causa", "requisiti", "sedute", "trade", "sedute_attive")
esiti["4 verdetto ricalcolato"] = all(w[k] == v[k] for k in chiavi)
esiti["5 rapporto"] = (d / "rapporto_P1.txt").read_bytes() == EV.rapporto_da_record(rec).encode("utf-8")   # DGS-18: byte, non testo
print(json.dumps({"python": sys.version.split()[0], "esiti": esiti, "tutti": all(esiti.values()),
                  "sedute": len(date), "sedute_attive": v["sedute_attive"], "media": v["media"],
                  "media_esadecimale": float.hex(v["media"]), "esito": v["esito"], "causa": v["causa"]},
                 ensure_ascii=False, indent=1))
sys.exit(0 if all(esiti.values()) else 1)
