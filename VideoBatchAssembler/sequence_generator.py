import os
import random
from pathlib import Path

# ===== SETTINGS =====
video_dir = Path("./clips")   # folder with split video files
output_dir = Path("./sequences")  # folder to save sequence txt files
seed_value = 42               # seed for random pattern

output_dir.mkdir(exist_ok=True)

# ===== HELPER FUNCTIONS =====

def alternating_ends(lst):
    left, right = 0, len(lst) - 1
    order = []
    turn_left = True
    while left <= right:
        if turn_left:
            order.append(lst[left]); left += 1
        else:
            order.append(lst[right]); right -= 1
        turn_left = not turn_left
    return order

def endcaps_middle(lst):
    left, right = 0, len(lst) - 1
    order = []
    while left < right:
        order.append(lst[left]); order.append(lst[right])
        left += 1; right -= 1
    if left == right:
        order.append(lst[left])
    return order

def fibonacci_first(lst):
    fib = [1, 2]
    while fib[-1] + fib[-2] <= len(lst):
        fib.append(fib[-1] + fib[-2])
    fib_set = {f-1 for f in fib if 1 <= f <= len(lst)}
    fib_list = [lst[i] for i in sorted(fib_set)]
    rest = [lst[i] for i in range(len(lst)) if i not in fib_set]
    return fib_list + rest

def write_concat_file(name, sequence):
    with open(output_dir / f"{name}.txt", "w", encoding="utf-8") as f:
        for clip in sequence:
            f.write(f"file '{clip}'\n")

# ===== MAIN =====

video_files = sorted(video_dir.glob("*.*"), key=lambda x: x.name)
video_files_str = [str(f.name) for f in video_files]  # Only names for portability

patterns = {
    "reverse": list(reversed(video_files_str)),
    "alternating_ends": alternating_ends(video_files_str),
    "endcaps_middle": endcaps_middle(video_files_str),
    "fibonacci_first": fibonacci_first(video_files_str),
}

random.seed(seed_value)
rand_list = video_files_str.copy()
random.shuffle(rand_list)
patterns["random_seed"] = rand_list

for name, seq in patterns.items():
    write_concat_file(name, seq)

print(f"Generated {len(patterns)} concat sequence files in {output_dir}")
