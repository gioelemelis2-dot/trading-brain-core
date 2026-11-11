"""Strumento didattico per la lezione L2.2 (aspettative e sorprese).

Due calcoli, entrambi su futures sul tasso medio mensile (es. fed funds a 30 giorni):

1. Sorpresa alla Kuttner (2001): variazione del tasso implicito nel giorno
   dell'annuncio, riscalata perché il future paga la MEDIA del mese.
       sorpresa = m / (m - d) * (f_d - f_{d-1})
   con m = giorni del mese, d = giorno dell'annuncio, f = 100 - prezzo.

2. Probabilità implicita di una mossa da 25 pb (logica semplificata del CME
   FedWatch, un solo meeting nel mese):
       media_mese = (d/m) * tasso_pre + ((m-d)/m) * tasso_post
       tasso_post = (media_mese*m - tasso_pre*d) / (m - d)
       P(mossa da 25 pb) = (tasso_post - tasso_pre) / ±0.25

Limiti: ignora il premio per il rischio nei futures (Piazzesi-Swanson 2008),
le convenzioni sui giorni festivi e la differenza tra tasso obiettivo e EFFR.
Serve a capire il meccanismo, non a sostituire i dati ufficiali.
"""
from __future__ import annotations


def tasso_implicito(prezzo_future: float) -> float:
    return 100.0 - prezzo_future


def sorpresa_kuttner(prezzo_prima: float, prezzo_dopo: float, giorno: int, giorni_mese: int) -> float:
    """Sorpresa in punti percentuali. giorno = giorno dell'annuncio (1..m)."""
    if not 1 <= giorno < giorni_mese:
        raise ValueError("Per gli ultimi giorni del mese usare il contratto del mese successivo")
    variazione = tasso_implicito(prezzo_dopo) - tasso_implicito(prezzo_prima)
    return giorni_mese / (giorni_mese - giorno) * variazione


def tasso_post_meeting(media_mese: float, tasso_pre: float, giorno_effetto: int, giorni_mese: int) -> float:
    """giorno_effetto = giorni del mese al vecchio tasso."""
    d, m = giorno_effetto, giorni_mese
    return (media_mese * m - tasso_pre * d) / (m - d)


def probabilita_mossa(media_mese: float, tasso_pre: float, giorno_effetto: int, giorni_mese: int,
                      passo: float = 0.25) -> tuple[float, float]:
    """Restituisce (tasso post atteso, probabilità di una mossa da `passo` nella direzione implicita)."""
    post = tasso_post_meeting(media_mese, tasso_pre, giorno_effetto, giorni_mese)
    return post, abs(post - tasso_pre) / passo


def main() -> None:
    print("Esempio 1 · sorpresa alla Kuttner")
    s = sorpresa_kuttner(prezzo_prima=95.700, prezzo_dopo=95.750, giorno=18, giorni_mese=30)
    print(f"  tasso implicito 4,300% -> 4,250%, annuncio il giorno 18 di 30: sorpresa = {s*100:+.1f} pb")

    print("\nEsempio 2 · probabilità implicita (logica FedWatch semplificata)")
    post, p = probabilita_mossa(media_mese=4.23, tasso_pre=4.33, giorno_effetto=15, giorni_mese=30)
    print(f"  media mese 4,23%, tasso pre 4,33%, 15 giorni su 30 al vecchio tasso")
    print(f"  tasso post atteso = {post:.3f}%  -> P(taglio da 25 pb) = {p:.0%}")

    print("\nEsempio 3 · reazione media attesa (Bernanke-Kuttner 2005: -25 pb ≈ +1% indici)")
    print(f"  sorpresa {s*100:+.1f} pb -> reazione media stimata {(-s/0.25)*1:+.1f}% (solo media storica, dispersione ampia)")


if __name__ == "__main__":
    main()
