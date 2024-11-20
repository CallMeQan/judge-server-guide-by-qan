# Get current submission

## Judge server expectation

```python
req = {
    "name": "get-current-submission",
}
```

## Judge server return

```python
res = {
    'name': 'current-submission-id', 
    'submission-id': self.judge.current_submission.id
}
```
