```python
incoming_req = {
    "name": "test-case-status",
    "submission-id": "aplusb",
    "cases": [
        {
            "position": "1",
            "status": "TLE",
            "time": 1,
            "memory": 256,
            "points": 1.0,
            "total-points": 2.0,

            # May not exist in req
            "feedback": "", 
            "extended-feedback": "",
            "voluntary-context-switches": 0,
            "involuntary-context-switches": 0,
            "runtime-version": "",

            "output": "3",
        },
        ...
    ]
}
```