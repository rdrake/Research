# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class AcCourse(models.Model):
    course_code = models.CharField(max_length=48, primary_key=True)
    title = models.CharField(max_length=765)
    description = models.CharField(max_length=765, blank=True)
    related = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'ac_course'
    
    def __unicode__(self):
      return self.title

class Directory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=600, blank=True)
    position = models.CharField(max_length=150, blank=True)
    faculty = models.CharField(max_length=300, blank=True)
    extension = models.CharField(max_length=30, blank=True)
    office = models.CharField(max_length=150, blank=True)
    email = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = u'directory'
    
    def __unicode__(self):
      return self.name

class MycCourse(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=765)
    levels = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'myc_course'
    
    def __unicode__(self):
      return self.title

class MycInstructor(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    office = models.CharField(max_length=765, blank=True)
    email = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'myc_instructor'
    
    def __unicode__(self):
      return self.name

class MycPrerq(models.Model):
    id = models.IntegerField(primary_key=True)
    course_code = models.CharField(unique=True, max_length=30, blank=True)
    course_req = models.CharField(max_length=30, blank=True)
    term = models.CharField(max_length=30, blank=True)
    flag = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'myc_prerq'
    
    def __unicode__(self):
      return self.course_code

class MycSchedule(models.Model):
    id = models.IntegerField(primary_key=True)
    #section_id = models.IntegerField(unique=True)
    section = models.ForeignKey('MycSection')
    instruct_name = models.CharField(max_length=765)
    type = models.CharField(max_length=60, blank=True)
    location = models.CharField(max_length=384, blank=True)
    day = models.CharField(unique=True, max_length=6)
    time_start = models.CharField(unique=True, max_length=60, blank=True)
    time_end = models.CharField(unique=True, max_length=60, blank=True)
    class Meta:
        db_table = u'myc_schedule'
    
    def __unicode__(self):
      return self.instruct_name

class MycSection(models.Model):
    id = models.IntegerField(primary_key=True)
    #course_code = models.CharField(unique=True, max_length=30)
    course = models.ForeignKey(MycCourse, db_column='course_code')
    crn = models.CharField(max_length=30, db_column='CRN') # Field name made lowercase.
    section = models.CharField(unique=True, max_length=30)
    term = models.CharField(unique=True, max_length=255)
    register_start = models.CharField(max_length=384, blank=True)
    register_end = models.CharField(max_length=384, blank=True)
    credits = models.FloatField()
    campus = models.CharField(max_length=765, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    actual = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'myc_section'
    
    def __unicode__(self):
      return self.section

class MycSectionInstructor(models.Model):
    id = models.IntegerField(primary_key=True)
    #sec_id = models.IntegerField(unique=True)
    sec = models.ForeignKey(MycSection)
    instruct_name = models.CharField(unique=True, max_length=255)
    class Meta:
        db_table = u'myc_section_instructor'
    
    def __unicode__(self):
      return self.instruct_name

