from django.db import models


class Volunteer(models.Model):
    first_name = models.CharField(max_length=100,)
    last_name = models.CharField(max_length=100,)

    phone_number = models.CharField(max_length=12, blank=True)

    seller_number = models.CharField(max_length=100, blank=True)

    role = models.ForeignKey('Role', related_name='volunteers')

    class Meta:
        unique_together = ("first_name", "last_name", "seller_number")

    def get_full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    full_name = property(get_full_name)

    def __unicode__(self):
        if self.seller_number:
            return u'%s %s (%s)' % (self.first_name, self.last_name, self.seller_number)
        else:
            return u'%s %s' % (self.first_name, self.last_name)


class Role(models.Model):
    role = models.CharField(max_length=100,)
    manager = models.BooleanField(default=False)

    def __unicode__(self):
        return self.role


class Shift(models.Model):
    volunteer = models.ForeignKey('Volunteer', related_name='shifts')

    job = models.ForeignKey('Job', related_name='shifts')

    group_shift = models.ForeignKey('GroupShift', related_name='shifts', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    # need to be able to filter this to managers only
    managers_in_charge = models.ManyToManyField('Volunteer', blank=True)

    notes = models.TextField(blank=True)

    present_for_shift = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s - %s' % (self.volunteer, self.job)

    class Meta:
        ordering = ['volunteer__first_name', 'volunteer__last_name']


class Job(models.Model):
    job = models.CharField(max_length=100,)
    heavy_lifting = models.BooleanField(default=False)

    def __unicode__(self):
        return self.job



class GroupShift(models.Model):
    group_shift_name = models.CharField(max_length=100,)

    def __unicode__(self):
        return self.group_shift_name
