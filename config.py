import os


BASE_DIR = os.path.dirname(__file__)
SECRET_KEY = 'dev'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://hankyungedudb002:gksrud70292!@my8001.gabiadb.com/hankyung002'
SQLALCHEMY_TRACK_MODIFICATIONS = False

if __name__ == '__main__':
    print(BASE_DIR)