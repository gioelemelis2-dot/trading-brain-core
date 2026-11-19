"""Mutation testing del modulo del verdetto D-31 (laboratorio/verdetto/verdetto_d31.py, D-34), 19/11/2026.
Stesso meccanismo di mutazioni_esecuzione.py: ogni mutante è una copia di brain/ con UN difetto; la copia non mutata deve
superare i test; ogni sostituzione deve comparire una sola volta; una sintassi rotta non conta come ucciso.
Uso (dalla radice del repository): python3 -s -B brain/laboratorio/tests/mutazioni_verdetto.py <cartella> [processi] [prefissi]
"""
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

if len(sys.argv) not in (2, 3, 4):
    sys.exit(__doc__)
BRAIN, OUT = Path(__file__).resolve().parents[2], Path(sys.argv[1]).resolve()
PROCESSI = int(sys.argv[2]) if len(sys.argv) >= 3 else 2
PREFISSI = tuple(sys.argv[3].split(",")) if len(sys.argv) == 4 else ("",)
SUITE = ["brain.laboratorio.tests.test_verdetto_d31"]
VD = "laboratorio/verdetto/verdetto_d31.py"
M = {
    "VD01 soglia di promozione 0,15": [(VD, "SOGLIA_PROMOZIONE = 0.20", "SOGLIA_PROMOZIONE = 0.15")],
    "VD02 soglia di bocciatura 0,15": [(VD, "SOGLIA_BOCCIATURA = 0.10", "SOGLIA_BOCCIATURA = 0.15")],
    "VD03 uguaglianza promuove": [(VD, "    if iv[0] > SOGLIA_PROMOZIONE:", "    if iv[0] >= SOGLIA_PROMOZIONE:")],
    "VD04 uguaglianza boccia": [(VD, "    if iv[1] < SOGLIA_BOCCIATURA:", "    if iv[1] <= SOGLIA_BOCCIATURA:")],
    "VD05 intervallo non controllato": [(VD, " or P.intervallo_valido(iv[0], iv[1]) is None or", " or")],
    "VD47 ampiezza minima 1e-10 (#119)": [(VD, "AMPIEZZA_MINIMA = 1e-9 ", "AMPIEZZA_MINIMA = 1e-10 ")],
    "VD48 ampiezza minima non controllata (#119)": [(VD, " or iv[1] - iv[0] < AMPIEZZA_MINIMA:", ":")],
    "VD06 vicinanza 1e-8": [(VD, "VICINANZA = 1e-9", "VICINANZA = 1e-8")],
    "VD07 vicinanza di U non riportata": [(VD, '        out.append("U")', "        pass")],
    "VD08 K booleano accettato": [(VD, "        if type(k) is not int or k < 0:", "        if not isinstance(k, int) or k < 0:")],
    "VD09 K negativo accettato": [(VD, "        if type(k) is not int or k < 0:", "        if type(k) is not int or k < -1:")],
    "VD10 S non finito accettato": [(VD, "        if type(s) not in (int, float) or not math.isfinite(s):", "        if type(s) not in (int, float):")],
    "VD11 risultato senza trade accettato": [(VD, "        if k == 0 and s != 0:", "        if False:")],
    "VD12 elenco vuoto accettato": [(VD, "    if not coppie:\n        raise ValueError(\"nessuna seduta\")", "    if False:\n        raise ValueError(\"nessuna seduta\")")],
    "VD13 coppia senza controllo di lunghezza (atteso EQUIVALENTE: l'assegnazione s, k = c solleva comunque ValueError)": [(VD, "        if len(c) != 2:", "        if False:")],
    "VD14 sedute collaudate 999": [(VD, "D_COLLAUDATO = 1000", "D_COLLAUDATO = 999")],
    "VD15 minimo di trade 299": [(VD, "MIN_TRADE = 300", "MIN_TRADE = 299")],
    "VD16 minimo di sedute attive 199": [(VD, "MIN_SEDUTE_ATTIVE = 200", "MIN_SEDUTE_ATTIVE = 199")],
    "VD17 impronta del pilota non controllata": [(VD, "    if P.impronta_modulo() != IMPRONTA_PILOTA:", "    if False:")],
    "VD18 seme ignorato": [(VD, "    return P.intervallo_bootstrap(coppie, random.Random(seme), B, BLOCCO)", "    return P.intervallo_bootstrap(coppie, random.Random(0), B, BLOCCO)")],
    "VD19 B = 999": [(VD, "    return P.intervallo_bootstrap(coppie, random.Random(seme), B, BLOCCO)", "    return P.intervallo_bootstrap(coppie, random.Random(seme), 999, BLOCCO)")],
    "VD20 requisito fallito senza veto boccia": [(VD, '        if r["veto"] and r["esito"] == "fallito":', '        if r["esito"] == "fallito":')],
    "VD21 veto non valutabile boccia": [(VD, '        if r["veto"] and r["esito"] == "fallito":', '        if r["veto"]:')],
    "VD22 sfavorevole non boccia": [(VD, '        return fine("bocciata", "statistica: U < +0,10 R")', '        return fine("non decidibile", "statistica: U < +0,10 R")')],
    "VD23 requisito non valutabile non blocca la promozione": [(VD, '        aperti = [r["id"] for r in req if r["esito"] != "superato"]', '        aperti = [r["id"] for r in req if r["esito"] == "fallito"]')],
    "VD24 promossa con requisiti aperti": [(VD, "        if not aperti:", "        if True:")],
    "VD25 vicini non riportati nel verdetto": [(VD, "        v[\"vicini_soglia\"] = vicini(*iv)", "        pass")],
    "VD26 media divisa per le sedute": [(VD, '    v["media"] = sum(s for s, _ in coppie) / v["trade"] if v["trade"] else None', '    v["media"] = sum(s for s, _ in coppie) / len(coppie) if v["trade"] else None')],
    "VD27 minimi non applicati": [(VD, "    if mancano:", "    if False:")],
    "VD28 intervallo invalido trattato come inconclusivo": [(VD, '    if sg == "invalido":\n        return fine', '    if False:\n        return fine')],
    "VD29 veto come intero accettato": [(VD, 'type(r.get("veto")) is not bool', 'r.get("veto") is None')],
    "VD30 screening: media uguale alla soglia passa": [(VD, '    if not s["media"] > SCREENING_MEDIA:', '    if not s["media"] >= SCREENING_MEDIA:')],
    "VD31 screening: limite zero passa": [(VD, "        if not iv[0] > 0:", "        if not iv[0] >= 0:")],
    "VD32 screening: potenza 50% esclusa": [(VD, "    if not potenza_stimata >= SCREENING_POTENZA:", "    if not potenza_stimata > SCREENING_POTENZA:")],
    "VD33 screening: potenza sopra 1 accettata": [(VD, "not 0.0 <= potenza_stimata <= 1.0:", "not 0.0 <= potenza_stimata:")],
    "VD34 screening: nessun trade non gestito": [(VD, "    if trade == 0:\n        s[", "    if False:\n        s[")],
    "VD35 screening: media divisa per le sedute": [(VD, '    s["media"] = sum(x for x, _ in coppie) / trade', '    s["media"] = sum(x for x, _ in coppie) / len(coppie)')],
    "VD36 screening: soglia di media 0,20": [(VD, "SCREENING_MEDIA = 0.25", "SCREENING_MEDIA = 0.20")],
    "VD37 screening: intervallo invalido non segnalato": [(VD, '        s["cause"].append("intervallo invalido")', '        pass')],
    "VD38 screening: coppie non controllate": [(VD, "    controlla_coppie(coppie)\n    trade = sum(k for _, k in coppie)\n    s =", "    trade = sum(k for _, k in coppie)\n    s =")],
    "VD39 blocchi: uguaglianza alla soglia fa scattare il veto": [(VD, "        elif m < soglia:", "        elif m <= soglia:")],
    "VD40 blocchi: minimo escluso": [(VD, "        if k < minimo_trade_blocco:", "        if k <= minimo_trade_blocco:")],
    "VD41 blocchi: sottile prima del veto": [(VD, '    esito = "fallito" if fallito else "non valutabile" if sottile else "superato"', '    esito = "non valutabile" if sottile else "fallito" if fallito else "superato"')],
    "VD42 blocchi: divisibilità non controllata": [(VD, " or not coppie or len(coppie) % ampiezza:", " or not coppie:")],
    "VD43 blocchi: minimo zero accettato": [(VD, "    if type(minimo_trade_blocco) is not int or minimo_trade_blocco < 1:", "    if type(minimo_trade_blocco) is not int or minimo_trade_blocco < 0:")],
    "VD44 blocchi: soglia non finita accettata": [(VD, "    if type(soglia) not in (int, float) or not math.isfinite(soglia):", "    if type(soglia) not in (int, float):")],
    "VD45 blocchi: minimo non intero accettato": [(VD, "    if type(minimo_trade_blocco) is not int or minimo_trade_blocco < 1:", "    if minimo_trade_blocco < 1:")],
    "VD46 verdetto: veto dopo il controllo dei dati": [(VD, "    for r in req:\n        if r[\"veto\"] and r[\"esito\"] == \"fallito\":\n            return fine(\"bocciata\", f\"veto: {r['id']}\")\n    try:\n        controlla_coppie(coppie)\n    except ValueError as e:\n        return fine(\"non decidibile\", f\"dati inidonei: {e}\")", "    try:\n        controlla_coppie(coppie)\n    except ValueError as e:\n        return fine(\"non decidibile\", f\"dati inidonei: {e}\")\n    for r in req:\n        if r[\"veto\"] and r[\"esito\"] == \"fallito\":\n            return fine(\"bocciata\", f\"veto: {r['id']}\")")],
}


