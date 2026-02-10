from __future__ import annotations
import pandas as pd

def main(out_dir: str = "outputs") -> None:
    df = pd.read_csv(f"{out_dir}/benchmark_results.csv")
    acc = pd.read_csv(f"{out_dir}/prediction_accuracy.csv")

    summary = (
        df.groupby(["ds", "op", "expected"])
          .agg(min_time=("seconds", "min"), max_time=("seconds", "max"))
          .reset_index()
          .sort_values(["ds", "op"])
    )

    overall_acc = acc["match"].mean()

    md = []
    md.append("# Performance Comparison Report\n")
    md.append("## What was tested\n")
    md.append("Operations were executed across increasing input sizes (n). Median runtime was used to reduce noise.\n")
    md.append("## Summary table (min/max measured time)\n")
    md.append(summary.to_markdown(index=False))
    md.append("\n## Prediction accuracy\n")
    md.append(acc.to_markdown(index=False))
    md.append(f"\n**Overall accuracy:** {overall_acc:.2%}\n")
    md.append("\n## Charts generated\n")
    md.append("- outputs/chart_stack.png\n- outputs/chart_queue.png\n- outputs/chart_linkedlist.png\n- outputs/accuracy_overview.png\n")

    with open(f"{out_dir}/report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"Wrote {out_dir}/report.md")

if __name__ == "__main__":
    main()
