#!/usr/bin/env python3
"""One-click build script for MMA3001 project documentation.

Generates (in order):
  1. pdoc HTML documentation    → docs/pdoc_html/
  2. pytest HTML test report    → docs/pytest_report.html
  3. Mermaid flowchart PNG      → docs/matmul_flowchart.png
  4. GPS bug demonstration plot → data/gps_error_plot.png

Usage:
    python tools/build_docs.py            # full build
    python tools/build_docs.py --pdoc     # pdoc only
    python tools/build_docs.py --pytest   # pytest only
    python tools/build_docs.py --plots    # plots only
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SRC = ROOT / "src"
TESTS = ROOT / "tests"
TOOLS = ROOT / "tools"
DATA = ROOT / "data"


# --------------------------------------------------------------------------- #
# Step 1: pdoc HTML documentation
# --------------------------------------------------------------------------- #

def build_pdoc() -> None:
    """Generate pdoc HTML docs for src/matmul.py into docs/pdoc_html/."""
    output_dir = DOCS / "pdoc_html"
    print(f"[pdoc] Generating HTML docs → {output_dir}")
    subprocess.run(
        [
            sys.executable, "-m", "pdoc",
            str(SRC / "matmul.py"),
            "-o", str(output_dir),
        ],
        check=True,
        cwd=str(ROOT),
    )
    print(f"[pdoc] Done: {output_dir / 'matmul.html'}")


# --------------------------------------------------------------------------- #
# Step 2: pytest HTML report
# --------------------------------------------------------------------------- #

def build_pytest() -> None:
    """Run pytest and produce an HTML report in docs/pytest_report.html."""
    report_path = DOCS / "pytest_report.html"
    print(f"[pytest] Running tests → {report_path}")
    subprocess.run(
        [
            sys.executable, "-m", "pytest",
            str(TESTS / "test_matmul.py"),
            f"--html={report_path}",
            "--self-contained-html",
            "-v",
        ],
        check=True,
        cwd=str(ROOT),
    )
    print(f"[pytest] Done: {report_path}")


# --------------------------------------------------------------------------- #
# Step 3: Mermaid flowchart → PNG
# --------------------------------------------------------------------------- #

def build_flowchart() -> None:
    """Render the Mermaid flowchart from docs/matmul_flowchart.md to PNG.

    Uses matplotlib to draw a styled version of the matmul flowchart
    directly (no external Mermaid CLI required).
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    output_path = DOCS / "matmul_flowchart.png"
    print(f"[flowchart] Rendering → {output_path}")

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")
    ax.set_title("matmul(A, B) Algorithm Flowchart", fontsize=14, fontweight="bold", pad=20)

    # --- Define node positions and content ---
    # (x, y, width, height, label, shape)
    # shape: 'rounded'=start/end, 'rectangle'=process, 'diamond'=decision
    nodes: list[dict] = [
        {"xy": (5.0, 11.5), "label": "Start", "shape": "rounded", "color": "#e8f5e9"},
        {"xy": (5.0, 10.8), "label": "Get dims: m,n = shape(A)\nn,p = shape(B)", "shape": "rect", "color": "#e3f2fd"},
        {"xy": (5.0, 10.1), "label": "C = zeros(m, p)", "shape": "rect", "color": "#e3f2fd"},
        {"xy": (5.0, 9.0), "label": "i = 0", "shape": "rect", "color": "#e3f2fd"},
        {"xy": (5.0, 7.8), "label": "i < m ?", "shape": "diamond", "color": "#fff3e0"},
        {"xy": (5.0, 6.5), "label": "j = 0", "shape": "rect", "color": "#e3f2fd"},
        {"xy": (5.0, 5.3), "label": "j < p ?", "shape": "diamond", "color": "#fff3e0"},
        {"xy": (5.0, 4.1), "label": "s = 0, k = 0", "shape": "rect", "color": "#e3f2fd"},
        {"xy": (5.0, 2.9), "label": "k < n ?", "shape": "diamond", "color": "#fff3e0"},
        {"xy": (5.0, 1.7), "label": "s += A[i][k] * B[k][j]\nk = k + 1", "shape": "rect", "color": "#fce4ec"},
        {"xy": (5.0, 0.9), "label": "C[i][j] = s", "shape": "rect", "color": "#e3f2fd"},
        {"xy": (7.8, 5.3), "label": "j = j + 1", "shape": "rect", "color": "#f3e5f5"},
        {"xy": (7.8, 7.8), "label": "i = i + 1", "shape": "rect", "color": "#f3e5f5"},
        {"xy": (2.2, 7.8), "label": "Return C", "shape": "rect", "color": "#e8f5e9"},
        {"xy": (2.2, 6.8), "label": "End", "shape": "rounded", "color": "#e8f5e9"},
    ]

    for node in nodes:
        x, y = node["xy"]
        w, h = 2.2, 0.5
        fc = node["color"]

        if node["shape"] == "rounded":
            patch = mpatches.FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.1", facecolor=fc, edgecolor="black", linewidth=1.5
            )
        elif node["shape"] == "diamond":
            diamond_verts = [
                (x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)
            ]
            patch = mpatches.Polygon(diamond_verts, facecolor=fc, edgecolor="black", linewidth=1.5)
        else:
            patch = mpatches.FancyBboxPatch(
                (x - w/2, y - h/2), w, h,
                boxstyle="round,pad=0.05", facecolor=fc, edgecolor="black", linewidth=1.5
            )
        ax.add_patch(patch)
        ax.text(x, y, node["label"], ha="center", va="center", fontsize=7, fontweight="bold")

    # --- Draw arrows ---
    # (from_xy, to_xy, label)
    arrows = [
        ((5.0, 11.25), (5.0, 11.05), ""),
        ((5.0, 10.55), (5.0, 10.35), ""),
        ((5.0, 9.85), (5.0, 9.25), ""),
        ((5.0, 8.75), (5.0, 8.1), ""),
        ((5.0, 7.55), (6.1, 6.75), "True"),
        ((3.9, 7.8), (3.3, 7.8), "False"),
        ((5.0, 6.25), (5.0, 5.6), ""),
        ((5.0, 5.05), (6.1, 4.35), "True"),
        ((3.9, 5.3), (6.7, 6.75), "False"),
        ((5.0, 3.85), (5.0, 3.2), ""),
        ((5.0, 2.65), (6.1, 1.95), "True"),
        ((3.9, 2.9), (3.9, 1.2), "False"),
        ((6.05, 1.7), (6.05, 2.9), ""),  # k loop back
        ((6.05, 0.9), (6.05, 5.3), ""),  # to j++
        ((6.7, 5.3), (6.7, 7.55), ""),   # j loop back
        ((6.7, 7.8), (6.7, 9.0), ""),    # i loop back
        ((3.3, 7.55), (3.3, 7.05), ""),
    ]

    for (x1, y1), (x2, y2), label in arrows:
        ax.annotate(
            label, xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
            fontsize=7, ha="center", va="center",
        )

    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[flowchart] Done: {output_path}")


