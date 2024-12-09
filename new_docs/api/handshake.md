# How to handle a handshake

## First judge server send to backend server a packet

```json
{
    "name": "handshake",
    "problems": "A long string that wtf",
    "executors": "A long string?",
    "id": "id string of that judge profile",
    "key": "Auth key of that judge profile"
}
```

## Backend must respond

- Before respond please use the `id` and `key` to check is it matched with `id` and `auth_key` created on backend server, store the `problems` and `executors`
- After that, respond with:

```json
{
    "name": "handshake-success"
}
```
