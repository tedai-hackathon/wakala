![alt text](https://github.com/tedai-hackathon/wakala/blob/main/media/banner.jpg)

# Wakala

![alt text](https://github.com/tedai-hackathon/wakala/blob/main/media/TEDAI.jpg)


## Installation and running locally

1. Create and activate a virtual environment

   ```sh
   virtualenv MY_ENV
   source MY_ENV/bin/activate
   ```

set FLASK_APP=newproj
set FLASK_ENV=development

1. Install packages with pip

   ```sh
   cd ad-gpt
   pip install -r requirements.txt
   ```

1. Set up your .env file

   - Duplicate `.env.example` to `.env`

1. Run the project

   ```sh
   flask --app run app
   ```

## Deploying to Google Cloud Run, requires CloudSDK and Google Cloud Project with billing enabled

1. Use Google builds command to create the docker image in the container registry

   ```sh
   gcloud builds submit --tag gcr.io/PROJECT_ID/langchain
   ```

1. Create a Cloud Run service

   ```sh
   gcloud run deploy --image gcr.io/PROJECT_ID/langchain --timeout=300 --platform managed
   ```

1. Verify the deployed cloud run service in the Google Cloud Console


gcloud builds submit --tag gcr.io/langflow-399804/langchain_wakala  
gcloud run deploy --image gcr.io/langflow-399804/langchain_wakala --timeout=300 --platform managed
gcloud run services update <name of app> --memory 1024Mi
