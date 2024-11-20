# How does the judge server read the submission that sent from server?

## 1. In `judge.py`

As we can see in line 660, the judge start `listen()` which monitor is on.

Inside function `listen(self)`, we don't care about updater, the judge start the `packet_manager.run()`

## 2. Move to `packet.py`

1. It run `_periodically_flush_testcase_queue` as a Thread, so it run paralel with the `_read_forever`.

    - `_periodically_flush_testcase_queue` is function that flush all testcases remain in task queue by `_send_packet` with request:

        ```python
        req = {
            'name': 'test-case-status',
            'submission-id': self.judge.current_submission.id,
            'cases': [
                {
                    'position': position,
                    'status': result.result_flag,
                    'time': result.execution_time,
                    'points': result.points,
                    'total-points': result.total_points,
                    'memory': result.max_memory,
                    'output': result.output,
                    'extended-feedback': result.extended_feedback,
                    'feedback': result.feedback,
                    'voluntary-context-switches': result.context_switches[0],
                    'involuntary-context-switches': result.context_switches[1],
                    'runtime-version': result.runtime_version,
                }
                for position, result in self._testcase_queue
            ],
        }
        ```

    - **But here we don't care about flushing**

2. Inside `_read_forever`, it perform a while loop constantly `self._receive_packet(self._read_single())`, exit when hit KeyboardInterrupt or unknown Exception.

3. In `_receive_packet()`, it receive the unzipped variable and perform many stuff.
