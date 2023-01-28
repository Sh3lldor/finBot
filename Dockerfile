# Start by pulling the python image
FROM python:3.10.8

# Copy the requirements file into the image
RUN mkdir -p /finBot

# Switch working directory
WORKDIR /finBot
COPY . /finBot

# Install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# Configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

# Run redeye
CMD ["finBot.py"]