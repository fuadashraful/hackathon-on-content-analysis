## Add your API key in the environment.yml file

Before fetching content you have to add api key in environment.yml file like shown below
`HACK_API_KEY: <API_KEY>`

#Project setup instruction

1. create a virtualenv ex: python -m venv zelfenv
2. activate virtualenv
   For Windows: zelfenv\Scripts\activate
   For Linux: zelfenv\bin\activate
3. install dependencies `pip install -r requirements.txt'
4. Fetch data using command `python manage.py fetch_contents`
5. Run the Server `python manage.py runserver`

## You will see the API endpoints in the link after running the application

Swagger API Endpoints (This is not fully complete due to time constraint)
http://localhost:8000/api_test/

## API Docs (This is not fully complete due to time constraint)

http://localhost:8000/docs/
