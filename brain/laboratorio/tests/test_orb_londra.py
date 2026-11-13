"""Test del simulatore di H-002 v2 (laboratorio/simulatori/orb_londra.py), scritti DALLA SCHEDA
(brain/laboratorio/ipotesi/H-002-ORB-v2.md) con numeri calcolati a mano. Dati inventati.
Nota: il simulatore è stato scritto prima di questi test (deroga dichiarata alla regola TDD).
Uso (dalla radice del repository): python3 -s -B -W error -m unittest brain.laboratorio.tests.test_orb_londra
"""
import sys
import unittest
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from brain.laboratorio.simulatori import orb_londra as O       # noqa: E402

UTC = timezone.utc
SPREAD = 0.3


def giorni_lavorativi_prima(g, n):
    out, d = [], g
    while len(out) < n:
        d -= timedelta(days=1)
        if d.weekday() < 5 and d not in O.esclusi(d.year):
            out.append(d)
    return sorted(out)


class Mercato:
    """Minuti BID (e ASK = BID + spread) dalle 07:00 alle 17:00 UTC; a gennaio Londra = UTC."""

    def __init__(self):
        self.bid, self.ask = {}, {}

    def minuto(self, t, o, h, l, c, spread=SPREAD, spread_alto=None):
        self.bid[t] = (o, h, l, c)
        sa = spread if spread_alto is None else spread_alto
        self.ask[t] = (o + spread, h + sa, l + spread, c + spread)

    def giornata(self, g, prezzo_fn):
        t = datetime(g.year, g.month, g.day, 7, 0, tzinfo=UTC)
        while t < datetime(g.year, g.month, g.day, 17, 0, tzinfo=UTC):
            o, h, l, c = prezzo_fn(t)
            self.minuto(t, o, h, l, c)
            t += timedelta(minutes=1)

    def storia(self, g, a=5.0):
        """20 sessioni precedenti con range di apertura largo `a` (mediana = a)."""
        for d in giorni_lavorativi_prima(g, 20):
            def f(t, d=d):
                if time(8, 0) <= t.time() < time(8, 30):
                    return 2000.0, 2000.0 + a / 2, 2000.0 - a / 2, 2000.0
                return 2000.0, 2000.0, 2000.0, 2000.0
            self.giornata(d, f)


G = date(2026, 1, 7)    # mercoledì


def rialzo(t):
    """Range 1998–2002 (A = 4); la candela 08:30–08:45 chiude a 2003 (segnale di acquisto); dalle 08:45 sale di
    0,1 al minuto fino a 2012 e lì resta."""
    hm = t.time()
    if hm < time(8, 0):
        return 2000.0, 2000.0, 2000.0, 2000.0
    if hm < time(8, 30):
        return 2000.0, 2002.0, 1998.0, 2000.0
    if hm < time(8, 45):
        return 2003.0, 2003.0, 2003.0, 2003.0
    minuti = (t - datetime(G.year, G.month, G.day, 8, 45, tzinfo=UTC)).seconds // 60
    p = min(2012.0, 2003.0 + 0.1 * minuti)
    return p, p, p, p


class TestCalendario(unittest.TestCase):
    def test_pasqua_e_giorni_esclusi(self):
        self.assertEqual(O.pasqua(2024), date(2024, 3, 31))
        self.assertEqual(O.pasqua(2025), date(2025, 4, 20))
        self.assertEqual(O.pasqua(2026), date(2026, 4, 5))
        e = O.esclusi(2026)
        for d in (date(2026, 4, 3), date(2026, 4, 6), date(2026, 12, 24), date(2026, 12, 31), date(2026, 1, 1)):
            self.assertIn(d, e)
        self.assertNotIn(date(2026, 4, 7), e)


