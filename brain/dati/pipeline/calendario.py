"""Calendario dell'oro: una sola fonte per le chiusure note, usata dal controllo della cache (dati) e dal caricatore
del laboratorio. Prima ognuno aveva la sua copia e la correzione #50 (R12bis-A3-03) arrivava solo a uno dei due."""
from datetime import date, timedelta


def pasqua(anno: int) -> date:
    """Domenica di Pasqua (calendario gregoriano, algoritmo anonimo di Meeus/Jones/Butcher)."""
    a, b, c = anno % 19, anno // 100, anno % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    return date(anno, (h + l_ - 7 * m + 114) // 31, (h + l_ - 7 * m + 114) % 31 + 1)


def chiusure_note(anno: int) -> set:
    """Giorni feriali in cui l'oro può non avere scambi, tollerati SOLO se vuoti (R11-S2, #50):
    1° gennaio, 25 e 26 dicembre, Venerdì Santo, Lunedì dell'Angelo, e i giorni che li sostituiscono quando cadono
    nel fine settimana (regole britanniche e statunitensi):
    - 1° gennaio di sabato: venerdì 31 dicembre e lunedì 3 gennaio; di domenica: lunedì 2 gennaio;
    - 25 dicembre di venerdì: lunedì 28; di sabato: venerdì 24, lunedì 27 e martedì 28; di domenica: martedì 27."""
    g = set()
    for a in (anno - 1, anno, anno + 1):
        cap, nat = date(a, 1, 1), date(a, 12, 25)
        g |= {cap, nat, date(a, 12, 26), pasqua(a) - timedelta(days=2), pasqua(a) + timedelta(days=1)}
        if cap.weekday() == 5:
            g |= {cap - timedelta(days=1), cap + timedelta(days=2)}
        elif cap.weekday() == 6:
            g.add(cap + timedelta(days=1))
        if nat.weekday() == 4:
            g.add(nat + timedelta(days=3))
        elif nat.weekday() == 5:
            g |= {nat - timedelta(days=1), nat + timedelta(days=2), nat + timedelta(days=3)}
        elif nat.weekday() == 6:
            g.add(nat + timedelta(days=2))
    return {d for d in g if d.year == anno}


def giorni_corti(anno: int) -> set:
    """Vigilie con chiusura anticipata a Londra: tollerate se incomplete, non se vuote."""
    return {date(anno, 12, 24), date(anno, 12, 31)}
