"""Check that an executed notebook actually reproduced its headline results.

`jupyter nbconvert --execute` already fails when a cell raises, so this script
covers the quieter failure mode: a notebook that runs to completion but whose
numbers have silently drifted, for example because a preprocessing step stopped
doing anything on a newer pandas.

The checks are deliberately threshold-based rather than exact. On the committed
seed the top models are separated by very little (Lasso beats Elastic Net by
0.0006 R2, Logistic Regression beats Gradient Boosting by 0.0035 F1), so
asserting *which* model wins would make CI fail on harmless floating-point
tie-breaking between library versions. Asserting that the winning score is still
in the right band catches real regressions without the false alarms.

Used by .github/workflows/validate-notebook.yml.
"""

import json
import re
import sys


def notebook_stdout(path):
    """Return the notebook's combined text output, exiting if a cell errored."""
    with open(path, encoding="utf-8") as handle:
        notebook = json.load(handle)

    chunks = []
    for index, cell in enumerate(notebook["cells"]):
        for output in cell.get("outputs", []):
            kind = output.get("output_type")
            if kind == "error":
                sys.exit(
                    "FAIL: cell {} raised {}: {}".format(
                        index, output.get("ename"), output.get("evalue")
                    )
                )
            if kind == "stream":
                chunks.append("".join(output.get("text", [])))
            elif kind == "execute_result":
                chunks.append("".join(output.get("data", {}).get("text/plain", [])))
    return "\n".join(chunks)


def find(text, pattern, description, results):
    """Record whether `pattern` appears at all."""
    if re.search(pattern, text):
        results.append((True, description, "found"))
    else:
        results.append((False, description, "not found"))


def find_number(text, pattern, description, low, high, results):
    """Record whether the number captured by `pattern` falls within [low, high]."""
    match = re.search(pattern, text)
    if not match:
        results.append((False, description, "value not found in output"))
        return
    value = float(match.group(1))
    ok = low <= value <= high
    results.append((ok, description, "{:.4f} (expected {}-{})".format(value, low, high)))


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: check_results.py <executed-notebook.ipynb>")

    text = notebook_stdout(sys.argv[1])
    results = []

    # Structural: the data actually loaded and preprocessing produced features.
    find(text, r"Dataset cargado desde .*rendimiento_estudiantes\.csv",
         "dataset located and loaded", results)
    find(text, r"4424 filas x 37 columnas",
         "dataset has 4424 rows and 37 columns", results)
    find_number(text, r"Train: \d+ muestras, (\d+) features",
                "encoded feature count", 80, 130, results)

    # Task 1: classification.
    find_number(text, r"=> Mejor modelo: .+ \(F1 = ([\d.]+)\)",
                "best classifier weighted F1", 0.72, 0.82, results)

    # Task 2: regression, reported separately at the end of the notebook.
    find_number(text, r"R2 en test: ([\d.]+)",
                "best regressor R2", 0.68, 0.82, results)

    # Early-warning comparison: proves the leakage-free rerun happened.
    find_number(text, r"Modelo solo con info previa al 1er sem: F1 = ([\d.]+)",
                "early-warning F1 (pre-first-semester features only)",
                0.56, 0.70, results)

    # Task 3: clustering. K = 3 wins by a comfortable margin, so assert it.
    find(text, r"K elegido \(maxima silueta\): 3 ",
         "clustering selects K = 3", results)
    find_number(text, r"K elegido \(maxima silueta\): 3 \(silueta = ([\d.]+)\)",
                "K-Means silhouette", 0.25, 0.40, results)
    find_number(text, r"ARI medio:\s+([\d.]+)",
                "cluster stability, mean subsampling ARI", 0.90, 1.0, results)

    # The notebook ran all the way to its last cell.
    find(text, r"PROYECTO FINALIZADO", "notebook reached its final cell", results)

    for ok, description, detail in results:
        print("  {}  {} -> {}".format("ok  " if ok else "FAIL", description, detail))

    failures = [description for ok, description, _ in results if not ok]
    if failures:
        sys.exit("\n{} of {} checks failed.".format(len(failures), len(results)))

    print("\nAll {} checks passed.".format(len(results)))


if __name__ == "__main__":
    main()