class TestAcquistoConTarget(unittest.TestCase):
    """Calcolo a mano (V-T): ingresso = ASK 2003,3 + 0,10 = 2003,4; stop 1998; rischio 5,4 (≥ 0,25 × 4);
    target 2003,4 + 1,5 × 5,4 = 2011,5. Perdita allo stop per oncia = 2003,4 − (1998 − 0,2) = 5,6;
    once = floor(500 / (5,6 + 0,07)) = 88. Vince al target: 88 × (8,1 − 0,07) = 706,64 USD = 1,41328 R.
    V-S: uscita alle 16:30 al BID 2012 − 0,2 = 2011,8: 88 × (8,4 − 0,07) = 733,04 USD = 1,46608 R."""

    def setUp(self):
        m = Mercato()
        m.storia(G)
        m.giornata(G, rialzo)
        self.bid, self.ask = m.bid, m.ask

    def test_giorno_valido_con_segnale_di_acquisto(self):
        g = [x for x in O.prepara(self.bid, self.ask) if x.data == G][0]
        self.assertTrue(g.valido, g.motivo)
        self.assertEqual((g.ra_alto, g.ra_basso, g.a), (2002.0, 1998.0, 4.0))
        self.assertEqual(g.lato, "acquisto")
        self.assertEqual(g.minuti[0][0], datetime(2026, 1, 7, 8, 45, tzinfo=UTC))

    def test_v_t(self):
        tr = O.trade(O.prepara(self.bid, self.ask), O.V_T)
        self.assertEqual(len(tr), 1)
        x = tr[0]
        self.assertEqual((x["motivo"], x["once"]), ("target", 88))
        self.assertAlmostEqual(x["entrata"], 2003.4)
        self.assertAlmostEqual(x["uscita"], 2011.5)
        self.assertAlmostEqual(x["r"], 1.41328, places=6)

    def test_v_s(self):
        x = O.trade(O.prepara(self.bid, self.ask, O.V_S), O.V_S)[0]
        self.assertEqual(x["motivo"], "fine sessione")
        self.assertAlmostEqual(x["uscita"], 2011.8)
        self.assertAlmostEqual(x["r"], 1.46608, places=6)

    def test_stress_peggiora(self):
        stress = O.Parametri(stress=0.2)
        self.assertLess(O.trade(O.prepara(self.bid, self.ask, stress), stress)[0]["r"],
                        O.trade(O.prepara(self.bid, self.ask), O.V_T)[0]["r"])


class TestVenditaStopSullAsk(unittest.TestCase):
    """Rilievo di Gemini: lo stop di una vendita scatta quando l'ASK tocca RA alto, anche se il BID non lo tocca.
    Range 1998–2002, candela 08:30–08:45 chiude a 1997 (vendita); ingresso BID 1997 − 0,1 = 1996,9. Alle 09:30 il BID
    sale a massimo 2001,8 ma l'ASK (spread 0,3 sul massimo) arriva a 2002,1: stop a 2002 + 0,2 = 2002,2."""

    def test_stop_sull_ask(self):
        m = Mercato()
        m.storia(G)

        def f(t):
            hm = t.time()
            if time(8, 0) <= hm < time(8, 30):
                return 2000.0, 2002.0, 1998.0, 2000.0
            if time(8, 30) <= hm < time(9, 30):
                return 1997.0, 1997.0, 1997.0, 1997.0
            if hm == time(9, 30):
                return 1997.0, 2001.8, 1997.0, 1999.0
            return 1999.0, 1999.0, 1999.0, 1999.0
        m.giornata(G, f)
        x = O.trade(O.prepara(m.bid, m.ask), O.V_T)[0]
        self.assertEqual((x["lato"], x["motivo"]), ("vendita", "stop"))
        self.assertAlmostEqual(x["entrata"], 1996.9)
        self.assertAlmostEqual(x["uscita"], 2002.2)
        self.assertLess(x["r"], -0.99)
        self.assertGreater(x["r"], -1.0001)


class TestFiltriEGiorni(unittest.TestCase):
    def costruisci(self, a_giorno, storia_a=5.0, giorno=G):
        m = Mercato()
        m.storia(giorno, storia_a)

        def f(t):
            if time(8, 0) <= t.time() < time(8, 30):
                return 2000.0, 2000.0 + a_giorno / 2, 2000.0 - a_giorno / 2, 2000.0
            return 2000.0, 2000.0, 2000.0, 2000.0
        m.giornata(giorno, f)
        return [x for x in O.prepara(m.bid, m.ask) if x.data == giorno]

    def test_tetto_e_minimo(self):
        self.assertEqual(self.costruisci(10.0)[0].motivo, "valido")                 # 10 = 2 × 5: ammesso
        self.assertEqual(self.costruisci(10.2)[0].motivo, "range oltre il tetto")
        self.assertEqual(self.costruisci(2.9, storia_a=3.0)[0].motivo, "range sotto il minimo dei costi")

    def test_servono_20_sessioni_precedenti(self):
        m = Mercato()
        m.giornata(G, rialzo)
        self.assertEqual(O.prepara(m.bid, m.ask)[0].motivo, "meno di 20 sessioni precedenti")

    def test_festivi_e_fine_settimana_esclusi(self):
        venerdi_santo = date(2026, 4, 3)
        self.assertEqual(self.costruisci(4.0, giorno=venerdi_santo), [])
        self.assertEqual(self.costruisci(4.0, giorno=date(2026, 1, 10)), [])          # sabato

    def test_minuti_del_range_insufficienti(self):
        m = Mercato()
        m.storia(G)
        m.giornata(G, rialzo)
        for k in range(7):                                                            # restano 23 minuti su 30
            t = datetime(2026, 1, 7, 8, k, tzinfo=UTC)
            del m.bid[t], m.ask[t]
        self.assertEqual([x for x in O.prepara(m.bid, m.ask) if x.data == G], [])

    def test_nessun_segnale_se_resta_dentro(self):
        g = self.costruisci(4.0)[0]
        self.assertTrue(g.valido)
        self.assertIsNone(g.lato)


