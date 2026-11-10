# Min heap used as a priority queue.
# The smallest score stays at index 0.
# insert and extract_min are both O(log n).


class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, item):
        self.heap.append(item)
        self._up(len(self.heap) - 1)

    def extract_min(self):
        if len(self.heap) == 0:
            return None

        smallest = self.heap[0]
        last = self.heap.pop()

        # if that was the only item, the heap is empty now
        if len(self.heap) > 0:
            self.heap[0] = last
            self._down(0)

        return smallest

    def is_empty(self):
        return len(self.heap) == 0

    def _smaller(self, i, j):
        # item is (score, slot id, slot)
        # lower score wins, if scores match the smaller slot id wins
        a = self.heap[i]
        b = self.heap[j]
        if a[0] != b[0]:
            return a[0] < b[0]
        return a[1] < b[1]

    def _up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._smaller(i, parent):
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def _down(self, i):
        n = len(self.heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i

            if left < n and self._smaller(left, smallest):
                smallest = left
            if right < n and self._smaller(right, smallest):
                smallest = right

            if smallest == i:
                break

            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest
