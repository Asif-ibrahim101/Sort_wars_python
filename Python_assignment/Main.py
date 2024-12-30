import sys
import numpy as np
import time
import psutil
import os

# Set recursion limit
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

def generate_random_numbers(size):
    return np.random.randint(10000, 100000, size=size)

def generate_reversed_random_numbers(size):
    numbers = np.arange(999999, 999999-size, -1)
    return numbers

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


def get_memory_usage():
    # Get the current process
    process = psutil.Process()
    # Get memory info in KB (divide by 1024 to convert from bytes to KB)
    return process.memory_info().rss / 1024

# Test with different array sizes
sizes = [10000, 100000]

for size in sizes:
    print(f"\nTesting arrays of size {size}")
    
    random_arr = generate_random_numbers(size)
    reversed_arr = generate_reversed_random_numbers(size)
    
    # Test Merge Sort
    print("\nMerge Sort:")
    
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_random, comparisons = merge_sort(random_arr)
    
    # saving the arrays
    save_sorted_array(sorted_random, "merge_sort", "random", size)
    memory_used = get_memory_usage() - start_memory
    print(f"Random array - Time: {(time.time() - start_time):.4f} seconds")
    print(f"Comparisons: {comparisons}")
    print(f"Memory Usage: {memory_used:.2f} KB")
    
    # Reversed array
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_reversed, comparisons = merge_sort(reversed_arr)
    
    # saving the arrays
    save_sorted_array(sorted_reversed, "merge_sort", "reversed", size)
    
    memory_used = get_memory_usage() - start_memory
    print(f"\nReversed array - Time: {(time.time() - start_time):.4f} seconds")
    print(f"Comparisons: {comparisons}")
    print(f"Memory Usage: {memory_used:.2f} KB")
    
    # Test Quick Sort
    print("\nQuick Sort:")
    
    # Random array
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_random, comparisons = quick_sort(random_arr)
    
    # saving the arrays
    save_sorted_array(sorted_random, "quick_sort", "random", size)
    
    memory_used = get_memory_usage() - start_memory
    print(f"Random array - Time: {(time.time() - start_time):.4f} seconds")
    print(f"Comparisons: {comparisons}")
    print(f"Memory Usage: {memory_used:.2f} KB")
    
    # Reversed array
    start_memory = get_memory_usage()
    start_time = time.time()
    sorted_reversed, comparisons = quick_sort(reversed_arr)
    
    # saving the arrays
    save_sorted_array(sorted_reversed, "quick_sort", "reversed", size)
    
    memory_used = get_memory_usage() - start_memory
    print(f"\nReversed array - Time: {(time.time() - start_time):.4f} seconds")
    print(f"Comparisons: {comparisons}")
    print(f"Memory Usage: {memory_used:.2f} KB")