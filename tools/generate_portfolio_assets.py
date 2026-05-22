#!/usr/bin/env python3
"""Generate and copy final visual assets for portfolio project pages.

This script reads source material from the standalone data-science portfolio
folder when it is present, then writes final website assets into
portfolio/resources. The live website does not import from the source folder.
"""

from __future__ import annotations

import html
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Mizher-Data-Science-AI-Portfolio"
DEST = ROOT / "portfolio" / "resources"

INK = "#1f2937"
MUTED = "#5f6f73"
ACCENT = "#0f766e"
WARM = "#8b5e34"
PANEL = "#f8f6f0"
LINE = "#d8ded8"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def copy_asset(src: Path, dest: Path) -> None:
    ensure_dir(dest.parent)
    shutil.copy2(src, dest)


def save_flow_svg(path: Path, title: str, subtitle: str, steps: list[tuple[str, str]]) -> None:
    ensure_dir(path.parent)
    width = 1120
    box_w = 190
    gap = 24
    box_h = 112
    start_x = 48
    start_y = 140
    height = 330
    defs = """<defs>
      <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
        <feDropShadow dx="0" dy="12" stdDeviation="12" flood-color="#0f172a" flood-opacity="0.12"/>
      </filter>
      <marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
        <path d="M0,0 L10,4 L0,8 z" fill="#0f766e"/>
      </marker>
    </defs>"""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f"<title id=\"title\">{html.escape(title)}</title>",
        f"<desc id=\"desc\">{html.escape(subtitle)}</desc>",
        defs,
        f'<rect width="{width}" height="{height}" rx="28" fill="{PANEL}"/>',
        f'<text x="48" y="58" font-family="Georgia, serif" font-size="34" font-weight="700" fill="{INK}">{html.escape(title)}</text>',
        f'<text x="48" y="92" font-family="Arial, sans-serif" font-size="17" fill="{MUTED}">{html.escape(subtitle)}</text>',
    ]
    for i, (heading, body) in enumerate(steps):
        x = start_x + i * (box_w + gap)
        parts.extend(
            [
                f'<rect x="{x}" y="{start_y}" width="{box_w}" height="{box_h}" rx="18" fill="#ffffff" stroke="{LINE}" filter="url(#shadow)"/>',
                f'<circle cx="{x + 28}" cy="{start_y + 30}" r="15" fill="#e6f4f1" stroke="#b6d8d1"/>',
                f'<text x="{x + 28}" y="{start_y + 36}" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" font-weight="700" fill="{ACCENT}">{i + 1}</text>',
                f'<text x="{x + 52}" y="{start_y + 30}" font-family="Arial, sans-serif" font-size="17" font-weight="700" fill="{INK}">{html.escape(heading)}</text>',
            ]
        )
        for line_i, line in enumerate(wrap_text(body, 22)[:3]):
            parts.append(
                f'<text x="{x + 18}" y="{start_y + 62 + line_i * 19}" font-family="Arial, sans-serif" font-size="14" fill="{MUTED}">{html.escape(line)}</text>'
            )
        if i < len(steps) - 1:
            x1 = x + box_w + 7
            x2 = x + box_w + gap - 7
            y = start_y + box_h / 2
            parts.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{ACCENT}" stroke-width="3" marker-end="url(#arrow)"/>')
    parts.append("</svg>")
    path.write_text("\n".join(parts), encoding="utf-8")


def wrap_text(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        if sum(len(w) for w in current) + len(current) + len(word) > max_chars and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines


def generate_breast_feature_distribution() -> None:
    src = SOURCE / "Mizher_Breast_Cancer_Analysis_AI" / "Data" / "data.csv"
    df = pd.read_csv(src)
    features = ["concave points_worst", "area_worst", "texture_mean"]
    labels = ["Concave points worst", "Area worst", "Texture mean"]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.6))
    colors = {"B": "#8fc7bf", "M": "#9a6a3e"}
    for ax, feature, label in zip(axes, features, labels):
        data = [df.loc[df["diagnosis"] == cls, feature].dropna() for cls in ["B", "M"]]
        box = ax.boxplot(data, patch_artist=True, labels=["Benign", "Malignant"], widths=0.55)
        for patch, color in zip(box["boxes"], [colors["B"], colors["M"]]):
            patch.set_facecolor(color)
            patch.set_alpha(0.78)
        for median in box["medians"]:
            median.set_color("#111827")
            median.set_linewidth(1.6)
        ax.set_title(label, fontsize=12, color=INK)
        ax.grid(axis="y", alpha=0.22)
        ax.tick_params(colors=MUTED)
    fig.suptitle("Feature Distribution by Diagnosis", fontsize=18, color=INK, y=1.02)
    fig.text(0.5, -0.02, "Generated from the Breast Cancer Wisconsin Diagnostic dataset in the project source folder.", ha="center", color=MUTED)
    fig.tight_layout()
    out = DEST / "cancer-malignancy" / "feature_distribution_by_diagnosis.png"
    ensure_dir(out.parent)
    fig.savefig(out, dpi=180, bbox_inches="tight", facecolor="#fbfaf7")
    plt.close(fig)