def copia(dest):
    if dest.exists():
        shutil.rmtree(dest)
    for parte in ("dati", "laboratorio", "guardian"):
        shutil.copytree(BRAIN / parte, dest / "brain" / parte,
                        ignore=shutil.ignore_patterns("__pycache__", "cache_dukascopy", "partizioni", "*.csv", "*.secret"))


def suite(radice):
    """Suite sul mutante, con la RETE BLOCCATA (#66: un mutante che esce in rete deve fallire subito, non scaricare né
    aspettare 20 minuti). Tempo scaduto: contato come ucciso, ma segnalato da guardare."""
    senza_rete = dict(os.environ, HTTPS_PROXY="http://127.0.0.1:9", HTTP_PROXY="http://127.0.0.1:9",
                      https_proxy="http://127.0.0.1:9", http_proxy="http://127.0.0.1:9", NO_PROXY="", no_proxy="")
    try:
        return subprocess.run([sys.executable, "-s", "-B", "-W", "error", "-m", "unittest", "-f", *SUITE], cwd=radice,
                              capture_output=True, text=True, timeout=900, env=senza_rete).returncode == 0
    except subprocess.TimeoutExpired:
        print(f"ATTENZIONE: tempo scaduto in {Path(radice).name}: contato come ucciso, da guardare", flush=True)
        return False


