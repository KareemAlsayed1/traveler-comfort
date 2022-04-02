## Description
This folder contains the backend server that is built with the Django framework. The backend mainly runs the Prolog inference engine, handles API requests, and generates the knowledge base. Most of the backend work is focused within the following folders:
- `prolog_api/prolog_engine`, where the prolog code lives
- `prolog_api/views.py`, where the APIs handling happens, besides tracking browser sessions.

## Requirements
- Ensure that you have `python` installed with the version `3.7.+`. You can run `python --version` to confirm that you have python working. 
- Ensure that you have `pip` installed with the version `21.3.+`. You can run `pip --version ` to check your version. 
- Ensure that the latest version of SWI-Prolog is installed on your machine. You can follow the instructions in that link to get it installed `https://www.swi-prolog.org/download/stable`

## Installing the Packages and Running the Backend Server

There are two servers that we would need to start for fully running the backend. The first server would be running the main Django server. The second would be starting the Django Q cluster. 

### Starting a virtual environment to install the packages locally on your machine. 
- Create a virtual environment by running `python3 -m venv env`
- Activate the virtual environment by running `. env/bin/activate`
    - On Windows, use `env\Scripts\activate`
- Install the requirements (packages) by running `pip install -r requirements.txt`
Now we should have all the needed packages are installed.

### Starting the Django server
- Open a terminal at the current directory
- Activate the virtual environment by running `. env/bin/activate`
    - On Windows, use `env\Scripts\activate`
- Start the Django Server by running `python manage.py runserver`
### Starting the Django Q Cluster
- Open another terminal at the current directory
- Activate the virtual environment by running `. env/bin/activate`
    - On Windows, use `env\Scripts\activate`
- Start the Django Q Cluster by running `python manage.py qcluster`

Now we are ready to use the backend! Once you get the frontend server, go to `http://localhost:3000/` and it will interact with the backend server.  