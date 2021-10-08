import datetime


class CurrentUser:

    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user.phone
        print(self.user)

    def __call__(self, *args, **kwargs):
        return self.user


def get_time():
    today = datetime.datetime.now()
    time = datetime.time(today.hour, today.minute)
    return time
