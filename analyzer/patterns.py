TIME_EXPLANATIONS: dict[str, str] = {
    "O(1)": (
        "No loops or recursion detected — every operation executes in "
        "constant time regardless of input size."
    ),
    "O(log n)": (
        "The while loop halves the search space on each iteration "
        "(binary search pattern), giving logarithmic time complexity."
    ),
    "O(n)": (
        "A single loop iterates over the input once, or the function "
        "recurses linearly, giving linear time complexity."
    ),
    "O(n log n)": (
        "A call to .sort() or sorted() is present, which runs in "
        "O(n log n) time."
    ),
    "O(n²)": (
        "Two nested loops each iterate over the input, giving "
        "quadratic time complexity."
    ),
    "O(n³)": (
        "Three nested loops each iterate over the input, giving "
        "cubic time complexity."
    ),
    "O(2^n)": (
        "The function calls itself twice recursively, causing an "
        "exponential number of calls (e.g. naive Fibonacci)."
    ),
}

SPACE_EXPLANATIONS: dict[str, str] = {
    "O(1)": (
        "No additional data structures are allocated proportional "
        "to the input — space usage is constant."
    ),
    "O(n)": (
        "A new collection (list, dict, or set) is constructed from "
        "the input, or recursion adds O(n) frames to the call stack."
    ),
    "O(n²)": (
        "A two-dimensional data structure is constructed proportional "
        "to the square of the input size."
    ),
}
