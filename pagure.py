import requests
import json


class Pagure:
    base_pagure_url = "https://pagure.io"

    def __init__(self, repo_name, auth_token=None):
        self.repo_name = repo_name
        self.auth_token = auth_token
        self.header_params = {
            "Content-Type": "application/json",
            "Authorization": "token {0}".format(auth_token)
        }

    def get_issues_from_pagure(self, status="Open", since=None, order="asc"):
        api_end_point = "/api/0/{0}/issues".format(self.repo_name)
        params = {
            "per_page": "5",
            "status": status,
            "order": order
        }

        if since:
            params["since"] = since

        results = []
        issues_url = self.base_pagure_url + api_end_point

        page = 1

        while True:
            params['page'] = page

            result = requests.get(url=issues_url, params=params, timeout=5).json()

            results.extend(result['issues'])

            if result['pagination']['page'] == result['pagination']['pages']:
                break

            #TODO: Remove the following line
            if page == 1:
                break

            page += 1

        return results

    def add_comment(self, issue_id, comment):
        api_end_point = "/api/0/{0}/issue/{1}/comment".format(self.repo_name, issue_id)

        body_params = {
            "comment": comment
        }

        add_comment_url = self.base_pagure_url + api_end_point

        result = requests.post(url=add_comment_url,
                               data=json.dumps(body_params),
                               headers=self.header_params)

        if "Comment added" in result.text:
            print("Successfully added comment to issue #{0}".format(issue_id))
        else:
            print("Failed to add migration comment to issue #{0}".format(issue_id))

    def change_issue_status(self, issue_id, status="Closed", close_status=""):

        api_end_point = "/api/0/{0}/issue/{1}/status".format(self.repo_name, issue_id)

        body_params = {
            "status": status
        }

        if close_status.strip():
            body_params["close_status"] = close_status

        change_issue_status_url = self.base_pagure_url + api_end_point

        result = requests.post(url=change_issue_status_url,
                               data=json.dumps(body_params),
                               headers=self.header_params)

        if "status updated" in result.text:
            print("Successfully closed Pagure issue #{0}".format(issue_id))
        else:
            print("Failed to close {0} issue".format(issue_id))
