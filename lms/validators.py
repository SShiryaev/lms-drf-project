from rest_framework.serializers import ValidationError


class LinkToVideoValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = dict(value).get(self.field)

        if url:
            if 'youtube.com' not in url:
                raise ValidationError('Ролик должен быть на www.youtube.com')