def generate_alpr_assets() -> None:
    src_root = SOURCE / "Mizher_License_Plate_Recognition_Project"
    out_dir = DEST / "lp-recognition"
    ensure_dir(out_dir)
    for src_name, dest_name in [
        ("Total Prediction Outcomes.png", "total_prediction_outcomes.png"),
        ("Confidence Score.png", "confidence_score_distribution.png"),
        ("Fourier Processing Outcomes.png", "fourier_processing_outcomes.png"),
    ]:
        copy_asset(src_root / "Visualizations" / src_name, out_dir / dest_name)

    df = pd.read_csv(src_root / "Data" / "analysis.csv")

    def norm(value: object) -> str:
        if pd.isna(value):
            return ""
        return "".join(ch for ch in str(value).upper() if ch.isalnum())

    df["actual_norm"] = df["actual_license_plate"].map(norm)
    df["pred_norm"] = df["final_prediction"].map(norm)
    scored = df[(df["actual_norm"] != "") & (df["pred_norm"] != "")]
    exact = int((scored["actual_norm"] == scored["pred_norm"]).sum())
    mismatch = int(len(scored) - exact)
    no_prediction = int(df["final_prediction"].isna().sum())
    unlabeled_or_unscored = int(len(df) - len(scored) - no_prediction)
    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    labels = ["Exact OCR match", "Mismatch", "No prediction", "Unscored / unlabeled"]
    values = [exact, mismatch, no_prediction, unlabeled_or_unscored]
    bars = ax.bar(labels, values, color=["#0f766e", "#9a6a3e", "#a5b4b0", "#d6c7b3"])
    ax.set_title("ALPR Output Review", fontsize=18, color=INK)
    ax.set_ylabel("Image count", color=MUTED)
    ax.tick_params(axis="x", rotation=18, colors=MUTED)
    ax.tick_params(axis="y", colors=MUTED)
    ax.grid(axis="y", alpha=0.22)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 4, f"{int(bar.get_height())}", ha="center", color=INK, fontsize=10)
    fig.text(0.5, -0.03, "Exact-match review generated from analysis.csv; it is not presented as production accuracy.", ha="center", color=MUTED)
    fig.tight_layout()
    fig.savefig(out_dir / "alpr_output_review.png", dpi=180, bbox_inches="tight", facecolor="#fbfaf7")
    plt.close(fig)

    sample_rows = [
        scored[scored["actual_norm"] == scored["pred_norm"]].iloc[0],
        scored[scored["actual_norm"] != scored["pred_norm"]].iloc[0],
    ]
    cards = []
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 28)
    font_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 22)
    for label, row in zip(["Successful exact match", "Failure case"], sample_rows):
        image_path = src_root / row["file_path"]
        im = Image.open(image_path).convert("RGB")
        im = ImageOps.contain(im, (500, 310), method=Image.Resampling.LANCZOS)
        card = Image.new("RGB", (560, 470), "#fbfaf7")
        draw = ImageDraw.Draw(card)
        x = (560 - im.width) // 2
        card.paste(im, (x, 28))
        y = 355
        draw.text((28, y), label, font=font_title, fill=INK)
        draw.text((28, y + 40), f"Actual: {row['actual_license_plate']}", font=font_body, fill=MUTED)
        draw.text((28, y + 72), f"Predicted: {row['final_prediction']}", font=font_body, fill=WARM if label == "Failure case" else ACCENT)
        cards.append(card)
    montage = Image.new("RGB", (1160, 500), "#f4f1ea")
    montage.paste(cards[0], (20, 15))
    montage.paste(cards[1], (580, 15))
    montage.save(out_dir / "alpr_case_examples.png", quality=95)

    save_flow_svg(
        out_dir / "alpr_pipeline.svg",
        "ALPR Processing Pipeline",
        "Conceptual workflow based on the project notebook and saved outputs.",
        [
            ("Vehicle image", "Input image from public plate datasets"),
            ("Plate detection", "YOLO-style model localizes the plate crop"),
            ("Preprocessing", "Fourier, soft, and binary image variants are tested"),
            ("OCR", "Character model extracts candidate plate text"),
            ("Review", "Confidence and exact-match checks expose failure modes"),
        ],
    )


