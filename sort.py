import numpy as np
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(10**6)
# Quick Sort

def partition(arr, low, high):
    ran = random.randint(low, high)
    arr[low], arr[ran] = arr[ran], arr[low]
    pivot = arr[low]
    
    i = low - 1
    j = high + 1
    
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        
        j -= 1
        while arr[j] > pivot:
            j -= 1
            
        if i >= j:
            return j
        
        arr[i], arr[j] = arr[j], arr[i]

def quick_sort_iterative(arr):

    stack = [(0, len(arr) - 1)]
    while stack:
        low, high = stack.pop()
        if low < high:
            split = partition(arr, low, high)
            
            if split + 1 < high:
                stack.append((split + 1, high))

            if split > low:
                stack.append((low, split))

# Merge Sort 
def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    
    L = arr[l:(l + n1)].copy()
    R = arr[m + 1:(m + 1 + n2)].copy()
    
    i = 0 
    j = 0 
    k = l 
    
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
        
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
        
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergesort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        mergesort(arr, left, mid)
        mergesort(arr, mid + 1, right)
        merge(arr, left, mid, right)

# Heap Sort
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    
    if l < n and arr[i] < arr[l]:
        largest = l
        
    if r < n and arr[largest] < arr[r]:
        largest = r
        
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


# 2. DATA

def generate_datasets(n_elements=1_000_000): 
    datasets = []
    labels = []
    
    MAX_VAL = 1_000_000 # Giá trị tối đa
    
    print(f"--- Đang khởi tạo dữ liệu ---")
    print(f"Số lượng: {n_elements} phần tử/mảng")
    print(f"Phạm vi giá trị: 0 - {MAX_VAL}")
    
    # 1. Float tăng dần
    arr1 = np.sort(np.random.rand(n_elements) * MAX_VAL)
    datasets.append(arr1)
    labels.append("1. Float Asc")

    # 2. Int giảm dần
    arr2 = np.sort(np.random.randint(0, MAX_VAL, n_elements))[::-1]
    datasets.append(arr2)
    labels.append("2. Int Desc")

    # 3-6. Float ngẫu nhiên (4 bộ)
    for i in range(3, 7):
        arr = np.random.rand(n_elements) * MAX_VAL
        datasets.append(arr)
        labels.append(f"{i}. Float Rand")

    # 7-10. Int ngẫu nhiên (4 bộ)
    for i in range(7, 11):
        arr = np.random.randint(0, MAX_VAL, n_elements)
        datasets.append(arr)
        labels.append(f"{i}. Int Rand")
        
    print("Đã tạo xong 10 bộ dữ liệu!\n")
    return datasets, labels

def measure_time(algo_func, data, algo_name):
    arr_copy = np.copy(data)
    start_time = time.time()
    
    if algo_name == "Quick Sort":
        quick_sort_iterative(arr_copy) 
    elif algo_name == "Merge Sort":
        mergesort(arr_copy, 0, len(arr_copy) - 1)
    elif algo_name == "Heap Sort":
        heap_sort(arr_copy)
    elif algo_name == "NumPy Sort":
        np.sort(arr_copy)
        
    end_time = time.time()
    return end_time - start_time

# 4. MAIN

def main():
    # Cấu hình
    N = 1_000_000 # 1 triệu phần tử
    
    # Tạo dữ liệu
    datasets, labels = generate_datasets(N)
    
    results = {
        "Dataset": [],
        "Quick Sort": [],
        "Merge Sort": [],
        "Heap Sort": [],
        "NumPy Sort": []
    }
    
    for i, data in enumerate(datasets):
        results["Dataset"].append(labels[i])
        
        # Đo thời gian lần lượt các thuật toán
        results["Quick Sort"].append(measure_time(None, data, "Quick Sort"))
        results["Merge Sort"].append(measure_time(mergesort, data, "Merge Sort"))
        results["Heap Sort"].append(measure_time(heap_sort, data, "Heap Sort"))
        results["NumPy Sort"].append(measure_time(None, data, "NumPy Sort"))
        
    df = pd.DataFrame(results)
    

    print("\n" + "="*50)
    print(f"KẾT QUẢ THỜI GIAN CHẠY (Giây) - N={N}")
    print("="*50)
    print(df.to_string(index=False)) 
    print("="*50)


if __name__ == "__main__":
    main()