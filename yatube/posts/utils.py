from django.core.paginator import Paginator
from . import constants


def paginate_page(posts, request):
    paginator = Paginator(posts, constants.PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
