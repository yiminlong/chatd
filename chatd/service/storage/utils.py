
class ShiftedList(object):
    """ List implementation with fixed indexes. """
    
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            self._items = list(args[0])
        else:
            self._items = list(args)
            
        self._shift = 0
    
    def __repr__(self):
        return self._items.__repr__()
    
    def __delitem__(self, index):
        del self._items[index-self._shift]
    
    def __getitem__(self, index):
        # XXX what if index is negative?
        return self._items[index-self._shift]
    
    def count(self):
        return len(self._items) + self._shift
    
    def __getslice__(self, i, j):
        if j and not i:
            return self._items[:j]
        elif i < 0:
            return self._items[i:j]
        else:
            return self._items[i-self._shift : j-self._shift]
    
    def append(self, object):
        self._items.append(object)
    
    def shift(self, count):
        self._items = self._items[count:]
        self._shift += count
