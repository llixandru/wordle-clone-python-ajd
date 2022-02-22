import cx_Oracle as oracledb
import json_db_env as dbclient
from random import randint


def database_connect():
    try:
        # Initialise Oracle Instant Client
        oracledb.init_oracle_client(lib_dir=dbclient.lib_dir)
        # Connect to the Autonomous JSON Database
        connection = oracledb.connect(dbclient.user, dbclient.password, dbclient.dsn)
        # Initialise SODA
        soda = connection.getSodaDatabase()
        # Open the collection
        collection = soda.openCollection("Wordle")

        # Get all JSON documents inside the collection
        doc = collection.find()
        docs = doc.getDocuments()
        res = docs[0].getContent()

        # Close the connection
        connection.close()

        # Return the JSON documents
        return res
    except oracledb.Error as e:
        print('Error:', e)

def get_word():
    result = database_connect()

    # Get a random word from the JSON documents
    random_index = randint(0, len(result)-1)
    return result[random_index]["word"] 