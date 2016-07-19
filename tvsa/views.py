from django.views.generic import View

from django.http import HttpResponse

from .models import Shift

from datetime import datetime

import json

class ShiftList(View):
    def get(self, request, *args, **kwargs):

        date_selection = request.GET.get('date_selection', None)

        if date_selection:
            date = datetime.strptime(date_selection, '%Y-%m-%d').date()
            queryset = Shift.objects.filter(date=date)
        else:
            queryset = Shift.objects.all()

        def build_json_string_from_queryset(qs):

            qs_list = list()
            for x in qs:
                qs_dict = {}
                qs_dict['id'] = str(x.pk)
                qs_dict['volunteer'] = x.volunteer.__unicode__()
                qs_dict['resource'] = x.job.__unicode__()
                qs_dict['start_time'] = datetime.combine(x.date, x.start_time).isoformat()
                qs_dict['end_time'] = datetime.combine(x.date, x.end_time).isoformat()
                qs_dict['duration'] = 'null'
                qs_dict['percent_complete'] = 'null'
                qs_dict['dependencies'] = 'null'
                qs_list.append(qs_dict)

            return json.dumps(qs_list, sort_keys=True)

        json_response = build_json_string_from_queryset(queryset)

        return HttpResponse(json_response, content_type="application/json")


class ShiftDateList(View):
    def get(self, request, *args, **kwargs):


        shifts = Shift.objects.all()
        date_set = set()
        for shift in shifts:
            date_set.add(shift.date.isoformat())

        date_list = list(date_set)

        json_response = json.dumps(date_list, sort_keys=True)

        return HttpResponse(json_response, content_type="application/json")
