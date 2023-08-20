import json
import os
import random
import string
from glob import glob

import requests

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_URL = "http://localhost:8004"


def get_random_id():
    return "".join(random.choices(string.ascii_lowercase, k=12))


def run_test_case(casename: str):
    with open(casename, "r") as f:
        test_case = json.load(f)

    sequence = test_case["sequence"]
    # each sequence is defined by
    # req_name, args, response code, response data
    # then we send each request to the app
    # get the response and verify

    session_id = get_random_id()

    with requests.Session() as session:
        for seq in sequence:
            req_name = seq["req_name"]
            page_id = seq["page_id"]
            body = seq["body"]
            response_code = seq["response_code"]
            response_data = seq["response_data"]
            req_method = seq["method"]

            req_url = BASE_URL + "/" + req_name
            page_uuid = session_id + "/" + page_id

            if req_method == "GET":
                resp = session.get(req_url, params={"page_uuid": page_uuid, **body})
            elif req_method == "POST":
                resp = session.post(req_url, json={"page_uuid": page_uuid, **body})
            else:
                raise Exception("Invalid method")

            assert resp.status_code == response_code, "wrong response code"
            if response_code == 200:
                json_body = resp.json()
                assert response_data == json_body, "predict != expected"


def main():
    all_test_cases = list(glob(os.path.join(DIR_PATH, "cases", "*.json")))
    sorted(all_test_cases)
    cases_count = len(all_test_cases)
    for i, test_case_file in enumerate(all_test_cases):
        print("CASE", i + 1, "/", cases_count, end="\t")
        try:
            run_test_case(test_case_file)
            print("SUCCESS", test_case_file[len(DIR_PATH) + 1 :])
        except AssertionError as e:
            print(
                "FAILED Test case",
                test_case_file[len(DIR_PATH) + 1 :],
                "---",
                e,
            )
    print("DONE")


if __name__ == "__main__":
    main()
