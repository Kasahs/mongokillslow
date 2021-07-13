# mongokillslow
Find and kill slow queries running on a mongodb cluster.

Usage as a script:

1. Setup the environment variables as provided in the .sample-env file
2. Install the python requirements `pip install -r requirements.txt`
3. run `python3 killslow.py`

Usage with docker:

1. `docker build -t killslow:1.0.0 .` to build the image
2. `docker run -it --env-file ./.env killslow:1.0.0` to run.

