To access the docker bot image at docker.hub please use: $ docker pull mathteacher/bot-app:latest

To launch the bot under the docker container please use

$ docker run -it -v [absolute path to the local folder data/ with json and pickle files]:/usr/local/data /mathteacher/bot-app

-it - this option allows us to use input() correctly. Without that we would have an "EOF Error" everytime when input() will be invoked.

-v - this option allow us to store the data outside the container. Without that we would rollout to the initial data when starting a new container (new copy of application).
