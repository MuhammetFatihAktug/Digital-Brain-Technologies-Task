FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y gcc libc-dev

# Copy all files to the container
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Run both the scraper and the Flask app
CMD ["sh", "-c", "python data_scraper.py && python app.py"]
