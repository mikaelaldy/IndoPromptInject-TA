import csv
import subprocess
import sys
import textwrap
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "outputs" / "manual_validation_stratified_sample.csv"
METRICS_SCRIPT = ROOT / "scripts" / "calculate_manual_validation_metrics.ps1"

REQUIRED_COLUMNS = [
    "review_id",
    "model",
    "id",
    "category",
    "attack_type",
    "prompt",
    "response",
    "judge_label",
    "judge_reason",
    "judge_confidence",
    "manual_label",
    "manual_notes",
    "manual_is_valid",
]


class ManualLabelingApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("IndoFinSafety Manual Validation")
        self.root.geometry("1180x760")
        self.root.minsize(980, 640)

        self.rows = []
        self.fieldnames = []
        self.filtered_indices = []
        self.current_pos = 0
        self.current_index = None
        self.dirty = False

        self.filter_var = tk.StringVar(value="Unreviewed")
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.meta_var = tk.StringVar()
        self.judge_var = tk.StringVar()
        self.manual_var = tk.StringVar(value="")

        self._load_rows()
        self._build_ui()
        self._apply_filter()
        self._bind_shortcuts()

    def _load_rows(self):
        if not SAMPLE_PATH.exists():
            messagebox.showerror("File not found", f"Missing sample file:\n{SAMPLE_PATH}")
            raise SystemExit(1)

        with SAMPLE_PATH.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            self.fieldnames = list(reader.fieldnames or [])
            self.rows = list(reader)

        missing = [col for col in REQUIRED_COLUMNS if col not in self.fieldnames]
        if missing:
            messagebox.showerror("Invalid CSV", "Missing columns:\n" + ", ".join(missing))
            raise SystemExit(1)

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        top = ttk.Frame(self.root, padding=(12, 10, 12, 6))
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(4, weight=1)

        ttk.Label(top, text="Filter").grid(row=0, column=0, padx=(0, 6))
        filter_box = ttk.Combobox(
            top,
            textvariable=self.filter_var,
            state="readonly",
            width=18,
            values=["All", "Unreviewed", "Reviewed", "Judge safe", "Judge unsafe", "Disagreements"],
        )
        filter_box.grid(row=0, column=1, padx=(0, 12))
        filter_box.bind("<<ComboboxSelected>>", lambda _event: self._apply_filter())

        ttk.Label(top, text="Search").grid(row=0, column=2, padx=(0, 6))
        search = ttk.Entry(top, textvariable=self.search_var, width=26)
        search.grid(row=0, column=3, padx=(0, 12))
        search.bind("<Return>", lambda _event: self._apply_filter())
        ttk.Button(top, text="Apply", command=self._apply_filter).grid(row=0, column=4, sticky="w")

        ttk.Label(top, textvariable=self.status_var, anchor="e").grid(row=0, column=5, sticky="e")

        meta = ttk.Frame(self.root, padding=(12, 0, 12, 8))
        meta.grid(row=1, column=0, sticky="ew")
        meta.columnconfigure(0, weight=1)
        ttk.Label(meta, textvariable=self.meta_var, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(meta, textvariable=self.judge_var).grid(row=1, column=0, sticky="w", pady=(4, 0))

        panes = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        panes.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 8))

        left = ttk.Frame(panes)
        right = ttk.Frame(panes)
        panes.add(left, weight=1)
        panes.add(right, weight=1)

        self.prompt_text = self._make_text_panel(left, "Prompt", row=0, height=8)
        self.response_text = self._make_text_panel(left, "Model Response", row=1, height=18)
        self.judge_reason_text = self._make_text_panel(right, "Judge Reason", row=0, height=10)
        self.notes_text = self._make_text_panel(right, "Manual Notes", row=1, height=10, editable=True)

        decision = ttk.LabelFrame(right, text="Manual Label", padding=10)
        decision.grid(row=2, column=0, sticky="ew", pady=(8, 0))
        decision.columnconfigure((0, 1, 2), weight=1)

        ttk.Radiobutton(decision, text="Safe", value="safe", variable=self.manual_var).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(decision, text="Unsafe", value="unsafe", variable=self.manual_var).grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(decision, text="Unlabeled", value="", variable=self.manual_var).grid(row=0, column=2, sticky="w")

        controls = ttk.Frame(self.root, padding=(12, 0, 12, 12))
        controls.grid(row=3, column=0, sticky="ew")
        controls.columnconfigure(8, weight=1)

        ttk.Button(controls, text="Prev", command=self.prev_item).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(controls, text="Next", command=self.next_item).grid(row=0, column=1, padx=(0, 16))
        ttk.Button(controls, text="Safe", command=lambda: self.label_current("safe")).grid(row=0, column=2, padx=(0, 6))
        ttk.Button(controls, text="Unsafe", command=lambda: self.label_current("unsafe")).grid(row=0, column=3, padx=(0, 6))
        ttk.Button(controls, text="Skip", command=self.skip_current).grid(row=0, column=4, padx=(0, 16))
        ttk.Button(controls, text="Save", command=self.save_current).grid(row=0, column=5, padx=(0, 6))
        ttk.Button(controls, text="Save + Metrics", command=self.save_and_metrics).grid(row=0, column=6, padx=(0, 6))
        ttk.Button(controls, text="Open CSV Folder", command=self.open_outputs).grid(row=0, column=7, padx=(0, 6))

        help_text = "Shortcuts: S safe, U unsafe, K skip, Ctrl+S save, Left/Right navigate"
        ttk.Label(controls, text=help_text).grid(row=0, column=8, sticky="e")

    def _make_text_panel(self, parent, title, row, height, editable=False):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(row, weight=1)
        frame = ttk.LabelFrame(parent, text=title, padding=8)
        frame.grid(row=row, column=0, sticky="nsew", pady=(0, 8))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        text = tk.Text(frame, wrap="word", height=height, font=("Segoe UI", 10), undo=editable)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        if not editable:
            text.configure(state="disabled", background="#f7f7f7")
        return text

    def _bind_shortcuts(self):
        self.root.bind("<Control-s>", lambda _event: self.save_current())
        self.root.bind("<Left>", lambda _event: self.prev_item())
        self.root.bind("<Right>", lambda _event: self.next_item())
        self.root.bind("s", lambda _event: self.label_current("safe"))
        self.root.bind("u", lambda _event: self.label_current("unsafe"))
        self.root.bind("k", lambda _event: self.skip_current())

    def _apply_filter(self):
        self._store_current_to_memory()
        query = self.search_var.get().strip().lower()
        mode = self.filter_var.get()
        indices = []

        for idx, row in enumerate(self.rows):
            manual_valid = row.get("manual_is_valid", "").strip().lower() == "true"
            judge_label = row.get("judge_label", "").strip().lower()
            manual_label = row.get("manual_label", "").strip().lower()

            if mode == "Unreviewed" and manual_valid:
                continue
            if mode == "Reviewed" and not manual_valid:
                continue
            if mode == "Judge safe" and judge_label != "safe":
                continue
            if mode == "Judge unsafe" and judge_label != "unsafe":
                continue
            if mode == "Disagreements" and (not manual_valid or judge_label == manual_label):
                continue

            haystack = " ".join(
                str(row.get(col, "")) for col in ["review_id", "model", "id", "category", "attack_type", "prompt", "response"]
            ).lower()
            if query and query not in haystack:
                continue
            indices.append(idx)

        self.filtered_indices = indices
        self.current_pos = 0
        self._show_current()

    def _show_current(self):
        if not self.filtered_indices:
            self.current_index = None
            self.meta_var.set("No rows match the current filter.")
            self.judge_var.set("")
            self.status_var.set(self._progress_text())
            self._set_text(self.prompt_text, "")
            self._set_text(self.response_text, "")
            self._set_text(self.judge_reason_text, "")
            self.notes_text.delete("1.0", "end")
            self.manual_var.set("")
            return

        self.current_pos = max(0, min(self.current_pos, len(self.filtered_indices) - 1))
        self.current_index = self.filtered_indices[self.current_pos]
        row = self.rows[self.current_index]

        self.meta_var.set(
            f"{row.get('review_id')} | {row.get('model')} | {row.get('id')} | "
            f"{row.get('category')} | {row.get('attack_type')}"
        )
        self.judge_var.set(
            f"Judge: {row.get('judge_label')} | confidence: {row.get('judge_confidence')} | "
            f"Manual: {row.get('manual_label') or '-'} | valid: {row.get('manual_is_valid')}"
        )
        self.status_var.set(self._progress_text())
        self.manual_var.set(row.get("manual_label", "").strip().lower())
        self._set_text(self.prompt_text, row.get("prompt", ""))
        self._set_text(self.response_text, row.get("response", ""))
        self._set_text(self.judge_reason_text, row.get("judge_reason", ""))
        self.notes_text.delete("1.0", "end")
        self.notes_text.insert("1.0", row.get("manual_notes", ""))

    def _set_text(self, widget, value):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value or "")
        widget.configure(state="disabled")

    def _store_current_to_memory(self):
        if self.current_index is None:
            return
        row = self.rows[self.current_index]
        row["manual_label"] = self.manual_var.get().strip().lower()
        row["manual_notes"] = self.notes_text.get("1.0", "end").strip()

    def _progress_text(self):
        reviewed = sum(1 for row in self.rows if row.get("manual_is_valid", "").strip().lower() == "true")
        total = len(self.rows)
        shown = len(self.filtered_indices)
        pos = self.current_pos + 1 if shown else 0
        return f"Reviewed {reviewed}/{total} | Showing {pos}/{shown}"

    def _write_csv(self):
        self._store_current_to_memory()
        with SAMPLE_PATH.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.rows)
        self.dirty = False
        self.status_var.set(self._progress_text() + " | Saved")

    def save_current(self):
        self._write_csv()

    def label_current(self, label):
        if self.current_index is None:
            return
        self.manual_var.set(label)
        row = self.rows[self.current_index]
        row["manual_label"] = label
        row["manual_notes"] = self.notes_text.get("1.0", "end").strip()
        row["manual_is_valid"] = "True"
        self._write_csv()
        self.next_item()

    def skip_current(self):
        if self.current_index is None:
            return
        self._store_current_to_memory()
        self._write_csv()
        self.next_item()

    def prev_item(self):
        self._store_current_to_memory()
        if self.current_pos > 0:
            self.current_pos -= 1
        self._show_current()

    def next_item(self):
        self._store_current_to_memory()
        if self.current_pos < len(self.filtered_indices) - 1:
            self.current_pos += 1
        self._show_current()

    def save_and_metrics(self):
        self._write_csv()
        if not METRICS_SCRIPT.exists():
            messagebox.showwarning("Metrics script missing", f"Cannot find:\n{METRICS_SCRIPT}")
            return

        try:
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(METRICS_SCRIPT),
                ],
                cwd=str(ROOT),
                text=True,
                capture_output=True,
                check=True,
            )
        except Exception as exc:
            messagebox.showerror("Metrics failed", str(exc))
            return

        message = result.stdout.strip() or "Metrics updated."
        messagebox.showinfo("Saved", "\n".join(textwrap.wrap(message, width=90)))

    def open_outputs(self):
        subprocess.Popen(["explorer", str(SAMPLE_PATH.parent)])


def main():
    root = tk.Tk()
    try:
        ttk.Style().theme_use("vista")
    except tk.TclError:
        pass
    ManualLabelingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
