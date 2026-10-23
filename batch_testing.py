"""Run repeatable workloads across multiple frame counts."""
import csv
from performance import compare_performance

WORKLOADS = {
    "mixed_small": [1, 2, 3, 2, 4, 1, 3, 4],
    "repeated_locality": [1, 2, 1, 2, 3, 1, 2, 1, 4, 1, 2, 3],
    "sequential": [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4],
    "looping": [1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3],
    "longer_mixed": [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2],
}
FRAME_COUNTS = [2, 3, 4]

def run_batch(workloads=None, frame_counts=None, output_csv="batch_results.csv"):
    workloads = workloads or WORKLOADS
    frame_counts = frame_counts or FRAME_COUNTS
    rows = []

    for workload_name, references in workloads.items():
        for frame_count in frame_counts:
            results = compare_performance(references, frame_count)
            for policy, result in results.items():
                rows.append({
                    "workload": workload_name,
                    "reference_string": " ".join(map(str, references)),
                    "frame_count": frame_count,
                    "algorithm": policy,
                    "page_faults": result["faults"],
                    "page_hits": result["hits"],
                    "hit_ratio": round(result["hit_ratio"], 6),
                    "fault_ratio": round(result["fault_ratio"], 6),
                    "execution_time_ms": round(result["execution_time_ms"], 6),
                })

    with open(output_csv, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Completed {len(rows)} algorithm runs.")
    print(f"Saved results to: {output_csv}")
    print("\nSample results:")
    print(f'{"Workload":<18} {"Frames":>6} {"Algorithm":<10} {"Faults":>7} {"Hits":>6} {"Time (ms)":>12}')
    print("-" * 65)
    for row in rows[:min(20, len(rows))]:
        print(f'{row["workload"]:<18} {row["frame_count"]:>6} {row["algorithm"]:<10} {row["page_faults"]:>7} {row["page_hits"]:>6} {row["execution_time_ms"]:>12.4f}')
    return rows

if __name__ == "__main__":
    run_batch()
