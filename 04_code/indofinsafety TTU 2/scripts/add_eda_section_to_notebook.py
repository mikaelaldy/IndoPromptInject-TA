import json
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "indofinsafety.ipynb"
MARKER = "## Section 9 - Additional EDA for Dataset, Responses, and Manual Validation"


def md_cell(text: str) -> dict:
    text = textwrap.dedent(text).strip()
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.splitlines()],
    }


def code_cell(code: str) -> dict:
    code = textwrap.dedent(code).strip()
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.splitlines()],
    }


def main():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    all_source = "\n".join("".join(cell.get("source", [])) for cell in nb.get("cells", []))
    if MARKER in all_source:
        for cell in nb.get("cells", []):
            source = "".join(cell.get("source", []))
            if MARKER in source or "# Section 9 - Additional EDA outputs" in source:
                fixed_lines = []
                for line in source.splitlines():
                    if line.startswith("            "):
                        fixed_lines.append(line[12:])
                    else:
                        fixed_lines.append(line)
                fixed = textwrap.dedent("\n".join(fixed_lines)).strip()
                cell["source"] = [line + "\n" for line in fixed.splitlines()]
        NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        print("EDA section already exists; repaired indentation.")
        return

    nb["cells"].append(
        md_cell(
            """
            ## Section 9 - Additional EDA for Dataset, Responses, and Manual Validation

            Bagian ini melengkapi EDA yang sudah ada dengan pemeriksaan kualitas dataset, distribusi panjang prompt, panjang respons model, confidence judge, dan hasil validasi manual. Output disimpan ke folder `outputs/eda` agar dapat digunakan langsung untuk TTU 2 dan TTU 3.
            """
        )
    )

    nb["cells"].append(
        code_cell(
            """
            # Section 9 - Additional EDA outputs
            import subprocess
            import sys
            from pathlib import Path

            import pandas as pd
            from IPython.display import Image, Markdown, display

            eda_script = PROJECT_DIR / "scripts" / "generate_eda_outputs.py"
            subprocess.check_call([sys.executable, str(eda_script)])

            EDA_DIR = OUTPUT_DIR / "eda"

            display(Markdown("### Dataset Overview"))
            display(pd.read_csv(EDA_DIR / "dataset_overview.csv"))

            display(Markdown("### Final Prompt Distribution by Category x Attack Type"))
            display(pd.read_csv(EDA_DIR / "augmented_category_attack_distribution.csv"))
            display(Image(filename=str(EDA_DIR / "eda_augmented_category_attack_heatmap.png")))

            display(Markdown("### Prompt Length EDA"))
            display(pd.read_csv(EDA_DIR / "prompt_length_by_category.csv"))
            display(pd.read_csv(EDA_DIR / "prompt_length_by_attack_type.csv"))
            display(Image(filename=str(EDA_DIR / "eda_prompt_length_by_category.png")))
            display(Image(filename=str(EDA_DIR / "eda_prompt_length_by_attack_type.png")))

            display(Markdown("### Response and Judge EDA"))
            display(pd.read_csv(EDA_DIR / "response_length_summary_by_model.csv"))
            display(pd.read_csv(EDA_DIR / "judge_label_confidence_summary_by_model.csv"))
            display(Image(filename=str(EDA_DIR / "eda_median_response_length_by_model.png")))
            display(Image(filename=str(EDA_DIR / "eda_judge_confidence_by_model.png")))

            manual_confusion = EDA_DIR / "manual_validation_confusion_matrix.csv"
            if manual_confusion.exists():
                display(Markdown("### Manual Validation EDA"))
                display(pd.read_csv(EDA_DIR / "manual_validation_metrics_copy.csv"))
                display(pd.read_csv(manual_confusion))
                display(Image(filename=str(EDA_DIR / "eda_manual_validation_confusion_matrix.png")))
            """
        )
    )

    NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Added EDA section to notebook.")


if __name__ == "__main__":
    main()
