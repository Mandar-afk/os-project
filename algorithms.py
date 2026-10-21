def choose_victim(algorithm, frames, references, current_index,
                  last_used, frequency, loaded_at):
    if algorithm == "FIFO":
        return min(range(len(frames)), key=lambda i: loaded_at[frames[i]])

    if algorithm == "LRU":
        return min(range(len(frames)), key=lambda i: last_used[frames[i]])

    if algorithm == "Optimal":
        
        def next_use(page):
            try:
                return references.index(page, current_index + 1)
            except ValueError:
                return float("inf")
        return max(range(len(frames)), key=lambda i: next_use(frames[i]))

    if algorithm == "AF-LRU":
        
        def score(page):
            age = current_index - last_used[page]
            recency_score = age / max(1, current_index + 1)
            low_frequency_score = 1 / (1 + frequency[page])
            alpha, beta = 0.5, 0.5
            return alpha * recency_score + beta * low_frequency_score
        return max(range(len(frames)), key=lambda i: score(frames[i]))

    raise ValueError(f"Unknown algorithm: {algorithm}")
