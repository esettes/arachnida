class URLlists(): 
    """
    Manage the extracted URLs
    """
    def __init__(self):
        self.stack = []
        self.visited = []
        self.level = 0
    
    def set_level(self, lev):
        self.level = lev

    def get_level(self):
        return self.level

    def get_visited(self):
        return self.visited
    
    def get_stack(self):
        return self.stack
    
    def remove_from_stack_and_add_to_visit(self):
        """ Pops first `url` of stack and appends it to visited."""
        p = self.stack.pop(0)
        self.visited.append(p)
    
    def add_to_stack(self, url):
        """ Adds `url` at the head of list."""
        self.stack.insert(0, url)

    def add_to_visited(self, url):
        """ Adds `url` at the end of list."""
        self.visited.append(url)