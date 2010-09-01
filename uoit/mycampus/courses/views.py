import json
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import connection
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import list_detail
from uoit.mycampus.models import *

aterms = ["UOIT Summer 2004", "UOIT Summer 2005", "UOIT Fall 2005",
  "UOIT Winter 2006", "UOIT Summer 2006", "UOIT Fall 2006", "UOIT Winter 2007",
  "UOIT Summer 2007", "UOIT Fall 2007", "UOIT Winter 2008", "UOIT Summer 2008",
  "UOIT Fall 2008", "UOIT Winter 2009", "UOIT Summer 2009", "UOIT Fall 2009",
  "UOIT Winter 2010", "UOIT Spring/Summer 2010", "UOIT Fall 2010",
  "UOIT Winter 2011"]

dates = { "M": 1, "T": 2, "W": 3, "R": 4, "F": 5 }

def details(request, object_id):
  term = request.GET.get('term')
  
  if term == '':
    term = "UOIT Fall 2010"
  
  return list_detail.object_detail(
    request,
    queryset=MycCourse.objects.all(),
    object_id=object_id,
    template_name='mycampus/templates/myccourse_detail.html',
    extra_context={
      'sections': MycSection.objects.filter(course=object_id).filter(term=term)
    }
  )

def _extract_params(params):
  return (
    params.get("code", ""),
    params.get("title", ""),
    params.get("term", "UOIT Fall 2010"),
    params.get("instructor", "")
  )

def get_objects(request):
	(code, title, term, instructor) = _extract_params(request.GET)
	cursor = connection.cursor()
	args = [term]
	sql = "SELECT myc_course.code, myc_course.title, myc_section.CRN, myc_section.section, myc_section.term, myc_schedule.instruct_name, myc_schedule.location, myc_schedule.day, myc_schedule.time_start, myc_schedule.time_end FROM myc_course JOIN myc_section ON myc_section.course_code = myc_course.code JOIN myc_schedule ON myc_schedule.section_id = myc_section.id WHERE myc_section.term = %s"
		
	if code != "":
		sql += " AND myc_course.code LIKE %s"
		args.append('%' + code + '%')
	
	if title != "":
		sql += " AND myc_course.title LIKE %s"
		args.append('%' + title + '%')
	
	if instructor != "":
		sql += " AND myc_schedule.instruct_name LIKE %s"
		args.append('%' + instructor + '%')
	
	cursor.execute(sql, args)
	
	return cursor.fetchall()

def calendar_json(request):
	records = get_objects(request)
	result = []
	
	for a in records:
		result.append({
			'title': a[1],
			'start': datetime(2010, 2, dates[a[7]], int(a[8].split(':')[0]), int(a[8].split(':')[1])), #'2010-01-01 %s:00' % a[8],
			'stop': datetime(2010, 2, dates[a[7]], int(a[9].split(':')[0]), int(a[9].split(':')[1]))
		})
	
	# Solution found here:  http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript/2680060#2680060
	dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
	return HttpResponse(json.dumps(result, default=dthandler))

def listing_json(request):
  start = int(request.GET.get('iDisplayStart', '0'))
  length = min(int(request.GET.get('iDataLength', '25')), 100)
  
  paginator = Paginator(get_objects(request), length)
  page = int(start / float(length)) + 1
  
  try:
    queryset = paginator.page(page)
  except (EmptyPage, InvalidPage):
    queryset = paginator.page(paginator.num_pages)
  
  # Create and populate the various parameters datatables requires.
  result = {}
  result['iTotalRecords'] = result['iTotalDisplayRecords'] = paginator.count
  result['sEcho'] = request.GET.get('sEcho', '0')
  result['aaData'] = [[a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9]] for a in queryset.object_list] #[[course.code, course.title, course.levels] for course in queryset.object_list.all()]
  
  # Return JSON for displaying.
  return HttpResponse(json.dumps(result))

def listing(request):
  instructor = request.GET.get("instructor", "")
  term = request.GET.get("term", "")
  code = request.GET.get("code", "")
  title = request.GET.get("title", "")
  avail_terms = aterms
  
  if term == "":
    term = "UOIT Fall 2010"
  
  return render_to_response("mycampus/templates/myccourse_list.html", locals(), context_instance=RequestContext(request))
