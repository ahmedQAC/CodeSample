

class IsOrganiserQuerysetMixin():
    """Used to update queryset to get all objects in which the organiser is the
    requested user"""
    organiser_field = 'organiser'
    allow_staff_view = False

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.organiser_field] = user
        qs = super().get_queryset(*args, **kwargs)
        print('super queryset is')
        print(qs)
        if self.allow_staff_view and user.is_staff:
            return qs
        return qs.filter(**lookup_data)