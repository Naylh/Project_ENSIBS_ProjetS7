# set base image (host OS)
FROM python:3.10

# Auteur : CHAPRON Lucas

# Create app directory
WORKDIR /usr/src/app

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

EXPOSE 8002
CMD ["python", "./app.py"]