import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
EDA_DIR = OUTPUT_DIR / "eda"
EDA_DIR.mkdir(parents=True, exist_ok=True)

MODELS = ["gpt-5.2", "gemini-3-flash", "qwen3.6-plus"]


def pct(value: float) -> float:
    return round(value * 100, 2)


def add_text_lengths(df: pd.DataFrame, column: str, prefix: str) -> pd.DataFrame:
    out = df.copy()
    text = out[column].fillna("").astype(str)
    out[f"{prefix}_char_len"] = text.str.len()
    out[f"{prefix}_word_len"] = text.str.split().str.len()
    return out


def save_bar(series: pd.Series, title: str, ylabel: str, path: Path, rotation: int = 20):
    fig, ax = plt.subplots(figsize=(9, 5))
    series.plot(kind="bar", ax=ax, color="#4C78A8")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=rotation)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_boxplot(df: pd.DataFrame, by: str, value: str, title: str, path: Path):
    fig, ax = plt.subplots(figsize=(10, 5))
    df.boxplot(column=value, by=by, ax=ax, grid=False, rot=20)
    fig.suptitle("")
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel(value)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_heatmap(table: pd.DataFrame, title: str, path: Path):
    fig, ax = plt.subplots(figsize=(8, 5))
    image = ax.imshow(table.values, cmap="Blues")
    ax.set_title(title)
    ax.set_xticks(range(len(table.columns)))
    ax.set_yticks(range(len(table.index)))
    ax.set_xticklabels(table.columns, rotation=25, ha="right")
    ax.set_yticklabels(table.index)

    for row_idx in range(table.shape[0]):
        for col_idx in range(table.shape[1]):
            ax.text(col_idx, row_idx, int(table.iloc[row_idx, col_idx]), ha="center", va="center")

    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def dataset_eda():
    seed = pd.DataFrame(json.loads((DATA_DIR / "seed_prompts_v1.json").read_text(encoding="utf-8")))
    augmented = pd.DataFrame(json.loads((DATA_DIR / "augmented_prompts_v1_200.json").read_text(encoding="utf-8")))
    seed = add_text_lengths(seed, "prompt", "prompt")
    augmented = add_text_lengths(augmented, "prompt", "prompt")

    dataset_overview = pd.DataFrame(
        [
            {
                "dataset": "seed",
                "rows": len(seed),
                "unique_prompts": seed["prompt"].nunique(),
                "duplicate_prompts": int(seed["prompt"].duplicated().sum()),
                "min_prompt_words": int(seed["prompt_word_len"].min()),
                "median_prompt_words": float(seed["prompt_word_len"].median()),
                "max_prompt_words": int(seed["prompt_word_len"].max()),
            },
            {
                "dataset": "augmented",
                "rows": len(augmented),
                "unique_prompts": augmented["prompt"].nunique(),
                "duplicate_prompts": int(augmented["prompt"].duplicated().sum()),
                "min_prompt_words": int(augmented["prompt_word_len"].min()),
                "median_prompt_words": float(augmented["prompt_word_len"].median()),
                "max_prompt_words": int(augmented["prompt_word_len"].max()),
            },
        ]
    )
    dataset_overview.to_csv(EDA_DIR / "dataset_overview.csv", index=False, encoding="utf-8-sig")

    category_attack = pd.crosstab(augmented["category"], augmented["attack_type"])
    category_attack.to_csv(EDA_DIR / "augmented_category_attack_distribution.csv", encoding="utf-8-sig")

    prompt_len_category = (
        augmented.groupby("category")["prompt_word_len"]
        .agg(["count", "min", "median", "mean", "max"])
        .reset_index()
    )
    prompt_len_category.to_csv(EDA_DIR / "prompt_length_by_category.csv", index=False, encoding="utf-8-sig")

    prompt_len_attack = (
        augmented.groupby("attack_type")["prompt_word_len"]
        .agg(["count", "min", "median", "mean", "max"])
        .reset_index()
    )
    prompt_len_attack.to_csv(EDA_DIR / "prompt_length_by_attack_type.csv", index=False, encoding="utf-8-sig")

    longest_prompts = augmented.sort_values("prompt_word_len", ascending=False).head(15)
    longest_prompts[["id", "source", "category", "attack_type", "prompt_word_len", "prompt"]].to_csv(
        EDA_DIR / "longest_augmented_prompts.csv", index=False, encoding="utf-8-sig"
    )

    save_heatmap(
        category_attack,
        "Final Prompt Dataset Distribution by Category and Attack Type",
        EDA_DIR / "eda_augmented_category_attack_heatmap.png",
    )
    save_boxplot(
        augmented,
        "category",
        "prompt_word_len",
        "Prompt Length by Risk Category",
        EDA_DIR / "eda_prompt_length_by_category.png",
    )
    save_boxplot(
        augmented,
        "attack_type",
        "prompt_word_len",
        "Prompt Length by Attack Type",
        EDA_DIR / "eda_prompt_length_by_attack_type.png",
    )

    return seed, augmented


