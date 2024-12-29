import numpy as np
import time

def generate_random_numbers(size):
    return np.random.randint(100000, 1000000, size=size)

def generate_reversed_random_numbers(size):
    numbers = np.arange(999999, 999999-size, -1)
    return numbers

# Merge Sort with comparison counter
def merge_sort(arr):
    # Using a list for the counter so it can be modified in nested functions
    comparisons = [0]
    
    def merge(left, right):
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            comparisons[0] += 1  # Count each comparison between elements
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
    
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            comparisons[0] += 1  # Count each comparison with pivot
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            sort(arr, low, pi - 1)
            sort(arr, pi + 1, high)

    arr_copy = arr.copy()
    sort(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy, comparisons[0]

# Test with different array sizes
sizes = [10000, 100000]

for size in sizes:
    print(f"\nTesting arrays of size {size}")
    
    random_arr = generate_random_numbers(size)
    reversed_arr = generate_reversed_random_numbers(size)
    
    # Test Merge Sort
    print("\nMerge Sort:")
    start_time = time.time()
    sorted_random, comparisons = merge_sort(random_arr)
    print(f"Random array - Time: {(time.time() - start_time):.4f} seconds, Comparisons: {comparisons}")
    
    start_time = time.time()
    sorted_reversed, comparisons = merge_sort(reversed_arr)
    print(f"Reversed array - Time: {(time.time() - start_time):.4f} seconds, Comparisons: {comparisons}")
    
    # Test Quick Sort
    print("\nQuick Sort:")
    start_time = time.time()
    sorted_random, comparisons = quick_sort(random_arr)
    print(f"Random array - Time: {(time.time() - start_time):.4f} seconds, Comparisons: {comparisons}")
    
    start_time = time.time()
    sorted_reversed, comparisons = quick_sort(reversed_arr)
    print(f"Reversed array - Time: {(time.time() - start_time):.4f} seconds, Comparisons: {comparisons}")