class TestCasiLimite(unittest.TestCase):
    def test_prezzo_gia_oltre_lo_stop_e_target_nel_minuto_d_ingresso(self):
        m = Mercato()
        m.storia(G)
        m.giornata(G, rialzo)
        g = [x for x in O.prepara(m.bid, m.ask) if x.data == G][0]
        t0, b0, a0 = g.minuti[0]
        g.minuti[0] = (t0, (1997.0, 1997.0, 1997.0, 1997.0), a0)                    # BID di apertura sotto lo stop
        self.assertIsNone(O.simula(g, "acquisto", O.V_T))
        g = [x for x in O.prepara(m.bid, m.ask) if x.data == G][0]
        t0, b0, a0 = g.minuti[0]
        g.minuti[0] = (t0, (2003.0, 2020.0, 2003.0, 2003.0), a0)                    # target toccato nel 1° minuto
        self.assertNotEqual(O.simula(g, "acquisto", O.V_T)["uscita"], 2011.5 - 100)  # non conta lì
        self.assertEqual(O.simula(g, "acquisto", O.V_T)["motivo"], "target")
        self.assertGreater(O.simula(g, "acquisto", O.V_T)["entrata"], 2003.0)

    def test_stop_e_target_nello_stesso_minuto_conta_lo_stop(self):
        m = Mercato()
        m.storia(G)
        m.giornata(G, rialzo)
        g = [x for x in O.prepara(m.bid, m.ask) if x.data == G][0]
        t1, b1, a1 = g.minuti[1]
        g.minuti[1] = (t1, (2003.0, 2020.0, 1990.0, 2003.0), a1)
        self.assertEqual(O.simula(g, "acquisto", O.V_T)["motivo"], "stop")


