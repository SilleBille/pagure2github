import time

GH_ISSUE_DESC_TEMPLATE = "This issue was migrated from [Pagure Issue #{0}](https://pagure.io/dogtagpki/issue/{0}). " \
                         "Originally filed by **{1}** on *{2}*:\n\n {3}"
GH_COMMENT_TEMPLATE = "Posted by {0} on {1}: \n\n{2}"

PG_COMMENT_TEMPLATE = "This issue has been migrated to [Github Issue #{0}](https://github.com/{1}/{2}/issues/{0})."


def convert_epoch_to_timestamp(epoch_time):
    return time.strftime('%Y-%m-%d', time.localtime(epoch_time))
