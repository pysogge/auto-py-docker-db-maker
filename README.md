# Postgres-Docker Database Initializer
This is a simple automation script that will create a Docker Postgres database with a custom username, password, and port based on the db_config.yaml file in the configs folder.

It also creates a persistent data storage for the database on the host machine in ~/$persistent_storage_area/$application_name/ so that you can start and stop the database docker container without losing your data.

The Makefile includes simple setup commands, as well as commands to view, start, stop, and remove the docker (while maintaining the host machine persistent storage), or to remove the docker and clean up (remove) the persistent data storage area if desired.

## 0. Setup Pre-Reqs
Ensure you have the following:
-Linux/Unix with read/write access to ~/
-Docker
-Python3

## 1. Setup
a. Edit configs file in configs/db_configs.yaml 
(optional if you want to leave defaults)

b. Setup
```
make init

# copies your desired configs to a secret-configs file and resests the original configs file. The secret-configs file will be used by the docker setup script, but will be ignored by git 
make configs

# this also starst the docker container
make setup

```

c. Show that the container is running
```
make show 
```

d. Operate while maintaing persistent storage(optional)
```
#stops the container
make stop 

#starts the container
make start

#remove the container image from the system
make reimage
```

d. Clean Up (wipe the persistent storage)
```
#starts the container
make clean
```

e. Log into the Database
```
Open a application like Postico to log into your database with the credentials from the config file, e.g.:

 database_name: db_name
 database_password: db_password
 database_username: db_username
 container_name: db_container_name
 database_port: 5432

```