## Installation

Git clone this repo to your PC

    $ git clone https://github.com/switbit-9/fleet-repo.git

Dependencies
Cd into your the cloned repo as such:

    $ cd aircraft
After you cloned the repository, you want to create a virtual environment, so you have a clean python installation. You can do this by running the command    $ python -m venv venv
    
    $ source venv/bin/activate
Install the dependencies needed to run the app:
    
    $ pip install -r requirements.txt
Make those migrations work
    
    $ python manage.py makemigrations
    $ python manage.py migrate
Run It
Fire up the server using this one simple command:

    $ python manage.py runserver
You can now access the file api service on your browser by using

    http://localhost:8000/api/

## Docker setup 

Build the image and run the container:

```
docker-compose up -d --build
```

## Structure

Endpoint |HTTP Method  | Result
-- | -- |-- |--
`aircraft` | GET POST | List or Create the aircraft
`aircraft/:serial_number` | GET PUT | Retrieve or Update an aircraft
`flights`| GET POST | Create or List filtered flights
`flights/:id` | GET PUT DELETE | Retrieve, Delete or Update a flight
`report/` | GET |  List the report for the user

## Documentation 

Can check the API in your local environment using  [url](http://127.0.0.1:8000/api/docs/) or [url]http://127.0.0.1:8000/api/redoc/) or we use [Postman](https://www.postman.com/)


## URLs

http://127.0.0.1:8000/api/aircraft/{serial_number}/ -> Get or Update aircraft
http://127.0.0.1:8000/api/aircraft/ -> List or Create an aircraft
http://127.0.0.1:8000/api/flights/{id} -> Get or Retrieve or Delete flight
http://127.0.0.1:8000/api/flights/ -> List or Create Flight
http://127.0.0.1:8000/api/report/ -> Reports on Flights

## Filters and Pagination

http://127.0.0.1:8000/api/aircraft/?page=1
http://127.0.0.1:8000/api/flights/?page=1&departure_airport=00AA&date_from=2023-07-14&date_to=2023-07-19&arrival_airport=00IS
http://127.0.0.1:8000/api/report/?date_to=2023-08-22T20:00:00&date_from=2023-08-22T16:00:00

