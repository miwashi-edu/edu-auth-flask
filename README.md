# edu-auth-flask

## Instructions

```bash
docker build -t auth-server .
docker run -p 3000:3000 --name auth-server auth-server 
```

## requirements.txt

```bash
cd ~
cd ws
cd auth-server
cat > requirements.txt << 'EOF'
Flask
PyJWT
flask_cors
EOF
```

## Dockerfile

```bash
cd ~
cd ws
cd auth-server
cat > Dockerfile << 'EOF'
# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 3000

# Define environment variables
ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Run the application
CMD ["python", "server.py"]
EOF
```
