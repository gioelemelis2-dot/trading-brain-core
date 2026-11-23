# Diagnosi del manifesto sui registri veri · 23/11/2026

**Eseguita dal titolare sul suo Mac**, con il codice del commit `c611217` (`dati/PROCEDURA-DIAGNOSI-MANIFESTO.md`), più un controllo in sola lettura sulle voci doppie preparato da Claude. Qui ci sono solo conteggi e date, come sono stati stampati. Nessun registro è stato modificato.

## 1. Esiti della diagnosi (codice 1 su entrambi i periodi)

**Riserva, dal 01/01/2005 al 31/10/2023** (6.878 giorni attesi per lato):

| Anomalia | Lato | Conteggio per anno |
|---|---|---|
| omesso | BID | 2005: 365 · 2006: 365 · 2007: 365 · 2008: 366 · 2009: 158 (totale 1.619) |
| voce doppia | BID | 2009: 14 · 2010: 139 · 2011: 83 (totale 236), tutte con esiti «dati+dati» |
| impronta diversa, file mancante | — | **nessuna** |

- File controllati contro il registro: ASK 6.878 su 6.878, BID 5.023 su 5.023 (6.878 − 1.619 omessi − 236 doppi).
- **Tutti hanno l'impronta registrata.**

**Sviluppo, dal 15/11/2023 al 12/11/2026** (1.094 giorni attesi per lato):

| Anomalia | Lato | Conteggio per anno |
|---|---|---|
| omesso | ASK | 2023: 47 · 2024: 366 · 2025: 365 · 2026: 316 (tutti) |
| omesso | BID | 2023: 47 · 2024: 366 · 2025: 365 · 2026: 316 (tutti) |

Nessun file di sviluppo è stato controllato, perché nessun giorno ha una riga.

## 2. Controllo delle voci doppie e dell'estensione dei registri

- **BID:** 236 giorni con righe doppie. In tutti i **236** le due righe hanno la **stessa impronta**, uguale anche a quella del file in cache. Tutte le 472 righe sono state registrate il **16/11/2026**.
- **BID:** 5.270 giorni nel registro, dal **08/06/2009** all'**11/11/2023**.
- **ASK:** nessuna riga doppia; 6.889 giorni nel registro, dal 01/01/2005 all'11/11/2023.

## 3. Lettura di Claude

| Anomalia | Causa | Gravità |
|---|---|---|
| BID omesso fino al 07/06/2009 | [DEDOTTO] File scaricati prima che nascesse il registro per giorno: il 15/11 il BID era già in cache fino al 07/06/2009 (REGISTRO-MODIFICHE v1.33). `scarica_cache` è ripartito dal giorno dopo e non è mai ripassato sul periodo precedente | I file ci sono; manca la loro provenienza nel registro |
| BID voci doppie 2009–2011 | [DEDOTTO] Il 16/11 due copie dello scaricamento hanno girato insieme (difetto #60) e hanno registrato due volte gli stessi giorni. Le righe sono **identiche nell'impronta** e coincidono con il file | Innocue nel contenuto; bloccano il manifesto per come è scritto |
| Sviluppo senza registro | [DEDOTTO] I dati di sviluppo sono stati scaricati il 13–14/11 con lo scaricatore precedente, che non scriveva il registro per giorno; i registri di `scarica_cache` partono dal 2005 e finiscono all'11/11/2023 | **Blocca oggi lo screening di qualunque scheda H-003**: il percorso ordinario si fermerebbe prima |

**In tutti e tre i casi il manifesto blocca:** il verso è quello giusto, non è passato niente. Il codice del perimetro non ha difetti; è lo stato dei registri veri che non era stato confrontato con il manifesto. **Errore di Claude:** questo controllo andava fatto quando è stato scritto il manifesto (22/11), non dopo.

## 4. Opzioni (decisione di metodo: DGS, poi il titolare)

**A. Voci doppie identiche (236 giorni).**
- **A1:** il manifesto accetta più righe valide per lo stesso giorno e lato **solo se sono identiche** in esito, byte e impronta. Righe diverse continuano a bloccare. È una modifica al perimetro: test prima, mutanti, revisione. I registri restano intatti, perché sono prove scritte solo in aggiunta.
- **A2:** si ripulisce il registro togliendo i doppioni, con uno strumento e una copia prima. Sconsigliata: tocca la prova originale.

**B. Righe mancanti (BID dal 2005 al 07/06/2009: 1.619 giorni; sviluppo: 1.094 giorni per lato).**
- **B1, registrazione a posteriori.** Si ripassa `scarica_cache` sui due periodi. Per i file già in cache scrive «in-cache-non-registrato» con l'impronta di oggi, senza scaricare niente (per lo sviluppo scaricherebbe solo i giorni eventualmente mancanti).
  - **Limite:** attesta i file come sono **oggi**, non come erano allo scaricamento.
  - **Ancore disponibili:** le copie con impronta del 18/11 e del 22/11 (D-39), che però non si aprono; il consuntivo del 22/11, che ha letto tutti i giorni senza trovare file illeggibili.
  - **Da controllare in TDD prima:** con «in-cache-non-registrato», un file vuoto del fine settimana risulterebbe «dati» invece che «nessun dato». Non blocca, ma l'elenco del manifesto direbbe una cosa inesatta.
- **B2:** quarantena dei giorni senza riga. Per la riserva toglierebbe circa 1.100 sedute dal 2005 al 2009 (le finestre scenderebbero da circa 4 a circa 3). Per lo sviluppo non è possibile: senza sviluppo non c'è screening.

**Consiglio di Claude:** A1 e B1.
- B1 va fatto con una procedura scritta: copia dei registri prima; comando dichiarato; conteggi e impronte dei registri prima e dopo registrati nel repository.
- Va fatto **dopo** la risposta del DGS alla Q2 del messaggio 17 e la decisione del titolare.
- Nel frattempo non si tocca nessun registro.
