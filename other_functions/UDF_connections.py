import pymysql
from sqlalchemy import create_engine
import pymongo
import app
# creating mysql connection
# Credentials to database connection
aws_endpoint = 'yt-scrapper.co2ntnc4f72p.us-east-1.rds.amazonaws.com'
hostname = aws_endpoint
dbname = 'yt_scrape'
uname = "admin"
pwd = "mds268ds"


def create_sql_engine():
    """
    This function create a mysql engine which allow user to post data in my sql.

    Returns:
        mysql alchemy engine

    """

    # Create SQLAlchemy engine to connect to MySQL Database
    try:
        engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                               .format(host=hostname, db=dbname, user=uname, pw=pwd))
    except Exception as e:
        app.logger('ERROR- from file connection : while connecting to mySQL, Error-key: %s' %(str(e)))
    return engine


def create_mongodb_conn():
    """
    Create connection with mongoDb.

    Returns:
        MongoDb Connection
    """

    try :
        # creating connection with mongodb
        client = pymongo.MongoClient(
                    "mongodb+srv://koustav300:kdeysonai@cluster0.o9pog9p.mongodb.net/?retryWrites=true&w=majority")
    except Exception as e:
        app.logger('ERROR- from file connection : while connecting to mongoDB, Error-key: %s' %(str(e)))
        raise
    return client

def create_pysql_connction():
    """
    This function create a py-mysql connection which allow user to run SQL QUERY in server.

    Returns:
       py-mysql connection

   Note: connection params are taken from Golbal variables

    """

    try:
        # Connect to the database
        connection = pymysql.connect(host=aws_endpoint,
                                     user=uname,
                                     password=pwd,
                                     db=dbname)
    except Exception as e:
        app.logger('ERROR- from file connection : while connecting to mySQL-pysql, Error-key: %s' %(str(e)))
        raise
    return connection