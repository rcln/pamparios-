


'''

    This file is the application configuration's file
    Before run the application on another host, you'll have to change information only about
    the database and perhaps the SECRET KEY(you genreate another secret key)

'''

DB_HOST = 'localhost'
DB_DRIVER = 'mysql'
DB_USER = 'azed'
DB_PASSWORD = '*--E9#_Nm+JuZ'
DB_DATABASE = 'pamparios'

SQLALCHEMY_DATABASE_URI = DB_DRIVER+'+pymysql://'+DB_USER+':'+DB_PASSWORD+'@'+DB_HOST+'/'+DB_DATABASE

SECRET_KEY = 'c2eea07fa7c379b8f42f244f4209f9ae'

UPLOAD_FOLDER = 'az_app/app_ressources'

ALLOWED_EXTENSIONS = {'pdf', 'txt'}

UPLOADED_FILE_DIR = '/translator_ressources/uploaded_files/'

EXTRACTED_FILE_DIR = '/translator_ressources/txt_extracted_files'

CONVERTED_FILE_DIR = '/translator_ressources/converted_files'
