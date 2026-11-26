# Scheda di stato del progetto

**Aggiornata:** 26/11/2026 · **a cura di:** Claude · richiesta dal DGS (DGS-04 §8).
Una pagina: dove siamo, i contatori, cosa manca. La versione precedente, del 17–18/11, è nella storia git (`a55953f`).

## Dove siamo, in tre frasi
- La **macchina che giudica una strategia** fa la corsa intera dal lanciatore sui dati sintetici (candidato `7191156`), ma **non è certificata**. R19 ha trovato un critico aperto (#143) e sei altri difetti; restano 15 dei 18 requisiti dell'ultimo lotto.
- **Nessuna verifica di strategia sulla riserva** è documentata, e nessuna strategia è candidata. H-002 ha prodotto solo osservazioni sullo sviluppo. Copie, inventario e consuntivo dei dati della riserva sono operazioni distinte dalla verifica (DGS-20).
- Guardian, diario e formazione esistono, ma **il titolare non li ha ancora potuti usare per decidere**.

## Contatori
| Cosa | Stato | Evidenza |
|---|---|---|
| Difetti | **149** registrati. **Aperti nel perimetro: #143 (critico), #144–#148 (importanti), #149 (minore)**, tutti da R19 e verificati da Claude il 26/11. #142 riclassificato critico | `laboratorio/REGISTRO-DIFETTI.md`; `governance/CONVERGENZA-REVISIONI-20261123.md` |
| Candidato | **`7191156`, non valido per #143–#148** (R19). Le sue prove restano: suite 759 verdi su 3.13 e 3.9; perimetro 299/299; percorso 62/63; verdetto 131/132 (MF09 e VD13 equivalenti); prova positiva completa dal lanciatore superata | `laboratorio/ricevute/2026-11-23-candidato-7191156/` (26/11) |
| Codice dopo il candidato | punti 4, 8 e 9 dell'ultimo lotto (`7ca55ae`, `23eab88`), non ancora in un candidato | `piano/REQUISITI-ULTIMO-LOTTO.md` |
| Criterio d'uscita dal Gate 2½ | **D-56** (26/11): scheda per difetto, bloccanti contro rinviabili, percorso valido completo, 2 giri puliti su un perimetro congelato, stop dopo 4 giri | `governance/DECISIONI.md` |
| Giri di revisione | R18 (21/11) e **R19 (26/11) non puliti**. Il prossimo giro sarà sul candidato congelato dopo il lotto, il primo dei due che contano per D-56 | `da-gemini/G-20261126-R19.md`; `ricevute/2026-11-26-verifica-r19/` |
| Riserva di verifica | 2005 → 31/10/2023, **mai letta**. Regole di spesa D-38 (α 5%). Una sola quota collaudata (2,5%, prima apertura). Date esatte, embargo e quarantena da fissare | D-38; DGS-19 Q2 |
| Dati | BID e ASK completi; copia finale su due cloud con impronta verificata (D-39, 23/11). **Registri dello scaricamento incompleti:** BID fino al 07/06/2009 e tutto lo sviluppo senza riga; 236 doppioni identici. Oggi lo screening si fermerebbe | `ricevute/2026-11-23-diagnosi-manifesto/` |
| Decisioni | D-01…D-56; aperte: A1/B1 (registri), DA-39 (GitHub Pro), D-38 (parametri), DA-25, DA-32, DA-33 | `DECISIONI.md`, `DECISIONI-APERTE.md` |

## Cosa manca per il primo accesso reale, in ordine
1. Ultimo lotto (`piano/REQUISITI-ULTIMO-LOTTO.md`, 18 requisiti, fatti 4, 8, 9): prima #143 (critico), poi #144–#149 da R19; D-55, D-54, procedura di potenza, A1, stati dei file, B1 (decisione del titolare).
2. Congelamento del perimetro e i due giri secondo D-56.
3. DA-39 (protezione del ramo), poi l'unione in `main`.
4. Date della riserva (D-38) e una scheda H-003 del titolare, con la potenza calcolata.
