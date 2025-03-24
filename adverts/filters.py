import django_filters
from .models import (
    Advert,
    Category,
)

class AdvertFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        field_name = "category",
        queryset = Category.objects.all(),
    )

    class Meta:
        model = Advert
        fields = (
            'category',
        )