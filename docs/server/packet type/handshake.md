# Handshake

## Judge server send

```python
req = {
    'name': 'handshake', 
    
    # file packet.py
    'problems': get_supported_problems_and_mtimes(), 
    'executors': get_runtime_versions(), 

    'id': "CUSTOM_ID_FOR_JUDGE_BOT", # Random name id 
    'key': "AUTH_KEY" # the authentication key for the judge, more at https://github.com/DMOJ/online-judge/blob/master/judge/admin/runtime.py
}
```

## Judge server expectation

```python
res = {
    'name': 'handshake-success', 
}
```
