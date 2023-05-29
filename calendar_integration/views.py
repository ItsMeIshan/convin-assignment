from django.http import HttpResponseRedirect
import googleapiclient.discovery
import google_auth_oauthlib.flow
import datetime
from django.http import JsonResponse


# Create your views here.

# def home(request):
#     status = True

#     return render(request, 'index.html', {'status': status})

SCOPES = ['https://www.googleapis.com/auth/calendar']

def GoogleCalendarInitView(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secrets.json', scopes=SCOPES)
    flow.redirect_uri = 'http://127.0.0.1:8000/rest/v1/calendar/redirect'
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    
    return HttpResponseRedirect(authorization_url)

def GoogleCalendarRedirectView(request):
    state = request.GET.get('state')

    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secrets.json', scopes=SCOPES, state=state) 
        flow.redirect_uri = 'http://127.0.0.1:8000/rest/v1/calendar/redirect'
        authorization_response = 'https://' + str(request.build_absolute_uri)
        flow.fetch_token(authorization_response=authorization_response)
        calendar = googleapiclient.discovery.build('calendar', 'v3', credentials=flow.credentials)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = calendar.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        if not events:
            return JsonResponse('No upcoming events found.')
        
        user_events = []    
        for event in events:
            user_events.append(event)
        return JsonResponse({'data': user_events})
        
    except ValueError:
        return JsonResponse('Error Occurred')