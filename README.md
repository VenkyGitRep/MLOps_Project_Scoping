Overview
========

Welcome to the Data pipeline group project. In this project, we will design and implement a data pipeline to orchestrate the data transfer from a local machine into cloud-based platform or GCP, more specifically. We used the Airflow, DBT and Soda to do this project. To be more specifically, we use the astro to help with the settings of the Airflow, cosmos to help with the integration between DBT and Airflow UI. Let's jump into the project!


Project Contents
================

Your Astro project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs. By default, this directory includes two example DAGs:
    - `example_dag_basic`: This DAG shows a simple ETL data pipeline example with three TaskFlow API tasks that run daily.
    - `example_dag_advanced`: This advanced DAG showcases a variety of Airflow features like branching, Jinja templates, task groups and several Airflow operators.
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

Deploy Your Project Locally
===========================

1. Start Airflow on your local machine by first installing the Astro. Astro is a package that helps developers set the Airflow locally:
   'brew install astro' and you can check your version of the astro by typing 'astro version'. You can also update your astro by using 'brew upgrade astro'.

2. Then after installing, you can start Airflow on your local machine by running 'astro dev init' to initialize your airflow project environment and type 'astro dev start' to start the project.

This command will spin up 4 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- Triggerer: The Airflow component responsible for triggering deferred tasks

3. Verify that all 4 Docker containers were created by running 'docker ps'

Note: Running 'astro dev start' will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either [stop your existing Docker containers or change the port](https://docs.astronomer.io/astro/test-and-troubleshoot-locally#ports-are-not-available).

4. Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with 'admin' for both your Username and Password.

You should also be able to access your Postgres Database at 'localhost:5432/postgres'.

5. To be available to use the repo, you also need to download the DBT and Soda onto your machine. The DBT(data build tool) and Soda are tools that help developers with data transformation and data quality checks. We also use the cosmos to make Airflow's UI more compatible with the DBT. We set all of them up in the requirement.txt and Dockerfile. The requirement.txt is to install the cosmos to connect with dbt and bigquery. The dockerfile is to download the soda and dbt venv into your astro development environment.

6. Before you do the transformation part of the data pipeline, you also need to create a new table in Bigquery. We add a new table in big query called country which includes all of the countries and phone num etc. We can do the transformation to the dataset in order to eliminate the null and outlier values. The sql query can be found in the query.txt.

our group use the dataset from Kaggle
=================================

The dataset is from kaggle called Online Retail and you can install the dataset though the install.py or by this link: https://www.kaggle.com/datasets/ulrikthygepedersen/online-retail-dataset.
Our data pipeline is trying to upload the dataset into the GCP and Google Bigquery. Do some transformations and data quality check by using Soda DBT and Soda.

The content of the Data Pipeline
=================================
![Blank diagram](https://github.com/VenkyGitRep/MLOps_Project_Scoping/assets/145687596/85742f7b-d02f-4b53-8e4b-0b0028a4ae2c)


The Airflow data pipeline
=======
![Screenshot 2024-03-13 at 3 58 33 AM](https://github.com/VenkyGitRep/MLOps_Project_Scoping/assets/145687596/728247dd-f5ef-443f-9262-392379e8df63)

