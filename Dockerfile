FROM python:3.9-alpine

# create user
RUN adduser -D killslow killslow -h /home/killslow

# switch user
USER killslow

# change working dir
WORKDIR /home/killslow

# copy requirements file
ADD ./requirements.txt ./

# copy scripts
ADD ./killslow.py ./

# install dependencies
RUN pip install -r requirements.txt

# setup entrypoint
CMD ["python3", "./killslow.py"]