class TestDopoLaMutazione(unittest.TestCase):
    """Test aggiunti dopo il primo giro di mutation testing (14/20): i test scritti dopo il codice lasciavano passare
    6 difetti, fra cui uno sguardo al futuro."""

    def test_mediana_solo_delle_sessioni_precedenti(self):
        """O01. Sessioni precedenti: 10 con A = 5 (le più vecchie) e 10 con A = 6, quindi mediana 5,5 e tetto 11.
        Oggi A = 11,5: escluso. Se la mediana includesse oggi (e perdesse la più vecchia) sarebbe 6, tetto 12: ammesso."""
        m = Mercato()
        for k, d in enumerate(giorni_lavorativi_prima(G, 20)):
            a = 5.0 if k < 10 else 6.0

            def f(t, a=a):
                if time(8, 0) <= t.time() < time(8, 30):
                    return 2000.0, 2000.0 + a / 2, 2000.0 - a / 2, 2000.0
                return 2000.0, 2000.0, 2000.0, 2000.0
            m.giornata(d, f)

        def oggi(t):
            if time(8, 0) <= t.time() < time(8, 30):
                return 2000.0, 2005.75, 1994.25, 2000.0
            return 2000.0, 2000.0, 2000.0, 2000.0
        m.giornata(G, oggi)
        g = [x for x in O.prepara(m.bid, m.ask) if x.data == G][0]
        self.assertEqual(g.motivo, "range oltre il tetto")

    def mercato_con(self, prezzo_fn):
        m = Mercato()
        m.storia(G)
        m.giornata(G, prezzo_fn)
        return O.prepara(m.bid, m.ask)

    def test_chiusura_della_candela_dall_ultimo_minuto(self):
        """O06. Nella candela 08:30–08:45 il primo minuto chiude dentro (2000), l'ultimo sopra (2003): segnale."""
        def f(t):
            hm = t.time()
            if time(8, 0) <= hm < time(8, 30):
                return 2000.0, 2002.0, 1998.0, 2000.0
            if hm == time(8, 30):
                return 2000.0, 2000.0, 2000.0, 2000.0
            if time(8, 31) <= hm:
                return 2003.0, 2003.0, 2003.0, 2003.0
            return 2000.0, 2000.0, 2000.0, 2000.0
        g = [x for x in self.mercato_con(f) if x.data == G][0]
        self.assertEqual((g.lato, g.minuti[0][0].time()), ("acquisto", time(8, 45)))

    def test_ultima_candela_di_segnale_alle_15_15(self):
        """O07. La rottura arriva solo nella candela che apre alle 15:15: il trade si fa, ingresso alle 15:30."""
        def f(t):
            hm = t.time()
            if time(8, 0) <= hm < time(8, 30):
                return 2000.0, 2002.0, 1998.0, 2000.0
            if hm >= time(15, 15):
                return 2003.0, 2003.0, 2003.0, 2003.0
            return 2000.0, 2000.0, 2000.0, 2000.0
        g = [x for x in self.mercato_con(f) if x.data == G][0]
        self.assertEqual((g.lato, g.minuti[0][0].time()), ("acquisto", time(15, 30)))
        def tardi(t):
            hm = t.time()
            if time(8, 0) <= hm < time(8, 30):
                return 2000.0, 2002.0, 1998.0, 2000.0
            if hm >= time(15, 30):
                return 2003.0, 2003.0, 2003.0, 2003.0
            return 2000.0, 2000.0, 2000.0, 2000.0
        self.assertIsNone([x for x in self.mercato_con(tardi) if x.data == G][0].lato)

    def test_target_nel_minuto_d_ingresso_non_conta(self):
        """O10. Nel minuto d'ingresso il BID tocca 2020 (oltre il target 2011,5), poi scende sotto 1998: stop."""
        giorni = self.mercato_con(rialzo)
        g = [x for x in giorni if x.data == G][0]
        t0, b0, a0 = g.minuti[0]
        g.minuti[0] = (t0, (2003.0, 2020.0, 2003.0, 2003.0), a0)
        t1, b1, a1 = g.minuti[1]
        g.minuti[1] = (t1, (2003.0, 2003.0, 1997.0, 1997.0), a1)
        self.assertEqual(O.simula(g, "acquisto", O.V_T)["motivo"], "stop")

    def test_rischio_troppo_piccolo_niente_trade(self):
        """O16. Range 1998–2002 (A = 4, minimo 1). Dopo il segnale il prezzo d'ingresso è 1998,5 BID (ASK 1998,8
        + 0,1 = 1998,9): rischio 0,9 < 1, il trade non si fa."""
        giorni = self.mercato_con(rialzo)
        g = [x for x in giorni if x.data == G][0]
        t0, b0, a0 = g.minuti[0]
        g.minuti[0] = (t0, (1998.5, 1998.5, 1998.5, 1998.5), (1998.8, 1998.8, 1998.8, 1998.8))
        self.assertIsNone(O.simula(g, "acquisto", O.V_T))

    def test_stress_valori_esatti(self):
        """O18. Stress 0,2: ingresso 2003,3 + 0,1 + 0,2 = 2003,6; rischio 5,6; target 2012,0 (raggiunto).
        Perdita allo stop = 2003,6 − (1998 − 0,2 − 0,2) = 6,0; once = floor(500 / 6,07) = 82;
        82 × (8,4 − 0,07) = 683,06 USD = 1,36612 R."""
        stress = O.Parametri(stress=0.2)
        x = O.trade(self.mercato_con(rialzo), stress)[0]
        self.assertAlmostEqual(x["entrata"], 2003.6)
        self.assertEqual((x["motivo"], x["once"]), ("target", 82))
        self.assertAlmostEqual(x["r"], 1.36612, places=6)


class TestBenchmarkEMetriche(unittest.TestCase):
    def test_specchio_stessa_distanza_dalla_parte_giusta(self):
        m = Mercato()
        m.storia(G)
        m.giornata(G, rialzo)
        giorni = O.prepara(m.bid, m.ask)
        base = O.trade(giorni, O.V_T)
        self.assertEqual(O.specchio(giorni, O.V_T, "acquisto"), base)
        vendita = O.specchio(giorni, O.V_T, "vendita")[0]
        self.assertEqual(vendita["lato"], "vendita")
        # vende a 2003 − 0,1 = 2002,9 con stop alla stessa distanza (5,4) → 2008,3; il prezzo sale: stop
        self.assertAlmostEqual(vendita["entrata"], 2002.9)
        self.assertEqual(vendita["motivo"], "stop")
        self.assertAlmostEqual(vendita["uscita"], 2002.9 + 5.4 + 0.2)

    def test_metriche(self):
        tr = [{"data": date(2025, 1, 2), "lato": "acquisto", "r": 1.0},
              {"data": date(2025, 1, 3), "lato": "vendita", "r": -1.0},
              {"data": date(2026, 1, 2), "lato": "vendita", "r": -1.0},
              {"data": date(2026, 1, 5), "lato": "acquisto", "r": 2.0}]
        x = O.metriche(tr)
        self.assertEqual((x["n"], x["vinti"], x["r_medio"]), (4, 0.5, 0.25))
        self.assertEqual((x["dd_max"], x["serie_perdite"]), (2.0, 2))
        self.assertEqual((x["r_vendite"], x["n_vendite"], x["r_acquisti"]), (-1.0, 2, 1.5))
        self.assertEqual(x["per_anno"], {2025: (2, 0.0), 2026: (2, 0.5)})


if __name__ == "__main__":
    unittest.main()
