# Use an official Python runtime as a parent image
FROM python

# Set the working directory to /code
WORKDIR /code

COPY requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at /code
COPY ./app /code/app

# Define the command to run on container start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
