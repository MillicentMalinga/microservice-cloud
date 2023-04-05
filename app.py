from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import boto3
import os
import pymysql.cursors
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

# AWS S3 Configuration
s3 = boto3.client('s3',
                  aws_access_key_id=os.environ.get('AWS_ACCESS_ID'),
                  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

# MySQL Configuration
connection = pymysql.connect(host=os.environ.get('DATABASE_HOST'),
                             user=os.environ.get('DB_USERNAME'),
                             password=os.environ.get('DB_PASSWORD'),
                             db=os.environ.get('DATABASE'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

@app.route('/api/v1/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # upload the file to AWS S3
        s3.upload_fileobj(file, os.environ.get('AWS_BUCKET_NAME'), filename)
        # get the URL of the uploaded file
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': os.environ.get('AWS_BUCKET_NAME'), 'Key': filename})
        # store the file URL in the database
        with connection.cursor() as cursor:
            # create a new record for the file
            sql = "INSERT INTO files (filename, url) VALUES (%s, %s)"
            cursor.execute(sql, (filename, url))
            connection.commit()

        return jsonify({'url': url, 
                        'name': filename,
                        'CreatedAt': datetime.now()}), 201
    else:
        return jsonify({'error': 'File not allowed'}), 400

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/api/v1/files', methods=['GET'])
def get_files():
    with connection.cursor() as cursor:
        # retrieve all files from the database
        sql = "SELECT * FROM files"
        cursor.execute(sql)
        files = cursor.fetchall()
    return jsonify({'files': files}), 200

if __name__ == '__main__':
    app.run(debug=True)
