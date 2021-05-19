from django.http import HttpResponse
from django.core.serializers import serialize
from django.views.generic import FormView, ListView, TemplateView

from .models import Product
from .forms import SiteForm


class HomeView(TemplateView):
    template_name = 'monitoring/base.html'


class ParserView(FormView):
    form_class = SiteForm
    template_name = 'monitoring/parse.html'
    success_url = 'products'


class ProductListView(ListView):
    model = Product

    def get_queryset(self, pk):
        return Product.objects.filter(search_id=pk)

    def get(self, request, pk, *args, **kwargs):
        product = serialize('json', self.get_queryset(pk))
        return HttpResponse(product)