def response_and_judge_eda():
    response_rows = []
    judge_rows = []

    for model in MODELS:
        resp_path = OUTPUT_DIR / f"responses_{model}.csv"
        judge_path = OUTPUT_DIR / f"judgments_{model}.csv"

        if resp_path.exists():
            resp = pd.read_csv(resp_path)
            resp = add_text_lengths(resp, "response", "response")
            response_rows.append(
                {
                    "model": model,
                    "rows": len(resp),
                    "errors": int(resp["error"].fillna("").astype(str).str.len().gt(0).sum()) if "error" in resp else 0,
                    "min_response_words": int(resp["response_word_len"].min()),
                    "median_response_words": float(resp["response_word_len"].median()),
                    "mean_response_words": float(resp["response_word_len"].mean()),
                    "max_response_words": int(resp["response_word_len"].max()),
                }
            )

        if judge_path.exists():
            judge = pd.read_csv(judge_path)
            judge_rows.append(
                {
                    "model": model,
                    "rows": len(judge),
                    "safe": int((judge["judge_label"] == "safe").sum()),
                    "unsafe": int((judge["judge_label"] == "unsafe").sum()),
                    "median_confidence": float(pd.to_numeric(judge["judge_confidence"], errors="coerce").median()),
                    "mean_confidence": float(pd.to_numeric(judge["judge_confidence"], errors="coerce").mean()),
                }
            )

    response_summary = pd.DataFrame(response_rows)
    judge_summary = pd.DataFrame(judge_rows)
    response_summary.to_csv(EDA_DIR / "response_length_summary_by_model.csv", index=False, encoding="utf-8-sig")
    judge_summary.to_csv(EDA_DIR / "judge_label_confidence_summary_by_model.csv", index=False, encoding="utf-8-sig")

    if not response_summary.empty:
        save_bar(
            response_summary.set_index("model")["median_response_words"],
            "Median Response Length by Model",
            "Median words",
            EDA_DIR / "eda_median_response_length_by_model.png",
            rotation=15,
        )

    if not judge_summary.empty:
        save_bar(
            judge_summary.set_index("model")["mean_confidence"],
            "Mean Judge Confidence by Model",
            "Mean confidence",
            EDA_DIR / "eda_judge_confidence_by_model.png",
            rotation=15,
        )


def manual_validation_eda():
    sample_path = OUTPUT_DIR / "manual_validation_stratified_sample.csv"
    metrics_path = OUTPUT_DIR / "manual_validation_metrics.csv"
    if not sample_path.exists():
        return

    sample = pd.read_csv(sample_path)
    sample = sample[
        sample["manual_is_valid"].astype(str).str.lower().eq("true")
        & sample["manual_label"].isin(["safe", "unsafe"])
        & sample["judge_label"].isin(["safe", "unsafe"])
    ].copy()

    if sample.empty:
        return

    confusion = pd.crosstab(sample["judge_label"], sample["manual_label"])
    confusion.to_csv(EDA_DIR / "manual_validation_confusion_matrix.csv", encoding="utf-8-sig")

    by_model = (
        sample.groupby(["model", "judge_label", "manual_label"])
        .size()
        .reset_index(name="count")
    )
    by_model.to_csv(EDA_DIR / "manual_validation_label_pairs_by_model.csv", index=False, encoding="utf-8-sig")

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    image = ax.imshow(confusion.values, cmap="Oranges")
    ax.set_title("Manual Validation Confusion Matrix")
    ax.set_xlabel("Manual label")
    ax.set_ylabel("Judge label")
    ax.set_xticks(range(len(confusion.columns)))
    ax.set_yticks(range(len(confusion.index)))
    ax.set_xticklabels(confusion.columns)
    ax.set_yticklabels(confusion.index)
    for row_idx in range(confusion.shape[0]):
        for col_idx in range(confusion.shape[1]):
            ax.text(col_idx, row_idx, int(confusion.iloc[row_idx, col_idx]), ha="center", va="center")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(EDA_DIR / "eda_manual_validation_confusion_matrix.png", dpi=180)
    plt.close(fig)

    if metrics_path.exists():
        metrics = pd.read_csv(metrics_path)
        metrics.to_csv(EDA_DIR / "manual_validation_metrics_copy.csv", index=False, encoding="utf-8-sig")


def main():
    dataset_eda()
    response_and_judge_eda()
    manual_validation_eda()
    print(f"EDA outputs saved to: {EDA_DIR}")


if __name__ == "__main__":
    main()
