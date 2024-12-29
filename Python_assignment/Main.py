import random
import os
import sys
import time
import psutil

sys.setrecursionlimit(15000) #Due to execive resurssion limmit

##################################################################
# Generating the datasets

# Generating random datasets
def generate_random_dataset(size):
    return [random.randint(100000, 999999) for _ in range(size)]

# generating reversed datasets
def generate_reverse_dataset(size):
    # Generate sorted list of random numbers first
    numbers = generate_random_dataset(size)
    return sorted(numbers, reverse=True)

# Modified save functions with error handling
def save_dataset_merge(data, filename):
    try:
        os.makedirs('Merge_sort_datasets', exist_ok=True)
        filepath = os.path.join('Merge_sort_datasets', filename)
        
        with open(filepath, 'w') as f:
            for number in data:
                f.write(f"{number}\n")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

def save_dataset_quick(data, filename):
    try:
        os.makedirs('Quick_sort_datasets', exist_ok=True)
        filepath = os.path.join('Quick_sort_datasets', filename)
        
        with open(filepath, 'w') as f:
            for number in data:
                f.write(f"{number}\n")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

# Merge function for merge sort
def Merge(left, right):
    result = []
    i = 0
    j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Merge Sort Main function
def MergeSort(arr):
    if len(arr) <= 1:
        return arr
    
    # calculating the mid
    mid = len(arr) // 2
    left = MergeSort(arr[:mid])
    right = MergeSort(arr[mid:])
    return Merge(left, right)

# Modified Quick Sort for better performance
def partition(array, low, high):
   pivot = array[high]
   i = low - 1
   for j in range(low, high):
       if array[j] <= pivot:
           i += 1
           array[i], array[j] = array[j], array[i]
   array[i + 1], array[high] = array[high], array[i + 1]
   return i + 1

def QuickSort(array):
    def _quick_sort(arr, low, high):
        while low < high:
            pi = partition(arr, low, high)
            # Recursive call on smaller partition
            if pi - low < high - pi:
                _quick_sort(arr, low, pi - 1)
                low = pi + 1
            else:
                _quick_sort(arr, pi + 1, high)
                high = pi - 1
    
    arr_copy = array.copy()
    _quick_sort(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy

# Added performance measurement
def measure_sort_performance(sort_func, data):
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / 1024 / 1024  # in MB

    start_time = time.time()
    sorted_data = sort_func(data)
    end_time = time.time()

    memory_after = process.memory_info().rss / 1024 / 1024  # in MB
    memory_usage = memory_after - memory_before
    execution_time = (end_time - start_time) * 1000

    return sorted_data, execution_time, memory_usage
    
def main():
    sizes = [10000, 100000]
    
    for size in sizes:
        print(f"\nProcessing dataset size: {size}")
        
        # Generate datasets
        random_data = generate_random_dataset(size)
        reverse_data = generate_reverse_dataset(size)
        
        merge_random, merge_random_time, merge_random_memory = measure_sort_performance(MergeSort, random_data)
        merge_reverse, merge_reverse_time, merge_reverse_memory = measure_sort_performance(MergeSort, reverse_data)
        
        # Measure Quick Sort performance
        quick_random, quick_random_time, quick_random_memory = measure_sort_performance(QuickSort, random_data)
        quick_reverse, quick_reverse_time, quick_reverse_memory = measure_sort_performance(QuickSort, reverse_data)
        
        # Print performance results
        print(f"\nPerformance Results for size {size}:")
        
        # for Merge sort
        print(f"Merge Sort (Random): {merge_random_memory:.4f} MB")
        print(f"Merge Sort (Reverse): {merge_reverse_memory:.4f} MB")
        print(f"Merge Sort (Random): {merge_random_time:.4f} seconds")
        print(f"Merge Sort (Reverse): {merge_reverse_time:.4f} seconds")
        
        # for Quick sort
        print(f"Quick Sort (Random): {quick_random_memory:.4f} MB")
        print(f"Quick Sort (Reverse): {quick_reverse_memory:.4f} MB")
        print(f"Quick Sort (Random): {quick_random_time:.4f} seconds")
        print(f"Quick Sort (Reverse): {quick_reverse_time:.4f} seconds")
        
        # Save results
        save_dataset_merge(merge_random, f'random_{size}.txt')
        save_dataset_merge(merge_reverse, f'reverse_merge_{size}.txt')
        save_dataset_quick(quick_random, f'random_{size}.txt')
        save_dataset_quick(quick_reverse, f'reverse_quick_{size}.txt')

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")