# Riconteggio del 17/11/2026 con lo strumento corretto

**Perché:** la revisione notturna ha trovato quattro buchi in `riconta.py` (#75, #78, #80, #81) che potevano nascondere uscite della riserva nel riconteggio del 16/11. La conclusione «riserva intatta» era quindi da riconfermare.

**Come:** l'utente ha lanciato sul Mac lo strumento corretto due volte, entrambe con codice 0. Lo strumento legge soltanto e stampa conteggi, date ed estratti dei comandi con i prezzi mascherati, mai il contenuto delle uscite.
- `riconta2.txt`: commit `296b014`.
- `riconta3.txt`: commit `e3eeb08`. Questa versione aggiunge, per ogni uscita segnalata, la chiamata che l'ha prodotta (solo comando o percorso).

| | 16/11 (strumento vecchio) | 17/11 (strumento corretto) |
|---|---|---|
| File esaminati | 374 | 428 |
| Esecuzioni contate | 1.409 | 2.583 (#75: comandi su più righe, più i file nuovi) |
| Uscite con date della riserva | 144 | 416 |
| Da guardare | 19 | 112 |

**Classificazione delle 112 segnalazioni, per origine.** Nessuna viene dalla cache vera né da file di dati reali.
- **Lettura o scrittura di codice, test e documenti del progetto** (`test_dukascopy.py`, `test_g0.py`, `orb_londra.py`, script d'attacco R12-bis, schede H-002, rapporti di Gemini, R12-bis, DGS-03, BANCO-02): dati inventati, oppure i confini della riserva citati nel testo.
- **Replica di H-002 di Gemini del 13/11** (`replica_h002/confronto.py`, i suoi log, e le letture delle sue uscite salvate, `steps/2212` e `steps/2247`): il generatore `genera_dati.py` (commit `619a6a4`) produce minuti SINTETICI con festività inglesi del 2022–2024. Da qui vengono le date 2022–2023.
- **Test ufficiali di R13 con la rete bloccata** e i loro log (task 3340, 3343, 3188, 3189).
- **Censimento di Gemini del 15/11** (passi 3035, 3037 e 3074), che conta parole e date nelle trascrizioni. Il passo 3037 ha 4 date, 2009-02-16 e 2022-02-21 comprese: sono giorni festivi USA (Presidents' Day), da un calendario.
- **Altro:** pagina delle regole FTMO; compilazione di un'app web del 07/11, in un'altra conversazione e con le dimensioni dei file; verifica numerica di un overflow; `git diff` di codice.
- **Trascrizioni di Claude Code sul Mac:** nessuna segnalazione.

**Chiamate sensibili nuove nei file già esaminati il 16/11:** tutte successive al 16/11 (R12-bis e R13, con dati inventati). Una sola nomina `cache_dukascopy` in un comando: il passo 3360 del 16/11, R13, una sonda con `tempfile` e la rete bloccata. **Da confermare con Gemini** che fosse una cartella temporanea.

**Conclusione:** per tutto ciò che è contabile nelle trascrizioni presenti sul Mac, **la riserva resta intatta** anche con lo strumento corretto. Restano due cose:
- la conferma del passo 3360;
- il limite già dichiarato: ciò che una persona ha guardato a mano non si conta.

**Limite del metodo:** l'origine è la chiamata più recente prima dell'uscita, non un legame certo. Con chiamate in parallelo sono elencate tutte. La classificazione si basa su comandi e percorsi, non sui contenuti, che nessuno ha letto.
