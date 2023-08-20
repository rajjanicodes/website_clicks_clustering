# RAFT Assignment (Website Click Clustering)

This is a FastAPI app to cluster the clicks made on a website, as given in the assignment.  

## API Endpoints
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

## Comments:
This project was a challenging task. I loved doing it.  
*Never use inverted commas while naming objects in SQL* was a lesson I learnt the hard way.

Happy grading!
