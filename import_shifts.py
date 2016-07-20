import os, sys

from datetime import datetime

proj_path = "."
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TPOM.settings")
sys.path.append(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import csv

from tvsa.models import (Volunteer, Role, Shift, GroupShift, Job)

f = open(sys.argv[1], 'rU')
reader = csv.DictReader(f)

for row in reader:
    phone_number = row['Mobile Number']

    seller_number = row['Seller Number']
    if seller_number.lower() == 'volunteer only':
        seller_number = ''

    volunteer_name = row['Volunteer Name']
    last_name, first_name  = volunteer_name.split(',')
    first_name = first_name.strip()

    role = Role.objects.get(role='Sale Volunteer')

    volunteer, volunteer_created = Volunteer.objects.get_or_create(first_name=first_name,
                                                         last_name=last_name,
                                                         seller_number=seller_number,
                                                         phone_number=phone_number,
                                                         role=role)

    job_name = row['Description']
    heavy_lifting = False
    if 'heavy lifting' in job_name:
        heavy_lifting = True

    if 'NON MEMBER VOLUNTEER' in job_name:
        job_name = 'Sale Volunteer'

    job, job_created = Job.objects.get_or_create(job=job_name, heavy_lifting=heavy_lifting)

    date_string = row['Date']

    date = datetime.strptime(date_string, '%a, %b %d, %Y').date()

    start_time_string = row['Start Time']
    start_time = datetime.strptime(start_time_string, '%I:%M %p').time()

    end_time_string = row['End Time']
    end_time = datetime.strptime(end_time_string, '%I:%M %p').time()

    shift, shift_created = Shift.objects.get_or_create(volunteer=volunteer,
                                                       job=job,
                                                       date=date,
                                                       start_time=start_time,
                                                       end_time=end_time)



