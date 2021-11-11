# Postgres-Docker Database Initializer

## Pre-Reqs
-Docker
-Python3

## Setup
1. Edit configs file in configs/db_configs.yaml (optional if you want to leave defaults)

2. Setup
```
make init

make configs

make setup
## also runs
```

3. Show and Test
```
make show 
```

Open a application like Postico to log into your database instance