"""Mandato R17 — Compito B: verifica indipendente di riproducibilità del collaudo IA-02 (fase 2).

Controlla:
1. SHA-256 del file decompresso `limiti_fase2.json.gz` rispetto a `IMPEGNO-PROTOCOLLO-IA02.md` §7.
2. Rilancio meccanico di `protocollo_ia02 --fase 2 --candidato bootstrap:0.05` vs `verdetto_fase2.md`.
3. Rigenerazione delle prime 200 repliche delle celle 2 e 11 su Apple Python 3.9 con `pilota_ia02`
   (fase 2, solo bootstrap) e confronto bit per bit con `limiti_fase2.json.gz`.

Solo dati inventati; nessuna scrittura nel repository; eseguire con HTTPS_PROXY=http://127.0.0.1:9.
"""
import gzip
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STUDI = ROOT / "brain" / "laboratorio" / "studi"
RIS_IA02 = STUDI / "risultati" / "ia02"
IMPEGNO_MD = STUDI / "IMPEGNO-PROTOCOLLO-IA02.md"
LIMITI_GZ = RIS_IA02 / "limiti_fase2.json.gz"
VERDETTO_MD = RIS_IA02 / "verdetto_fase2.md"


def _no_net_env():
    return dict(
        os.environ,
        HTTPS_PROXY="http://127.0.0.1:9",
        HTTP_PROXY="http://127.0.0.1:9",
        https_proxy="http://127.0.0.1:9",
        http_proxy="http://127.0.0.1:9",
        NO_PROXY="",
        no_proxy="",
    )


def _float_bits(x: float) -> bytes:
    return struct.pack("!d", float(x))


