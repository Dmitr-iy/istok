from django_filters import FilterSet, ChoiceFilter
from .models import Catalog


class CatalogFilter(FilterSet):
    category = ChoiceFilter(choices=Catalog.CATEGORY_CHOICES, label='Категория')
    shape = ChoiceFilter(choices=Catalog.SHAPE_CHOICES, label='Форма')
    kitchen = ChoiceFilter(choices=Catalog.KITCHEN_CHOICES, label='Кухни')
    purpose = ChoiceFilter(choices=Catalog.PURPOSE_CHOICES, label='Назначение')
    facade_material = ChoiceFilter(choices=Catalog.FASADE_MATERIAL, label='Материал фасадов')
    Table_top_material = ChoiceFilter(choices=Catalog.TABLE_TOP_MATERIAL, label='Материал столешницы')

    class Meta:
        model = Catalog
        fields = ['category', 'shape', 'kitchen', 'purpose', 'facade_material', 'Table_top_material']
