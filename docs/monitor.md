# Monitor class

## Init

1. Check is [`watchdog`](https://www.youtube.com/watch?v=M9CT6MMry0U) package installed AND in [env](../dmoj/judgeenv.py) enable watchdog stuff
2. Create `RefreshWorker` (Thread) if env enable it
3. Create `SendProblemsHandler`, which based on [`watchdog/FileSystemEventHandler`](https://python-watchdog.readthedocs.io/en/stable/api.html#watchdog.events.FileSystemEventHandler)
4. Setup basic [`Observer`](https://python-watchdog.readthedocs.io/en/stable/api.html#module-watchdog.observers)
5. Put all problem data folder into `Observer` to watch it

## More Information

Empty...
