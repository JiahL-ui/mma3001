"""GPS point plotter — bug-fixed version from the pdb debugging exercise.

Original bug (found using pdb, see docs/pdb_debug_report.md):
    One GPS point (index 100 in the sample data) had latitude/longitude
    values that were *just* outside the valid range for a Plate-Carree
    projection (lat in [-90, 90], lon in [-180, 180]) due to floating-point
    drift, e.g. lat = 90.00000000000001. Cartopy/Matplotlib would then fail
    or silently misrender that point.

Fix:
    Clip every latitude/longitude value to the valid range with
    numpy.clip before plotting (see `clip_coordinates`).

This file replaces the versions that were duplicated across notebook
cells 90 and 94 (a pure-matplotlib+PIL draft and a cartopy+pandas draft)
with a single, documented, importable module.
"""

from __future__ import annotations

import pdb
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cartopy.crs as ccrs

LAT_RANGE = (-90.0, 90.0)
LON_RANGE = (-180.0, 180.0)


def load_or_create_sample_data(csv_path: str = "gps.csv") -> pd.DataFrame:
    """Load GPS data from ``csv_path``, generating a demo file if missing.

    The generated demo data intentionally includes one out-of-range point
    (index 100) so the clipping fix below can be demonstrated/tested.

    Args:
        csv_path: Path to a CSV file with `time,latitude,longitude` columns.

    Returns:
        The loaded (or newly created) DataFrame.
    """
    path = Path(csv_path)
    if path.exists():
        return pd.read_csv(path)

    print(f"{csv_path} not found — creating a sample file for demonstration.")
    n_points = 101
    sample_data = {
        "time": range(n_points),
        "latitude": [i * 0.89 for i in range(n_points)],
        "longitude": [i * 1.79 for i in range(n_points)],
    }
    # Simulate the original bug: point 100 drifts just outside valid range.
    sample_data["latitude"][100] = 90.00000000000001
    sample_data["longitude"][100] = 180.00000000000001

    data = pd.DataFrame(sample_data)
    data.to_csv(path, index=False)
    return data


def clip_coordinates(lat: float, lon: float) -> tuple[float, float]:
    """Clip a (lat, lon) pair into the valid Plate-Carree range.

    Args:
        lat: Latitude in degrees.
        lon: Longitude in degrees.

    Returns:
        The clipped ``(lat, lon)`` pair, guaranteed to be within
        ``LAT_RANGE`` / ``LON_RANGE``.
    """
    lat_fixed = float(np.clip(lat, *LAT_RANGE))
    lon_fixed = float(np.clip(lon, *LON_RANGE))
    return lat_fixed, lon_fixed


def plot_gps_points(
    data: pd.DataFrame,
    debug_at_index: int | None = None,
) -> None:
    """Plot GPS points on a Plate-Carree world map, with values clipped.

    Args:
        data: DataFrame with `latitude` and `longitude` columns.
        debug_at_index: If set, drop into `pdb` right before plotting the
            point at this row index — mirrors the original debugging
            exercise ("break when loop_counter == 100").
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([*LON_RANGE, *LAT_RANGE], crs=ccrs.PlateCarree())
    ax.coastlines()
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

    for loop_counter in range(len(data)):
        lat = data["latitude"][loop_counter]
        lon = data["longitude"][loop_counter]

        if debug_at_index is not None and loop_counter == debug_at_index:
            pdb.set_trace()  # noqa: T100 — intentional, this is the debugging exercise

        lat_fixed, lon_fixed = clip_coordinates(lat, lon)
        ax.plot(lon_fixed, lat_fixed, "ro", markersize=3, transform=ccrs.PlateCarree())

    plt.title("GPS Data on Plate-Carree Projection (bug fixed: coords clipped)")
    plt.show()


if __name__ == "__main__":
    gps_data = load_or_create_sample_data()
    plot_gps_points(gps_data)
    print("Done — all points were clipped into valid map bounds before plotting.")
