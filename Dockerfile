# Use an official Python runtime as a parent image
FROM python:3.11
LABEL maintainer="Jakir Hossain, mdavir814@gmail.com"
RUN groupadd -r app &&\
    useradd -r -g app -d /home/app -s /sbin/nologin -c "Docker image user" app

# Install curl 

RUN apt-get update && apt-get install curl -y

# Set the working directory in the container

WORKDIR /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make port 1046 available to the world outside this container
EXPOSE 8000

# Define environment variable to hold the port number
ENV PORT=8000
USER app

# Run uvicorn when the container launches. Use the --host flag to bind uvicorn
# to 0.0.0.0 so that it's accessible from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
