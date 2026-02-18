import numpy as np
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

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

def load_data_from_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"LỖI: Không tìm thấy thư mục '{folder_path}'")
        return [], []

    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    files.sort() # Sắp xếp tên file để thứ tự 01, 02... đúng
    
    datasets = []
    labels = []
    
    print(f"Đang đọc dữ liệu từ thư mục '{folder_path}'...")
    for filename in files:
        filepath = os.path.join(folder_path, filename)
        try:
            data = np.loadtxt(filepath)
            datasets.append(data)
            labels.append(filename.replace('.txt', ''))
            print(f"-> Đã tải: {filename} (Size: {len(data)})")
        except Exception as e:
            print(f"-> Lỗi khi đọc {filename}: {e}")
            
    return datasets, labels

def measure_time(algo_func, data, algo_name):
    arr_copy = np.copy(data) 
    
    start_time = time.time()
    
    # Gọi thuật toán tương ứng
    if algo_name == "Quick Sort":
        quick_sort_iterative(arr_copy) 
    elif algo_name == "Merge Sort":
        mergesort(arr_copy, 0, len(arr_copy) - 1)
    elif algo_name == "Heap Sort":
        heap_sort(arr_copy)
    elif algo_name == "NumPy Sort":
        np.sort(arr_copy)
        
    end_time = time.time()

    return (end_time - start_time) * 1000 


def main():
    DATA_FOLDER = 'dataset_thuc_nghiem' 
    
    datasets, labels = load_data_from_folder(DATA_FOLDER)
    
    if not datasets:
        print("Không có dữ liệu để chạy. Vui lòng kiểm tra lại thư mục.")
        return

    results = {
        "Dữ liệu": labels,
        "Quick Sort": [],
        "Heap Sort": [],  
        "Merge Sort": [],
        "sort (numpy)": []
    }
    
    print("\nBẮT ĐẦU CHẠY THỰC NGHIỆM (Đơn vị: ms)...")
    print("-" * 60)

    for i, data in enumerate(datasets):
        print(f"Đang xử lý file {i+1}/{len(datasets)}: {labels[i]}...")
        
        t_quick = measure_time(None, data, "Quick Sort")
        t_heap = measure_time(None, data, "Heap Sort")
        t_merge = measure_time(None, data, "Merge Sort")
        t_numpy = measure_time(None, data, "NumPy Sort")
        
        
        results["Quick Sort"].append(round(t_quick,3))
        results["Heap Sort"].append(round(t_heap,3))
        results["Merge Sort"].append(round(t_merge,3))
        results["sort (numpy)"].append(round(t_numpy,3))

        avg_quick = sum(results["Quick Sort"]) / len(datasets)
        avg_heap = sum(results["Heap Sort"]) / len(datasets)
        avg_merge = sum(results["Merge Sort"]) / len(datasets)
        avg_numpy = sum(results["sort (numpy)"]) / len(datasets)

    # 2. Thêm dòng "Trung bình" vào dữ liệu
        results["Dữ liệu"].append("Trung bình")
        results["Quick Sort"].append(round(avg_quick, 3))
        results["Heap Sort"].append(round(avg_heap, 3))
        results["Merge Sort"].append(round(avg_merge, 3))
        results["sort (numpy)"].append(round(avg_numpy, 3))

    # 3. Tạo DataFrame và Xuất ra CSV
    df = pd.DataFrame(results)
    
    # In ra màn hình để kiểm tra
    print("\n" + "="*70)
    print(f"BẢNG KẾT QUẢ (ms)")
    print("="*70)
    print(df.to_string(index=False)) 
    print("="*70)

    # Lệnh quan trọng nhất: Lưu ra file CSV
    # encoding='utf-8-sig' giúp Excel mở lên không bị lỗi font tiếng Việt
    df.to_csv("ket_qua_thuc_nghiem.csv", index=False, encoding='utf-8-sig')
    
    print("\nĐã lưu file: ket_qua_thuc_nghiem.csv")
   

if __name__ == "__main__":
    main()