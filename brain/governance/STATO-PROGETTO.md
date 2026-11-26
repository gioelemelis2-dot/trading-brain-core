# Scheda di stato del progetto

**Aggiornata:** 26/11/2026 · **a cura di:** Claude · richiesta dal DGS (DGS-04 §8).
Una pagina: dove siamo, i contatori, cosa manca. La versione precedente, del 17–18/11, è nella storia git (`a55953f`).

## Dove siamo, in tre frasi
- La **macchina che giudica una strategia** è completa e prova la corsa intera dal lanciatore sui dati sintetici (candidato `7191156`), ma **non è certificata**: R19 è aperto e restano gli 11 requisiti dell'ultimo lotto.
- **Nessuna strategia è stata provata**, nessuna è candidata, e la riserva non è mai stata letta dal sistema.
- Guardian, diario e formazione esistono, ma **il titolare non li ha ancora potuti usare per decidere**.

## Contatori
| Cosa | Stato | Evidenza |
|---|---|---|
| Difetti | **142** registrati; 0 aperti nel perimetro, tranne quelli dichiarati come limiti. Dal 18/11 nessuno classificato «critico», ma #126 lo era alla lettera (riesame del 25/11) | `laboratorio/REGISTRO-DIFETTI.md`; `governance/CONVERGENZA-REVISIONI-20261123.md` |
| Candidato | **`7191156`**: suite 759 verdi su 3.13 e 3.9; perimetro 299/299; percorso 62/63; verdetto 131/132 (MF09 e VD13 equivalenti); prova positiva completa dal lanciatore superata | `laboratorio/ricevute/2026-11-23-candidato-7191156/` (26/11) |
| Codice dopo il candidato | punti 4, 8 e 9 dell'ultimo lotto (`7ca55ae`, `23eab88`), non ancora in un candidato | `piano/REQUISITI-ULTIMO-LOTTO.md` |
| Criterio d'uscita dal Gate 2½ | **D-56** (26/11): scheda per difetto, bloccanti contro rinviabili, percorso valido completo, 2 giri puliti su un perimetro congelato, stop dopo 4 giri | `governance/DECISIONI.md` |
| Giri di revisione | R18 (21/11) non pulito. **R19 in attesa:** Gemini lavora su `1431190`; la chiusura va fatta sul candidato finale | `collaborazione/da-gemini/G-20261121-R18.md`; mandato R19 e aggiunta |
| Riserva di verifica | 2005 → 31/10/2023, **mai letta**. Regole di spesa D-38 (α 5%). Una sola quota collaudata (2,5%, prima apertura). Date esatte, embargo e quarantena da fissare | D-38; DGS-19 Q2 |
| Dati | BID e ASK completi; copia finale su due cloud con impronta verificata (D-39, 23/11). **Registri dello scaricamento incompleti:** BID fino al 07/06/2009 e tutto lo sviluppo senza riga; 236 doppioni identici. Oggi lo screening si fermerebbe | `ricevute/2026-11-23-diagnosi-manifesto/` |
| Decisioni | D-01…D-56; aperte: A1/B1 (registri), DA-39 (GitHub Pro), D-38 (parametri), DA-25, DA-32, DA-33 | `DECISIONI.md`, `DECISIONI-APERTE.md` |

## Cosa manca per il primo accesso reale, in ordine
1. Ultimo lotto (`piano/REQUISITI-ULTIMO-LOTTO.md`): D-55, D-54, procedura di potenza, A1, stati dei file, B1 (decisione del titolare), testa del registro della riserva (sonda R19-04 da riprodurre).
2. Congelamento del perimetro e i due giri secondo D-56.
3. DA-39 (protezione del ramo), poi l'unione in `main`.
4. Date della riserva (D-38) e una scheda H-003 del titolare, con la potenza calcolata.
