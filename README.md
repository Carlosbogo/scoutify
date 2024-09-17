# Companies Scraper

One of the biggest challenges when looking for new job opportunities is to find out where to apply. Thousands of new job openings are posted in LinkedIn each day, and it's impossible to get through all of them.

What's worse, LinkedIn search is not remotely perfect, and it can hinder job search quite a lot, and there is no way to check about some of the most important characteristics of a company inside LinkedIn (such as employees reviews, average salaries or even some positions that might be posted only in the company's website).

The idea of this repository is to figure out a way to automate some of the most frustrating parts of finding a new job. That starts with figuring out which companies are the ones you want to apply to, which is not a trival task. Currently we tackle that issue by using Selenium to automate getting relevant information of each company. This allows you to spend the time you would use up looking up those details into taking a well informed decision on which companies you should further investigate, and potentially apply to.

## Requirements

- Google Cloud Platform (Account and Project) - As mentioned earlier, to run the code without any changes we will need to have a GCP account and a project into which we can deploy the resources. Although not strictly necessary, [enabling billing](https://cloud.google.com/billing/docs/how-to/modify-project) in our project will make the set up much simpler and quicker.
  - [Google Cloud Console](https://cloud.google.com)
  - [Documentation](https://cloud.google.com/docs).
  - [Free tier](https://cloud.google.com/free).
- Google Cloud CLI - It allows us to interact with Google Cloud resources using the command line
  - [Installation](https://cloud.google.com/sdk/docs/install).
  - [Documentation](https://cloud.google.com/sdk/gcloud).
- Docker - We will containerize all our services through Docker, allowing for a more consistent and reproducible environment.
  - [Installation](https://docs.docker.com/get-docker/).
  - [Documentation](https://docs.docker.com/).
- Python 3.11 - The code is written in Python 3.11, and it is the version we will use to run our code.
  - [Installation](https://www.python.org/downloads/).
  - [Documentation](https://docs.python.org/3/).
- Poetry - We will use Poetry to manage our Python dependencies.
  - [Installation](https://python-poetry.org/docs/#installation).
  - [Documentation](https://python-poetry.org/docs/).
- Selenium - We will use Selenium to automate the scraping of the companies' information.
  - [Installation](https://selenium-python.readthedocs.io/installation.html).
  - [Documentation](https://selenium-python.readthedocs.io/).
- Terraform - We will use Terraform to manage our infrastructure as code. We will only be able to use it if we allow billing in our GCP project.
  - [Installation](https://learn.hashicorp.com/tutorials/terraform/install-cli).
  - [Documentation](https://learn.hashicorp.com/collections/terraform/gcp-get-started).

 ## Set up

1. **Create a Google Cloud Platform account and project**

   - Go to the [Google Cloud Console](https://cloud.google.com) and create an account.
   - Create a new project.
   - Enable billing in the project.

2. **Enable the necessary APIs**
   - Go to the [APIs & Services](https://console.cloud.google.com/apis/dashboard) section in the Google Cloud Console.
   - Enable the following APIs:
     - Cloud Compute Engine API
     - Docker Registry API
     - Cloud Run API

3. **Set up the Google Cloud CLI**
   - Install the Google Cloud CLI by following the instructions [here](https://cloud.google.com/sdk/docs/install).
   - Authenticate the CLI by running `gcloud auth login`.
   - Set the default project by running `gcloud config set project PROJECT_ID`, replacing `PROJECT_ID` with the ID of the project you created.

4. **Set up Docker**
    - Install Docker by following the instructions [here](https://docs.docker.com/get-docker/).
    - Start the Docker daemon by running `Docker Desktop` if you are on Windows or Mac or by running `sudo systemctl start docker`.
    - Check that Docker is running by running `docker --version`.

5. **Set up Python**
    - Install Python by following the instructions [here](https://www.python.org/downloads/).
    - Check that Python is installed by running `python --version`.
    - Install Poetry by following the instructions [here](https://python-poetry.org/docs/#installation).
    - Check that Poetry is installed by running `poetry --version`.

6. **Download the code**
    - Clone the repository by running `git clone`.
    - Change into the `src` directory by running `cd companies-scraper`.
    - Install the dependencies by running `poetry install`.

After following these steps, you should have all the necessary tools installed and the code downloaded. You can now start deploying the infrastructure and running the code.

The Terraform code is located in a different repository for security reasons. If you want to access it, please contact me. However, it is also possible to manually create the infrastructure and run the code without using Terraform by following the instructions in the `docs/manual-setup.md` file.
