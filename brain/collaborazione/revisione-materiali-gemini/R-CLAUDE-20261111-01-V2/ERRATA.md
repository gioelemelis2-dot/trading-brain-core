# Errata corrige · CLAUDE_SECOND_REVIEW_ANTIGRAVITY_V2.md

Data: 11/11/2026 · Autore: Claude · Il documento originale **non è stato modificato** (SHA-256 `4d07122f0a2e53437863ae7927daa746b873dae7332bfa527badcff0ca58025d`, commit `3bbe137`).

| # | Dove | Testo errato | Testo corretto | Fonte del dato |
|---|---|---|---|---|
| ER-01 | §4.6, riga "I test sono sufficienti?" | "I miei test aggiuntivi (gruppo A) uccidono 6 dei 7 sopravvissuti. Il settimo e i due equivalenti non sono distinguibili dal percorso usato nelle simulazioni" | "I miei test aggiuntivi (gruppo A) uccidono **4 dei 7** sopravvissuti (M06, M07, M08, M09). Gli altri 3 (M04 e M05 equivalenti, M11 neutralizzato dal valore passato in modo esplicito) non sono distinguibili da nessuna delle due suite. Insieme, le due suite uccidono **8 mutanti su 11**." | `output/c10_test_aggiuntivi_mutanti.txt`; tabella della §7 (già corretta) |

Impatto sulle conclusioni: nessuno. Il giudizio "i test di Gemini confermano la correzione ma non proteggono il resto del motore" resta valido.
