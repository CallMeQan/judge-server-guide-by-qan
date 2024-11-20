ClassicJudge depend on Judge which automatic create [`PacketManager`](./packet.md) with input `host_name` and `port`

# Judge class

## Init

initial `packet_manager`, empty `current_judge_worker`, way to lock `_grading_lock`, flag `updater_exit`, signal event `updater_signal` and a thread `updater` which point to itself `_updater_thread`

## `_updater_thread`

