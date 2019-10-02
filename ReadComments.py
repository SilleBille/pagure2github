import requests
import time
import json

base_pagure_url = "https://pagure.io"
base_github_url = "https://api.github.com"


def create_gh_head(gh_token):
    header_params = {
        "Content-Type": "application/json",
        "Authorization": "token {0}".format(gh_token)
    }
    return header_params


def convert_epoch_to_timestamp(epoch_time):
    return time.strftime('%Y-%m-%d', time.localtime(epoch_time))


def get_issues_from_pagure(project_name):
    params = {
        "status": "Open",
        "since": "2017-10-20",
        "order": "asc",
        "per_page": "5"
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


def create_gh_comment(repo_space, project_name, issue_number, gh_token, comment):
    api_end_point = "/repos/{0}/{1}/issues/{2}/comments".format(repo_space, project_name, issue_number)

    create_issue_comment_url = base_github_url + api_end_point

    print(create_issue_comment_url)

    comment_content = "Posted by {0} on {1}: \n\n{2}".format(
        comment['user']['name'],
        convert_epoch_to_timestamp(int(comment['date_created'])),
        comment['comment']
    )

    body_params = {
        "body": comment_content.replace('@', '')
    }

    print(body_params)

    response = requests.post(url=create_issue_comment_url, data=json.dumps(body_params), headers=create_gh_head(gh_token))

    if response.status_code == 201:
        print("Comment created successfully for issue: {0}".format(issue_number))
    else:
        print("Comment creation failed for issue {0} with status code {1}".format(issue_number, response.status_code))


def create_gh_issue(repo_space, project_name, gh_token, record):

    api_end_point = "/repos/{0}/{1}/issues".format(repo_space, project_name)

    create_issue_url = base_github_url + api_end_point

    issue_title = record["title"]
    issue_desc = "This issue was migrated from [pagure ticket #{0}](https://pagure.io/dogtagpki/issue/{0}). " \
                 "Originally filed by {1} on {2}\n\n {3}".format(
        record["id"],
        record["user"]["name"],
        convert_epoch_to_timestamp(int(record["date_created"])),
        record["content"]
    )

    body_params = {
        "title": issue_title,
        "body": issue_desc.replace("@", "")
    }

    # Uncomment if assignee is required
    #if record["assignee"]:
    #    body_params["assignee"] = record["assignee"]["name"]

    if len(record['tags']) > 0:
        for tag in record['tags']:
            body_params['labels'].append(tag)

    print("BODY: " + json.dumps(body_params))

    response = requests.post(url=create_issue_url, data=json.dumps(body_params), headers=create_gh_head(gh_token))

    print (response.json())

    if response.status_code == 201:
        print('Created new GH issue for: {0}'.format(str(record['id'])))
    else:
        print("Something went wrong while processing issue: {0}".format(
            str(record['id'])))
        print("Received response: " + str(response.status_code))
        return

    # Add comments
    for comment in record['comments']:
        # Skip meta data comments
        if not comment['comment'].startswith("**Metadata Update from"):
            create_gh_comment(
                repo_space=repo_space,
                project_name=project_name,
                issue_number=response.json()['number'],
                gh_token=gh_token,
                comment=comment
            )


if __name__ == "__main__":

    gh_token = input("Enter the GH Personal Access Token: ")

    issues = get_issues_from_pagure(project_name="dogtagpki")

    print(len(issues))
    for issue in issues:
        create_gh_issue(repo_space="SilleBille", project_name="pki", gh_token=gh_token, record=issue)
