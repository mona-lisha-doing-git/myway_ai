from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import cudf  # type: ignore
except Exception:  # pragma: no cover - depends on GPU/RAPIDS runtime
    cudf = None


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@dataclass(frozen=True)
class DatasetBundle:
    colleges: Any
    courses: Any
    placements: Any
    cutoffs: Any
    backend: str


def _normalize_columns(frame: Any) -> Any:
    frame.columns = (
        frame.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return frame


def _read_csv(path: Path, use_gpu: bool) -> Any:
    if use_gpu and cudf is not None:
        return cudf.read_csv(path)
    return pd.read_csv(path, na_values=["NULL", "null", ""])


def load_datasets(data_dir: Path | str = DATA_DIR, prefer_gpu: bool = True) -> DatasetBundle:
    base_path = Path(data_dir)
    use_gpu = prefer_gpu and cudf is not None

    colleges = _normalize_columns(_read_csv(base_path / "colleges.csv", use_gpu))
    courses = _normalize_columns(_read_csv(base_path / "courses.csv", use_gpu))
    placements = _normalize_columns(_read_csv(base_path / "placements.csv", use_gpu))
    cutoffs = _normalize_columns(_read_csv(base_path / "cutoffs.csv", use_gpu))

    return DatasetBundle(
        colleges=colleges,
        courses=courses,
        placements=placements,
        cutoffs=cutoffs,
        backend="cudf" if use_gpu else "pandas",
    )


def to_pandas(frame: Any) -> pd.DataFrame:
    if hasattr(frame, "to_pandas"):
        return frame.to_pandas()
    return frame.copy()
