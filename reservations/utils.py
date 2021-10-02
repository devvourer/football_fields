import datetime


class CurrentUser():

    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['user']

    def __call__(self, *args, **kwargs):

        return self.user_id


def get_time():
    today = datetime.datetime.now()
    time = datetime.time(today.hour, today.minute)
    return time