def main() -> int:
    t0 = time.time()
    impegno_text = IMPEGNO_MD.read_text(encoding="utf-8")
    m_sha = re.search(
        r"File dei limiti:\s*([0-9.]+)\s*byte,\s*SHA-256\s*`([0-9a-f]{64})`",
        impegno_text,
    )
    if not m_sha:
        raise RuntimeError("SHA-256 di fase 2 non trovato in IMPEGNO-PROTOCOLLO-IA02.md")
    atteso_bytes = int(m_sha.group(1).replace(".", ""))
    atteso_sha = m_sha.group(2)

    with tempfile.TemporaryDirectory(prefix="r17_compito_b_") as td:
        tmp = Path(td)
        json_path = tmp / "limiti_fase2.json"
        h = hashlib.sha256()
        nbytes = 0
        with gzip.open(LIMITI_GZ, "rb") as src, open(json_path, "wb") as dst:
            while True:
                chunk = src.read(1 << 16)
                if not chunk:
                    break
                dst.write(chunk)
                h.update(chunk)
                nbytes += len(chunk)
        sha_osservato = h.hexdigest()
        print(
            f"[B.1] limiti_fase2.json: bytes={nbytes} (atteso={atteso_bytes}, match={nbytes == atteso_bytes}) | "
            f"sha256={sha_osservato} | match_impegno={sha_osservato == atteso_sha}"
        )
        assert nbytes == atteso_bytes, f"Dimensione diversa: {nbytes} != {atteso_bytes}"
        assert sha_osservato == atteso_sha, f"SHA-256 diverso: {sha_osservato} != {atteso_sha}"

        archived = json.loads(json_path.read_text(encoding="utf-8"))
        print(
            f"[B.1b] intestazione: versione={archived['versione']}, fase={archived['fase']}, "
            f"repliche={archived['repliche']}, ricampionamenti={archived['ricampionamenti']}, "
            f"master={archived['master']}, celle={sorted(archived['celle'], key=int)}"
        )

        # B.2: Rilancio protocollo_ia02 --fase 2 --candidato bootstrap:0.05
        proc_proto = subprocess.run(
            [
                sys.executable,
                "-s",
                "-B",
                "-W",
                "error",
                "-m",
                "brain.laboratorio.studi.protocollo_ia02",
                "--limiti",
                str(json_path),
                "--fase",
                "2",
                "--candidato",
                "bootstrap:0.05",
            ],
            cwd=ROOT,
            env=_no_net_env(),
            capture_output=True,
            text=True,
        )
        assert proc_proto.returncode == 0, f"protocollo_ia02 rc={proc_proto.returncode}: {proc_proto.stderr}"
        verdetto_archiviato = VERDETTO_MD.read_text(encoding="utf-8").strip().splitlines()
        verdetto_attuale = proc_proto.stdout.strip().splitlines()
        identico_verdetto = verdetto_attuale == verdetto_archiviato
        print(
            f"[B.2] protocollo_ia02 rc={proc_proto.returncode}, righe_attuali={len(verdetto_attuale)}, "
            f"righe_archiviate={len(verdetto_archiviato)}, identico_riga_per_riga={identico_verdetto}"
        )
        if not identico_verdetto:
            for idx, (a, b) in enumerate(zip(verdetto_archiviato, verdetto_attuale), 1):
                if a != b:
                    print(f"  DIFF riga {idx}:\n    arch={a!r}\n    curr={b!r}")
        for line in verdetto_attuale[-3:]:
            print(f"  > {line}")
        assert identico_verdetto, "Output di protocollo_ia02 diverso da verdetto_fase2.md"

        # B.3: Rigenera prime 200 repliche celle 2 e 11 su Apple Python 3.9
        regen_path = tmp / "regen_2_11_200.json"
        t_gen0 = time.time()
        proc_pilota = subprocess.run(
            [
                sys.executable,
                "-s",
                "-B",
                "-W",
                "error",
                "-m",
                "brain.laboratorio.studi.pilota_ia02",
                "--fase",
                "2",
                "--repliche",
                "200",
                "--celle",
                "2,11",
                "--metodi",
                "bootstrap",
                "--processi",
                "2",
                "--limiti",
                str(regen_path),
            ],
            cwd=ROOT,
            env=_no_net_env(),
            capture_output=True,
            text=True,
        )
        t_gen = time.time() - t_gen0
        assert proc_pilota.returncode == 0, f"pilota_ia02 rc={proc_pilota.returncode}: {proc_pilota.stderr}"
        regen = json.loads(regen_path.read_text(encoding="utf-8"))
        print(
            f"[B.3] rigenerazione 200x2 repliche in {t_gen:.1f} s | versione={regen['versione']} | "
            f"stessa_versione_pilota={regen['versione'] == archived['versione']}"
        )

        tutte_bit_identiche = True
        for c in ("2", "11"):
            arch_list = archived["celle"][c]["bootstrap"][:200]
            reg_list = regen["celle"][c]["bootstrap"]
            assert len(reg_list) == 200
            bit_ok = 0
            val_ok = 0
            max_diff = 0.0
            first_diff = None
            for i, (a_iv, r_iv) in enumerate(zip(arch_list, reg_list), 1):
                if a_iv is None or r_iv is None:
                    same = a_iv == r_iv
                    bit_ok += int(same)
                    val_ok += int(same)
                    if not same and first_diff is None:
                        first_diff = (i, a_iv, r_iv)
                    continue
                same_val = (a_iv[0] == r_iv[0]) and (a_iv[1] == r_iv[1])
                same_bits = (
                    _float_bits(a_iv[0]) == _float_bits(r_iv[0])
                    and _float_bits(a_iv[1]) == _float_bits(r_iv[1])
                )
                val_ok += int(same_val)
                bit_ok += int(same_bits)
                diff = max(abs(a_iv[0] - r_iv[0]), abs(a_iv[1] - r_iv[1]))
                if diff > max_diff:
                    max_diff = diff
                if not same_bits and first_diff is None:
                    first_diff = (i, a_iv, r_iv)
            if bit_ok != 200:
                tutte_bit_identiche = False
            print(
                f"  cella {c}: val_ok={val_ok}/200, bit_ok={bit_ok}/200, max_diff={max_diff:.3e}, "
                f"first_diff={first_diff}"
            )
        print(f"[B.3-ESITO] coincidenza_bit_per_bit={tutte_bit_identiche} | tempo_totale={time.time() - t0:.1f} s")
        if not tutte_bit_identiche:
            print("  NOTA: differenze numeriche rispetto a CPython 3.13 (Linux) dettagliate sopra.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
