from input_module import get_user_input
from simulation import ALGORITHMS, run_simulation

def print_trace(result):
    print(f"--- {result['algorithm']} trace ---")
    print(f"{'Request':>8} | {'Frames after request':<24} | {'Status':<6} | {'Evicted':>7}")
    print("-" * 59)
    for row in result["trace"]:
        evicted = "-" if row["evicted"] is None else str(row["evicted"])
        print(f"{row['request']:>8} | {str(row['frames']):<24} | {row['status']:<6} | {evicted:>7}")

def main():
    print("\nPAGE REPLACEMENT ALGORITHM COMPARISON")
    print("\nAlgorithms: FIFO, LRU, Optimal, and proposed AF-LRU\\n")
    references, frame_count = get_user_input()
    results = [run_simulation(references, frame_count, name) for name in ALGORITHMS]

    for result in results:
        print_trace(result)

    print("\n=== PERFORMANCE COMPARISON ===")
    print(f"{'Algorithm':<12} {'Faults':>8} {'Hits':>8} {'Hit ratio':>12} {'Fault ratio':>12}")
    print("-" * 56)
    for result in results:
        print(f"{result['algorithm']:<12} {result['faults']:>8} {result['hits']:>8} "
              f"{result['hit_ratio'] * 100:>11.2f}% {result['fault_ratio'] * 100:>11.2f}%")

    best = min(results, key=lambda item: item["faults"])
    print(f"\nFewest page faults for this input: {best['algorithm']} ({best['faults']} faults)")
    print("Optimal is a theoretical benchmark; AF-LRU is a heuristic and may not always beat LRU.")

if __name__ == "__main__":
    main()
