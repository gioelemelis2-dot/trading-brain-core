"""
Partizionamento rigoroso In-Sample / Out-Of-Sample e Sigillo Crittografico OOS.
Previene:
1. Data snooping e contaminazione da ricerca.
2. Manomissione retroattiva del dataset Out-Of-Sample.
Genera un commitment crittografico con Nonce casuale a 256-bit (CSPRNG).
"""

import hashlib
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from .models import Candle


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
    ) -> Tuple[Path, Path, Path]:
        """
        Separa fisicamente le candele in IN-SAMPLE e OUT-OF-SAMPLE.
        Genera commitment.json sigillando l'OOS con Nonce a 256 bit.
        Restituisce: (in_sample_path, out_of_sample_path, commitment_path)
        """
        if not candles:
            raise ValueError("Impossibile partizionare un dataset vuoto.")

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        if split_time is not None:
            if split_time.tzinfo is None:
                split_time = split_time.replace(tzinfo=timezone.utc)
            in_sample = [c for c in candles if c.close_time <= split_time]
            out_of_sample = [c for c in candles if c.open_time >= split_time]
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
                f.write(json.dumps(c.to_dict()) + "\n")

        # 2. Scrittura Out-Of-Sample JSONL (canonico deterministico)
        oos_path = output_dir / "out_of_sample.jsonl"
        oos_bytes = bytearray()
        with open(oos_path, "wb") as f:
            for c in out_of_sample:
                line_bytes = (json.dumps(c.to_dict(), sort_keys=True) + "\n").encode("utf-8")
                f.write(line_bytes)
                oos_bytes.extend(line_bytes)

        # 3. Generazione Nonce Casuale a 256-bit (32 byte hex)
        nonce_hex = secrets.token_hex(32)
        nonce_bytes = bytes.fromhex(nonce_hex)

        # 4. Calcolo Sigillo Crittografico SHA-256
        oos_sha256 = hashlib.sha256(oos_bytes).hexdigest()
        nonce_sha256 = hashlib.sha256(nonce_bytes).hexdigest()
        
        # Commitment: SHA256( OOS_bytes || Nonce_bytes )
        hasher = hashlib.sha256()
        hasher.update(oos_bytes)
        hasher.update(nonce_bytes)
        commitment_hash = hasher.hexdigest()

        # 5. Scrittura commitment.json
        commitment_data = {
            "protocol": "SEALED_OOS_RESEARCH_COMMITMENT_V1",
            "epistemic_type": "REGOLA",
            "condition_h": "{H_oos_sigillato}",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "symbol": candles[0].symbol,
            "timeframe": candles[0].timeframe,
            "total_records": len(candles),
            "in_sample_count": len(in_sample),
            "out_of_sample_count": len(out_of_sample),
            "split_boundary_utc": in_sample[-1].close_time.isoformat(),
            "oos_sha256": oos_sha256,
            "nonce_sha256": nonce_sha256,
            "commitment_hash": commitment_hash,
            "status": "SEALED_LOCKED",
        }

        commitment_path = output_dir / "commitment.json"
        with open(commitment_path, "w", encoding="utf-8") as f:
            json.dump(commitment_data, f, indent=2)

        # 6. Scrittura file nonce isolato (da custodire per apertura)
        nonce_path = output_dir / "sealed_nonce.secret"
        with open(nonce_path, "w", encoding="utf-8") as f:
            f.write(nonce_hex + "\n")

        return is_path, oos_path, commitment_path

    @staticmethod
    def verify_commitment(oos_file: Path, commitment_file: Path, nonce_file: Path) -> Dict[str, Any]:
        """
        Verifica crittografica formale dell'integrita' del dataset Out-Of-Sample.
        Controlla se l'OOS o il commitment sono stati manomessi.
        """
        oos_file = Path(oos_file)
        commitment_file = Path(commitment_file)
        nonce_file = Path(nonce_file)

        with open(commitment_file, "r", encoding="utf-8") as f:
            comm = json.load(f)

        with open(nonce_file, "r", encoding="utf-8") as f:
            nonce_hex = f.read().strip()
        nonce_bytes = bytes.fromhex(nonce_hex)

        with open(oos_file, "rb") as f:
            oos_bytes = f.read()

        computed_oos_sha = hashlib.sha256(oos_bytes).hexdigest()
        computed_nonce_sha = hashlib.sha256(nonce_bytes).hexdigest()

        hasher = hashlib.sha256()
        hasher.update(oos_bytes)
        hasher.update(nonce_bytes)
        computed_commitment = hasher.hexdigest()

        is_oos_valid = (computed_oos_sha == comm["oos_sha256"])
        is_nonce_valid = (computed_nonce_sha == comm["nonce_sha256"])
        is_commitment_valid = (computed_commitment == comm["commitment_hash"])

        return {
            "valid": is_oos_valid and is_nonce_valid and is_commitment_valid,
            "oos_match": is_oos_valid,
            "nonce_match": is_nonce_valid,
            "commitment_match": is_commitment_valid,
            "expected_commitment": comm["commitment_hash"],
            "computed_commitment": computed_commitment,
        }
