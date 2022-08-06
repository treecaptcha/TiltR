# method stubs
# public interface controller

# returns idx
def register(id: int) -> int: ...

# value is between -1 and 1
def update(idx: int, value: int) -> None: ...

# forwards real controls to the virtual ones
# should be just pass on OSes that support injecting controls
def forwardVirts() -> None: ...

# returns an abstract list of devices that can be of any type the index may be passed into register
def getDevices() -> []: ...

# returns a string that can be used by load to reload the state of the controllers
def save() -> str: ...

# takes the string given by save()
def load(text: str) -> None: ...

# release all controllers and do any other shut down logic
# cleanup is not required
def shutdown() -> None: ...

# text representation of any usefull debug info
def dump() -> str: ...