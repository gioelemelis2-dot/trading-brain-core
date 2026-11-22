# Piano di D-51: disattivare la verifica di `esegui_h002` senza perdere protezioni (DGS-16 Q7) · 22/11/2026

**Decisione del titolare (D-51):** la verifica del vecchio esecutore si disattiva e passa solo dal percorso ordinario D-31 (`esegui_verifica`).

**Principio del DGS (Q7):** per ogni protezione si prende un caso valido, si cambia un solo elemento, e si esegue attraverso l'ingresso che dovrà proteggere davvero. Poi si controllano la causa, la fase del rifiuto, le chiamate al caricatore e gli stati scritti.

## 1. Il rifiuto sul vecchio comando

`esegui_h002 --modalita verifica` si ferma **subito**: prima di sigillo, registri, ambiente e caricatore. Il codice d'uscita è 2, il messaggio cita D-51 e il percorso ordinario. Il test verifica:
- zero chiamate al caricatore;
- registro delle prove invariato, byte per byte;
- nessun rapporto scritto.

Il ramo di verifica di `main` e la funzione `esegui_verifica` di `esegui_h002` diventano codice morto. Si tolgono, insieme ai loro mutanti (lo segnala `test_mutanti_applicabili`). Lo sviluppo resta com'è.

## 2. I 24 test del vecchio esecutore che passano dalla verifica

