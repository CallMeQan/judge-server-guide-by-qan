# Submission

##

### Judge server define Submission object

```python
# In `judge.py`, line 58:
Submission = NamedTuple(
    'Submission',
    [
        ('id', int),
        ('problem_id', str),
        ('language', str),
        ('source', str),
        ('time_limit', float),
        ('memory_limit', int),
        ('short_circuit', bool),
        ('meta', Dict),
    ],
)
```

### Judge server expect request contains

```python
# In `packet.py`, line 259

req = {
    "name": "submission-request",
    "submission-id": "1", # int, Server self-manage id
    
    "problem-id": "aplusb", # str, Must match id in problem root defined in judge env
    "language": "cpp", # str, All availible in https://github.com/DMOJ/judge-server
    "source": "SOURCE_CODE", # str, The fucking source code
    "time-limit": 1.0, # float, in seconds
    "memory-limit": 256, # int, in KB
    "short-circuit": False, # bool, Lmao what is this
    "meta": {}, # Lmao?
}
```
