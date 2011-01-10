# email-issues

email-issues is a small python script which will parse a local email directory
for new emails and add them to a github-projects issue tracker. Nothing fancy,
just doing one simple task. Emails are expected to be stored in the
[Maildir](http://en.wikipedia.org/wiki/Maildir) format, but the python
[mailbox](http://docs.python.org/py3k/library/mailbox.html) has support for
others if needed.

## install

get source code.

    $ git clone git://github.com/simonz05/email-issues.git
    $ cd email-issues

setup virtualenv and get dependencies.

    $ python contrib/bootstrap.py

add `settings.py`.

    $ mv settings_example.py settings.py
    $ vim settings.py

edit crontabs to run your script automatically.

    crontab -e

and add something like:

    */1 * * * * getmail --quiet
    */1 * * * * full/path/to/virtualenv/ve/bin/python /full/path/to/email-issues/ei.py

notice how we have to add the full path for the python interpreter and the
`ei.py`-file. 

## settings.py

`settings.py` should contain all of the following constants.

    GITHUB_USER = '<username>'        # simonz05
    GITHUB_API = '<api_key>'          # e4d909c290d0fb1ca068ffaddf22cbd0
    GITHUB_PROJ = '<project_name>'    # simonz05/email-issues
    MAIL_PATH_DIR = '<local_dir>'     # ~/mail/
