from flask import Flask, g, request
from mongokit import Connection
from os import environ
from bp.logger import logger
from reverseproxy import ReverseProxied


try:
    # Get MongoDB config from Docker environment variables
    MONGODB_HOST = environ['MONGODB_PORT_27017_TCP_ADDR']
    MONGODB_PORT = int(environ['MONGODB_PORT_27017_TCP_PORT'])
except:
    # Use defaults instead
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017

DEBUG = True

# Create the app and register Blueprints
app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.debug = DEBUG
app.config.from_object(__name__)
app.register_blueprint(logger)

# Global variable to hold the MongoClient connection
db = None

# Function to return the connection to the MongoDB
def get_connection():
    global db
    if db is None or not db.alive():
        app.logger.info('Opening Connection to MongoDB at %s:%s' % (app.config['MONGODB_HOST'], app.config['MONGODB_PORT']))
        try:
            db = Connection(app.config['MONGODB_HOST'], app.config['MONGODB_PORT'])
            app.logger.debug('Successfully opened connection to MongoDB')
        except Exception, e:
            app.logger.critical("Failed to open connection to MongoDB. Error: %s" % str(e))
            raise e
    else:
        app.logger.debug('Reusing existing MongoDB connection')
    return db

# Before the request place useful objects onto the shared request context
@app.before_request
def before_request():
    app.logger.debug("doing pre-request")
    app.logger.debug(
        '\t'.join([request.remote_addr, request.method, request.url, request.data, ','.join([': '.join(x) for x in request.headers])])
    )
    g.log = app.logger
    g.connection = get_connection()

# Commented out decorator as the app context seems to be
# destroyed after each request causing each request to make a
# new connection to MongoDB - TODO May need more investigation
#@app.teardown_appcontext
def teardown_connection(exception):
    connection = getattr(g, 'connection', None)
    if connection is not None:
        connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
