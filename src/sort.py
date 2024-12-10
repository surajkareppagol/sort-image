from typing import Generator


class SVSort:
    def __init__(self, array: list[int]) -> None:
        self.array = array
        self.size = len(array)

        self.algorithms: list[object] = []
        self.algorithms.append(self.bubble_sort)
        self.algorithms.append(self.selection_sort)
        self.algorithms.append(self.insertion_sort)
        self.algorithms.append(self.merge_sort)
        self.algorithms.append(self.quick_sort)
        self.algorithms.append(self.heap_sort)

    def swap(self, i: int, j: int) -> None:
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def bubble_sort(self) -> Generator[list[int], None, None]:
        for _ in range(self.size):
            for j in range(self.size - 1):
                if self.array[j] > self.array[j + 1]:
                    self.swap(j, j + 1)

            yield self.array

    def selection_sort(self) -> Generator[list[int], None, None]:
        for i in range(self.size):
            min_idx = i
            for j in range(i + 1, self.size):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            self.swap(i, min_idx)
            yield self.array

    def insertion_sort(self) -> Generator[list[int], None, None]:
        for i in range(1, self.size):
            key = self.array[i]
            j = i - 1
            while j >= 0 and self.array[j] > key:
                self.array[j + 1] = self.array[j]
                j -= 1
            self.array[j + 1] = key
            yield self.array

    def merge_sort(self) -> Generator[list[int], None, None]:
        def merge(start, mid, end):
            left, right = self.array[start:mid], self.array[mid:end]
            i = j = 0
            for k in range(start, end):
                if j >= len(right) or (i < len(left) and left[i] <= right[j]):
                    self.array[k] = left[i]
                    i += 1
                else:
                    self.array[k] = right[j]
                    j += 1
                yield self.array

        def merge_sort_recursive(start, end):
            if end - start > 1:
                mid = (start + end) // 2
                yield from merge_sort_recursive(start, mid)
                yield from merge_sort_recursive(mid, end)
                yield from merge(start, mid, end)

        yield from merge_sort_recursive(0, self.size)

    def quick_sort(self) -> Generator[list[int], None, None]:
        def partition(low, high):
            pivot = self.array[high]
            i = low - 1
            for j in range(low, high):
                if self.array[j] <= pivot:
                    i += 1
                    self.swap(i, j)
                    yield self.array
            self.swap(i + 1, high)
            yield self.array
            return i + 1

        def quick_sort_recursive(low, high):
            if low < high:
                pi = yield from partition(low, high)
                yield from quick_sort_recursive(low, pi - 1)
                yield from quick_sort_recursive(pi + 1, high)

        yield from quick_sort_recursive(0, self.size - 1)

    def heap_sort(self) -> Generator[list[int], None, None]:
        def heapify(size, root):
            largest = root
            left, right = 2 * root + 1, 2 * root + 2
            if left < size and self.array[left] > self.array[largest]:
                largest = left
            if right < size and self.array[right] > self.array[largest]:
                largest = right
            if largest != root:
                self.swap(root, largest)
                yield self.array
                yield from heapify(size, largest)

        for i in range(self.size // 2 - 1, -1, -1):
            yield from heapify(self.size, i)

        for i in range(self.size - 1, 0, -1):
            self.swap(0, i)
            yield self.array
            yield from heapify(i, 0)

    def sort(self, index: int) -> object:
        algorithm = self.algorithms[index]
        return algorithm