def mutante(i, nome, sost):
    dest = OUT / f"M{i:02d}"
    copia(dest)
    for f, vecchio, nuovo in sost:
        testo = (dest / "brain" / f).read_text(encoding="utf-8")
        if testo.count(vecchio) != 1:
            shutil.rmtree(dest)
            return nome, f"ERRORE: la sostituzione compare {testo.count(vecchio)} volte in {f}"
        (dest / "brain" / f).write_text(testo.replace(vecchio, nuovo), encoding="utf-8")
        try:                                               # #59: una sintassi rotta non è un mutante ucciso
            compile((dest / "brain" / f).read_text(encoding="utf-8"), str(f), "exec")
        except SyntaxError:
            shutil.rmtree(dest)
            return nome, "NON VALIDO: sintassi rotta"
    vivo = suite(dest)
    shutil.rmtree(dest)
    return nome, "VIVO" if vivo else "UCCISO"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    copia(OUT / "M00")
    if not suite(OUT / "M00"):
        sys.exit("M00 NON supera la suite: fermo")
    shutil.rmtree(OUT / "M00")
    print("M00 copia non mutata: suite verde", flush=True)
    with ThreadPoolExecutor(PROCESSI) as ex:
        esiti = []
        for nome, esito in ex.map(lambda a: mutante(*a), [(i, n, s) for i, (n, s) in enumerate(M.items(), 1) if n.startswith(PREFISSI)]):
            esiti.append((nome, esito))                    # R17: ogni esito si stampa appena è pronto
            print(f"{esito:6} {nome}", flush=True)
    uccisi = sum(1 for _, e in esiti if e == "UCCISO")
    print(f"\n{uccisi}/{len(esiti)} mutanti uccisi ({sys.version.split()[0]})")
    return 0 if uccisi == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