def generate_walter_assets() -> None:
    src_root = SOURCE / "Mizher_Walter_Chemistry_Chatbot"
    out_dir = DEST / "walter"
    ensure_dir(out_dir)
    for src, dest in [
        (src_root / "Result Screenshots" / "Samples" / "Hydrogen Summary.png", out_dir / "hydrogen_summary_response.png"),
        (src_root / "Result Screenshots" / "Samples" / "Is Carbon Important to Life.png", out_dir / "carbon_life_response.png"),
    ]:
        copy_asset(src, dest)

    df = pd.read_csv(src_root / "Data" / "Final_Chemical_Element_Data.csv")
    lengths = df["Data"].astype(str).str.split().str.len()
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.scatter(df["Atomic Number"], lengths, s=38, color=ACCENT, alpha=0.78, edgecolor="#0b4f49", linewidth=0.4)
    ax.set_title("Chemistry Corpus Coverage", fontsize=18, color=INK)
    ax.set_xlabel("Atomic number", color=MUTED)
    ax.set_ylabel("Approximate token count", color=MUTED)
    ax.grid(alpha=0.24)
    ax.tick_params(colors=MUTED)
    fig.text(0.5, -0.02, f"Generated from {len(df)} element records in the Walter chemistry corpus.", ha="center", color=MUTED)
    fig.tight_layout()
    fig.savefig(out_dir / "chemistry_corpus_coverage.png", dpi=180, bbox_inches="tight", facecolor="#fbfaf7")
    plt.close(fig)

    save_flow_svg(
        out_dir / "semantic_chatbot_pipeline.svg",
        "Domain Chatbot Retrieval Flow",
        "Conceptual pipeline summarizing the chemistry chatbot and related semantic-retrieval work.",
        [
            ("Question", "User asks a chemistry or corpus-specific question"),
            ("Normalize", "Lowercase, tokenize, lemmatize, and remove noise"),
            ("Represent", "TF-IDF or sentence embeddings encode query and corpus"),
            ("Rank", "Cosine similarity selects the closest reference text"),
            ("Respond", "Template and summary logic returns a grounded answer"),
        ],
    )


def generate_redistricting_assets() -> None:
    out_dir = DEST / "redistricting"
    ensure_dir(out_dir)
    district_pop = pd.DataFrame(
        {
            "District": list(range(1, 11)),
            "Population": [423793, 930745, 2272161, 480574, 493856, 473419, 1106130, 621946, 360043, 349798],
        }
    )
    target = 751246
    fig, ax = plt.subplots(figsize=(9.2, 5))
    colors = ["#0f766e" if pop <= target * 1.25 else "#9a6a3e" for pop in district_pop["Population"]]
    ax.bar(district_pop["District"].astype(str), district_pop["Population"], color=colors)
    ax.axhline(target, color="#1f2937", linestyle="--", linewidth=1.5, label="Ideal equal population")
    ax.set_title("Modeled District Population Balance", fontsize=18, color=INK)
    ax.set_xlabel("Assigned district", color=MUTED)
    ax.set_ylabel("Population", color=MUTED)
    ax.tick_params(colors=MUTED)
    ax.grid(axis="y", alpha=0.22)
    ax.legend(frameon=False)
    fig.text(0.5, -0.02, "Generated from the district assignment table saved in the project notebook output.", ha="center", color=MUTED)
    fig.tight_layout()
    fig.savefig(out_dir / "district_population_balance.png", dpi=180, bbox_inches="tight", facecolor="#fbfaf7")
    plt.close(fig)

    save_flow_svg(
        out_dir / "redistricting_optimization_flow.svg",
        "Optimization Model Flow",
        "Conceptual workflow for translating redistricting into a constrained decision model.",
        [
            ("Inputs", "County populations, demographics, and adjacency data"),
            ("Variables", "Binary county-to-district assignments"),
            ("Constraints", "Allocation, county minimums, and geography cuts"),
            ("Objective", "Reduce arbitrary assignment while meeting model rules"),
            ("Outputs", "District table, map, and tradeoff review"),
        ],
    )


def generate_pixxeleate_assets() -> None:
    out_dir = DEST / "pixxeleate"
    ensure_dir(out_dir)
    save_flow_svg(
        out_dir / "pixxeleate_backend_architecture.svg",
        "Pixxeleate Backend Architecture",
        "Conceptual architecture diagram. Sensitive vendor and fulfillment details are intentionally omitted.",
        [
            ("Storefront", "Customer upload and preview request"),
            ("Django API", "Validation, job state, and request routing"),
            ("Image engine", "Resize, palette map, dot plan, and render"),
            ("Storage", "Local or cloud-backed asset persistence"),
            ("Dashboard", "Review tools, logs, and manual checks"),
        ],
    )
    save_flow_svg(
        out_dir / "image_to_canvas_workflow.svg",
        "Image-to-Canvas Workflow",
        "Conceptual processing flow for turning an uploaded image into reviewable outputs.",
        [
            ("Upload", "Receive source image and rendering settings"),
            ("Normalize", "Resize and prepare image for deterministic processing"),
            ("Quantize", "Map image colors to a constrained palette"),
            ("Render", "Create preview image and print-oriented guides"),
            ("Review", "Store artifacts for dashboard inspection"),
        ],
    )


def generate_carbon_assets() -> None:
    src = SOURCE / "Data_Visualization_Carbon_Footprint_of_Trade" / "Graphics" / "Climate Change Trends" / "sea_levels.png"
    copy_asset(src, DEST / "carbon-footprint" / "sea_levels.png")


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Source folder not found: {SOURCE}")
    generate_breast_feature_distribution()
    generate_alpr_assets()
    generate_walter_assets()
    generate_redistricting_assets()
    generate_pixxeleate_assets()
    generate_carbon_assets()
    print("Portfolio assets generated.")


if __name__ == "__main__":
    main()
