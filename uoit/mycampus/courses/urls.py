from django.conf import settings
from django.conf.urls.defaults import *
from uoit.mycampus.models import MycCourse, MycSection

info_dict = {
  'queryset': MycCourse.objects.all()
}

urlpatterns = patterns('',#'uoit.mycampus.courses.views',
  (r'^$', 'uoit.mycampus.courses.views.listing'),
  (r'^json$', 'uoit.mycampus.courses.views.listing_json'),
  (r'^calendar$', 'uoit.mycampus.courses.views.calendar_json'),
  (r'^(?P<object_id>[\w\s]+)/$', 'uoit.mycampus.courses.views.details')
)