# --------------------------------------------------------------------------- #
# Step 4: GPS error plot
# --------------------------------------------------------------------------- #

def build_gps_plot() -> None:
    """Generate a GPS error demonstration plot and save to data/gps_error_plot.png."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    output_path = DATA / "gps_error_plot.png"
    print(f"[gps] Rendering error demo → {output_path}")

    # Simulate the buggy scenario: one point slightly out of bounds
    np.random.seed(42)
    n_points = 101
    lats = np.random.uniform(-85, 85, n_points).tolist()
    lons = np.random.uniform(-175, 175, n_points).tolist()
    # Insert the buggy point at index 100
    lats[100] = 90.00000000000001
    lons[100] = 180.00000000000001

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # --- Left: Buggy version (point rendered outside) ---
    ax1.set_title("Before Fix — Buggy (point outside bounds)", fontweight="bold", color="red")
    ax1.set_xlim(-185, 185)
    ax1.set_ylim(-95, 95)
    ax1.axhline(y=90, color="gray", linestyle="--", alpha=0.5)
    ax1.axhline(y=-90, color="gray", linestyle="--", alpha=0.5)
    ax1.axvline(x=180, color="gray", linestyle="--", alpha=0.5)
    ax1.axvline(x=-180, color="gray", linestyle="--", alpha=0.5)
    ax1.fill_between([-180, 180], -90, 90, alpha=0.1, color="blue")
    ax1.scatter(lons[:100], lats[:100], c="blue", s=8, label="Valid points")
    ax1.scatter([lons[100]], [lats[100]], c="red", s=80, marker="x", linewidths=2,
                label=f"Out-of-bounds\n(lat={lats[100]:.10f})")
    ax1.set_xlabel("Longitude")
    ax1.set_ylabel("Latitude")
    ax1.legend(fontsize=8)
    ax1.text(0, -93, "Valid range: lat ∈ [-90,90], lon ∈ [-180,180]", ha="center", fontsize=8, color="gray")

    # --- Right: Fixed version (clipped) ---
    lats_fixed = np.clip(lats, -90, 90)
    lons_fixed = np.clip(lons, -180, 180)

    ax2.set_title("After Fix — np.clip() applied (all points in bounds)", fontweight="bold", color="green")
    ax2.set_xlim(-185, 185)
    ax2.set_ylim(-95, 95)
    ax2.axhline(y=90, color="gray", linestyle="--", alpha=0.5)
    ax2.axhline(y=-90, color="gray", linestyle="--", alpha=0.5)
    ax2.axvline(x=180, color="gray", linestyle="--", alpha=0.5)
    ax2.axvline(x=-180, color="gray", linestyle="--", alpha=0.5)
    ax2.fill_between([-180, 180], -90, 90, alpha=0.1, color="green")
    ax2.scatter(lons_fixed, lats_fixed, c="green", s=8, label="All points (clipped)")
    ax2.scatter([np.clip(lons[100], -180, 180)], [np.clip(lats[100], -90, 90)],
                c="orange", s=60, marker="o", edgecolors="black", linewidths=1,
                label=f"Fixed point\n(clipped to 90°, 180°)")
    ax2.set_xlabel("Longitude")
    ax2.set_ylabel("Latitude")
    ax2.legend(fontsize=8)

    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[gps] Done: {output_path}")


# --------------------------------------------------------------------------- #
# Main dispatcher
# --------------------------------------------------------------------------- #

def main() -> None:
    parser = argparse.ArgumentParser(description="Build MMA3001 project documentation.")
    parser.add_argument("--pdoc", action="store_true", help="Only build pdoc HTML")
    parser.add_argument("--pytest", action="store_true", help="Only run pytest report")
    parser.add_argument("--plots", action="store_true", help="Only generate plots")
    args = parser.parse_args()

    run_all = not (args.pdoc or args.pytest or args.plots)

    if run_all or args.pdoc:
        build_pdoc()
    if run_all or args.pytest:
        build_pytest()
    if run_all or args.plots:
        build_flowchart()
        build_gps_plot()

    print("\n✅ All requested documentation builds complete.")


if __name__ == "__main__":
    main()
