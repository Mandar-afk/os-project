from algorithms import choose_victim

ALGORITHMS = ("FIFO", "LRU", "Optimal", "AF-LRU")

def run_simulation(references, frame_count, algorithm):
    frames = []
    last_used = {}
    frequency = {}
    loaded_at = {}
    trace = []
    hits = faults = 0

    for index, page in enumerate(references):
        frequency[page] = frequency.get(page, 0) + 1
        evicted = None

        if page in frames:
            hits += 1
            status = "HIT"
        else:
            faults += 1
            status = "FAULT"
            if len(frames) < frame_count:
                frames.append(page)
            else:
                victim_index = choose_victim(
                    algorithm, frames, references, index,
                    last_used, frequency, loaded_at
                )
                evicted = frames[victim_index]
                frames[victim_index] = page
            loaded_at[page] = index

        last_used[page] = index
        trace.append({
            "request": page,
            "frames": frames.copy(),
            "status": status,
            "evicted": evicted
        })

    total = len(references)
    return {
        "algorithm": algorithm,
        "trace": trace,
        "hits": hits,
        "faults": faults,
        "total": total,
        "hit_ratio": hits / total if total else 0,
        "fault_ratio": faults / total if total else 0
    }
