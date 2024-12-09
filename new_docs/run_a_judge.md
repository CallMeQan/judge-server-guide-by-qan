# Running a judge

Assume that you followed the [installation instruction](./setting_up_a_judge.md)!

## Getting Prerequisites

You need:

- **WAN_IP** of your backend server `123.xxx.xxx.xxx` or if you host judge server in the same VPS or machine with your backend server, then this is `0.0.0.0` or `localhost`
- **PORT** of your backend server, by default of judge server is `9999`
- [**What tier?**](./judge-tier.md), here we assume you using `dmoj/judge-tier1`

## Setting up judge profile (Skip if you already created)

Read [Judge profile template here](https://docs.dmoj.ca/#/judge/judge_configuration) or

```yaml
id: <judge name>
key: <judge authentication key>
problem_storage_globs:
  - /problems/*
```

- Assume that you are login as user `judger`, create folder `problems` to store judge profile and problems data inside it.

```sh
judger@callmeqan:~$ mkdir problems
judger@callmeqan:~$ cd problems
judger@callmeqan:~/problems$ nano judge01.yml
...Paste the sample configuration above to yaml file
```

- Now we have root problems is **`/home/judger/problems`**

## Running

```bash
judger@callmeqan:~/problems$ cd /home/judger
judger@callmeqan:~$ sudo docker run \
    --name judge \
    --network="host" \
    -v /home/judger/problems:/problems \
    --cap-add=SYS_PTRACE \
    -d \
    --restart=always \
    dmoj/judge-tier1:latest \
    run -p PORT -c /problems/judge01.yml WAN_IP -A 0.0.0.0 -a 9111
```

> Note: <br>
    - Remember to change the name of docker container `judge` to sth else if you run multiple judge<br>
    - If you create multiple profiles, replace it with judge02, judge03 for easier management!<br>
    - Multiple judge on same Server, you must increase the number id `9111` up
