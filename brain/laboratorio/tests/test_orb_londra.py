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

    def giornata(self, g, prezzo_fn, spread=SPREAD):
        t = datetime(g.year, g.month, g.day, 7, 0, tzinfo=UTC)
        while t < datetime(g.year, g.month, g.day, 17, 0, tzinfo=UTC):
            o, h, l, c = prezzo_fn(t)
            self.minuto(t, o, h, l, c, spread=spread)
            t += timedelta(minutes=1)

    def storia(self, g, a=5.0, spread=0.1):
        """20 sessioni precedenti con range di apertura largo `a` (mediana = a) e spread `spread`: il costo di
        riferimento è spread + 0,07 + 0,10 + 0,20 (con 0,1: 0,47, minimo dell'ampiezza 6 × 0,47 = 2,82 USD)."""
        for d in giorni_lavorativi_prima(g, 20):
            def f(t, d=d):
                if time(8, 0) <= t.time() < time(8, 30):
                    return 2000.0, 2000.0 + a / 2, 2000.0 - a / 2, 2000.0
                return 2000.0, 2000.0, 2000.0, 2000.0
            self.giornata(d, f, spread)


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
        self.assertEqual(self.costruisci(2.7, storia_a=3.0)[0].motivo, "range sotto il minimo dei costi")
        self.assertEqual(self.costruisci(2.9, storia_a=3.0)[0].motivo, "valido")               # 2,9 ≥ 2,82

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


class TestRiletturaGemini(unittest.TestCase):
    """Rilievi di Gemini G-20261114-03 sulla v2, verificati da Claude: test scritti PRIMA delle correzioni."""

    def prepara(self, prezzo_fn, togli=(), modifica=None, storia_spread=0.1):
        m = Mercato()
        m.storia(G, spread=storia_spread)
        m.giornata(G, prezzo_fn)
        for t in togli:
            m.bid.pop(t, None)
            m.ask.pop(t, None)
        if modifica:
            modifica(m)
        return [x for x in O.prepara(m.bid, m.ask) if x.data == G]

    def test_stop_in_salto_eseguito_all_apertura(self):
        """Il minuto dopo l'ingresso apre a 1996, già sotto lo stop 1998: si esce a 1996 − 0,2 = 1995,8, non a
        1998 − 0,2 (sarebbe un vantaggio irreale)."""
        g = self.prepara(rialzo)[0]
        t1, b1, a1 = g.minuti[1]
        g.minuti[1] = (t1, (1996.0, 1996.0, 1995.0, 1995.5), (1996.3, 1996.3, 1995.3, 1995.8))
        x = O.simula(g, "acquisto", O.V_T)
        self.assertEqual(x["motivo"], "stop")
        self.assertAlmostEqual(x["uscita"], 1995.8)

    def test_stop_in_salto_della_vendita(self):
        """Vendita: l'ASK apre a 2003, sopra RA alto 2002: uscita 2003 + 0,2 = 2003,2."""
        def f(t):
            hm = t.time()
            if time(8, 0) <= hm < time(8, 30):
                return 2000.0, 2002.0, 1998.0, 2000.0
            if hm < time(9, 30):
                return 1997.0, 1997.0, 1997.0, 1997.0
            return 2002.7, 2002.7, 2002.7, 2002.7
        x = O.trade(self.prepara(f), O.V_T)[0]
        self.assertEqual((x["lato"], x["motivo"]), ("vendita", "stop"))
        self.assertAlmostEqual(x["uscita"], 2003.2)

    def test_fine_sessione_senza_quotazioni_vicine(self):
        """Mancano i minuti dalle 16:30 alle 16:50: il primo dopo è alle 16:51, oltre le 16:45. Si esce alla chiusura
        dell'ultimo minuto prima delle 16:30 (BID 2012) − 0,2 = 2011,8, mai più tardi."""
        togli = [datetime(2026, 1, 7, 16, k, tzinfo=UTC) for k in range(30, 51)]
        x = O.trade(self.prepara(rialzo, togli), O.V_S)[0]
        self.assertEqual(x["motivo"], "fine sessione senza quotazioni")
        self.assertAlmostEqual(x["uscita"], 2011.8)

    def test_ingresso_solo_dentro_la_candela_successiva(self):
        """Il segnale finisce alle 08:45; se mancano tutti i minuti dalle 08:45 alle 08:59, l'ingresso alle 09:00 è
        oltre la candela successiva: niente trade."""
        togli = [datetime(2026, 1, 7, 8, k, tzinfo=UTC) for k in range(45, 60)]
        g = self.prepara(rialzo, togli)[0]
        self.assertIsNone(g.minuti)
        self.assertEqual(g.motivo, "ingresso oltre la candela successiva")
        self.assertEqual(O.trade([g], O.V_T), [])

    def test_spread_negativo_minuto_non_eseguibile(self):
        """Un minuto con ASK sotto il BID è un dato errato: non si usa per eseguire (come se mancasse) e si conta.
        Escludere il GIORNO sarebbe uno sguardo al futuro: alle 08:45, quando si entra, il minuto delle 09:00 non si
        conosce ancora (errore di Claude nella prima stesura di questo test)."""
        def rompi(m):
            t = datetime(2026, 1, 7, 9, 0, tzinfo=UTC)
            b = m.bid[t]
            m.ask[t] = (b[0] - 0.5, b[1], b[2] - 0.5, b[3])
        g = self.prepara(rialzo, modifica=rompi)[0]
        self.assertTrue(g.valido)
        self.assertNotIn(datetime(2026, 1, 7, 9, 0, tzinfo=UTC), [x[0] for x in g.minuti])
        self.assertEqual(g.minuti_scartati, 1)

    def test_minimo_dell_ampiezza_dai_costi_veri(self):
        """Storia con spread 0,3: costo di riferimento 0,3 + 0,07 + 0,1 + 0,2 = 0,67, minimo 4,02 USD; oggi A = 4:
        escluso. Con spread 0,1 (minimo 2,82) lo stesso giorno è valido."""
        self.assertEqual(self.prepara(rialzo, storia_spread=0.3)[0].motivo, "range sotto il minimo dei costi")
        self.assertEqual(self.prepara(rialzo, storia_spread=0.1)[0].motivo, "valido")

    def test_festivi_inglesi(self):
        e = O.esclusi
        for d in (date(2026, 5, 4), date(2026, 5, 25), date(2026, 8, 31), date(2020, 5, 8), date(2022, 6, 2),
                  date(2022, 6, 3), date(2022, 9, 19), date(2023, 5, 8), date(2012, 6, 4), date(2012, 6, 5),
                  date(2011, 4, 29), date(2021, 12, 27), date(2021, 12, 28), date(2022, 1, 3), date(2022, 12, 27)):
            self.assertIn(d, e(d.year), d)
        for d in (date(2020, 5, 4), date(2012, 5, 28), date(2022, 5, 30), date(2026, 5, 5)):
            self.assertNotIn(d, e(d.year), d)


