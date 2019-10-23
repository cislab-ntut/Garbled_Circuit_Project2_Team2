class Stack:
    def __init__(self):
        self.contains = []

    def is_empty(self):
        return self.contains == []

    def pop(self):
        return self.contains.pop()

    def Top(self):
        return self.contains[len(self.contains)-1]

    def push(self, item):
        self.contains.append(item)

    def size(self):
        return len(self.contains)
            
        


