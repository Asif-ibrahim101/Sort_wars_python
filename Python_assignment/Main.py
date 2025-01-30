import sys
import numpy as np
import time
import psutil
import os
import matplotlib.pyplot as plt  # for plotting graphs

# Setting recursion limit to handle large arrays
sys.setrecursionlimit(10**6)

# Create a directory to store the sorted files
output_directory = "sorting_results"
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Function to save the sorted arrays to files
def save_sorted_array(array, algorithm, array_type, size):
    filename = f"{algorithm}_{array_type}_{size}.txt"
    filepath = os.path.join(output_directory, filename)
    np.savetxt(filepath, array, fmt='%d')
    print(f"Saved sorted array to {filepath}")

# Generate an array of random numbers between 100000 and 999999
def generate_random_numbers(size):
    return np.random.randint(100000, 1000000, size=size)

# Generate an array of reversed sequential numbers starting from 100000
def generate_reversed_numbers(size):
    numbers = np.arange(100000, 100000 + size)
    return numbers[::-1]  # Reverse the order to get descending data

# Merge Sort with comparison counter
def merge_sort(array):
    comparisons = [0]

    def sort(array):
        if len(array) <= 1:
            return array.copy()
        mid = len(array) // 2
        left = sort(array[:mid])
        right = sort(array[mid:])
        return merge(left, right)

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return np.array(result)

    sorted_array = sort(array)
    return sorted_array, comparisons[0]

# Quick Sort with comparison counter
def quick_sort(array):
    comparisons = [0]

    def partition(array, left, right):
        random_idx = np.random.randint(left, right + 1)
        array[random_idx], array[right] = array[right], array[random_idx]
        pivot = array[right]
        i = left - 1
        for j in range(left, right):
            comparisons[0] += 1
            if array[j] <= pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
        array[i + 1], array[right] = array[right], array[i + 1]
        return i + 1

    def sort(array, low, high):
        if low < high:
            pi = partition(array, low, high)
            sort(array, low, pi - 1)
            sort(array, pi + 1, high)

    array_copy = array.copy()
    sort(array_copy, 0, len(array_copy) - 1)
    return array_copy, comparisons[0]

# Get the current memory usage of the system in KB
def get_memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / 1024

# Initialize lists to store metrics for plotting
merge_sort_random_times = []
quick_sort_random_times = []

merge_sort_reversed_times = []
quick_sort_reversed_times = []

merge_sort_random_memories = []
quick_sort_random_memories = []

merge_sort_reversed_memories = []
quick_sort_reversed_memories = []

merge_sort_random_comparisons = []
quick_sort_random_comparisons = []

merge_sort_reversed_comparisons = []
quick_sort_reversed_comparisons = []

# Test with different array sizes
sizes = [10000, 100000]

for size in sizes:
    print(f"\nTesting arrays of size {size}")

    # Generate the arrays
    random_array = generate_random_numbers(size)
    reversed_array = generate_reversed_numbers(size)

    # --- Merge Sort for Random Array ---
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_random, comparisons = merge_sort(random_array)
    memory_used = get_memory_usage() - start_memory
    time_taken = time.time() - start_time

    merge_sort_random_times.append(time_taken)
    merge_sort_random_memories.append(memory_used)
    merge_sort_random_comparisons.append(comparisons)
    save_sorted_array(sorted_random, "merge_sort", "random", size)

    # --- Merge Sort for Reversed Array ---
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_reversed, comparisons = merge_sort(reversed_array)
    memory_used = get_memory_usage() - start_memory
    time_taken = time.time() - start_time

    merge_sort_reversed_times.append(time_taken)
    merge_sort_reversed_memories.append(memory_used)
    merge_sort_reversed_comparisons.append(comparisons)
    save_sorted_array(sorted_reversed, "merge_sort", "reversed", size)

    # --- Quick Sort for Random Array ---
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_random, comparisons = quick_sort(random_array)
    memory_used = get_memory_usage() - start_memory
    time_taken = time.time() - start_time

    quick_sort_random_times.append(time_taken)
    quick_sort_random_memories.append(memory_used)
    quick_sort_random_comparisons.append(comparisons)
    save_sorted_array(sorted_random, "quick_sort", "random", size)

    # --- Quick Sort for Reversed Array ---
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_reversed, comparisons = quick_sort(reversed_array)
    memory_used = get_memory_usage() - start_memory
    time_taken = time.time() - start_time

    quick_sort_reversed_times.append(time_taken)
    quick_sort_reversed_memories.append(memory_used)
    quick_sort_reversed_comparisons.append(comparisons)
    save_sorted_array(sorted_reversed, "quick_sort", "reversed", size)

# Plotting the Metrics
plt.figure(figsize=(15, 15))

# Time Plot
plt.subplot(2, 3, 1)
plt.plot(sizes, merge_sort_random_times, marker='o', label='Merge Sort (Random)')
plt.plot(sizes, merge_sort_reversed_times, marker='o', label='Merge Sort (Reversed)')
plt.plot(sizes, quick_sort_random_times, marker='o', label='Quick Sort (Random)')
plt.plot(sizes, quick_sort_reversed_times, marker='o', label='Quick Sort (Reversed)')
plt.title("Time Complexity")
plt.xlabel("Array Size")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid()

# Memory Plot
plt.subplot(2, 3, 2)
plt.plot(sizes, merge_sort_random_memories, marker='o', label='Merge Sort (Random)')
plt.plot(sizes, merge_sort_reversed_memories, marker='o', label='Merge Sort (Reversed)')
plt.plot(sizes, quick_sort_random_memories, marker='o', label='Quick Sort (Random)')
plt.plot(sizes, quick_sort_reversed_memories, marker='o', label='Quick Sort (Reversed)')
plt.title("Memory Usage")
plt.xlabel("Array Size")
plt.ylabel("Memory (KB)")
plt.legend()
plt.grid()

# Comparisons Plot
plt.subplot(2, 3, 3)
plt.plot(sizes, merge_sort_random_comparisons, marker='o', label='Merge Sort (Random)')
plt.plot(sizes, merge_sort_reversed_comparisons, marker='o', label='Merge Sort (Reversed)')
plt.plot(sizes, quick_sort_random_comparisons, marker='o', label='Quick Sort (Random)')
plt.plot(sizes, quick_sort_reversed_comparisons, marker='o', label='Quick Sort (Reversed)')
plt.title("Number of Comparisons")
plt.xlabel("Array Size")
plt.ylabel("Comparisons")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
