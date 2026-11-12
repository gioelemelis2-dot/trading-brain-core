"""
Partizionamento rigoroso In-Sample / Out-Of-Sample e Sigillo Crittografico OOS.
Nota di Sicurezza: Questo modulo implementa un *commitment* crittografico basato su hash
(hiding & binding tramite nonce segreto CSPRNG a 256-bit), NON una firma digitale asimmetrica.
Chi custodisce il nonce puo' ricalcolare o rigenerare il commitment: per garantire la
separazione dei ruoli, il nonce puo' essere isolato in un percorso dedicato tramite `nonce_dir`
o la variabile d'ambiente `TRADING_OOS_NONCE_DIR`.
Allineato formalmente allo standard di brain/guardian/journal/journal.py (sigilla):
Impegno = SHA256((nonce_hex + oos_text_canonico).encode("utf-8"))
Verifica tramite secrets.compare_digest.
"""

import hashlib
import json
import os
import secrets
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from .models import Candle, DataValidationError


def _canonico(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class DatasetPartitioner:
    def __init__(self, in_sample_ratio: float = 0.7):
        if not (0.1 <= in_sample_ratio <= 0.9):
            raise ValueError(f"in_sample_ratio deve essere compreso tra 0.1 e 0.9. Trovato: {in_sample_ratio}")
        self.in_sample_ratio = in_sample_ratio

    def split(
        self,
        candles: List[Candle],
        output_dir: Path,
        split_time: Optional[datetime] = None,
        nonce_dir: Optional[Path] = None,
    ) -> Tuple[Path, Path, Path]:
        """
        Separa fisicamente le candele in IN-SAMPLE e OUT-OF-SAMPLE.
        Genera commitment.json sigillando l'OOS con Nonce CSPRNG a 256 bit (commitment crittografico).
        Il nonce viene salvato in `nonce_dir`, oppure in `TRADING_OOS_NONCE_DIR` se impostata,
        altrimenti in `output_dir`.
        """
        if not candles:
            raise ValueError("Impossibile partizionare un dataset vuoto.")

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        if split_time is not None:
            if split_time.tzinfo is None or split_time.utcoffset() != timedelta(0):
                raise DataValidationError("split_time deve avere timezone UTC esplicito.")
            in_sample = [c for c in candles if c.close_time <= split_time]
            out_of_sample = [c for c in candles if c.close_time > split_time]
            assert len(in_sample) + len(out_of_sample) == len(candles), (
                "Partizione non disgiunta/esaustiva su split_time."
            )
            if not in_sample or not out_of_sample:
                raise ValueError(
                    "Partizione non valida su split_time: in_sample e out_of_sample devono essere entrambi non vuoti."
                )
        else:
            split_idx = int(len(candles) * self.in_sample_ratio)
            if split_idx <= 0 or split_idx >= len(candles):
                raise ValueError("Dimensione insufficiente per partizionare In-Sample e Out-Of-Sample.")
            in_sample = candles[:split_idx]
            out_of_sample = candles[split_idx:]

        # 1. Scrittura In-Sample JSONL
        is_path = output_dir / "in_sample.jsonl"
        with open(is_path, "w", encoding="utf-8") as f:
            for c in in_sample:
                f.write(_canonico(c.to_dict()) + "\n")

        # 2. Scrittura Out-Of-Sample JSONL Canonico
        oos_path = output_dir / "out_of_sample.jsonl"
        oos_canonical_lines = []
        with open(oos_path, "w", encoding="utf-8") as f:
            for c in out_of_sample:
                line = _canonico(c.to_dict())
                f.write(line + "\n")
                oos_canonical_lines.append(line)

        oos_text_canonico = "\n".join(oos_canonical_lines) + "\n"

        # 3. Generazione Nonce Casuale a 256-bit (32 byte hex) CSPRNG
        nonce_hex = secrets.token_hex(32)

        # 4. Calcolo Sigillo Crittografico SHA-256 standard Journal
        # Formula journal.sigilla: SHA256((nonce_hex + payload_text).encode("utf-8"))
        hasher = hashlib.sha256()
        hasher.update((nonce_hex + oos_text_canonico).encode("utf-8"))
        commitment_hash = hasher.hexdigest()

        oos_sha256 = hashlib.sha256(oos_text_canonico.encode("utf-8")).hexdigest()

        # 5. Scrittura commitment.json
        commitment_data = {
            "protocol": "SEALED_OOS_RESEARCH_COMMITMENT_V2",
            "epistemic_type": "REGOLA",
            "condition_h": "{H_oos_sigillato}",
            "created_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "symbol": candles[0].symbol,
            "timeframe": candles[0].timeframe,
            "total_records": len(candles),
            "in_sample_count": len(in_sample),
            "out_of_sample_count": len(out_of_sample),
            "split_boundary_utc": in_sample[-1].close_time.isoformat(),
            "oos_sha256": oos_sha256,
            "commitment_hash": commitment_hash,
            "status": "SEALED_LOCKED",
        }

        commitment_path = output_dir / "commitment.json"
        with open(commitment_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(commitment_data, indent=2) + "\n")

        # 6. Scrittura file nonce in percorso isolabile (parametro -> env -> output_dir)
        env_nonce_dir = os.environ.get("TRADING_OOS_NONCE_DIR")
        if nonce_dir is not None:
            resolved_nonce_dir = Path(nonce_dir)
        elif env_nonce_dir:
            resolved_nonce_dir = Path(env_nonce_dir)
        else:
            resolved_nonce_dir = output_dir
        resolved_nonce_dir.mkdir(parents=True, exist_ok=True)
        nonce_path = resolved_nonce_dir / "sealed_nonce.secret"
        with open(nonce_path, "w", encoding="utf-8") as f:
            f.write(nonce_hex + "\n")

        return is_path, oos_path, commitment_path

    @staticmethod
    def verify_commitment(oos_file: Path, commitment_file: Path, nonce_file: Path) -> Dict[str, Any]:
        """
        Verifica crittografica formale dell'integrita' del dataset Out-Of-Sample.
        Usa secrets.compare_digest per prevenire attacchi di temporizzazione.
        Gestisce gracefully commitment.json malformati restituendo valid=False e reason.
        """
        oos_file = Path(oos_file)
        commitment_file = Path(commitment_file)
        nonce_file = Path(nonce_file)

        try:
            with open(commitment_file, "r", encoding="utf-8") as f:
                comm = json.load(f)
        except (OSError, json.JSONDecodeError, ValueError):
            return {
                "valid": False,
                "oos_match": False,
                "commitment_match": False,
                "reason": "commitment malformato",
            }

        if (
            not isinstance(comm, dict)
            or not isinstance(comm.get("oos_sha256"), str)
            or not isinstance(comm.get("commitment_hash"), str)
        ):
            return {
                "valid": False,
                "oos_match": False,
                "commitment_match": False,
                "reason": "commitment malformato",
            }

        with open(nonce_file, "r", encoding="utf-8") as f:
            nonce_hex = f.read().strip()

        with open(oos_file, "r", encoding="utf-8") as f:
            oos_text = f.read()

        computed_oos_sha = hashlib.sha256(oos_text.encode("utf-8")).hexdigest()

        hasher = hashlib.sha256()
        hasher.update((nonce_hex + oos_text).encode("utf-8"))
        computed_commitment = hasher.hexdigest()

        is_oos_valid = secrets.compare_digest(computed_oos_sha, comm["oos_sha256"])
        is_commitment_valid = secrets.compare_digest(computed_commitment, comm["commitment_hash"])

        return {
            "valid": is_oos_valid and is_commitment_valid,
            "oos_match": is_oos_valid,
            "commitment_match": is_commitment_valid,
            "expected_commitment": comm["commitment_hash"],
            "computed_commitment": computed_commitment,
        }
