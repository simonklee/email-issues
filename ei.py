#!/home/simon/src/email-issues/ve/bin/python
import email
import mailbox
import sys

from github2.client import Github
try:
    from settings import SETTINGS
except ImportError:
    exit('Usage: You must add a settings.py file to your project, see readme.md\n')

inbox = mailbox.Maildir(SETTINGS['MAIL_PATH_DIR'])
github = Github(
    username=SETTINGS['GITHUB_USER'],
    api_token=SETTINGS['GITHUB_API'],
    requests_per_second=1)

def read(m_str):
    m = email.message_from_string(m_str)
    return {
        'message': m.get_payload(),
        'subject': m['subject'] if m['subject'] else 'no subject'}

def read_messages():
    messages = dict()
    for k in inbox.keys():
        m = read(inbox.get_string(k))
        messages[k] = m
    return messages

def remove_messages(messages):
    for k in messages.keys():
        inbox.remove(k)
    inbox.flush()

def add_issues(project=SETTINGS['GITHUB_PROJ']):
    messages = read_messages()
    if not messages:
        return

    issues = dict(((i.title, i.number) for i in github.issues.list(project)))
    for m in messages.values():
        print m['subject']
        if m['subject'] in issues.keys():
            github.issues.comment(project, issues[m['subject']], m['message'])
        else:
            github.issues.open(project, title=m['subject'], body=m['message'])
    remove_messages(messages)

if __name__ == '__main__':
    add_issues()
    inbox.close()
