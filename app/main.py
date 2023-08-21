from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
import numpy as np
from sklearn.cluster import DBSCAN
from starlette.routing import Route

from config import *
from data_models import NewClickRequest, NewClickResponse, PredictClickResponse
from database.instance import *
from database.table_functions_file import *

# --->  To create a fresh table everytime this class is instantiated
#       i.e. everytime the test.py is run.
table_functions.create_table()


async def version(request):
    return JSONResponse({"version": 0})


async def save_click_and_predict_cluster_api(request: NewClickRequest):
    """
    It assigns a cluster to click coordinates or creates a new cluster id.
    The cluster ids are zero-indexed incremental integers.

    This can be done in two modes:
    A>  Keeps track of assigned cluster_id, i.e. start cluster_id from 0 only
        once. (A is assumed here.)
    B>  Assign cluster_id pagewise. i.e. start cluster_id from 0, for every
        new page_uuid. To achieve B, we can pass: where=f"{current_page_uuid}"
        while fetching cluster_id.

    This will fetch an empty list for every new page_uuid, and will thus enter
    the except block.

    NOTE:   DBSCAN is the Clustering algorithm used as:
        1>  Most webpage buttons are of a rectangular shape. But other
            algorithms like knn are limited to circular clusters.

        2>  This also makes sure the clusters are not overlapped because
            of its shape.
    """

    # --->  Makes array from the variables of request.
    current_coordinates = (request.coordinates.x, request.coordinates.y)
    current_coordinates = np.array(current_coordinates, dtype=float).reshape(-1, 2)
    current_page_uuid = request.page_uuid

    # --->  Fetches x and y from the table as per only the current_page_uuid.
    previous_x = table_functions.fetch("x", where=f"{current_page_uuid}")
    previous_y = table_functions.fetch("y", where=f"{current_page_uuid}")

    # --->  Makes them into arrays and resizes them.
    previous_x = np.array(previous_x, dtype=float).reshape(-1, 1)
    previous_y = np.array(previous_y, dtype=float).reshape(-1, 1)

    # --->  Fetches cluster ids from the table, and finds the highest number
    #       from it. This is used to know the number of clusters already
    #       assigned. When running the code with an empty db, fetch will
    #       return an empty list, thus max function will not
    #       work. So, assigning -1 manually, which will become 0 after
    #       incrementing.
    try:
        latest_cluster_id = max(table_functions.fetch("cluster_id"))
    except ValueError:
        latest_cluster_id = -1
    except Exception as e:
        print(e)
        return {"Error": "Check Logs for Error."}

    previous_coordinates = np.column_stack((previous_x, previous_y))
    coordinates = np.concatenate(
            (previous_coordinates, current_coordinates), axis=0)
    is_new = False

    labels = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit_predict(coordinates)

    # --->  To find the label of the cluster of current_coordinates
    #       located at the end of labels list.
    cluster_id = labels[-1]

    # --->  If it is an outlier, the cluster_id WILL BE -1
    #       Call it the cluster_id of current_coordinates
    #       Increment the latest_cluster_id by 1.
    if cluster_id == -1:
        latest_cluster_id += 1
        cluster_id = latest_cluster_id
        is_new = True

    # --->  Store into the table.
    click_data = table_functions.table.insert().values(
        x=float(current_coordinates[0][0]),
        y=float(current_coordinates[0][1]),
        page_uuid=current_page_uuid,
        cluster_id=int(cluster_id),
    )
    with safe_session() as session:
        session.execute(click_data)

    return NewClickResponse(cluster_idx=cluster_id, is_new=is_new)


async def predict_cluster_api(request: NewClickRequest):
    """
    This function take the coordinates of a click and predicts their cluster.
    It returns ``null`` if it does not fall in any of the cluster.
    It does not store any data into the database.

    ``NOTE:`` DBSCAN is the Clustering algorithm used as:
        1>  Most webpage buttons are of a rectangular shape. But other
            algorithms like knn make circular clusters.

        2>  This also makes sure the clusters are not overlapped because
            of its shape.

    """
    current_coordinates = (request.coordinates.x, request.coordinates.y)
    current_coordinates = np.array(current_coordinates, dtype=float).reshape(-1, 2)
    current_page_uuid = request.page_uuid

    # --->  Fetches x and y from the table as per only the current_page_uuid.
    previous_x = table_functions.fetch("x", where=f"page_uuid = {current_page_uuid}")
    previous_y = table_functions.fetch("y", where=f"page_uuid = {current_page_uuid}")

    # --->  Makes them into arrays and resizes them.
    previous_x = np.array(previous_x, dtype=float,).reshape(-1, 1)
    previous_y = np.array(previous_y, dtype=float,).reshape(-1, 1)

    previous_coordinates = np.column_stack((previous_x, previous_y))
    coordinates = np.concatenate((previous_coordinates, current_coordinates), axis=0)

    labels = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit_predict(coordinates)

    # --->  To find the label of the cluster of current_coordinates
    #       located at the end of labels list.
    cluster_id = labels[-1]

    if cluster_id != -1:
        # --->  Returns the actual cluster_id. This point is not an outlier.
        return PredictClickResponse(cluster_idx=cluster_id)

    # --->  Returns null if it doesn't belong to any cluster. This means that
    #       the point is an outlier.
    return PredictClickResponse(cluster_idx=None)


prod_routes = [
    Route("/", endpoint=version, methods=["GET"]),
    APIRoute(
        "/save_click_and_predict_cluster",
        endpoint=save_click_and_predict_cluster_api,
        methods=["POST"],
    ),
    APIRoute(
        "/predict_cluster",
        endpoint=predict_cluster_api,
        methods=["POST"],
    ),
]

app = FastAPI(routes=prod_routes)
