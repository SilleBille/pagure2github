# pagure2github

Fork of [droideck/patogith](https://github.com/droideck/patogith). Original credits to [Simon Pichugin](https://github.com/droideck)

A simple tool for Pagure issues to GitHub issues migration.

*Remember to test the process before doing it on production!*

## Installation

The library is re-written with dogtagpki/pki repository in mind. You need to change a few things to make it work for your repo.
Please, go to `lib/patogith/__init__.py`, look at the comment section at the top of the file and modify it according to your needs.

`pagure2github` can be installed using `pip`. Run from the root repo directory:

    python3 -m pip install ./

## Prerequisite

### Backup issues

First, go to your repo and clone Pagure issues to the working directory. You can find the links if
you got to your pagure repository web page (i.e. https://pagure.io/dogtagpki) and click on `Clone` button.

    git clone ssh://git@pagure.io/tickets/dogtagpki.git tickets

### Get the API keys

#### Github

1. Login to Github
2. Goto profile [settings](https://github.com/settings/profile)
3. Click [Developer Settings](https://github.com/settings/apps)
4. Click [Personal Access Tokens](https://github.com/settings/tokens)
5. Generate **New token** with appropriate scope

#### Pagure

1. Goto your intended repo. Example [dogtagpki](https://pagure.io/dogtagpki/)
2. Click on Settings (you need to have admin access on the repo to do this)
3. Click on [API Keys](https://pagure.io/dogtagpki/settings#apikeys-tab)
4. Click on **Create New API key** with appropriate permissions

**NOTE:** Though this API key is generated for project, this is specific to YOU (ie) comments/modifications made to any
tikcets will be done by YOU!

### Pagure Modifications

#### Set the pagure to read-only

1. Goto your intended repo. Example [dogtagpki](https://pagure.io/dogtagpki/)
2. Click on Settings (you need to have admin access on the repo to do this)
3. Click on **Project Options**
4. Check the **Issue tracker read only**
5. Make sure to clik on **update**

#### Create a new Close status: Migrated

1. Goto your intended repo. Example [dogtagpki](https://pagure.io/dogtagpki/)
2. Click on Settings (you need to have admin access on the repo to do this)
3. Click on **Close Status**
4. Add new close status **migrated**
5. Make sure to click on **update**

## Usage

Once you are done with all pre-requisite, you can just run the program one stage at a time:

`pagure2github` is an interactive tool. Simply run it and answer the questions:

    pagure2github create-gh-issues         # Stage 1. Create GitHub issues using Pagure info
    pagure2github check-issue-statuses     # Stage 2. Check that all issues have the right statuses
    pagure2github update-pagure            # Stage 3. Update Pagure issues
    pagure2github update-bugzillas         # Stage 4. Update Bugzillas
    pagure2github close-unused-milestones  # Stage 5. Close Unused Milestones
    pagure2github fix-references-comments  # Stage 6. Replace issue/PR links with \#0000 references
    pagure2github fix-documentation-files  # Stage 7. Replace Pagure links with GitHub links in a tree

### Stage 1: Copy issues from Pagure to Github

This stage **copies all Pagure issues to Github Issues**

    pagure2github -p <Pagure Repo> -g <Github Repo> -i <Log File> -v create-gh-issues

**NOTE:** The `<Log File>` will be used in all other stages. Please keep this handy and safe.

### Stage 2: Check if all issues have been copied correctly

This stage **checks if all the issues have been copied correctly** into Github Issues, by reading the `<Log File>`
generated in previous stage

    pagure2github -p <Pagure Repo> -g <Github Repo> -i <Log File> -v check-issue-statuses
