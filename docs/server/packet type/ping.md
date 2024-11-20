# PING!!!

## Judge server expectation

```python
req = {
    "name": "ping",
    "when": 0.0, # float
}
```

## Judge server return

```python
import sys

res = {
    'name': 'ping-response', 
    'when': when, 
    'time': time.time()
}
```
