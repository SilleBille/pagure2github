import requests


class Pagure:
    base_pagure_url = "https://pagure.io"

    def __init__(self, repo_name, auth_token=None):
        self.repo_name = repo_name
        self.auth_token = auth_token

    def get_issues_from_pagure(self, status="Open", since=None, order="asc"):
        params = {
            "per_page": "5",
            "status": status,
            "order": order
        }

        if since:
            params["since"] = since

        api_end_point = "/api/0/{0}/issues".format(self.repo_name)

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
