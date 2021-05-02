import os


BASE_DIR = os.path.dirname(__file__)
SECRET_KEY = 'dev'

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

if __name__ == '__main__':
    print(BASE_DIR)
