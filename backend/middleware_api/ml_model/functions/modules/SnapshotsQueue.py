from collections import deque

class SnapshotsQueue:
    def __init__(self, max_size):
        self.queue = deque([10000000000] * max_size)
        self.max_size = max_size

    def enqueue(self, item):
        if len(self.queue) < self.max_size:
            self.queue.append(item)

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()

    def shift(self, item):
        self.dequeue()
        self.enqueue(item)

    def size(self):
        return len(self.queue)

    def is_empty(self):
        return len(self.queue) == 0

    def is_full(self):
        return len(self.queue) == self.max_size

    def all_items_same(self):
        if len(self.queue) < self.max_size:
            return False
        first_item = self.queue[0]
        return all(item == first_item for item in self.queue)

