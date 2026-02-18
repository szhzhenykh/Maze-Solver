class Stack:
    def __init__(self, default):
        """
        Stack
        ----------------------------
        :param default: list: Default stack
        """
        self.items = default

    def __len__(self):
        """
        Checks the length of stack
        ----------------------------
        :return: int: Length of stack
        """
        return len(self.items)

    def push(self, item):
        """
        Adds new item
        ----------------------------
        :param item: Item
        ----------------------------
        :return: Stack
        """
        self.items.insert(0, item)

    def peek(self):
        """
        Looks at first item in the stack
        ----------------------------
        :return: First item in the stack
        """
        if len(self.items) == 0:
            raise Exception("peek() called on empty list")
        else:
            return self.items[0]

    def pop(self):
        """
        Deletes and returns the first item from stack
        ----------------------------
        :return: First item from stack
        """
        if len(self.items) == 0:
            raise Exception("peek() called on empty list")
        else:
            return self.items.pop(0)

    def is_Empty(self):
        """
        Checks if the stack is empty
        ----------------------------
        :return: Bool
        """
        if len(self.items) == 0:
            return True
        else:
            return False

    def __str__(self):
        """
        Returns stack as string
        ----------------------------
        :return: str: Stack string
        """
        return str(self.items)


class Queue:
    def __init__(self, default):
        self.items = default

    def enqueue(self, item):
         self.items.insert(0, item)

    def dequeue(self):
         if len(self.items)==0:
             raise Exception("dequeue() called on empty list")
         else:
             return self.items.pop()

    def peek(self):
         if len(self.items)==0:
             raise Exception("dequeue() called on empty list")
         else:
            return self.items[len(self.items)-1]

    def size(self):
         ''' Returns the number of items on the queue.
            It needs no parameters and returns an integer.'''
         return len(self.items)

    def isEmpty(self):
         ''' tests to see whether the queue is empty.
            It needs no parameters and returns a boolean value.'''
         return self.items == []

    def __str__(self):
        """
        Returns stack as string
        ----------------------------
        :return: str: Stack string
        """
        return str(self.items)