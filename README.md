# CMSC447-recipe-management

## 1: Getting set up to work locally (as of branch 13)

Hopefully, this gets updated before the project is submitted. While in development, though, it'll do

0. Install docker on your system and start the docker engine
1. Run `source installElasticDocker.sh` and `installMariaDBDocker.sh`
2. Run `docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic`. You should see a string outputted to the terminal, something like `kl61qgnh5BKN-bUL2s0x` -- this is the password for elasticsearch
3. Run `docker cp elasticsearch:/usr/share/elasticsearch/config/certs/http_ca.crt flask`
4. Copy the password from step 2 to the second value in the tuple declaring the basic_auth argument of ElasticSearch(...) in `elastic.py`. Yes, this is not best practice. If you're just running locally, it's not a big deal -- in any case, try to remember not to commit it.
5. Run `pip install -r flask/requirements.txt` and `pip install -r tests/requirements.txt`

At this point, you are ready to begin development

## 2: Initializing ElasticSearch and MariaDB

0. Start the ElasticSearch & MariaDB containers -- you can do this from docker desktop
1. Change directory to `flask` and run `python app.py [USERNAME] [PASSWORD]`. This sets the default user's username and password to whatever you passed as commandline arguments.
2. In your browser (or with a `GET` from curl) go to `localhost:5000/init` -- this will drop the database and elasticsearch, then refill them with the data from the CSV. They will be inserted under the default user, whose credentials were defined in step 1.

## 3: Running tests

1. Run `python tests/backend_tests.py`. You will be prompted for the password of the default user. This is essentially logging you into the system under that user, just directly instead of via the front end.

## Front End

0. ensure both node.js and npm are installed
    a. the node_modules folder must be populated and placed in the /recipe-manager directory
2. open a command prompt and navigate to /recipe-manager
3. run the command `npm run dev`, this will start the react app up, but not open it
4. Either click the pop-up that might appear to open in browser, otherwise enter `o` in the command prompt
5. this opens to the home page where all functions can be found
