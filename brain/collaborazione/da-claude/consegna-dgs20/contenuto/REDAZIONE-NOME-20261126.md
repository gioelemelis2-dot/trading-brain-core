# Redazione del nome del titolare · 26/11/2026 (D-58)

**Che cosa è stato fatto:** nel contenuto attuale dei file di `brain/` il nome e il cognome del titolare sono stati sostituiti, per decisione del titolare (D-58). Regole, per parola intera:
- `/Users/<nome>` diventa `~`, come prevede D-28;
- nome e cognome diventano «il titolare»;
- l'account GitHub diventa `<account-titolare>`.

27 file, 166 sostituzioni; nessun residuo (`git grep -i -E 'nome|\bcognome\b' -- brain` vuoto).

**Integrità delle consegne passate.** Gli originali restano nella storia git al commit **`636583b`**. Per i file la cui impronta è registrata in un manifest, il manifest **non** è stato modificato, perché documenta che cosa fu consegnato allora. Si verifica così: `git show 636583b:<file> | sha256sum` deve dare l'impronta del manifest.

| File | Impronta originale (= manifest) | Manifest che la registra | Impronta attuale (redatta) |
|---|---|---|---|
| `brain/collaborazione/HANDOFF-GEMINI.md` | `9cbc7184e11b0b70efc093c6fc10878f1df17da9eedfb780c2a676fa9a00fd99` | brain/collaborazione/pacchetto-per-gemini/MANIFEST.sha256  | `d0503eadaa4e4f0946842e8c3e31055d9fd367336776f4b6ac99e9f285a688c6` |
| `brain/collaborazione/da-claude/CONSEGNA_FIX_G0/RAPPORTO_FIX_G0.md` | `a262e93beb9fb04d811eed61190372c5371400216d5773119483de76a7029c37` | brain/collaborazione/da-claude/CONSEGNA_FIX_G0/MANIFEST.sha256  | `d361305f01faece3a3601c0e9cc0453e30f8896b18d465d5c31b1d4064256639` |
| `brain/collaborazione/da-claude/CONSEGNA_FIX_G0/diff_fix_g0.patch` | `6fe698f50447abfc12a526c399b14a56f428cbaa3eec2177ed4e07ee388940c9` | brain/collaborazione/da-claude/CONSEGNA_FIX_G0/MANIFEST.sha256  | `14a16d446c1146b0504ffa09e5bd2f62b89173bc6fe42b6e03164afeeb5fb5cf` |
| `brain/collaborazione/da-gemini/CONSEGNA_LAB_V2/AUDIT_OSTILE_SU_CLAUDE.md` | `d508d9a54772791702c1aabed17ac1a745c714f1a5c0eacf46f6c3c7286240dd` | brain/collaborazione/da-gemini/CONSEGNA_LAB_V2/MANIFEST.sha256  | `a0166e34ec0587761c0ceafae5cc00316a86111575da7344e7210ca4f1b2f786` |
| `brain/collaborazione/da-gemini/CONSEGNA_LAB_V2/diff_lab_v2.patch` | `928fbe88e16333489da0ca486239d597cec47603c58c7183c59c7c8fde5a67ab` | brain/collaborazione/da-gemini/CONSEGNA_LAB_V2/MANIFEST.sha256  | `8c5ec96624afb6f14353dfb18203b215c3b85beac115d089165f03af299ec8d7` |
| `brain/collaborazione/da-gemini/consegne/TRADING_BRAIN_ARCHITECTURE_AND_ROADMAP_REVISED_V2.md` | `62dda32d05e8a2362dd3739ce3942c5d89370e97973d3775057ff791c8092b59` | brain/collaborazione/da-gemini/consegne/MANIFEST.sha256 brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-06-ARCH-V2/output/integrita_pacchetto.txt brain/collaborazione/revisione-materiali-gemini/R-CLAUDE-20261112-08-REVISIONE-ESTERNA/MANIFEST_PACCHETTO.sha256  | `e2e9985351b955993e580e86891063e845d3b0286a607499dab9ebc0bff51f9d` |
| `brain/collaborazione/da-gemini/consegne/TRADING_BRAIN_DOSSIER_CONSOLIDATO_GEMINI_V1.md` | `4784f1de1682ee304515cd0a2854119b99a13625f16735045b8db158e3462cfc` | brain/collaborazione/da-gemini/consegne/MANIFEST.sha256  | `a8e9ca8d071b0ab382dac7585a3768b45bc4e572610cef45c66607cc66c0ec6a` |
| `brain/piano/PIANO-MIGRAZIONE.md` | `26d35ef70d3c79caebd6ee8079ca10e23a1c663c8b6bc69017338a541db416f2` | brain/collaborazione/pacchetto-per-gemini/MANIFEST.sha256  | `8ebf02747554ca3c48517129bacfc7b577d8d2ef23a060836bdbdc8f712e7ee7` |

**Eccezione:** `da-gemini/consegne/TRADING_BRAIN_V3_3_PACKAGE.zip` (V3.3 congelata, D-17) contiene il nome 6 volte dentro l'archivio. **Non è stato rifatto:** la sua impronta `6fb9d76e…` è citata in almeno 7 documenti. Rifarlo è una decisione separata del titolare.

## Verifica eseguita (26/11)
Per ognuno dei 5 manifest coinvolti, l'impronta di ogni file redatto ricostruita da `git show 636583b:<file>` è **uguale** a quella registrata. In tutto i file sono 9, uno dei quali compare in due manifest:
- `pacchetto-per-gemini`: 2;
- `CONSEGNA_FIX_G0`: 2;
- `CONSEGNA_LAB_V2`: 2;
- `consegne`: 2;
- `R-CLAUDE-20261112-08`: 1.

Tre voci risultano diverse anche sul commit **precedente** alla redazione: `CONTINUITA.md`, `REGISTRO-MODIFICHE.md`, `DECISIONI-APERTE.md`. Sono documenti vivi, cambiati dopo quei pacchetti: la differenza non dipende dalla redazione.
