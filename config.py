import os

mysqlHost = "localhost"
mysqlPort = 3306
mysqlUser = "root"
mysqlPassword = ""
mysqlDbName = "kopicening"

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{mysqlUser}:{mysqlPassword}@{mysqlHost}:{mysqlPort}/{mysqlDbName}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False