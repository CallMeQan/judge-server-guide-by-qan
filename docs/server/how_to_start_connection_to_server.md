# How does judge SERVER work?

Before we start, lets assume that we use default config, which is `0.0.0.0:9998` [^1].

## 1. From file `judge.py` (The begin)

On line 627, it create `ClassicJudge` which in that class will create a PacketManager in `packet.py`.

The rests are just basic stuff in order to run smoothly.

## 2. Into `packet.py`

in `__init__` function:

1. Check for SSL certification.
2. Create basic variable
3. Get into `self._do_reconnect`

In `self._do_reconnect`, it is a recursive loop where:

- Try to run `self._connect`
- If encounter the `JudgeAuthenticationFailed` or `socket.error`, get into `self._reconnect`

## 2. The `self._connect`

```python
def _connect(self):
    # ...
    log.info('Opening connection to: [%s]:%s', self.host, self.port)

    while True:
        try:
            # First attempting to create a connection to `0.0.0.0:9998` with a timeout of 5 seconds

            self.conn = socket.create_connection((self.host, self.port), timeout=5)
        except OSError as e:
            if e.errno != errno.EINTR:
                raise
        else:
            break

    # After create success, set timeout 300 seconds if that connection not respond.

    self.conn.settimeout(300)
    self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    # ... SSL check

    log.info('Starting handshake with: [%s]:%s', self.host, self.port)
    self.input = self.conn.makefile('rb')
    # ================HANDSHAKE=====================
    self.handshake(problems, versions, self.name, self.key)
    log.info('Judge "%s" online: [%s]:%s', self.name, self.host, self.port)
```

1. First attempting to create a connection to `0.0.0.0:9998` with a timeout of 5 seconds
2. After create success, set timeout 300 seconds if that connection not respond.
3. Call `self.handshake`

## 3. Into `handshake` and `_send_packet`

1. At beginning of handshake function, the judge create a request dict-type:

    ```python
    {
        'name': 'handshake', 
        'problems': ..., 
        'executors': ..., 
        'id': JUDGE_ID, 
        'key': AUTH_KEY
    }
    ```

    - Then it call function `_send_packet` with that request.
2. Into the `_send_packet`, it zip the dict. Then use `self.conn` to deliver it to `0.0.0.0:9998` that judge created in section 2.
3. After sent, judge wait for respond of the handshake. The server that host in `0.0.0.0:9998` must return respond:

    ```python
    res = {
        'name':'handshake-success',
        ...
    }
    ```

## 4. Success let judge server online

[^1]: In Linux a program may specify 0.0.0.0 as the remote address to connect to the current host (AKA localhost).
