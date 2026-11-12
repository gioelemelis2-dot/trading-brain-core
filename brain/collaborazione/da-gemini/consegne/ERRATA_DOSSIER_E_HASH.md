# ERRATA CORRIGE UFFICIALE: RETTIFICA HASH SHA-256 E PROTOCOLLO INTEGRITÀ

**Data:** 12 Novembre 2026  
**Autore:** Gemini Antigravity (Quantitative Research Lab)  
**Oggetto:** Rettifica formale dell'hash SHA-256 dell'archivio V3.3 e protocollo zero-trust sulle evidenze crittografiche.

---

## 1. RETTIFICA DELL'HASH SHA-256 DELLA BASELINE V3.3

Nel testo di `TRADING_BRAIN_DOSSIER_CONSOLIDATO_GEMINI_V1.md` (e relative comunicazioni) era stato trascritto un valore errato nei caratteri centrali dell'hash:
- **VALORE ERRATO DIGITATO NEL TESTO:**  
  `6fb9d76e-ALLUCINATO-73fbf509938ca9e28bf6152ef3225883ef5fbe8e1bb3f7a1fec97638`
- **VALORE REALE ED EFFETTIVO SU DISCO (CALCOLATO CON `shasum -a 256`):**  
  `6fb9d76e54daabecd5215aaa255ef3b94f2a0052569b20734b1ac90181627638`

### Causa Tecnica del Difetto:
Il difetto è scaturito dall'inserimento manuale a testo della stringa esadecimale partendo dalla visualizzazione troncata (`6fb9d76e...7638`), con conseguente allucinazione dei 48 caratteri interni.  
Al contempo, il file canonico `brain/collaborazione/da-gemini/consegne/MANIFEST.sha256` conteneva l'hash reale calcolato meccanicamente (`6fb9d76e54daabecd5...`), creando una discrepanza inaccettabile tra testo e manifest.

---

## 2. REGOLA FERREA ZERO-TRUST SULLE EVIDENZE CRITTOGRAFICHE

A partire dal presente mandato:
1. **Divieto Assoluto di Digitazione Manuale di Hash:**  
   Nessun hash SHA-256 può essere scritto o formattato manualmente. Ogni impronta crittografica deve essere generata direttamente dal comando standard del sistema operativo (`shasum -a 256 <file>`) e verificata tramite asserzione programmatica nei test unitari.
2. **Aggiornamento del Dossier e del Manifest:**  
   Il file `TRADING_BRAIN_DOSSIER_CONSOLIDATO_GEMINI_V1.md` è stato rettificato inserendo il valore esatto `6fb9d76e54daabecd5215aaa255ef3b94f2a0052569b20734b1ac90181627638`.
   Il file `MANIFEST.sha256` di `consegne/` è stato rigenerato e validato.
3. **Audit Bibliografico:**  
   Nessuna citazione bibliografica o numerica può essere marcata come verificata (`V`) in assenza di riscontro testuale materiale.
