from pagure import Pagure
from github import Github
import os

if __name__ == "__main__":

    # Variables that needs to be modified based on the project
    pagure_repo = "dogtagpki"
    pagure_since_date = "2017-10-01"
    github_name_space= "SilleBille"
    github_repo_name = "pki"

    pg_token = os.environ["PG_TOKEN"]
    gh_token = os.environ["GH_TOKEN"]

    if pg_token is None:
        pg_token = input("Enter the Pagure Personal Access Token:")

    if gh_token is None:
        gh_token = input("Enter the Github Personal Access Token: ")

    p = Pagure(repo_name=pagure_repo, auth_token=pg_token)
    g = Github(repo_name_space=github_name_space, repo_name=github_repo_name, auth_token=gh_token)

    issues = p.get_issues_from_pagure(since=pagure_since_date)

    print(len(issues))
    for issue in issues:
        # Create corresponding GitHub Issues
        issue_number = g.create_gh_issue(record=issue)

        if issue_number < 0:
            exit(issue_number)

        # Add the comments to the newly create github issue
        for comment in issue['comments']:
            # Skip meta data comments
            if not comment['comment'].startswith("**Metadata Update from"):
                g.create_gh_comment(
                    issue_number=issue_number,
                    comment=comment
                )
