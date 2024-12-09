# Installation Documentation (maybe better version of DMOJ?)

## Installing Prerequisites

- Install [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
- Install [Docker Compose](https://docs.docker.com/compose/install/linux/)
- Install require packages:

```sh
sudo apt update
sudo apt install git gcc g++ make python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev gettext curl
```

## Create folder for storing

## Setting up judge profile

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

## Installing judge server

```sh
judger@callmeqan:~$ git clone --recursive https://github.com/DMOJ/judge-server.git
judger@callmeqan:~$ cd judge-server/.docker
judger@callmeqan:~/judge-server/.docker$ make judge-tier1
```

### Move on [Running a judge](./run_a_judge.md)
