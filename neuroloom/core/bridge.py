"""The bridge algorithm: linear interpolation in (Energy, Valence) space."""
import numpy as np
import pandas as pd


def build_bridge(df: pd.DataFrame, start: tuple, target: tuple, n: int = 5) -> pd.DataFrame:
    """Build an n-song path from start (E, V) to target (E, V) by nearest-neighbor at each step."""
    es, vs = start
    et, vt = target
    points = [
        (es + (et - es) * i / (n - 1), vs + (vt - vs) * i / (n - 1))
        for i in range(n)
    ]
    used, picks = set(), []
    for (e, v) in points:
        tmp = df.copy()
        tmp["_d"] = np.sqrt((tmp["Energy"] - e) ** 2 + (tmp["Valence"] - v) ** 2)
        tmp = tmp[~tmp.index.isin(used)].sort_values("_d")
        if len(tmp) == 0:
            continue
        row = tmp.iloc[0]
        used.add(row.name)
        picks.append(row.drop("_d"))
    return pd.DataFrame(picks).reset_index(drop=True)