| Test | Che cosa proteggeva | Destino |
|---|---|---|
| `TestCasiLimite.test_verifica`; `TestVarianzaDelleProve.test_sharpe_dispersi_alzano_la_soglia`; `TestRevisioneR7Gemini.test_mg01_…`; `TestRevisioneR11Gemini.test_s6_anni_obbligatori_nella_funzione` | Calcoli della vecchia verifica (DSR, anni, Sharpe delle altre promosse) | **Tolti con la funzione.** Il verdetto ora è D-31: lo coprono `test_verdetto_d31` e `test_prova_generale_dgs12`. |
| `TestRigaDiComando.test_verifica_una_volta_sola`; `TestVerificheInsieme.test_tutte_o_nessuna`; `TestEsitiUnici…`; `TestEsitoDopoIlControlloFinale.test_verifica_senza_esito`; `TestRapportoPrimaDegliEsiti…`; `TestRevisioneR11Gemini.test_s4_…` (2) | Una verifica sola; esiti unici e dopo la verifica; rapporto prima degli esiti | **Sostituiti dal percorso nuovo:** consumo nel registro della riserva (una prenotazione, un'autorizzazione, un esito); record prima del rapporto; ripresa senza rilettura (prove C, D, F). Servono ancora alcune prove sul registro delle prove per il percorso nuovo (§3, punto 4). |
| `TestRigaDiComando.test_verifica_senza_varianti_fermata_prima_dei_dati`; `TestRevisioneR7Gemini.test_p1_…`; `TestRevisioneR11Gemini.test_s1_periodo_di_verifica_fisso_nel_codice`; `test_periodi_e_scheda_modificata` (la riga di verifica) | Niente letture prima dei controlli; solo le varianti promosse; periodo fisso | **Sostituiti:** rifiuto immediato del vecchio comando (§1). Nel percorso nuovo: screening obbligatorio (EV14), finestra della prenotazione con le sedute fissate nell'impegno, manifesto. La parte sulla scheda modificata resta nello sviluppo. |
| `TestRevisioneR11Gemini.test_mr03_mr04_ipotesi_diverse_nello_stesso_registro` | Le verifiche di un'ipotesi non bloccano quelle di un'altra | **Da riscrivere sul percorso nuovo:** due ipotesi sigillate, due prenotazioni (prova D in parte). |
| `TestRevisioneR11Gemini.test_s6_stessa_cache_dello_sviluppo`; `TestRigaDiComandoR12bis.test_verifica_rifiutata_se_i_dati_dello_sviluppo_sono_cambiati` | Lo screening e la verifica usano i dati dello sviluppo registrati | **LACUNA nel percorso nuovo:** oggi lo screening si ricalcola sulla cache di sviluppo passata all'esecutore, che non è legata a niente. Serve legare l'impronta dei dati di sviluppo allo screening registrato e controllarla prima dell'autorizzazione (§3, punto 2). |
| `TestVerificaUnaVoltaNellaStoria.test_registro_diverso_da_quello_canonico_rifiutato`; `…_registro_canonico_non_committato_rifiutato`; `…_storia_parziale_rifiutata`; `…_copia_senza_blob_rifiutata` | Registro canonico, ancorato a GitHub; storia git completa (#86, #125) | **Spostati sullo sviluppo** (gli stessi controlli girano prima della scelta della modalità) **e da portare nel percorso nuovo** (§3, punto 1). |
| `TestVerificaUnaVoltaNellaStoria.test_verifica_gia_fatta_su_un_altro_ramo_rifiutata`; `…_ramo_cancellato_e_riferimento_remoto_riscritto_visti_nel_reflog`; `…_n_non_scende_su_un_ramo_piu_vecchio` | Una verifica non si ripete su un altro ramo; N non scende | **Da portare nel percorso nuovo sul registro della riserva:** una prenotazione autorizzata o con esito in un'altra versione del registro (storia git, tutti i rami, reflog) non si può rifare; N non scende (§3, punto 1). |

## 3. Protezioni da portare nel percorso nuovo prima di R19 (test scritti prima)

1. **Ancora e storia** per il registro delle prove e per il registro della riserva, come in `esegui_h002`:
   - registro canonico, `controlla_ancora`, `versioni_nella_storia`, rifiuto delle copie parziali;
   - una prenotazione già consumata in un'altra versione non si riusa;
   - N non scende.
2. **Identità dei dati di sviluppo:** lo screening registrato porta l'impronta della cache di sviluppo. Prima dell'autorizzazione l'esecutore controlla che i dati letti per lo screening abbiano la stessa impronta.
3. **Avvio isolato e lanciatore:** `python3 -I -S` e `avvio.py`, poi `controlla_ambiente` sul codice sigillato, come per il vecchio esecutore.
4. **Registro delle prove nel percorso nuovo:** prove dirette di «una verifica sola per variante», di «esito unico dopo la verifica» e di due ipotesi nello stesso registro.
5. **Separazione fra sviluppo e riserva:** già coperta dal caricatore (date dello sviluppo dal 15/11/2023, verifica fino a FINE_VERIFICA) e dalla prenotazione. Va aggiunta una prova che una prenotazione con date di sviluppo sia rifiutata dal registro della riserva.

Ogni punto si prova attraverso `esegui_verifica.main`, con il caso valido e il caso con un solo elemento cambiato. Di ognuno si registrano causa, fase, chiamate al caricatore e stato dei registri.

## 4. Ordine di lavoro

1. Test rossi per §1, poi il rifiuto. Si tolgono i test e i mutanti del ramo morto; i test del §2 «spostati sullo sviluppo» si riscrivono.
2. Test rossi per §3, punti 1–5, poi il codice.
3. Corsa completa dei mutanti del perimetro (`mutazioni_esecuzione`), del percorso e del verdetto, su 3.13 e 3.9, in un worktree bloccato. Questo è il **candidato di R19**.
4. Ricevuta delle protezioni sul percorso ordinario, per il DGS e per Gemini (R19).

## Stato al 23/11/2026, notte (Claude)

- **§1 fatto** (`c6813a0`): rifiuto immediato del vecchio comando, ramo morto tolto, protezioni comuni spostate sullo sviluppo.
- **§3.1 fatto** (test rossi, poi `c737f12` e `0d2e432`):
  - registri canonici e ancorati a GitHub; storia completa;
  - prenotazione consumata in un'altra versione rifiutata; j e N che non scendono;
  - prove in un repository git temporaneo, attraverso l'ingresso ordinario.
- **§3.2 fatto** (`b75b5cf`): sviluppo letto con il manifesto e i byte verificati; impronta nell'impegno e nello screening registrato; una registrazione con un'altra impronta è rifiutata.
- **§3.3 fatto** (`1080da8`):
  - il lanciatore `avvio.py verifica` legge l'ipotesi dal contratto H-003 e controlla il codice sigillato di quell'ipotesi **prima degli import**;
  - l'esecutore si ferma se chiamato senza lanciatore e ricontrolla l'ambiente prima di leggere;
  - prove in una copia di `brain`, in un processo separato.
- **§3.4 fatto** (`716f00a`): una sola verifica per ipotesi e variante, rifiutata prima di ogni lettura e della quota. Ha trovato il difetto **#138**: oggi la ferma solo la quota.
- **§3.5:** date di sviluppo rifiutate dal registro della riserva con i confini di D-29 (test; il comportamento c'era già).
- **Corsa completa dei tre script di mutanti e delle suite su `1080da8`:** in corso. Sarà il candidato proposto per R19.
