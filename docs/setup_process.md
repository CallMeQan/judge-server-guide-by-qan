# Main process start in `judge.py`, line 592, function name `main`

The main process start in [judge.py](../dmoj/judge.py). It begin with:

1. `sanity_check`:

    - Stop user from Windows without WSL to run judge-server
    - Stop user from running as root, since this [pull](https://github.com/DMOJ/judge-server/pull/757)
    - Try to enable [Berkeley Packet Filter](https://en.wikipedia.org/wiki/Berkeley_Packet_Filter), reason why judge can't run on Windows.
    - Mac support is unknown

2. load [env](../dmoj/judgeenv.py), [executors](../dmoj/executors/__init__.py) and [contrib_modules](../dmoj/contrib/__init__.py)
3. Check and print all previous warning from last run, skip if this is first run
4. Setup logging system, use `setproctitle` to set the judge process's name to

    ```python
    'DMOJ Judge %s on %s' % (env['id'], make_host_port(judgeenv))
    ```

    - `make_host_port` just a function to combine 2 variable into one string `host_name:port`

5. Setup [ClassicJudge](./JudgeClass.md).
6. Setup [`Monitor`](./monitor.md) and point `callback` to `ClassicJudge.update_problems`
7. Check for signal **SIGUSR2**

    - `SIGUSR2` is a user-defined signal available on Unix-like systems, but it not available on Windows, second reason why Windows not supported.
8. Create `api_server`, default is on [`0.0.0.0:9998`](https://en.wikipedia.org/wiki/0.0.0.0)

    - Create [HTTPServer](https://docs.python.org/3/library/http.server.html) with [Handler](../dmoj/control.py) (based on [BaseHTTPRequestHandler](https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler))
    - Start HTTPServer as a Thread

9. Get into loop with monitor, only stop if user perform exit action in control or any Exception may occur, kill everything
