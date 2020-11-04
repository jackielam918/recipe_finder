# PlaceHolder for Project Details

# Backend Details 
Our project is a python Flask project deployed to Azure App Service on Linux.

All back end set up was done with Azure App Services following similar instructions mentioned on [Microsoft's Azure and Python Flask Quickstart](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask). 

To run our project follow the instruction under the [run the sample ](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask#run-the-sample) section in the guide using our repo. 

### Set up dependencies
`git clone https://github.gatech.edu/dva-pamplemousse/DVA_Project.git`  
`cd DVA_Project`  
`py -3 -m venv .venv`  
`.venv\scripts\activate`  
`pip install -r requirements.txt</code>`  

#### for production DB access locally 
Download the .env file that was given by Oak in Slack into the project directory
`pip install python-dotenv`

### Run project locally
`flask run`  
Open project by visiting http://localhost:5000/

## Continuous Deployment
Updates to our master branch will trigger a deployment to https://pamplemousse.azurewebsites.net/ using Azure Pipeline. Our pipeline is located https://dev.azure.com/hnguyen405/pamplemousse/
If you'd like access to it, please reach out to Oak. 

## Generating SQLAlchemy model.py
`./genmodel.sh`



