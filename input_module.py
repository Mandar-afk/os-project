def get_user_input():
    while True:
        raw = input("Enter page reference string (space-separated) ").strip()
        try:
            references = [int(x) for x in raw.replace(",", " ").split()]
            if references:
                break
        except ValueError:
            pass
        print("Enter one or more integer page numbers.")

    while True:
        try:
            frame_count = int(input("Enter number of memory frames: ").strip())
            if frame_count > 0:
                break
        except ValueError:
            pass
        print("Frame count must be a positive integer.")
    return references, frame_count
