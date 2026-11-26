# Verifica delle sonde di chiusura di Gemini (`r20_sonde_chiusura.py`) · 26/11/2026

**Consegna verificata:** ramo `rev/gemini-sonde-chiusura`, commit `b290348`, un solo commit sopra `7f35740`. Contiene tre file, tutti in `brain/collaborazione/da-gemini/`, archiviati senza modifiche (impronte git identiche).

**Esame prima dell'esecuzione:**
- manomissioni e operazioni git solo in copie temporanee, con un remoto locale;
- rete bloccata nello script;
- nessun percorso personale;
- nel repository vero solo letture.

## Come ho rieseguito

- Due copie estratte con `git archive`, ciascuna con lo script di Gemini invariato:
  - **A = `7f35740`**, il commit esaminato da Gemini;
  - **B = `0c28299`**, il codice attuale con #143, #145–#151 corretti.
- Python 3.13.18 (Gemini aveva Apple Python 3.9.6), rete bloccata, opzione `--esigi-zero-difetti`.
- In entrambe le copie, 26 righe e codice d'uscita 1, cioè almeno un difetto presente. Su B quel difetto è #144, ancora aperto.
- Log grezzi:
  - `log/sonde_chiusura_gemini_su_7f35740_py313.jsonl`
  - `log/sonde_chiusura_gemini_su_0c28299_py313.jsonl`

## 1. Riproduzione su `7f35740` (A contro l'output consegnato)

- `difetto_presente` è **identico in 26 righe su 26**: 12 rilievi con difetto presente, 7 percorsi validi e 7 sonde #124 senza.
- Lo stato osservato coincide in 23 righe. Nelle altre 3 differisce solo per l'ambiente:
  - **S-143:** testo del traceback di Python, con `rc` e `codice_manomesso_importato` identici;
  - **S-146d:** testo del messaggio d'errore di `json`, diverso fra 3.9 e 3.13;
  - **S-148:** nome casuale del file temporaneo orfano.
- **S-146a riprodotta:** con `O.LONDRA = timezone.utc` l'impronta dell'impegno resta la stessa (`8b9edc3675aa…`), ma l'esito passa da «promossa» (+0,5363 R) a «bocciata» (−0,2796 R), con 1.489 giorni consumati in entrambi i casi.

## 2. Il codice attuale (B): stato osservato, non l'etichetta

| Sonda | `difetto_presente` | Stato osservato su B |
|---|---|---|
| S-143 | false | Doppia `--scheda`: `rc 2`, «--scheda ripetuta 2 volte», codice manomesso **non** importato. Sigillo senza `esegui_verifica.py`: `rc 2`, codice non importato. `--scheda=X`: `rc 0` |
| S-144 | **true** | **#144 aperto:** 20 feriali vuoti, «promossa», 1.489 giorni consumati. Atteso, in attesa del DGS (messaggio 20) |
| S-145 | false | α 0,75: rifiuto per α ≠ D-38, 0 letture, 0 eventi. **α 0,05: rifiuto «date già consumate in un'altra versione», 0 letture, 0 eventi.** È la prima prova indipendente della parte sulla storia di #145, che finora era provata solo dai test di Claude |
| S-146a | false | tzdata senza ora legale: rifiuto «fuso … diverso dalla regola europea», 0 letture, 0 giorni. `TZ=America/New_York` con tzdata integro: corsa completa, come sul riferimento |
| S-146b | false | Modulo estraneo prima dell'esito: fermo, l'esito non è scritto in nessuno dei due registri, l'apertura resta autorizzata senza esito, il consumo resta. È il comportamento scelto (ripresa in ambiente pulito, v2.19). Alla ripresa: fermo |
| S-146c | false | Rifiuto «--ora … non è nel formato», 0 letture, 0 voci, 0 giorni, nessun file |
| S-146d | false | −∞, +∞ e NaN rifiutati da `leggi_contratto`. `esegui` con −∞: rifiuto al passo 1, 0 letture |
| S-146e | false | `""` e `"   "` rifiutati |
| S-147a | false | Dominio falso e data di un altro anno: anomalia «indirizzo diverso da quello atteso», rifiuto prima dell'autorizzazione con l'evento `tentativo`, 0 giorni consumati. Resta 1 lettura e 1 voce dello **sviluppo**, come da ordine del percorso (passo 6 prima del 7) |
| S-147b | false | `sha256` vuota e non esadecimale: anomalia «impronta non valida», evento `tentativo`, 0 giorni. Anche qui resta lo screening di sviluppo |
| S-148 | false | Cartella come rapporto: rifiuto al passo 1, 0 letture, 0 voci, 0 giorni, nessun file orfano |
| S-149 | false | `quota(0.15, 2, 1) = 0.025` esatta. L'esecuzione con α 0,15 è però rifiutata per α ≠ D-38 (#145), non per la quota |
| V-143…V-149 | false | Tutti completati: «promossa» e, alle riprese, «rapporto rigenerato». V-147 con 2.978 voci nel manifesto e nessuna anomalia |
| S-124-D1…D6b | false | Invariati |

## 3. Limiti dichiarati

- **S-149 non prova più il percorso della quota fino all'esito.** Con α diverso da D-38 l'esecutore si ferma prima. La sua aritmetica, e il percorso alla quota 2,5%, sono provati da V-149 e dai test `TestQuotaEsatta`.
- **S-147a/b:** dopo la correzione il rifiuto arriva al passo 7, quindi dopo lo screening di sviluppo, che resta registrato. È l'ordine documentato del percorso, non un consumo della riserva.
- **Ambiente:** ho eseguito solo su 3.13. La riesecuzione su 3.9 la farà Gemini sul candidato congelato (D-56).
- **L'impronta dell'impegno di B (`346a7e73…`) è diversa da quella di A,** perché l'impegno contiene le impronte del codice: è un effetto atteso della correzione.

## 4. Conclusione

- Le sonde indipendenti di Gemini confermano la correzione di #143, #145, #146 (a–e), #147, #148 e #149 sul codice attuale, ciascuna con il suo percorso valido.
- Resta **#144**, l'unico rilievo aperto del lotto R19.
