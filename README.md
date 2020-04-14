# VS code env

`python3 -m venv .venv`  
`source .venv/bin/activate`

## Install dependencies

`pip install -r requirements.txt`

## Save requirements

`pip freeze > requirements.txt`

## Run app

`python -m app`

## Run jupyter in Docker

### Windows

docker run --rm -it -e NB_GID=100 -p 8890:8888 -v "$(pwd)/jupyter:/home/jovyan/host-note" jupyter/scipy-notebook:latest start-notebook.sh --NotebookApp.token=''

### MacOS

docker run --rm -it -e GRANT_SUDO=yes -p 8888:8888 -v $PWD/jupyter:/home/jovyan/host-note jupyter/scipy-notebook:latest