class TestRevisioneDeepSeek(unittest.TestCase):
    """Rilievi della revisione esterna di DeepSeek sulla v3 (14/11/2026), verificati da Claude; test scritti PRIMA
    delle correzioni, più i casi della sua sezione C che i test non coprivano."""

    def mercato(self, prezzo_fn, storia_spread=0.1, togli_ask_storia=0):
        m = Mercato()
        m.storia(G, spread=storia_spread)
        if togli_ask_storia:                     # nelle prime sessioni della storia manca l'ASK dalle 08:30 in poi
            for d in giorni_lavorativi_prima(G, 20)[:togli_ask_storia]:
                for t in [t for t in m.ask if t.date() == d and t.time() >= time(8, 30)]:
                    del m.ask[t]
        m.giornata(G, prezzo_fn)
        return m

    def test_spread_richiesto_in_almeno_15_sessioni_su_20(self):
        """B1.8/B1.9. Con 6 sessioni precedenti senza ASK restano 14 spread: giorno non valido. Con 5: valido."""
        g = [x for x in O.prepara(*self.bidask(self.mercato(rialzo, togli_ask_storia=6))) if x.data == G][0]
        self.assertEqual(g.motivo, "manca lo spread delle sessioni precedenti")
        g = [x for x in O.prepara(*self.bidask(self.mercato(rialzo, togli_ask_storia=5))) if x.data == G][0]
        self.assertEqual(g.motivo, "valido")

    def bidask(self, m):
        return m.bid, m.ask

    def test_sharpe_con_deviazione_campionaria(self):
        """B1.7. r = 1, −1, 1, −1, 2: media 0,4; scarti al quadrato 0,36 + 1,96 + 0,36 + 1,96 + 2,56 = 7,2; deviazione
        campionaria sqrt(7,2 / 4) = 1,34164 → Sharpe 0,29814 (con la deviazione di popolazione sarebbe 0,33333).
        Prima stesura del test con la somma sbagliata (4,6): errore aritmetico di Claude, corretto."""
        tr = [{"data": date(2025, 1, k + 2), "lato": "acquisto", "r": r} for k, r in enumerate((1, -1, 1, -1, 2))]
        self.assertAlmostEqual(O.metriche(tr)["sharpe"], 0.4 / (7.2 / 4) ** 0.5, places=6)

    def test_somme_per_anno_e_ultimi_anni(self):
        """B1.6. per_anno riporta (trade, media, somma); somma degli ultimi 2 anni = 0 + 1 = 1."""
        tr = [{"data": date(2024, 3, 1), "lato": "acquisto", "r": -3.0},
              {"data": date(2025, 3, 1), "lato": "vendita", "r": 1.0}, {"data": date(2025, 3, 2), "lato": "vendita", "r": -1.0},
              {"data": date(2026, 3, 1), "lato": "acquisto", "r": 1.0}]
        x = O.metriche(tr)
        self.assertEqual(x["per_anno"][2025], (2, 0.0, 0.0))
        self.assertEqual(O.somma_ultimi_anni(tr, 2), 1.0)

    def test_specchio_richiede_la_direzione(self):
        """B1.14. Senza direzione fissa né direzioni per giorno: errore esplicito, non KeyError."""
        with self.assertRaises(ValueError):
            O.specchio(O.prepara(*self.bidask(self.mercato(rialzo))), O.V_T)

    def test_resoconto_dei_giorni(self):
        """B1.5/B1.11. Il resoconto conta i giorni esclusi per motivo (anche fine settimana e festivi) e i minuti con
        spread negativo di TUTTE le sessioni di base, non solo dei giorni con segnale."""
        m = self.mercato(rialzo)
        m.giornata(date(2026, 1, 3), lambda t: (2000.0, 2000.0, 2000.0, 2000.0))   # un sabato con dati
        t = datetime(2026, 1, 6, 10, 0, tzinfo=UTC)                 # sessione della storia, senza segnale
        b = m.bid[t]
        m.ask[t] = (b[0] - 0.5, b[1], b[2] - 0.5, b[3])
        r = O.resoconto(m.bid, m.ask)
        self.assertEqual(r["minuti_spread_negativo"], 1)
        self.assertEqual(r["giorni_per_motivo"]["valido"], 1)
        self.assertEqual(r["giorni_per_motivo"]["meno di 20 sessioni precedenti"], 20)
        self.assertEqual(r["giorni_per_motivo"]["fine settimana o festivo"], 1)

    def test_ora_legale_range_di_trenta_minuti(self):
        """C1. Lunedì 30/3/2026, primo giorno feriale con l'ora legale inglese: il range va dalle 07:00 alle 07:30 UTC."""
        g = date(2026, 3, 30)
        m = Mercato()
        m.storia(g)

        def f(t):
            if datetime(2026, 3, 30, 7, 0, tzinfo=UTC) <= t < datetime(2026, 3, 30, 7, 30, tzinfo=UTC):
                return 2000.0, 2002.0, 1998.0, 2000.0
            return 2000.0, 2000.0, 2000.0, 2000.0
        m.giornata(g, f)
        x = [x for x in O.prepara(m.bid, m.ask) if x.data == g][0]
        self.assertEqual((x.ra_alto, x.ra_basso, x.motivo), (2002.0, 1998.0, "valido"))

    def test_target_della_vendita_sull_ask(self):
        """C1. Vendita a 1996,9 (BID 1997 − 0,1), stop 2002, rischio 5,1, target 1996,9 − 7,65 = 1989,25. Il BID scende a
        1989,1 ma l'ASK (spread 0,3) solo a 1989,4: niente target. Quando l'ASK arriva a 1989,2: target a 1989,25."""
        def f(t):
            hm = t.time()
            if time(8, 0) <= hm < time(8, 30):
                return 2000.0, 2002.0, 1998.0, 2000.0
            if hm < time(9, 30):
                return 1997.0, 1997.0, 1997.0, 1997.0
            if hm < time(10, 0):
                return 1990.0, 1990.0, 1989.1, 1990.0
            return 1989.0, 1989.0, 1988.9, 1989.0
        m = self.mercato(f)
        x = O.trade(O.prepara(m.bid, m.ask), O.V_T)[0]
        self.assertEqual((x["lato"], x["motivo"]), ("vendita", "target"))
        self.assertAlmostEqual(x["uscita"], 1989.25)

    def test_minuto_delle_16_30_esce_all_apertura(self):
        """C1. Nel minuto delle 16:30 il BID tocca sia lo stop sia il target: si esce all'apertura (2012 − 0,2)."""
        m = self.mercato(rialzo)
        t = datetime(2026, 1, 7, 16, 30, tzinfo=UTC)
        m.bid[t] = (2005.0, 2030.0, 1990.0, 2005.0)
        m.ask[t] = (2005.3, 2030.3, 1990.3, 2005.3)
        x = O.trade(O.prepara(m.bid, m.ask, O.V_S), O.V_S)[0]
        self.assertEqual(x["motivo"], "fine sessione")
        self.assertAlmostEqual(x["uscita"], 2004.8)

    def test_due_rotture_un_solo_trade(self):
        """C1. Rottura sopra alle 08:45, poi il prezzo rompe sotto: un solo trade, il primo."""
        def f(t):
            hm = t.time()
            if time(8, 0) <= hm < time(8, 30):
                return 2000.0, 2002.0, 1998.0, 2000.0
            if hm < time(8, 45):
                return 2003.0, 2003.0, 2003.0, 2003.0
            if hm < time(9, 0):
                return 2001.0, 2001.0, 2001.0, 2001.0
            return 1996.0, 1996.0, 1996.0, 1996.0
        m = self.mercato(f)
        tr = O.trade(O.prepara(m.bid, m.ask), O.V_T)
        self.assertEqual([x["lato"] for x in tr], ["acquisto"])

    def test_once_meno_di_uno_niente_trade(self):
        """C1. Perdita allo stop 5,6 + 0,07 USD per oncia: con un rischio di 5 USD le once sono 0, quindi niente trade."""
        m = self.mercato(rialzo)
        par = O.Parametri(rischio_usd=5.0)                          # 5 / (5,6 + 0,07) < 1
        self.assertEqual(O.trade(O.prepara(m.bid, m.ask, par), par), [])

    def test_rischio_al_limite_del_quarto_di_a(self):
        """C1. A = 4, minimo 1: rischio 1,0 → trade; 0,9 → niente (già coperto). Ingresso ASK 1998,7 + 0,1 = 1998,8,
        stop 1998, rischio 0,8: niente; ingresso 1998,9 + 0,1 = 1999,0, rischio 1,0: trade."""
        m = self.mercato(rialzo)
        g = [x for x in O.prepara(m.bid, m.ask) if x.data == G][0]
        t0, b0, a0 = g.minuti[0]
        g.minuti[0] = (t0, (1998.6, 1998.6, 1998.6, 1998.6), (1998.9, 1998.9, 1998.9, 1998.9))
        self.assertIsNotNone(O.simula(g, "acquisto", O.V_T))
        g.minuti[0] = (t0, (1998.4, 1998.4, 1998.4, 1998.4), (1998.7, 1998.7, 1998.7, 1998.7))
        self.assertIsNone(O.simula(g, "acquisto", O.V_T))


class TestFestiviUfficiali(unittest.TestCase):
    """I festivi del codice coincidono con il file ufficiale gov.uk (dati/riferimenti/uk_bank_holidays.json, commit
    ac17502), che copre dal 2019 al 2028. Per il 2005–2018 il file non c'è: le date straordinarie del 2011 e del 2012
    restano dalla conoscenza di Claude (dichiarato nella scheda)."""

    def test_coincidono_con_gov_uk(self):
        import json
        f = repo_root / "brain" / "dati" / "riferimenti" / "uk_bank_holidays.json"
        eventi = json.loads(f.read_text(encoding="utf-8"))["england-and-wales"]["events"]
        ufficiali = {}
        for e in eventi:
            d = date.fromisoformat(e["date"])
            ufficiali.setdefault(d.year, set()).add(d)
        self.assertEqual(min(ufficiali), 2019)
        for anno, giorni in ufficiali.items():
            self.assertEqual(O.festivi_inglesi(anno), giorni, anno)


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
        self.assertEqual(x["per_anno"], {2025: (2, 0.0, 0.0), 2026: (2, 0.5, 1.0)})


if __name__ == "__main__":
    unittest.main()
