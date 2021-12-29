This project is a copy of the twitter API created with FastAPI, "requirements.txt" has
all the libraries used, this is a simplify version of twitter API, has path operations like 
create, update, delete and show users / tweets, this project is NOT connected to a database,
it works directly with .Json files which saves the information registered (users.json,
tweets.json). 

- To initialize Swagger UI or Redoc UI, please:
	- Be on your Venv where the requirements.txt was installed.
	- Run in console: 
			 uvicorn main:app --reload        #This launches the application.
	- Go to 127.0.0.1:8000 in your navigator (Google Chrome recomended):
		- 127.0.0.1:8000/docs : To use Swagger UI.
		- 127.0.0.1:8000/redoc: To user Redoc UI. 

- Open users.json and tweets.json and play with the API as long you want.



Kevyn Suarez
Colombia
https://github.com/efortish


	
