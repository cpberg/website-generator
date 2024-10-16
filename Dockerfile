# Use a Python base image
FROM python:3.12

# Install Node.js and npm (which includes npx)
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npx

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Expose the relevant ports (if needed)
EXPOSE 3000

# Command to run your app (you can change this based on your app entry point)
CMD ["python", "main.py"]

