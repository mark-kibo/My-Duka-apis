from datetime import timedelta
import os
from sqlalchemy import URL

# connection_string = URL.create(
#     'postgresql',
#     username='mark-kibo',
#     password='uY2lc4rQgUIL',
#     host='ep-bold-sun-95179335-pooler.us-east-2.aws.neon.tech',
#     database='mydukka'
#     # connect_args={'sslmode':'require'}
# )


from decouple import config

BASE_DIR=os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY=config("SECRET_KEY", 'secret')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_SECRET_KEY=config("JWT_SECRET_KEY")
    MAIL_SERVER="smtp.gmail.com"
    MAIL_USERNAME="kibochamark@gmail.com"
    MAIL_PASSWORD="lmgrcdoixjdiplul"
    MAIL_PORT=587
    MAIL_USE_SSL=False
    MAIL_USE_TLS=True

class DevConfig(Config):
    DEBUG=config("DEBUG", cast=bool)
    SQLALCHEMY_ECHO=True
    # SQLALCHEMY_DATABASE_URI="postgresql://postgres:chep@localhost/mydukka"
    # SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:kibo@localhost/mydukka'
    # SQLALCHEMY_DATABASE_URI=config("DATABASE_URI")
    
    # SQLALCHEMY_DATABASE_URI='postgresql://hasura_role_4ffbe699-bb05-4c14-a35a-9a1e37846e90:t2vwMVXebif7@broad-breeze-12060553.us-east-2.aws.neon.tech:5432/sharp-eel-19_db_3935532'

class ProductionConfig(Config):
    DEBUG=config("DEBUG", cast=bool)


config_dict={
    'dev': DevConfig,
    'prod': ProductionConfig
}