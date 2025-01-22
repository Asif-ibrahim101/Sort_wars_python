import sys
import numpy as np
import time
import psutil
import os
import matplotlib.pyplot as plt #for the graph

# Setting recursion limit
sys.setrecursionlimit(10**6)

# Making a dirrectory to store the sorted files
output_dirrectory = "sorting_results"
if not os.path.exists(output_dirrectory):
    os.mkdir(output_dirrectory)

# function to save the arrays
def save_sorted_array(arr, algorith, arr_type, size):
    filename = f"{algorith}_{arr_type}_{size}.txt"
    filepath = os.path.join(output_dirrectory, filename)
    
    np.savetxt(filepath, arr, fmt= '%d') 
    print(f"Saved sorted array to {filepath}")


# Generating random numbers btn 100000 to 999999
def generate_random_numbers(size):
    return np.random.randint(100000, 1000000, size=size)

def generate_reversed_random_numbers(size):
    numbers = np.arange(100000, 100000 + size)  # Generating a sequence of unique numbers.
    return numbers[::-1]  # Reversing the order to get descending data using python slicing.

# Merge Sort with comparison counter
def merge_sort(arr):
    comparisons = [0]
    
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
    
    def sort(arr):
        if len(arr) <= 1:
            return arr.copy()
            
        mid = len(arr) // 2
        left = sort(arr[:mid])
        right = sort(arr[mid:])
        
        return merge(left, right)
    
    sorted_arr = sort(arr)
    
    return sorted_arr, comparisons[0]

# Quick Sort with comparison counter
def quick_sort(arr):
    comparisons = [0]
    
    def partition(arr, left, right):
        random_idx = np.random.randint(left, right + 1)
        arr[random_idx], arr[right] = arr[right], arr[random_idx]
        pivot = arr[right]
        i = left - 1
        
        for j in range(left, right):
            comparisons[0] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[right] = arr[right], arr[i + 1]
        return i + 1

    def sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            sort(arr, low, pi - 1)
            sort(arr, pi + 1, high)

    arr_copy = arr.copy()
    sort(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy, comparisons[0]


# Geting the current memory of the system
def get_memory_usage():
    # Get the current process
    process = psutil.Process()
    # Get memory info in KB (divide by 1024 to convert from bytes to KB)
    return process.memory_info().rss / 1024


# Initialize lists to store metrics for plotting
merge_sort_random_time = []
quick_sort_random_time = []

merge_sort_reversed_time = []
quick_sort_reversed_time = []

merge_sort_random_memory = []
quick_sort_random_memory = []

merge_sort_reversed_memory = []
quick_sort_reversed_memory = []

merge_sort_random_comparisons = []
quick_sort_random_comparisons = []

merge_sort_reversed_comparisons = [] 
quick_sort_reversed_comparisons = []

# Test with different array sizes
sizes = [10000, 100000]

for size in sizes:
    print(f"\nTesting arrays of size {size}")
    
    # Generating the arrays
    random_arr = generate_random_numbers(size)
    reversed_arr = generate_reversed_random_numbers(size)
    
    # --- Merge Sort for Random Array ---
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_random, comparisons = merge_sort(random_arr)
    memory_used = get_memory_usage() - start_memory
    time_taken = time.time() - start_time
    
    merge_sort_random_time.append(time_taken)
    merge_sort_random_memory.append(memory_used)
    merge_sort_random_comparisons.append(comparisons)
    save_sorted_array(sorted_random, "merge_sort", "random", size)
    
    # --- Merge Sort for Reversed Array ---
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_reversed, comparisons = merge_sort(reversed_arr)
    memory_used = get_memory_usage() - start_memory
    time_taken = time.time() - start_time
    
    merge_sort_reversed_time.append(time_taken)
    merge_sort_reversed_memory.append(memory_used)
    merge_sort_reversed_comparisons.append(comparisons)
    save_sorted_array(sorted_reversed, "merge_sort", "reversed", size)

    # --- Quick Sort for Random Array ---
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_random, comparisons = quick_sort(random_arr)
    memory_used = get_memory_usage() - start_memory
    time_taken = time.time() - start_time
    quick_sort_random_time.append(time_taken)
    quick_sort_random_memory.append(memory_used)
    quick_sort_random_comparisons.append(comparisons)
    save_sorted_array(sorted_random, "quick_sort", "random", size)

    # --- Quick Sort for Reversed Array ---
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_reversed, comparisons = quick_sort(reversed_arr)
    memory_used = get_memory_usage() - start_memory
    time_taken = time.time() - start_time
    quick_sort_reversed_time.append(time_taken)
    quick_sort_reversed_memory.append(memory_used)
    quick_sort_reversed_comparisons.append(comparisons)
    save_sorted_array(sorted_reversed, "quick_sort", "reversed", size)

# Plotting the Metrics
plt.figure(figsize=(15, 15))

# Time Plot
plt.subplot(2, 3, 1)
plt.plot(sizes, merge_sort_random_time, marker='o', label='Merge Sort (Random)')
plt.plot(sizes, merge_sort_reversed_time, marker='o', label='Merge Sort (Reversed)')
plt.plot(sizes, quick_sort_random_time, marker='o', label='Quick Sort (Random)')
plt.plot(sizes, quick_sort_reversed_time, marker='o', label='Quick Sort (Reversed)')
plt.title("Time Complexity")
plt.xlabel("Array Size")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid()

# Memory Plot
plt.subplot(2, 3, 2)
plt.plot(sizes, merge_sort_random_memory, marker='o', label='Merge Sort (Random)')
plt.plot(sizes, merge_sort_reversed_memory, marker='o', label='Merge Sort (Reversed)')
plt.plot(sizes, quick_sort_random_memory, marker='o', label='Quick Sort (Random)')
plt.plot(sizes, quick_sort_reversed_memory, marker='o', label='Quick Sort (Reversed)')
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
