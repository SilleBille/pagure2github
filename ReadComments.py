import requests
import time
import json

base_pagure_url = "https://pagure.io"
base_github_url = "https://api.github.com"


def get_issues_from_pagure(project_name):
    params = {
        "status": "Open",
        "since": "2017-10-20",
        "order": "asc",
        "per_page": "1"
    }
    api_end_point = "/api/0/{0}/issues".format(project_name)
    results = []

    issues_url = base_pagure_url + api_end_point

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


def create_gh_issue(repo_space, project_name, gh_token, record):

    api_end_point = "/repos/{0}/{1}/issues".format(repo_space, project_name)

    create_issue_url = base_github_url + api_end_point

    print(create_issue_url)

    header_params = {
        "Content-Type": "application/json",
        "Authorization": "token {0}".format(gh_token)
    }

    issue_title = record["title"]
    issue_desc = "Originally filed by {0} on {1}\n\n {2}".format(
        record["user"]["name"],
        time.strftime('%Y-%m-%d', time.localtime(int(record["date_created"]))),
        record["content"]
    )

    body_params = {
        "title": issue_title,
        "body": issue_desc
    }
    if record["assignee"]:
        body_params["assignee"] = record["assignee"]

    if len(record['tags']) > 0:
        for tag in record['tags']:
            body_params['labels'].append(tag)


    print(json.dumps(body_params))

    print(header_params)
    response = requests.post(url=create_issue_url, data=json.dumps(body_params), headers=header_params)

    if response.status_code == 201:
        print('Created new GH issue for: {0}'.format(str(record['id'])))
    else:
        print("Something went wrong while processing issue: {0}".format(
            str(record['id'])))
        print("Received response: " + str(response.status_code))
        return

    # Add comments



##
#
#     {
#       "assignee": null,
#       "blocks": [],
#       "close_status": null,
#       "closed_at": null,
#       "closed_by": null,
#       "comments": [],
#       "content": "The `CertSearchRequest` interface does not admit a search like \"not revoked\" - it only allows one (positive) status match at a time.  Another example is all revoked certs (regardless whether expired), because there are two statuses involved: `REVOKED` and `REVOKED_EXPIRED`.\r\n\r\nUpdate the relevant types, routines, API and CLI interfaces to allow richer filtering by status.\r\n\r\nSee related FreeIPA bug: https://pagure.io/freeipa/issue/7549",
#       "custom_fields": [],
#       "date_created": "1569383294",
#       "depends": [],
#       "id": 3109,
#       "last_updated": "1569383294",
#       "milestone": null,
#       "priority": null,
#       "private": false,
#       "status": "Open",
#       "tags": [],
#       "title": "Cert search: support multiple statuses",
#       "user": {
#         "fullname": "Fraser Tweedale",
#         "name": "ftweedal"
#       }
#     }


if __name__ == "__main__":
    gh_token = input("Enter the GH Personal Access Token: ")

    issues = get_issues_from_pagure(project_name="dogtagpki")

    print(len(issues))
    for issue in issues:
        create_gh_issue(repo_space="SilleBille", project_name="pki", gh_token=gh_token, record=issue)
