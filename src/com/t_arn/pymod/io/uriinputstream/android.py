class UriInputStream:
    uri = None
    
    def __init__(self, uri):
        self.uri = uri
    # __init__
    
    def read(self, size):
        return f"{self.uri}::read({size})"
    # read
# UriInputStream
