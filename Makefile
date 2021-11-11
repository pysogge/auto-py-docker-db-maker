# define the name of the virtual environment directory
VENV := py3venv
CONFIGS := configs
UTILS := utils

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

# initialize the python virtual environment
init: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -U setuptools pip-tools
	./$(VENV)/bin/pip install -r requirements.txt
	echo ""
	echo "Initialized virtual environment"
	echo "Ensure configs are set."


configs: venv
	cp -n ./$(CONFIGS)/db_configs.yaml ./$(CONFIGS)/secret-db_configs.yaml 2> /dev/null
	cp ./$(UTILS)/backup-configs.yaml ./$(CONFIGS)/db_configs.yaml 2> /dev/null

# setup and start the database
setup: venv
	./$(VENV)/bin/python3 docker_db.py -p
	./$(VENV)/bin/python3 docker_db.py -w

# todo: seed the database
# todo: clear the database

# stop the database container, but keep the persistent data
stop: venv
	./$(VENV)/bin/python3 docker_db.py -t

# start the database
run: venv
	./$(VENV)/bin/python3 docker_db.py -e

# start the database
start: venv
	./$(VENV)/bin/python3 docker_db.py -e

# Swow running dockers (docker ps)
show: venv
	./$(VENV)/bin/python3 docker_db.py -w

# Stop the database container, but keep the image and persistent data
reimage: venv
	./$(VENV)/bin/python3 docker_db.py -r

# Stop the database, delete the image and persistent data, and remove the virtual environment
clean:
	./$(VENV)/bin/python3 docker_db.py -k
	rm output.log
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean setup stop start show

help:
	@echo "		init"
	@echo "			Setup virtual environment, install requirmeents"
	@echo ""
	@echo "  all: build the virtual environment and run the app"