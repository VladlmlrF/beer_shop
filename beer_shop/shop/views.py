from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product, Category, Country


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['category'] = Category.objects.get(slug=self.kwargs['category_slug'])
        except:
            context['category'] = None
        context['categories'] = Category.objects.all()
        try:
            context['country'] = Country.objects.get(slug=self.kwargs['country_slug'])
        except:
            context['country'] = None
        context['countries'] = Country.objects.all()
        context['products'] = Product.objects.filter(available=True)
        if context['category'] and context['country']:
            context['products'] = Product.objects.filter(available=True) \
                .filter(category=context['category']) \
                .filter(country=context['country'])
        elif context['category']:
            context['products'] = Product.objects.filter(available=True) \
                .filter(category=context['category'])
        elif context['country']:
            context['products'] = Product.objects.filter(available=True) \
                .filter(country=context['country'])

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'

