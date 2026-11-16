# Quanti dati servono per la soglia IA-02 (0,15 R)

**Data:** 16/11/2026 · **Autore:** Claude · **Codice:** `laboratorio/studi/potenza_soglia.py` (test `test_potenza_soglia`, 5/5 su 3.13 e 3.9; mutanti 8/8)
**Nessun dato vero:** formule (approssimazione normale) controllate con una simulazione su esiti inventati (−1 R / +T R).
**IA-02 era già fissata prima di questo calcolo** (commit `032250b`): il calcolo non può averla influenzata. Serve a scegliere *come* applicarla, e la scelta va scritta nella scheda di H-003 prima di guardarne i dati.

## Le due regole
- **Sulla stima:** l'R medio misurato deve essere ≥ 0,15 R.
- **Sul limite inferiore:** anche togliendo 1,96 errori standard (intervallo al 95%), l'R medio deve restare ≥ 0,15 R.

## I numeri (deviazione standard per trade 1,25 R, valore centrale; le tabelle con 1,0 e 1,5 si ottengono lanciando lo script)

Soglia 0.15 R, deviazione standard per trade 1.25 R (approssimazione normale).

Probabilità di promozione (stima / limite inferiore 95%):

| vantaggio vero | n = 300 | n = 500 | n = 1.000 | n = 2.500 |
|---|---|---|---|---|
| +0.00 R | 2% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| +0.05 R | 8% / 0% | 4% / 0% | 1% / 0% | 0% / 0% |
| +0.10 R | 24% / 0% | 19% / 0% | 10% / 0% | 2% / 0% |
| +0.15 R | 50% / 3% | 50% / 3% | 50% / 3% | 50% / 3% |
| +0.20 R | 76% / 10% | 81% / 14% | 90% / 24% | 98% / 52% |
| +0.25 R | 92% / 28% | 96% / 43% | 99% / 72% | 100% / 98% |
| +0.30 R | 98% / 55% | 100% / 77% | 100% / 97% | 100% / 100% |
| +0.40 R | 100% / 93% | 100% / 99% | 100% / 100% | 100% / 100% |

Trade necessari per promuovere con probabilità 80% (stima / limite inferiore 95%):

| vantaggio vero | trade |
|---|---|
| +0.20 R | 443 / 4.906 |
| +0.25 R | 111 / 1.227 |
| +0.30 R | 50 / 546 |
| +0.40 R | 18 / 197 |
| +0.50 R | 10 / 101 |

Per confronto, i trade disponibili per una strategia con al massimo un trade al giorno: circa **450 nello sviluppo** (H-002 ne aveva 456 in tre anni) e circa **2.500 nella riserva** 2005–2023, se i dati saranno completi (l'ASK storico è ancora da verificare).

## Cosa dicono, in parole semplici
1. **Sulla stima, con 450 trade, la soglia filtra poco.** Una strategia che vale davvero 0,10 R (sotto la soglia) passa circa una volta su cinque; una che vale esattamente 0,15 R passa una volta su due, sempre, qualunque sia il numero di trade.
2. **Sul limite inferiore, con 450 trade, quasi nulla passa.** Servirebbe un vantaggio vero di circa 0,35–0,40 R per avere buone probabilità: nel trading reale è rarissimo. Usata nello sviluppo, questa regola ucciderebbe quasi ogni idea, anche buona.
3. **Sul limite inferiore, con 2.500 trade, la regola diventa sensata.** Una strategia da 0,25 R passa quasi sempre (98%), una da 0,20 R circa una volta su due, una da 0,15 R o meno quasi mai (≤ 3%). È il comportamento giusto per l'esame finale: ciò che passa vale con buona sicurezza almeno 0,15 R.
4. **Il numero di prove pesa.** Con la regola sulla stima, se si provano molte idee, alcune strategie mediocri passano per fortuna. Per questo la verifica sulla riserva ha già il DSR con N = tutto il registro.

## Proposta di Claude (decide l'utente, nella scheda di H-003, prima dei dati)
- **Sviluppo (screening):** soglia **sulla stima**, R medio ≥ 0,15 R. Filtra le idee chiaramente deboli senza uccidere quelle buone.
- **Riserva (verifica finale):** soglia **sul limite inferiore**, R medio − 1,96 errori standard ≥ 0,15 R, **oltre** ai criteri già previsti (DSR ≥ 0,95, media > 0, anni positivi, ultimi 5 anni, drawdown).
- **Conseguenza da accettare:** una strategia che vale davvero 0,20 R ha circa il 50% di probabilità di superare l'esame finale. Il prezzo della severità sono strategie buone ma non ottime scartate. È coerente con «degna di soldi veri».
- **Alternativa più permissiva:** sulla stima anche nella riserva, affidando al DSR il controllo sui falsi positivi. Passano più strategie, con più rischio che il vantaggio vero stia sotto 0,15 R.

## Limiti
- Esiti a due valori (stop o target): le strategie vere hanno anche uscite intermedie. La deviazione standard per trade va presa come ordine di grandezza (1,0–1,5 R); le conclusioni non cambiano nella sostanza dentro questo intervallo.
- Trade indipendenti: se i risultati di giorni vicini sono correlati, l'errore standard vero è più grande e servono più trade.
- La riserva si usa una volta sola per ipotesi: un esame finale fallito non si ripete sugli stessi dati.
