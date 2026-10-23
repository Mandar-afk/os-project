"""Run a page-replacement simulation and return a trace plus metrics."""
from collections import Counter
from algorithms import choose_victim

POLICIES = ("FIFO", "LRU", "Optimal", "AF-LRU")

def run_simulation(references, frame_count, policy):
    if frame_count < 1:
        raise ValueError("frame_count must be at least 1")
    if not references:
        raise ValueError("references must not be empty")

    policy_key = policy.upper()
    frames = []
    trace = []
    last_used = {}
    frequencies = Counter()
    load_order = {}
    hits = faults = 0

    for index, page in enumerate(references):
        frequencies[page] += 1
        evicted = None

        if page in frames:
            hits += 1
            status = "HIT"
        else:
            faults += 1
            status = "FAULT"
            if len(frames) < frame_count:
                frames.append(page)
                load_order[page] = index
            else:
                evicted = choose_victim(
                    policy_key, frames, references, index,
                    last_used, frequencies, load_order
                )
                slot = frames.index(evicted)
                frames[slot] = page
                load_order.pop(evicted, None)
                load_order[page] = index

        last_used[page] = index
        trace.append({
            "request": page,
            "frames": frames.copy(),
            "status": status,
            "evicted": evicted,
        })

    total = len(references)
    return {
        "policy": policy,
        "trace": trace,
        "hits": hits,
        "faults": faults,
        "hit_ratio": hits / total,
        "fault_ratio": faults / total,
        "total_references": total,
    }
