# Hash table with separate chaining.
# Used to find a vehicle's slot without scanning the whole lot.
# put / get / remove are O(1) on average.
# If two keys land in the same bucket, that bucket is scanned.


class HashTable:
    def __init__(self, size=31):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        total = 0
        for ch in str(key):
            total = total + ord(ch)
        return total % self.size

    def put(self, key, value):
        bucket = self.buckets[self._hash(key)]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key):
        bucket = self.buckets[self._hash(key)]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return bucket[i][1]
        return None

    def remove(self, key):
        bucket = self.buckets[self._hash(key)]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                return True
        return False
