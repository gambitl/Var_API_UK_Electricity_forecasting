# 📈 UK Natural Gas Price Prediction Project

- [Project Overview](#-project-overview)
- [Architecture](#architecture)
- [Pipeline Testing](#pipeline-testing)
- [Configuration and Deployment](#configuration-and-deployment)
- [Application Link](#application-link)
- [Documentation](#documentation)

## Project Overview

This project focuses on deploying a multivariate time series model for predicting the price of natural gas in the UK. The model is built using the `statsmodels` library.

**Note**: As of now, the application has issues with image display and CSS styling (28/05/2023).
You can test the styling by running the code locally:
   1. Go to the `main.py` file in the `web_app` directory.
   2. Launch the online proxy via SSH (see configuration & deployment, point 5).
   3. Modify the very last line.

## Architecture

The project is deployed on Google Cloud Platform (GCP) using the following services:

1. 📂 **Google Cloud Storage**: Training data is stored in a dedicated Google Cloud Storage bucket.
2. 🐳 **API and Docker Container**: The model is made publicly accessible through an API hosted in a Docker container. It exposes an HTML page.
3. 🔨 **Google Cloud Build**: Continuous integration and deployment of the Docker container using Google Cloud Build.
4. ☁️ **Google Cloud Run**: Deployment of the Docker container on Google Cloud Run, allowing the execution of the API.
5. 🎛️ **Google Cloud Composer**: The Python DAG file located in the "dag_airflow" directory of the project is used to retrain the model every hour. The DAG runs on the Google Cloud Composer component.
6. 📊 **MLFlow**: Training metrics and artifacts, such as the model, are logged and stored using the MLFlow Python library. MLFlow data is stored in another dedicated Google Cloud Storage bucket.
7. 🗄️ **PostgreSQL**: MLFlow data is also backed up in a PostgreSQL database.
8. 💻 **Google Cloud Compute Engine**: The MLFlow component runs on a virtual machine created using Google Cloud Compute Engine.

## Pipeline Testing

The pipeline undergoes rigorous testing to ensure the quality of predictions and data used, focusing on the following aspects:

1. 📝 **API Request Testing**: API request endpoints are tested to ensure availability and reliability of the API.
2. 📊 **Training Data Statistical Testing**: Training data is subjected to statistical tests to verify its consistency and suitability for predictions.
3. 🧪 **Data Quality Testing**: Quality tests are performed on the data used, such as validity, completeness, and consistency checks.

**The test file is located in the 'test' directory.**

## Configuration and Deployment

1. 🚀 Create a project on Google Cloud Platform and set up the necessary services such as Google Cloud Build, Google Cloud Run, and Google Cloud Composer.
2. 📦 Create the necessary Google Cloud Storage buckets, one for storing the training data and another for backing up MLFlow outputs. Update the corresponding paths in the code.
3. ⚙️ Configure project-specific parameters such as GCP access credentials, paths to training data, etc.
4. 🖥️ Create a virtual machine on Google Cloud Compute Engine and set up the MLFlow environment.
5. 🗃️ Create a PostgreSQL database to store MLFlow data and configure connection parameters in the code. Run the following two commands to create a proxy between the database and the VM, and then create a bridge:
   1. ./cloud-sql-proxy --private-ip *project-name*:*db-name*
   2. mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://*instance-name*:*instance-password*@*proxy-listening-address*:5432/*db-name* --default-artifact-root gs://*artifact-storage-bucket-name*
6. 🔄 Set up the Airflow DAG by importing the Python DAG file located in the "dag_airflow" directory of the project through the Composer interface.
7. 🚢 Build the Docker container using Google Cloud Build (you can set up automatic CI by linking your GIT repo as we did) and deploy it on Google Cloud Run.

## Application Link

**Our application is available here**: https://test-api-one-shot-vilcobbika-od.a.run.app/

## Documentation

Detailed documentation on setting up various cloud services and the steps to follow can be found in the `docs` folder of the project. 📚

