from django.shortcuts import render
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
import base64
from cnisblog.forms import *
import os
from datetime import timedelta
import datetime
import pytz
import httplib2
import random
import string
from oauth2client.service_account import ServiceAccountCredentials
from dateutil import parser
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

posts = [
    {
        'author': 'Rastine Pinlac',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Shenn Tinsay',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': 'August 28, 2018'
    },
]


def home(request):
    form = emailForm(request.POST or None)
    err_msg = "Error!!!"

    if form.is_valid():
        subject = form.cleaned_data['subject']
        message_text = form.cleaned_data['message_text']
        to = form.cleaned_data['to']
        sender = form.cleaned_data['sender']
        msg = create_message(sender, to, subject, message_text)
        srvc = gmail()
        send_message(srvc, 1, message)

    create_event(request)

    context = {
        'form': form,
        'err_msg': err_msg,
    }
    return render(request, 'cnisblog/home.html', context)


def about(request):
    return render(request, 'cnisblog/about.html', {'title': 'About'})


def signup(request):
    return render(request, 'cnisblog/signup.html')


SCOPES = ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.send']


def gmail():
    store = file.Storage(settings.TOKEN_JSON)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(settings.GOOGLE_CLIENT_JSON, SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    #results = service.users().labels().list(userId='me').execute()
    #labels = results.get('labels', [])

    return service


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = 'rastinebpinlac@gmail.com'
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def build_service():

    SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict({
        "type": "service_account",
        "project_id": "lbyclds-japin",
        "private_key_id": "6a7aa347a416c74bf51762e6d3ad84b8e42ec262",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC0tr/Vd0HLXh/V\nDt95lD6yc03N36x31SC9LiOhnNbZ8YbRip3HklCvQ53ii2xpeNY0P1Wi4sJNdxPz\nFBgwZyliX1i9ZmoU+SybYFXboBzFGn0/juULrx3REn6OShxMf3JPFm68Gtb3SXfJ\nlhoIhpNVFplbMrY9EKlcjupWAU1ZMO0GaIRP7EwT7FnAyTNEDZ2bUVAtqT+E0Ie6\nDWFwsAvlA7gflPY94TG6rGsT7ZiHGzrZlZu+cutz+MgChmqPxBIa92MPE2nbcBbU\njFn/8AfYdnaE7U0Za3KRFKpQaqitre61GlNHlY4XLgoZqa7kgv0FivYZTGYyktSK\nFJLOHBozAgMBAAECggEAOe9et95oUv0FgoYmofEjWo15s5dSUQacXNoWZUEFZlC2\n0qW4aJthT5cDXnYpVvT84zosx7Af77rNw/+8s4PXMij0J6BWQQwTP2rWi7cckhoo\nbkBu8Nx+2CCwPwjGYsX3DSDZdme6ZAQDKbb7+KDASiaZGrI613/oc/qDaPg45m8t\nlLsRaL08AkJd9sEL76cQHKN/WEpunXVrP9YdU4QrD++JB0NcZhWtOhMsQXM2g43C\nOdowqVLTjKLTmJ+vxPxxa1HdTsnYXOCk7GZaFDYlkWjhbyANRyr31Y+0dA6UL3ul\nrDO6jsviHEQcfZlCWoe+ph3evzlEYaSOSvRMf8aUFQKBgQDbp3g4JKnN4kJVFspp\n9FBNI5khZwRnakr6+9uxRAEJtvGol1dzkBms+uigkKUWqIdnUjQMtugPI2kfoFJW\nMV0SzFOgoPQf7kk3rs1Toe24qq70CTx2dcNeeN9GUmBbWYU2p1ZqEkdv/p0d/eFC\n/uVSmNyYPz0VamtF7s0G9fZGTwKBgQDSncWPIW/318y6k07MhQcmAjru/LiPREVj\n7zBs1HHDQ77RQREJFd6g53TnxBrC79hyAPCK02AItw03Cfqc++thvEux/2ae0w8T\n91nNqQs2cZ9jb/H4oxryXiorKUOSYguSb7LOmOOKuVk5byU5czcrIs6Vcq/1k6WM\n6z0GjvYY3QKBgCJ0Wn80AQ6ydwUx1f5YvF/dPZ/nsOEn4ysLZqKfsCn98FopoyYV\nbHGdye+lwL+VH+gtFM0Jw8zcGRlE5KVwiNDyDAweMyzvC70YRkzgEZHt9BODf2B1\niHfBLgSx1zt9B1BTX1K0G1CN98dEk5kWspIKOFAJW2OIldsaYj69RiwxAoGACzCq\nwHIMWuSyUe9lrmQa/x/7NZtjyujbrvWUYxPef3tn9gI4/3yT+YSSp4W5zkWkAFqg\nbR/R6GShZR04nYKc/PJeKzTgpOudz3fC47Rpjhj3WPcnqggwdFQgdW6Z0ns3Fi6t\nF2D0Jfi3DuAi4CyI79fHlhUj2C5iC1ysP171IFkCgYEAi2kiV1By2ylHtJXzCcyc\nUC9ObtYjleJe9Z3UfpFryQeLCK8d627vWgY9HREG83BveVLE6iVyAyqXtv8zOZMI\neawpJOWtGSsaaqECff6dJ/rGvM+FOT00R4B23zAO0wBg/dkiTTVKW74qhKNIgqoj\n0MKaj+rDPfKN1bBCkFv425g=\n-----END PRIVATE KEY-----\n",
        "client_email": "cloudservice@lbyclds-japin.iam.gserviceaccount.com",
        "client_id": "111286104573596779782",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cloudservice%40lbyclds-japin.iam.gserviceaccount.com"
    }, SCOPES)

    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)

    return service


def create_event(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            username = request.user
            hike = request.POST.get("hike")
            datepick = request.POST.get("datepick")
            timepick = request.POST.get("timepick")

            subject = "[Hikers Turf] Booking Invoice"
            message = "Reference Number: " + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + "\n\nGood day!\n\nWe are please to inform you about your book on " + datepick + "."
            from_email = settings.EMAIL_HOST_USER
            to_list = [username.email]

            send_mail(subject, message, from_email, to_list, fail_silently=True)

            # Calendar
            service = build_service()

            datepick = parser.parse(datepick)
            timepick = datetime.time(7, 00)

            final_datetime = datetime.datetime.combine(datepick, timepick).isoformat()
            # Start of Hike
            event = service.events().insert(calendarId='rastinebpinlac@gmail.com', sendNotifications=True, body={
                'summary': '[Hikers Turf]' + hike,
                'description': 'You reserved ' + hike + ' hike',
                'start': {'dateTime': final_datetime, "timeZone": "Asia/Manila"},
                'end': {'dateTime': final_datetime, "timeZone": "Asia/Manila"},
                'location': hike,
            }).execute()

            messages.success(request, 'Your booking was successful! Proceed to check your email to find more details about your booking.')

            return render(request, 'cnisblog/home.html', {})

    return render(request, 'cnisblog/home.html', {})
