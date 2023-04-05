# microservice-cloud
# s3-file-uploader
Simple microservice to upload files to S3 using Python

## Running the application
### Manually
Update the database connection by updating
DATABASE_HOST=
DATABASE=
DB_USERNAME=
DB_PASSWORD=
on the .env file in the app folder preferably with localhost credentials for testing


#### Install the python packages of the applications by running 
```pip install -r requirements.txt```
#### create a table in your database with the following:
``` CREATE TABLE mydatabase.files (   id INT NOT NULL AUTO_INCREMENT,   filename VARCHAR(255) NOT NULL,   url VARCHAR(255) NOT NULL,   PRIMARY KEY (id) );
```


Run the server 
```python app.py```

Interact with the api via postman. The default URI is http://{your url}:{port number}/api/v1/your-route eg: http://localhost:5000/api/v1/upload

Check if all the files are there using a get request to: 
http://localhost:5000/api/v1/upload

