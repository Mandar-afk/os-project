"""Performance metrics including elapsed execution time."""
from time import perf_counter
from simulation import run_simulation, POLICIES

def measure_policy(references, frame_count, policy):
    start = perf_counter()
    result = run_simulation(references, frame_count, policy)
    elapsed = perf_counter() - start
    result["execution_time_ms"] = elapsed * 1000
    return result

def compare_performance(references, frame_count):
    return {
        policy: measure_policy(references, frame_count, policy)
        for policy in POLICIES
    }
