from django.contrib import admin


from .models import (Volunteer, Role, Shift, GroupShift, Job)

# Register your models here


class MemberListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Is a Seller?'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'seller'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'yes':
            return queryset.exclude(seller_number='')
        if self.value() == 'no':
            return queryset.filter(seller_number='')


class ManagerListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Is a Manager?'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'manager'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'yes':
            return queryset.filter(role__manager=True)
        if self.value() == 'no':
            return queryset.filter(role__manager=False)


class AssignedToManagerBooleanListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Assigned to Manager?'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'assigned'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        manager_qs = Volunteer.objects.filter(role__manager=True)
        if self.value() == 'yes':
            return queryset.filter(managers_in_charge__in=manager_qs)
        if self.value() == 'no':
            return queryset.exclude(managers_in_charge__in=manager_qs)


class AssignedManagerListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Managers in charge'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'managers'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        manager_qs = Volunteer.objects.filter(role__manager=True)
        big_list = []
        for manager in manager_qs:
            little_list = []
            little_list.append(manager.pk)
            little_list.append(manager.full_name)
            big_list.append(tuple(little_list))

        return tuple(big_list)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        manager_pk = self.value()
        return queryset.filter(managers_in_charge__pk=manager_pk)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'manager')

class JobAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'heavy_lifting')

class ShiftAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'job', 'get_phone_number', 'get_managers', 'date', 'start_time', 'end_time', 'group_shift')

    list_filter = (AssignedToManagerBooleanListFilter, AssignedManagerListFilter)

    search_fields = ['volunteer__first_name', 'volunteer__last_name','job__job',]

    def get_managers(self, obj):
        return ", ".join([str(m.get_full_name()) for m in obj.managers_in_charge.all()])

    get_managers.short_description = 'Manager(s)'

    def get_phone_number(self, obj):
        return obj.volunteer.phone_number

    get_phone_number.short_description = 'Phone Number'

    def get_form(self, request, obj=None, **kwargs):
        form = super(ShiftAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['managers_in_charge'].queryset = Volunteer.objects.filter(role__manager=True)
        return form





class GroupShiftAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'role')

    list_filter = (MemberListFilter, ManagerListFilter, 'role')

    search_fields = ['first_name', 'last_name', ]


admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(GroupShift, GroupShiftAdmin)
admin.site.register(Job, JobAdmin)

