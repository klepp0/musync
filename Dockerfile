# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Install Poetry
RUN pip install poetry

# Install build dependencies
RUN apt-get update && apt-get install -y gcc python3-dev

# Set the working directory in the container
WORKDIR /app

# Copy only the poetry files to leverage Docker cache
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["poetry", "run", "uvicorn", "musync.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
