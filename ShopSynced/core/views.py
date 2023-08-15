from django.shortcuts import render

from django.views.generic import TemplateView, ListView
from store.models import Product

class FrontPageView(ListView):
    model = Product
    template_name = 'core/frontpage.html'   # <app>/<model>_<viewtype>.html
    context_object_name = 'products'
    ordering = ['title']
    # paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(status=Product.ACTIVE)

class AboutPageView(TemplateView):
    template_name = 'core/about.html'   # <app>/<model>_<viewtype>.html
