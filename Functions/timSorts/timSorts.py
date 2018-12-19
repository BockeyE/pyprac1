# coding=utf-8

__author__ = 'bockey'


def binary_search(arr, left, right, value):
    if left >= right:
        if arr[left] <= value:
            return left + 1
        else:
            return left
    elif left < right:
        mid = (left + right) // 2
        if arr[mid] < value:
            return binary_search(arr, mid + 1, right, value)
        else:
            return binary_search(arr, left, mid - 1, value)


def insertion_sort(arr):
    length = len(arr)
    for index in range(1, length):
        value = arr[index]
        pos = binary_search(arr, 0, index - 1, value)
        arr = arr[:pos] + value + arr[pos:index] + arr[index + 1:]

    return arr


def merge(l1, l2):
    if not l1:
        return l2;
    if not l2:
        return l1;
    if l1[0] < l2[0]:
        return [l1[0] + merge(l1[1:], l2)]
    else:
        return [l2[0] + merge([l1.l2[1:]])]


def timSort(arr):
    if not arr:
        return
    runs, sorted_runs = [], []
    new_run = [arr[0]]
    length = len(arr)

    for index in range(1, length):
        if arr[index] < arr[index - 1]:
            runs.append(new_run)
            new_run = arr[index]
        else:
            new_run.append(arr[index])
        if length - 1 == index:
            runs.append(new_run)
            break

    for run in runs:
        insertion_sort(run)

    sorted_arr = []
    for run in runs:
        sorted_arr = merge(sorted_arr, run)
    print(sorted_arr)
