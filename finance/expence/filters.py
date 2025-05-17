import django_filters

from finance import models


class ExpenceFilter(django_filters.FilterSet):
    class Meta:
        model = models.Expence
        fields = [
            'category'
        ]