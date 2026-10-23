def get_user_input():
    """Read and validate a page-reference string and frame count."""
    while True:
        raw = input("Enter page reference string (space-separated): ").strip()
        try:
            references = [int(x) for x in raw.split()]
            if references:
                break
            print("Please enter at least one page reference.")
        except ValueError:
            print("Use integers separated by spaces.")

    while True:
        try:
            frames = int(input("Enter number of memory frames: ").strip())
            if frames > 0:
                return references, frames
            print("Number of frames must be greater than zero.")
        except ValueError:
            print("Enter a positive integer.")
