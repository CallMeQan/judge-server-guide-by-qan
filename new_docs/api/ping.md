# Handle the ping request & response

## Backend server send to judge server

```python
import time

req = {
    'name': 'ping',
    'when': time.time() # float type
}
```

## Judge server response with

```python
import time

data = {
    'name': 'ping-response', 
    'when': req.when, #
    'time': time.time()
}
```
