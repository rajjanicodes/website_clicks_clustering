# Website Click Clustering

This is a FastAPI app to cluster the clicks made on a website. 

## Problem Statement:

We want to understand user clicking patterns. We have multiple webpages and users often click parts of the webpage and we want to cluster the clicks by location.

## Requirements:
- Clicks are coming in as a stream. Clustering should be happening online as new clicks come in.
- The clustering algorithm should be smart enough to understand whether the coordinates belong to
an existing cluster or to a new cluster.
- The clusters will be distinct, will never overlap, and will never have any ambiguity.

## Input format:
The API calls will contain:
- The location of a click, i.e (x, y) coordinates between 0 and 1. (float)
- the page_uuid. We might have multiple pages and each page will have different clusters. (string)
The data models for the input are stored in app/data_models.py

## Solution:
  Making an API that will take the inputs as described above and clusters the clicks by pages, and saves the clicks in the PostgreSQL DB. The API Endpoints are described as under.
  
### API Endpoints
- ``save_click_and_predict_cluster_api``: This function takes coordinates of clicks and the page_uuid of the pafe on which the click as made. It assigns a cluster to coordinates or creates a new cluster id for an outlier. The cluster ids are zero-indexed incremental integers.

- ``predict_cluster_api``: This function take the coordinates of a click and predicts their cluster. It returns ``null`` if it does not fall in any of the cluster. It does not store any data into the database.

## Added Files:

- ``/app/config.py`` : Config file for the constants.
- ``/app/database/table_functions_file.py`` : All the functions for altering the table are written here.

## Best Practices Used:
These are the best practices I tried to implement:

- PEP8 variable naming conventions followed.
- Line length limited to 79 characters (a handful of exceptions are present, where the code looks better otherwise.)
- Same linespace for comments and docstrings.
- Sorted imports as per Standard > Third-party > Custom, and alphabetically, within them.
- Modular file structure.
- Avoided hard coding.
- Constants imported from config.

I used black and pycodestyle for code formatting.

## Clustering Algorithm Used:
### ✨ DBSCAN ✨

Most webpages have rectangular buttons but algorithms like KNN make circular clusters. Moreover, DBSCAN ensures there is no overlap making it the best choice for this application.
