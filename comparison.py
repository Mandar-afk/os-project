"""Command-line comparison of FIFO, LRU, Optimal, and AF-LRU."""
from input_module import get_user_input
from simulation import run_simulation, POLICIES

def print_trace(name, result):
    print(f"\n--- {name} trace ---")
    print(" Request | Frames after request | Status | Evicted")
    print("-" * 58)
    for row in result["trace"]:
        evicted = "-" if row["evicted"] is None else row["evicted"]
        print(f'{row["request"]:>8} | {str(row["frames"]):<21} | {row["status"]:<6} | {evicted}')

def main():
    print("PAGE REPLACEMENT ALGORITHM COMPARISON\n")
    print("Algorithms: FIFO, LRU, Optimal, and proposed AF-LRU\n")
    references, frame_count = get_user_input()
    results = {}
    for policy in POLICIES:
        result = run_simulation(references, frame_count, policy)
        results[policy] = result
        print_trace(policy, result)

    print("\n=== PERFORMANCE COMPARISON ===")
    print(f'{"Algorithm":<12} {"Faults":>7} {"Hits":>7} {"Hit ratio":>12} {"Fault ratio":>12}')
    print("-" * 55)
    for policy, result in results.items():
        print(f'{policy:<12} {result["faults"]:>7} {result["hits"]:>7} {result["hit_ratio"]:>11.2%} {result["fault_ratio"]:>11.2%}')
    best = min(results, key=lambda p: results[p]["faults"])
    print(f"\nFewest page faults for this input: {best} ({results[best]['faults']} faults)")
    print("Optimal is a theoretical benchmark; AF-LRU is a heuristic and may not always beat LRU.")

if __name__ == "__main__":
    main()
