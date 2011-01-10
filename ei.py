import email
import mailbox
import sys

from github2.client import Github
try:
    import settings
except ImportError:
    exit('Exit: You must add a settings.py file to your project, see readme.md\n')

inbox = mailbox.Maildir(settings.MAIL_PATH_DIR)
github = Github(
    username=settings.GITHUB_USER,
    api_token=settings.GITHUB_API,
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

def add_issues(project=settings.GITHUB_PROJ):
    messages = read_messages()
    if not messages:
        return

    issues = dict(((i.title, i.number) for i in github.issues.list(project)))
    for m in messages.values():
        if m['subject'] in issues.keys():
            github.issues.comment(project, issues[m['subject']], m['message'])
        else:
            github.issues.open(project, title=m['subject'], body=m['message'])
    remove_messages(messages)

if __name__ == '__main__':
    add_issues()
    inbox.close()
