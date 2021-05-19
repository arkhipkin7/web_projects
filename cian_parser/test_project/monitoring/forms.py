from django import forms


class SiteForm(forms.Form):
    url = forms.URLField(label='URL страницы', max_length=255)
    page = forms.IntegerField(label='Кол-во страниц для парсинга', min_value=1)
