from typing import Final

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django_mapper.constants import CURRENT_LEFT_STORE, NONE_INT
from django_mapper.models import Product, Match
from django_mapper.schemas.mapper_progress import MatchingProgress
from django_mapper.schemas.product_suggestions import ProductSuggestions
from django_mapper.service import get_next_product
from parsers.runnures.schemas.product import StoreEnum



def index(request):
    next_product_id: int = get_next_product(CURRENT_LEFT_STORE)
    url = reverse("django_mapper:product_view", args=(next_product_id,))
    return HttpResponse(f"You're at the django_mapper index. \n start here <a href=\"{url}\">{url}</a>")


def product_view(request, product_id):
    main_product_obj = Product.objects.get(pk=product_id)
    match_product_objs = Product.objects.filter(pk__in=list(range(product_id+1, product_id + 10)))
    progress = MatchingProgress.get_progress()
    suggestions = ProductSuggestions.get_suggestions(main_product_obj)

    return render(request, "django_mapper/mapper.html", {
        "main_product_obj": main_product_obj,
        'progress': progress,
        'suggestions': suggestions,
    })


def map_products(request, product_id_1: int, product_id_2: int | None):
    if product_id_1 == NONE_INT:
        raise ValueError(f"product_id_1 cannot be None ({NONE_INT})")
    insurance = 1
    if product_id_2 == NONE_INT:
        insurance = -1
        product_id_2 = None

    match = Match(product_1_id=product_id_1, product_2_id=product_id_2, insurance=insurance)
    match.save()

    next_product_id: int = get_next_product(CURRENT_LEFT_STORE)
    return HttpResponseRedirect(reverse("django_mapper:product_view", args=(next_product_id,)))
