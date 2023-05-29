from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.conf import settings
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from .models import CredentialsModel
from django.http import HttpResponseRedirect
from oauth2client.client import flow_from_clientsecrets
from httplib2 import Http
import googleapiclient.discovery
from googleapiclient.discovery import build
from django.middleware.csrf import get_token
from httplib2 import Http
from oauth2client.contrib import xsrfutil

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google_auth_oauthlib.flow
from google.oauth2 import id_token
from google.auth.transport import requests
import datetime


# Create your views here.

def home(request):
    status = True

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/admin')

    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    try:
        access_token = credential.access_token
        resp, cont = Http().request("https://www.googleapis.com/auth/gmail.readonly",
                                    headers={'Host': 'www.googleapis.com',
                                            'Authorization': access_token})
    except:
        status = False
        print('Not Found')

    return render(request, 'index.html', {'status': status})


# FLOW = flow_from_clientsecrets(
#     settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
#     scope='https://www.googleapis.com/auth/calendar',
#     redirect_uri='http://127.0.0.1:8000/oauth2callback',
#     prompt='consent')

SCOPES = ['https://www.googleapis.com/auth/calendar']

def GoogleCalendarInitView(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secrets.json', scopes=['https://www.googleapis.com/auth/calendar'])
    flow.redirect_uri = 'http://127.0.0.1:8000/rest/v1/calendar/oauth2callback'
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    return HttpResponseRedirect(authorization_url)

def auth_return(request):
    get_state = bytes(request.GET.get('state'), 'utf8')
    state = request.GET.get('state')

    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secrets.json', scopes=SCOPES, state=state) 
        flow.redirect_uri = 'http://127.0.0.1:8000/rest/v1/calendar/oauth2callback'
        authorization_response = 'https://' + str(request.build_absolute_uri)
        flow.fetch_token(authorization_response=authorization_response)
        print(flow.credentials);
        calendar = googleapiclient.discovery.build('calendar', 'v3', credentials=flow.credentials)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = calendar.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        # request = requests.Request()
        # id_info = id_token.verify_oauth2_token(get_state, request)
        # print(id_info)
        # userid = id_info['sub']

    except ValueError:
        print("Invalid token")
        pass
    # if not xsrfutil.validate_token(settings.SECRET_KEY, get_state,
    #                                request.user):
    #     return HttpResponseBadRequest()
    # credential = FLOW.step2_exchange(request.GET.get('code'))
    # storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    # storage.put(credential)
    # print("access_token: %s" % credential.access_token)
    return HttpResponseRedirect("/")  