import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
connection = pymysql.connect(host=os.getenv('DBHOST'),
                             user=os.getenv('USERDB'),
                             password=os.getenv('PASSWORDDB'),
                             database=os.getenv('DBNAME'),
                             cursorclass=pymysql.cursors.DictCursor)