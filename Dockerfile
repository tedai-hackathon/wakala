FROM python:3.11
# Use the python latest image
COPY . ./

ENV OPENAI_API_KEY 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
# Copy the current folder content into the docker image
RUN pip install chromadb flask gunicorn langchain openai python-dotenv tiktoken
# Install the required packages of the application
CMD gunicorn --bind :$PORT app:app
# Bind the port and refer to the app.py app