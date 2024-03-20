registered_classes = []

def register(cls):
    """Decorator to register a class."""
    registered_classes.append(cls)
    return cls