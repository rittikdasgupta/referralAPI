# REFERRAL API

## Technologies Used
* Python
* MongoDB
* Flask

## Github Steps:
* Fork the repository to your Github account
* Copy the link (ends with a .git) of your forked repository
* In a folder of your choice in your local machine, run git clone thelinkyoujustcopied.git
* ```cd referralAPI```

## Steps to run the API:
* ```cd referralAPI```
* Create a virtual environment ```py -3 -m venv venv```
* Activate virtual environment ```venv\Scripts\activate``` (for Windows) and ```venv\bin\activate``` (for Mac)
* ```pip install -r requirements.txt```(only for the first time after clonning)

## Testing the API:
* Locally
* Test the API with POSTMAN

Example for GET request :
* Set the URL to ```http://127.0.0.1:5000/api/user?api_key=<your_key>``` to get all the entries from the user database.

* Set the URL to ```http://127.0.0.1:5000/api/user/<userID>?api_key=<your_key>``` to get specific entries from the user database.

* Set the URL to ```http://127.0.0.1:5000/api/logs?api_key=<your_key>``` to get all the user logs from the logs database.

* Set the URL to ```http://127.0.0.1:5000/api/logs/<userID>?api_key=<your_key>``` to get specific user logs from the logs database.

Example for POST request :
* Set the URL to ```http://127.0.0.1:5000/api/user?api_key=<your_key>``` to add a user.<br><br>

    Sample JSON Data to contact route:
    ```json
    {
        "username": "sample2",
        "password":"damnsimple",
        "referrer":"referrer id"
    }
    ```
    <br>

