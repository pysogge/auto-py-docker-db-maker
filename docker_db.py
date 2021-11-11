import yaml
import os
import shutil
import subprocess
import argparse

# python setup_db.py -d -b -r, etc.

# Default Settings
DEBUG = False
OPT_REMOVE_DIR = False
OPT_CREATE_DIR = False
OPT_REMOVE_CONTAINER = False
OPT_CREATE_CONTAINER = False
OPT_STOP_CONTAINER = False
OPT_START_CONTAINER = False

OPT_SHOW_DETAILS = False

CONFIGS_FILEPATH = "configs"
CONFIGS_FILENAME = "secret-db_configs.yaml"

# Arg Parsing
parser = argparse.ArgumentParser(description='This is a database creation script.')
parser.add_argument('-p','--prod', help='Production, Remove all , Build all',action='store_true', required=False)
parser.add_argument('-d','--dir',help='Replace Dir',action='store_true',  required=False)
parser.add_argument('-c','--container',help='Container',action='store_true', required=False)
parser.add_argument('-r','--remove',help='Remove Image',action='store_true', required=False)
parser.add_argument('-t','--stop',help='Stop Container Only',action='store_true', required=False)
parser.add_argument('-k','--kill',help='Remove Container, Remove Dir',action='store_true', required=False)
parser.add_argument('-b','--debug',help='Debug',action='store_true',  required=False)
parser.add_argument('-e','--restart',help='Restart Container, Assuming it is an Image',action='store_true',  required=False)
parser.add_argument('-v','--devmode',help='Dev Mode, Dev Configs',action='store_true',  required=False)
parser.add_argument('-w','--show',help='Show Status',action='store_true',  required=False)
parser.add_argument('-i','--input',help='Input File', required=False)
args = parser.parse_args()

if(args.prod):
    OPT_REMOVE_DIR = True
    OPT_CREATE_DIR = True
    OPT_REMOVE_CONTAINER = True
    OPT_CREATE_CONTAINER = True
if(args.dir):
    OPT_REMOVE_DIR = True
    OPT_CREATE_DIR = True
if(args.stop):
    OPT_STOP_CONTAINER = True
if(args.kill):
    OPT_REMOVE_DIR = True
    OPT_REMOVE_CONTAINER = True
if(args.container):
    OPT_REMOVE_CONTAINER = True
    OPT_CREATE_CONTAINER = True
if(args.restart):
    OPT_START_CONTAINER = True
if(args.remove):
    OPT_REMOVE_CONTAINER = True
if(args.show):
    OPT_SHOW_DETAILS = True
if(args.devmode):
    CONFIGS_FILENAME = CONFIGS_FILENAME.replace("secret-","")
if(args.debug):
    DEBUG = True

if DEBUG: print(args)


CONFIGS_LOCATION = os.path.join(CONFIGS_FILEPATH,CONFIGS_FILENAME)
if DEBUG: print("Configs location: ",CONFIGS_LOCATION)

configs = {}

with open(CONFIGS_LOCATION, "r") as yamlfile:
    configs = yaml.load(yamlfile, Loader=yaml.FullLoader)
    if DEBUG: print("Read successful")

dbPDirPath = os.path.join(os.path.expanduser('~/'),configs["persistent_storage_area"],configs["application_name"])

if DEBUG: print("Storage area: ",configs["persistent_storage_area"])

if OPT_REMOVE_DIR and os.path.exists(dbPDirPath) and os.path.isdir(dbPDirPath):
    if DEBUG: print("Storage dir exists: ",os.path.exists(dbPDirPath))
    shutil.rmtree(dbPDirPath)
    if DEBUG: print("Removed: ",dbPDirPath)
    if DEBUG: print("Storage dir exists: ",os.path.exists(dbPDirPath))

if OPT_CREATE_DIR and not os.path.exists(dbPDirPath): 
    os.makedirs(dbPDirPath)
    if DEBUG: print("Created: ",dbPDirPath)
    if DEBUG: print("Storage dir exists: ",os.path.exists(dbPDirPath))

CNTNAME = configs["container_name"]
DBPASS = configs["database_password"]
DBUSER = configs["database_username"]
DBNAME = configs["database_name"]
DBDIR = dbPDirPath
DBPORT = configs["database_port"]

STOP_CONTAINER = f"docker stop {CNTNAME}"
START_CONTAINER = f"docker start {CNTNAME}"
REMOVE_CONTAINER = f"docker rm {CNTNAME}"
CREATE_CONTAINER = f"docker run --name {CNTNAME} -e POSTGRES_PASSWORD={DBPASS} -e POSTGRES_USER={DBUSER} -e POSTGRES_DB={DBNAME} -v {DBDIR}/var/lib/postgresql/data -p {DBPORT}:5432 -d postgres"
SHOW_CONTAINER = f"docker ps"

#SHELLCOMMAND = f"--name {CNTNAME} -e POSTGRES_PASSWORD={DBPASS} -e POSTGRES_USER={DBUSER} -e POSTGRES_DB={DBNAME} -v {DBDIR}/var/lib/postgresql/data -p {DBPORT}:5432 -d postgres"

if OPT_START_CONTAINER:
    with open("./output.log", "a") as output:
        if DEBUG: print("Starting container: ",CNTNAME)
        subprocess.run(START_CONTAINER, shell=True, stdout=output)

if OPT_STOP_CONTAINER:
    with open("./output.log", "a") as output:
        if DEBUG: print("Stopping container: ",CNTNAME)
        subprocess.run(STOP_CONTAINER, shell=True, stdout=output)

if OPT_REMOVE_CONTAINER:
    with open("./output.log", "a") as output:
        if DEBUG: print("Removing container: ",CNTNAME)
        subprocess.run(STOP_CONTAINER, shell=True, stdout=output)
        subprocess.run(REMOVE_CONTAINER, shell=True, stdout=output)

if OPT_CREATE_CONTAINER:
    with open("./output.log", "a") as output:
        print("Creating container: ",CNTNAME)
        # subprocess.call(["docker","run",SHELLCOMMAND],shell=True, stdout=output)
        subprocess.call(CREATE_CONTAINER, shell=True, stdout=output)
        subprocess.call(SHOW_CONTAINER, shell=True, stdout=output)

if OPT_SHOW_DETAILS:
    subprocess.run(SHOW_CONTAINER, shell=True)
