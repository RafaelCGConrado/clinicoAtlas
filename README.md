## ClinicoAtlas

ClinicoAtlas is a tool built to identify semantics between EHRs concepts and apply them in Graph Mining tasks.

You can watch a short demonstration video below:

https://github.com/user-attachments/assets/fd1c435c-43f3-4cf8-9d8a-f400ed3de429

## Python requirements


Check file `requirements.txt`

To create and use a virtual environment, type in the terminal:

    python -m venv clinicoatlas_venv  
    source clinicoatlas/bin/activate  
    pip install -r requirements.txt  

In the `config.py` file, change the database credentials to match yours.

## Install Ollama

ClinicoAtlas requires ollama to run and `gemma: latest` model. To install it, type in the terminal:

    pip install ollama
    ollama pull gemma:latest
    
To run the model:  

    ollama run 


## Running the app

Inside the `demo` directory, run the app with the following command on your Terminal:

    streamlit run main.py


## Database connection

ClinicoAtlas connects to PostgreSQL to query the data to model and mine.
Before using the tool, the user must configure the connection parameters.
The code is easily adaptable to work with CSV or other textual formats.

## 
