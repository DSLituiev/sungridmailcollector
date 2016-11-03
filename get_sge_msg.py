#!/usr/bin/env python3
from __future__ import print_function
import httplib2
import os
import sys
sys.path.append("google-api-python-client/")

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

CLIENT_SECRET_FILE = os.path.join(
            os.environ["HOME"], 
            '.google/client_secret_423201044976-e745ce413p00ceferjs3lh5vga3pajk9.apps.googleusercontent.com.json')
APPLICATION_NAME = 'sungridcollector'


from apiclient import errors
import base64
import email
from apiclient import errors

def GetMessage(service, user_id, msg_id, **kwargs):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id, **kwargs).execute()

    #print( 'Message snippet: %s' % message['snippet'] )

    return message
  except errors.HttpError as error:
    print( 'An error occurred: %s' % error)


def GetMimeMessage(service, user_id, msg_id):
  """Get a Message and use it to create a MIME Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A MIME Message, consisting of data from Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()

    print( 'Message snippet: %s' % message['snippet'])

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    mime_msg = email.message_from_string(msg_str)

    return mime_msg
  except errors.HttpError as error:
    print( 'An error occurred: %s' % error )


"""Get a list of Messages from the user's mailbox."""
def ListMessagesMatchingQuery(service, user_id = "me", query='', **kwargs):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query,
                                               **kwargs
                                               ).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def ListMessagesWithLabels(service, user_id = "me", label_ids=[]):
  """List all Messages of the user's mailbox with label_ids applied.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_ids: Only return Messages with these labelIds applied.

  Returns:
    List of Messages that have all required Labels applied. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate id to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               labelIds=label_ids).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id,
                                                 labelIds=label_ids,
                                                 pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print( 'An error occurred: %s' % error )

def get_credentials(flags=None):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    import sys
    try:
        import argparse
        parser = argparse.ArgumentParser(parents=[tools.argparser])
        parser.add_argument('--match', type=str, default=None)
        flags = parser.parse_args()
    except ImportError:
        flags = None

    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials(flags)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

 #   results = service.users().labels().list(userId='me').execute()
 #   labels = results.get('labels', [])
 #   if not labels:
 #       print('No labels found.')
 #   else:
 #     print('Labels:')
 #     for label in labels:
 #       print(label['name'])

    msgs = ListMessagesMatchingQuery(service, query = "from:root, is:unread", )
    msg_ids = [x['id'] for x in msgs]
    for mm in msg_ids:
        msgtxt = GetMessage(service, user_id="me", msg_id=mm, fields="snippet",)
        snpt = msgtxt['snippet']
        try:
            jobid = snpt.split(" Aborted")[0].split("Job-array task ")[1]
        except IndexError:
            continue
        if flags.match is not None and flags.match not in jobid:
            continue
        print(jobid)


if __name__ == '__main__':
    main()

