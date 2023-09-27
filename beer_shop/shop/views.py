from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from cart.forms import CartAddProductForm
from .models import Product, Category, Country
from .recommender import Recommender


def product_list(request, category_slug=None, country_slug=None):
    category = None
    country = None
    categories = Category.objects.all()
    countries = Country.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug and country_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        country = get_object_or_404(Country,
                                    translations__language_code=language,
                                    translations__slug=country_slug)
        products = products.filter(category=category).filter(country=country)
    elif category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
    elif country_slug:
        language = request.LANGUAGE_CODE
        country = get_object_or_404(Country,
                                    translations__language_code=language,
                                    translations__slug=country_slug)
        products = products.filter(country=country)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'country': country,
                   'categories': categories,
                   'countries': countries,
                   'products': products})

# class ProductListView(ListView):
#     model = Product
#     template_name = 'shop/product/list.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         try:
#             context['category'] = Category.objects.get(slug=self.kwargs['category_slug'])
#         except:
#             context['category'] = None
#         context['categories'] = Category.objects.all()
#         try:
#             context['country'] = Country.objects.get(slug=self.kwargs['country_slug'])
#         except:
#             context['country'] = None
#         context['countries'] = Country.objects.all()
#         context['products'] = Product.objects.filter(available=True)
#         if context['category'] and context['country']:
#             context['products'] = Product.objects.filter(available=True) \
#                 .filter(category=context['category']) \
#                 .filter(country=context['country'])
#         elif context['category']:
#             context['products'] = Product.objects.filter(available=True) \
#                 .filter(category=context['category'])
#         elif context['country']:
#             context['products'] = Product.objects.filter(available=True) \
#                 .filter(country=context['country'])
#
#         return context


def product_detail(request, id, slug):
    # language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                # translations__language_code=language,
                                # translations__slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products})


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'shop/product/detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         r = Recommender()
#         context['cart_product_form'] = CartAddProductForm()
#         context['recommended_products'] = r.suggest_products_for([context['product']], 4)
#         return context


def index_page(request):
    return redirect('shop:product_list')
