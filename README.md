# How To: Make your own Wordle clone with Python and Autonomous JSON


1. Introduction
2. Prerequisites
3. Create an Autonomous JSON Database
4. SODA Database Connection
5. Writing the Wordle Python code
6. Execution


## Introduction


**Wordle** is an extremely popular web-based word game developed by Josh Wardle. 

Players have six attempts to guess a five-letter word, with feedback given for each guess in the form of colored tiles indicating when letters match or occupy the correct position.

After every guess, each letter is marked as either **green**, **yellow** or **gray**: **green** indicates that letter is correct and in the correct position, **yellow** means it is in the answer but not in the right position, while **gray** indicates it is not in the answer at all.

In the following article, we will look at how to create our own Wordle clone by using Python and an Autonomous JSON database.


## Prerequisites


Before we get started, we need to install some dependencies.

- [Python 3](https://www.python.org/downloads/)

- A free or paid-tier Oracle account where to create the [Autonomous JSON Database](https://www.oracle.com/autonomous-database/autonomous-json-database/) in.

    > _Get an Always Free Oracle account [here](https://www.oracle.com/autonomous-database/free-trial/?source=:ow:o:p:nav:081320AutonomousJSONDbHero&intcmp=:ow:o:p:nav:081320AutonomousJSONDbHero). It includes access to two Oracle Autonomous Databases, two AMD Compute VMs, up to 4 instances of Ampere Arm A1 Compute, Block, Object, and Archive Storage; Load Balancer and data egress; Monitoring and Notifications._
  
- [cx_Oracle](https://github.com/oracle/python-cx_Oracle) which is a Python extension module that enables access to Oracle Database. It conforms to the Python database API 2.0 specification with a considerable number of additions and a couple of exclusions. 
  
  > _See the [cx_Oracle Documentation](https://cx-oracle.readthedocs.io/en/latest/user_guide/introduction.html) for more information._

- [Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client/downloads.html), which enables development and deployment of applications that connect to Oracle Database, either on-premise or in the Cloud. 
  
  > _The Instant Client libraries provide the necessary network connectivity and advanced data features to make full use of Oracle Database. The libraries are used by the Oracle APIs of popular languages and environments including Python, Node.js, Go, PHP and Ruby, as well as providing access for Oracle Call Interface (OCI), Oracle C++ Call Interface (OCCI), JDBC OCI, ODBC and Pro*C applications. Tools included in Instant Client, such as SQL*Plus, SQL*Loader and Oracle Data Pump, provide quick and convenient data access._
  

## Create an Autonomous JSON Database


- We will need an Autonomous JSON database to store our word collection in. Connect to your OCI Gen2 dashboard at https://cloud.oracle.com and navigate to **Oracle Database** - **Autonomous JSON Database**.

[![Select Autonomous JSON Database](https://i.postimg.cc/rFd4M2wb/Screenshot-2022-02-22-at-12-30-49.png)](https://postimg.cc/ZCSnxg3F)

- Click on **Create Autonomous Database**, change its name if you want to, and select *JSON*.

[![Database Settings 1](https://i.postimg.cc/9FG7rtyt/Screenshot-2022-02-22-at-13-05-48.png)](https://postimg.cc/hftjYmyf)

- Fill in your *admin password*, and leave everything else as default.

[![Database Settings 2](https://i.postimg.cc/WbRZNfq1/Screenshot-2022-02-22-at-13-06-04.png)](https://postimg.cc/jCX2vchp)

- Select *Secure access from everywhere* in order to be able to access your database from the Internet, and click on **Create Autonomous Database**.

[![Database Settings 3](https://i.postimg.cc/bYSbjjJ5/Screenshot-2022-02-22-at-13-06-18.png)](https://postimg.cc/V515jpX9)

- Once your database is up and running, click on its name and then on the *DB Connection* button, in order to download the wallet.

[![Download Wallet](https://i.postimg.cc/mgbLLQbn/Screenshot-2022-02-22-at-13-14-34.png)](https://postimg.cc/pp6bk55Q)


- Unzip the contents of your wallet in the `network/admin` folder inside your *Oracle Instant Client* installation. 

- Open `sqlnet.ora` and change the following line:

```

WALLET_LOCATION = (SOURCE = (METHOD = file) (METHOD_DATA = (DIRECTORY="?/network/admin")))

```

- To the actual directory where Oracle Instant Client is installed.

Example:

```

WALLET_LOCATION = (SOURCE = (METHOD = file) (METHOD_DATA = (DIRECTORY="/Users/llixandru/oracle/instantclient/network/admin")))

```


### Create a Collection and import your JSON


- Now we need to create a collection and import a JSON containing our 5-letter words. In order to connect to the JSON Database from the OCI Gen2 console, click on *Database Actions* and then on *JSON*.

[![Manage JSON Database](https://i.postimg.cc/JzP1GG0z/Screenshot-2022-02-22-at-13-15-41.png)](https://postimg.cc/PCvG7f1g)

- In the new webpage that opens, click on *Create Collection* and give your collection a name. You can also make this collection MongoDB compatible by checking the respective box.

[![Create Collection](https://i.postimg.cc/sXBDFsVD/Screenshot-2022-02-22-at-13-18-04.png)](https://postimg.cc/9RhjZ3Rv)

- Once the collection has been created, we can import a JSON containing our documents (each word will be a document in our usecase).

[![Import JSON](https://i.postimg.cc/WbcpyBxT/Screenshot-2022-02-22-at-13-18-34.png)](https://postimg.cc/kDwd6pnp)


>Example JSON

```

[{"word":"ABATE"},{"word":"IMPLY"},{"word":"WRIST"},{"word":"YOUNG"},{"word":"ZEBRA"}]

```


## SODA Database Connection


[Oracle Database Simple Oracle Document Access (SODA)](https://cx-oracle.readthedocs.io/en/latest/api_manual/soda.html#) allows documents to be inserted, queried, and retrieved from Oracle Database using a set of NoSQL-style cx_Oracle methods. By default, documents are JSON strings.

Next, let's look at how we can use SODA to easily connect to our database and get the data.

- First, let's create a file called, for example, *json_db_env.py* where we will store our database credentials. The user is *admin*, the password is the one you used for the database creation and the DSN is one of the 5 options available in your `tnsnames.ora` file in the wallet you have downloaded.

```

import os

# Oracle Instant Client Location
lib_dir=os.environ.get("HOME")+"/oracle/instantclient"

# Connection details

user="admin"
password="[PASSWORD]"
dsn="[DATABASENAME_tp]"

```

- Next, we'll create a file called `ajd_connection.py` which will actually handle the database connection and query a random word using SODA, from the cx_Oracle library.


```

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

```

In the code snippet above, you can see two methods defined, one that handles the connection to the database, and the second which returns a random document (representing a word in our case).


## Writing the Wordle Python code

And lastly, let's put all of that together. We'll create a third file called `wordle.py` where we will code the main game functionality.


```

# Wordle example in Python

import re
from rich.console import Console
import ajd_connection as word

console = Console()

# Function to compare the letters and display the squares

def compare(a, b):
    for x, y in zip(a, b):
        if x == y:
          console.print("🟩", end = '')
        elif b.find(x) <= 0: 
          console.print("⬛", end = '')
        else:
          console.print("🟨", end = '')

# Main

if __name__ == "__main__":

  # Get word from database
  w = word.get_word().lower()

  # Number of guesses = 6
  i = 6

  while i >= 1:
    guess = console.input("\nGuess: ").lower()
    try:
      # Check if input word is exactly 5 letters
      assert len(guess) == 5, console.print("Your guess should be a 5-letter word.")
      # Check if input word only contains allowed characters
      assert re.match("^[a-z]*$", guess), console.print("Your guess should only contain letters.")
    except Exception as e:
      continue

    compare(guess, w)
    
    if guess == w:
        console.print("\nWell done!")
        i = 1
    elif i == 1:
      console.print("\nGood tries! The answer was: " + w)  
    i -= 1

```


## Execution

- Run the code with:
  

```


$ python3 wordle.py


```

[![Wordle execution](https://i.postimg.cc/BZCqMHjN/Image-22-02-2022-at-11-53.jpg)](https://postimg.cc/14fhzgcN)


_Hope you found this example interesting. Happy coding!_


> Written by Liana Lixandru.