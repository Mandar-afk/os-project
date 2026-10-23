"""Victim-selection policies for page replacement."""
from collections import Counter

def choose_victim(policy, frames, references, current_index, last_used, frequencies, load_order):
    """Return the page to evict. Called only when memory is full."""
    policy = policy.upper()

    if policy == "FIFO":
        return min(frames, key=lambda page: load_order[page])

    if policy == "LRU":
        return min(frames, key=lambda page: last_used[page])

    if policy == "OPTIMAL":
        future = references[current_index + 1:]
        next_use = {}
        for page in frames:
            try:
                next_use[page] = future.index(page)
            except ValueError:
                next_use[page] = float("inf")
        return max(frames, key=lambda page: next_use[page])

    if policy == "AF-LRU":
        # Higher score means a better eviction candidate.
        # Normalize recency and inverse frequency within the current frame set.
        ages = {page: current_index - last_used[page] for page in frames}
        max_age = max(ages.values()) or 1
        max_frequency = max(frequencies[page] for page in frames) or 1
        scores = {}
        for page in frames:
            recency_score = ages[page] / max_age
            frequency_score = 1 - (frequencies[page] / max_frequency)
            scores[page] = 0.5 * recency_score + 0.5 * frequency_score
        return max(frames, key=lambda page: (scores[page], -last_used[page]))

    raise ValueError(f"Unknown policy: {policy}")
