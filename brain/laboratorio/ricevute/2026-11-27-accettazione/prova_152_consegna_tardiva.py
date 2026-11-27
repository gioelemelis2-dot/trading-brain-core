import sys, io, contextlib, json
from unittest import mock
sys.path.insert(0, ".")
import brain.laboratorio.tests.test_esegui_verifica as T
from brain.laboratorio.esecuzione import esegui_verifica as EV, riserva as RV, sigillo as S
T.setUpModule()
class X(T.Percorso):
    def runTest(self): pass
X.setUpClass(); x = X(); x.setUp()
try:
    scheda = x.prepara(); rap = x.d / "r.txt"
    arg = ["--scheda", str(scheda), "--registro", str(x.registro), "--riserva", str(x.riserva), "--prenotazione", "P1",
           "--cache", str(x.cache), "--cache-sviluppo", str(x.cache_sv), "--rapporto", str(rap), "--ora", T.ORA]
    vero = EV.os.replace
    def cade(a, b): raise OSError(28, "No space left on device (simulato)")
    rc, tipo = None, None
    import os, types
    finto = types.SimpleNamespace(**{k: getattr(os, k) for k in dir(os) if not k.startswith("__")}); finto.replace = cade
    with mock.patch.object(EV, "os", finto), contextlib.redirect_stdout(io.StringIO()):
        try: rc = EV.main(arg)
        except BaseException as e: tipo = f"{type(e).__name__}: {e}"
    p = RV.prenotazione(x.riserva, "P1")
    print(json.dumps({"rc_main": rc, "eccezione_non_catturata": tipo, "esito_riserva": p["esito"],
          "voci": [e["ruolo"] for e in S.leggi(x.registro)["esecuzioni"]], "rapporto": rap.exists(),
          "orfani": sorted(f.name for f in rap.parent.iterdir() if f.name.startswith(".r.txt."))}, ensure_ascii=False))
    r2 = EV.main(arg)
    print("dopo la riparazione: rc", r2, "| rapporto identico al record:", rap.read_text(encoding="utf-8") == EV.rapporto_da_record(RV.record_esito(x.riserva, "P1")))
finally:
    x.tearDown(); T.tearDownModule()
