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
        Dogtag PKI is moving from Pagure issues to GitHub issues. This means that existing or new
        issues will be reported and tracked through Dogtag PKI's [GitHub Issue tracker](https://github.com/{g_repo}/issues).

        This issue has been cloned to GitHub and is available here:
        https://github.com/{g_repo}/issues/{gh_issue_id}

        If you want to receive further updates on the issue, please navigate to the
        [GitHub issue](https://github.com/{g_repo}/issues/{gh_issue_id}) and click on `Subscribe` button.

        Thank you for understanding, and we apologize for any inconvenience.
        """
        ).strip()
        self.log.info(f"Updating issue {pg_issue_id} with {gh_issue_id}")
        self.api.comment_issue(pg_issue_id, msg)

    def close_issue(self, pq_issue_id, status=None):
        # Close the status as Migrated/Fixed, only if the issue is NOT closed
        if self.api.issue_info(pq_issue_id)['status'].lower() == 'open':
            if status is None:
                status = "Fixed"
            self.log.info(f"Closing issue {pq_issue_id} with '{status}' status")
            self.api.change_issue_status(pq_issue_id, "Closed", status)
