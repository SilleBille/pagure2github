# --- BEGIN COPYRIGHT BLOCK ---
# Copyright (C) 2020
#
# Authors:
#   Simon Pichugin <simon.pichugin@gmail.com>
#   Dinesh Prasanth M K <dmoluguw@redhat.com>
#
# All rights reserved.
#
# License: GPL (version 3 or any later version).
# See LICENSE for details.
# --- END COPYRIGHT BLOCK ---

import textwrap
from libpagure import Pagure

class PagureWorker:
    def __init__(self, repo, api_key, log):
        self.api = Pagure(pagure_token=api_key, repo_to=repo)
        self.log = log

    def comment_on_issue(self, pg_issue_id, gh_issue_id, g_repo):
        msg = textwrap.dedent(
            f"""
        dogtagpki is moving from Pagure issues to Github issues. This means that new issues
        will be reported only in [dogtagpki's github issues](https://github.com/{g_repo}/issues).

        This issue has been cloned to Github and is available here:
        - https://github.com/{g_repo}/issues/{gh_issue_id}

        If you want to receive further updates on the issue, please navigate
        [to the github issue](https://github.com/{g_repo}/issues/{gh_issue_id})
        and click on `subscribe` button.

        Thank you for understanding. We apologize for any inconvenience.
        """
        ).strip()
        self.log.info(f"Updating issue {pg_issue_id} with {gh_issue_id}")
        self.api.comment_issue(pg_issue_id, msg)

    def close_issue(self, pq_issue_id, status=None):
        # Close the status as Migrated/Fixed, only if the issue is NOT closed
        if not self.api.issue_info(pq_issue_id)['close_status']:
            if status is None:
                status = "Fixed"
            self.log.info(f"Closing issue {pq_issue_id} with '{status}' status")
            self.api.change_issue_status(pq_issue_id, "Closed", status)
