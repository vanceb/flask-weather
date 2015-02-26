# flask-weather
Python Flask webapp to provide web service of the weather data. The app will use MongoDB as its backing store

## Aim
Create a webapp that can receive weather reading updates, summarize the data, and provide restful access to the data

## Configure and Run

### Get a MongoDB instance with persistent data store

#### Create the data container

    sudo docker run -d \
                    -v /data \
                    --name data-mongo \
                    mongo \
                    mkdir /data/db

#### Create the MongoDB container

    sudo docker run -d \
                    --restart always\
                    --volumes-from data-mongo \
                    --name mongodb \
                    mongo

### Build the Python app docker container

    sudo docker build -t vanceb/weather-logger .

### Run the Python app and link to MongoDB container

    sudo docker run -d \
                    --restart always\
                    --link mongodb:mongodb \
                    -p 5000:5000 \
                    --name weather-logger \
                    vanceb/weather-logger
