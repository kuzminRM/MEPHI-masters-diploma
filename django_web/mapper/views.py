from django.http import HttpResponse
from django.shortcuts import render

from mapper.models import Product


def index(request):
    return HttpResponse("Hello, world. You're at the mapper index.")


def product_map_view(request, product_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    main_product_obj = Product.objects.get(pk=product_id)
    return render(request, "mapper/mapper.html", {"main_product_obj": main_product_obj})
