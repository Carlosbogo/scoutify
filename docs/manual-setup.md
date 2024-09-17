# Manual setup
If you are unable to use Terraform to deploy the infrastructure automatically, you want to avoid enabling billing in the Google Cloud project, or you want to understand how to set up the infrastructure manually, you can follow the steps below.

## Requirements
In the Terraform setup, we deploy everything using Google Cloud services. However, if you do it manually you can use any cloud provider or even your local machine (using your local machine is discouraged: we reduce our load as much as possible, but getting your IP blocked is still a risk).

Also, keep in mind that using other cloud providers will require slight modifications to the code (for example, we download and upload files to Google Cloud Storage, so you will need to change the code to use the equivalent services in your cloud provider).

The following tools are required to set up the infrastructure manually:

- Google Cloud CLI - It allows us to interact with Google Cloud resources using the command line
  - [Installation](https://cloud.google.com/sdk/docs/install).
  - [Documentation](https://cloud.google.com/sdk/gcloud).

- Docker - We will containerize all our services through Docker, allowing for a more consistent and reproducible environment.
  - [Installation](https://docs.docker.com/get-docker/).
  - [Documentation](https://docs.docker.com/).

- Python 3.11 - The code is written in Python 3.11, and it is the version we will use to run our code.
  - [Installation](https://www.python.org/downloads/).
  - [Documentation](https://docs.python.org/3/).
  - [Python 3.11 download](https://www.python.org/downloads/release/python-3110/).

- Poetry - We will use Poetry to manage our Python dependencies.
  - [Installation](https://python-poetry.org/docs/#installation).
  - [Documentation](https://python-poetry.org/docs/).


## Set up
1. **Create a Google Cloud Platform account and project**

   - Go to the [Google Cloud Console](https://cloud.google.com) and create an account.
   - Create a new project.

2. **Download the code**

   - Clone the repository by running `git clone`.
   - Change into the `src` directory by running `cd companies-scraper`.
   - Install the dependencies by running `poetry install`.

3. **Set up the Google Cloud CLI**

    - Install the Google Cloud CLI by following the instructions [here](https://cloud.google.com/sdk/docs/install).
    - Authenticate the CLI by running `gcloud auth login`.
    - Set the default project by running `gcloud config set project PROJECT_ID`, replacing `PROJECT_ID` with the ID of the project you created.

4. **Set up Docker**

    - Install Docker by following the instructions [here](https://docs.docker.com/get-docker/).
    - Start the Docker daemon by running `Docker Desktop` if you are on Windows or Mac or by running `sudo systemctl start docker`.
    - Check that Docker is running by running `docker --version`.
    - Set up Google Container Registry by running `gcloud services enable containerregistry.googleapis.com`.
    - Configure Docker to authenticate with the Google Container Registry by running `gcloud auth configure-docker`.
    - Build the Docker image by `cd`ing into the `src` directory and running `docker-compose build`.
    - Push the Docker image to the Google Container Registry by running `docker-compose push -t gcr.io/PROJECT_ID/companies-scraper`, replacing `PROJECT_ID` with the ID of the project you created.

5. **Set up the Google Cloud Storage Bucket**

    - Create a Google Cloud Storage bucket by running `gsutil mb -p PROJECT_ID -c STANDARD -l LOCATION -b on gs://BUCKET_NAME`, replacing `PROJECT_ID` with the ID of the project you created, `LOCATION` with the location of the bucket, and `BUCKET_NAME` with the name of the bucket.
    - Set the bucket to be publicly accessible by running `gsutil iam ch allUsers:objectViewer gs://BUCKET_NAME`.
    - Upload the `companies.csv` file to the bucket by running `gsutil cp companies.csv gs://BUCKET_NAME`.

6. **Set up environment variables**

   - Create a file named `.env` in the root of the `src` directory.
   - Add the following environment variables to the `.env` file:
     ```bash
    GCP_PROJECT = <PROJECT_ID>
    INPUT_BUCKET_NAME = <BUCKET_NAME>
    RATINGS_BUCKET_NAME = <BUCKET_NAME>
    DOWNLOADS_FOLDER = "/app/data"
     ```
     Replace `PROJECT_ID` with the ID of the project you created and `BUCKET_NAME` with the name of the bucket you created. For this tutorial we have restricted the storage bucket to be the same for both input and output, but you can change it if you want.

7. **Deploy the Cloud Compute instance**

    - Create a Cloud Compute instance by running `gcloud compute instances create-with-container INSTANCE_NAME --container-image gcr.io/PROJECT_ID/companies-scraper --zone ZONE --machine-type e2-micro`, replacing `INSTANCE_NAME` with the name of the instance, `PROJECT_ID` with the ID of the project you created, and `ZONE` with the zone where we want it deployed. The `e2-micro` machine type is slower but it allows us to use the free tier, so feel free to change it to a more powerful machine type if you want.
    - SSH into the instance by running `gcloud compute ssh INSTANCE_NAME --zone ZONE`, replacing `INSTANCE_NAME` with the name of the instance and `ZONE` with the zone where the instance is deployed.
    - Check that the Docker image is running by running `docker ps`.
    - Check the logs of the Docker container by running `docker logs CONTAINER_ID`, replacing `CONTAINER_ID` with the ID of the container.
    - If everything is working correctly, you should see the logs of the container scraping the companies' information.

8. **Download the scraped data**

    - Download the scraped data by running `gsutil cp gs://BUCKET_NAME/ratings.csv ratings.csv`.
    - The `ratings.csv` file should now be in the current directory.
    - You can now analyze the data or use it for further processing.
