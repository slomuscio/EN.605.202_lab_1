class ArrayStack:
    def __init__(self):
        self._data = []  # Create emtpy list to hold data 

    def is_empty(self): 
        return len(self._data) == 0  # Return True if stack is empty, False otherwise
    
    def __len__(self):
        return len(self._data)
    
    def push(self, item):
        return self._data.append(item)  # Append item to end of backend list 
    
    def pop(self):
        return self._data.pop()  # Remove the last item from the list and return it
    
    def peek(self):
        return self._data[-1]  # Return the last item in the list (top item in the stack)
    


