# pagure2github

Fork of [droideck/patogith](https://github.com/droideck/patogith). Original credits to [Simon Pichugin](https://github.com/droideck)

A simple tool for Pagure issues to GitHub issues migration.

*Remember to test the process before doing it on production!*

## Installation

The library is re-written with dogtagpki/pki repository in mind. You need to change a few things to make it work for your repo.
Please, go to `lib/patogith/__init__.py`, look at the comment section at the top of the file and modify it according to your needs.

`pagure2github` can be installed using `pip`. Run from the root repo directory:

    python3 -m pip install ./

## Usage

First, go to your repo and clone Pagure issues to the working directory. You can find the links if
you got to your pagure repository web page (i.e. https://pagure.io/dogtagpki) and click on `Clone` button.

    git clone ssh://git@pagure.io/tickets/dogtagpki.git tickets

And then, you can just run the program.
`pagure2github` is an interactive tool. Simply run it and answer the questions:

    pagure2github create-gh-issues         # Stage 1. Create GitHub issues using Pagure info
    pagure2github update-pagure            # Stage 2. Update Pagure issues
    pagure2github update-bugzillas         # Stage 3. Update Bugzillas
    pagure2github close-unused-milestones  # Stage 4. Close Unused Milestones
    pagure2github check-issue-statuses     # Stage 5. Check that all issues have the right statuses
    pagure2github fix-references-comments  # Stage 6. Replace issue/PR links with \#0000 references
    pagure2github fix-documentation-files  # Stage 7. Replace Pagure links with GitHub links in a tree
