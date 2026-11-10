# Insertion sort.
# O(n^2), which is fine because the lot is small.
# Returns a new list. The list passed in is not changed.


def insertion_sort(items, key):
    arr = list(items)

    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and key(arr[j]) > key(current):
            arr[j + 1] = arr[j]
            j = j - 1
        arr[j + 1] = current

    return arr
