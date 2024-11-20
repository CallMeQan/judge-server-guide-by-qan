# Normal packet type

Detail in file [packet.py](../../dmoj/packet.py), line 249

```python
req = {
    "name": "ping" | "get-current-submission" | "submission-request" | "terminate-submission" | "disconnect",
    
    # For ping type
    "when": "...",

    # For submission-request type
    "submission-id" : "ID_HERE", # str
    "problem-id": "PROBLEM_ID_HERE", # str
    "language": "", # Check in folder dmoj/executor
    "source": "SOURCE_CODE", #The fucking full source code
    "time-limit": "", # float, in second
    "memory-limit": "", # int, in KB
    "short-circuit": "", # Idk what the fuck is this
    "meta": "", # Idk what the fuck is this
}
```
