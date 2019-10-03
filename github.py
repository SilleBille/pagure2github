import requests
import utils
import json


class Github:
    base_github_url = "https://api.github.com"

    def __init__(self, repo_name_space, repo_name, auth_token):
        self.repo_name_space = repo_name_space
        self.repo_name = repo_name
        self.header_params = {
            "Content-Type": "application/json",
            "Authorization": "token {0}".format(auth_token)
        }

    def create_gh_comment(self, issue_number, comment):
        api_end_point = "/repos/{0}/{1}/issues/{2}/comments".format(self.repo_name_space, self.repo_name, issue_number)

        create_issue_comment_url = self.base_github_url + api_end_point

        print(create_issue_comment_url)

        comment_content = utils.GH_COMMENT_TEMPLATE.format(
            comment['user']['name'],
            utils.convert_epoch_to_timestamp(int(comment['date_created'])),
            comment['comment']
        )

        # Remove @ to avoid unnecessary notification to the upstream users
        body_params = {
            "body": comment_content.replace('@', '')
        }

        response = requests.post(url=create_issue_comment_url,
                                 data=json.dumps(body_params),
                                 headers=self.header_params)

        if response.status_code == 201:
            print("Comment created successfully for issue: {0}".format(issue_number))
        else:
            print("Comment creation failed for issue {0} with status code {1}".format(issue_number, response.status_code))

    def create_gh_issue(self, record):

        api_end_point = "/repos/{0}/{1}/issues".format(self.repo_name_space, self.repo_name)

        create_issue_url = self.base_github_url + api_end_point

        issue_title = record["title"]
        issue_desc = utils.GH_ISSUE_DESC_TEMPLATE.format(
            record["id"], record["user"]["name"],
            utils.convert_epoch_to_timestamp(int(record["date_created"])),
            record["content"])

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

        response = requests.post(url=create_issue_url, data=json.dumps(body_params), headers=self.header_params)

        print (response.json())

        if response.status_code == 201:
            print('Created new GH issue for: {0}'.format(str(record['id'])))
            return response.json()['number']
        else:
            print("Something went wrong while processing issue: {0}".format(
                str(record['id'])))
            print("Received response: " + str(response.status_code))
            return -1

