TODO:
 - add 'latest' tag to docker image
 - confirm the final name of model embeddings zip file (where is the file now?)
 - MUST make routes.py use relative path to model files

Team 145 - Pamplemousse - Final Project

Overview
========

This application is a food recipe search engine, that allows casual cooks to easily find recipes for ingredients that they already possess, and are also willing to experiment with recipes to substitute any missing ingredients with alternatives from their own pantry.


Usage Instructions
==================

The application is currently hosted online at: http://dva.waqasilyas.com

The overall workflow is very simply, all you need to provided is a list of available ingredients, and search. The available controls allow you to show search results with more lenient substitutions to more direct matches. Also another control allows you to control the quantity of returned results.

The recipe display area shows the search results, where you can inspect individual recipes.

Available workflows include the following:

1. Start a search of recipes by specifying ingredients that you currently have
    a. Each ingredient must be recognized by the application. Ingredients not recognized are currently not supported

2. Once all available ingredients have been specified, press Find recipes

3. Search results appear in the graph view. The legend explains the colors, and shapes.
    a. Each recipe node is colored based on difficulty of recipe for a casual cook
    b. Each recipe node has a border indicating the number of recipes that the system substitued to 
    c. The size of the recipe node indicates the closest match to your ingredients input

4. Click on a recipe node to show its details.

Instructions to Run Manually
============================

There are several options to run the application locally. However, all options listed below depend on the online database server hosted on Microsoft Azure Cloud Computing Services at:
dva-pamplemousse.postgres.database.azure.com

Your computer must be able to access this server. These options were tested on a clean Ubuntu 20.04 64-bit installation.

Using a Docker Container
========================

Follow these:

1. Install Docker software, if you do not have one installed.
    a. Open a terminal, and run the following commands:
    b. sudo apt-get update
    c. sudo apt install apt-transport-https ca-certificates curl software-properties-common
    d. curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    e. sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
    f. sudo apt update
    g. sudo apt -y install docker-ce
    h. For more details, please visit: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

2. Pull the docker image for the appear
    a. Open a terminal and run the following commands:
    b. sudo docker login
        i. Username: wiki1677
        ii. Password: Some1goThere
    c. sudo docker pull wiki1677/dva-recipe-app:latest

3. Run the docker image
    a. sudo docker run -d --name recipe-app -p 80:80 wiki1677/dva-recipe-app:latest
        i. The docker image requires at least 2GB of RAM
    b. To stop the app, use:
        i. sudo docker stop recipe-app

4. Open in browser
    a. Start a web browser, and enter address "localhost", without quotes
    b. The application may take a little time to load, as it fetches initial data

Run Flask Application Locally
=============================

The application can be run locally as well by following the instructions below. Note that all commands are expected to be run in default terminal shell. Also <app-extracted-dir> is the path to the directory where this app package was extracted.

1. Install Python 3.7, and requirements
    a. Install Python 3.7
        i. sudo add-apt-repository ppa:deadsnakes/ppa
        ii. sudo apt update
        iii. sudo apt -y install python3.7 python3-pip python3.7-venv
    b. Create a virtual environment
        i. python3.7 -m venv .venv
        ii. . .vevn/bin/activate
    b. Install required modules
        i. pip install -r environment/requirements.txt 
        ii. pip install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html

2. Install Node.js 15.x
    a. curl -sL https://deb.nodesource.com/setup_15.x | sudo bash -
    b. sudo apt install -y nodejs

3. Build front end application
    a. cd <app-extracted-dir>/CODE/web-app
    b. npm install
    c. npm run build

3. Unzip model files. "app-extracted-dir" is the directory this package was extracted to:
    a. cd <app-extracted-dir>/CODE/backend/modeling/outputs
    b. unzip 18411120.zip

4. Run flask:
    a. flask run -p 8080
    b. Open web browser and go to "localhost:8080", without quotes

Create Database
===============

??????????????

Build Docker image
==================

Here are the commands to build docker image:

1. cd <app-extracted-dir>/CODE/
2. sudo docker build -t wiki1677/dva-recipe-app -f environment/Dockerfile .