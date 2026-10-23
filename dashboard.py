"""Generate charts from automated batch results."""
import os
import pandas as pd
import matplotlib.pyplot as plt
from batch_testing import run_batch

RESULTS_FILE = "batch_results.csv"
OUTPUT_DIR = "charts"

def main():
    if not os.path.exists(RESULTS_FILE):
        run_batch(output_csv=RESULTS_FILE)

    data = pd.read_csv(RESULTS_FILE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Chart 1: page faults by algorithm, averaged over workloads for each frame count.
    summary = data.groupby(["frame_count", "algorithm"], as_index=False)["page_faults"].mean()
    pivot = summary.pivot(index="frame_count", columns="algorithm", values="page_faults")
    ax = pivot.plot(kind="bar", figsize=(10, 6))
    ax.set_title("Average Page Faults by Algorithm and Frame Count")
    ax.set_xlabel("Number of Frames")
    ax.set_ylabel("Average Page Faults")
    ax.legend(title="Algorithm")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "average_page_faults.png"), dpi=160)
    plt.close()

    # Chart 2: average hit ratio.
    summary = data.groupby("algorithm", as_index=False)["hit_ratio"].mean()
    ax = summary.plot(kind="bar", x="algorithm", y="hit_ratio", legend=False, figsize=(8, 5))
    ax.set_title("Average Hit Ratio Across Workloads")
    ax.set_xlabel("Algorithm")
    ax.set_ylabel("Average Hit Ratio")
    ax.set_ylim(0, 1)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "average_hit_ratio.png"), dpi=160)
    plt.close()

    # Chart 3: timing is noisy at small workload sizes; present as a measured average.
    summary = data.groupby("algorithm", as_index=False)["execution_time_ms"].mean()
    ax = summary.plot(kind="bar", x="algorithm", y="execution_time_ms", legend=False, figsize=(8, 5))
    ax.set_title("Average Simulation Execution Time")
    ax.set_xlabel("Algorithm")
    ax.set_ylabel("Time (milliseconds)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "average_execution_time.png"), dpi=160)
    plt.close()

    print("Dashboard charts generated in the 'charts' folder:")
    print(" - charts/average_page_faults.png")
    print(" - charts/average_hit_ratio.png")
    print(" - charts/average_execution_time.png")
    print("Note: execution times for small inputs are highly sensitive to system noise.")

if __name__ == "__main__":
    main()
