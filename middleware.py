import jwt

from django.urls import resolve
from Flipkart.views import return_response
from datetime import datetime

class flipkart_middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        current_url = resolve(request.path_info).url_name
        if current_url == 'register' or current_url == 'add_category' or current_url == 'login' \
                or current_url == 'add_product' or current_url == 'add_subcategory' \
                or current_url == 'refresh_token' or current_url == 'get_users' or current_url == 'get_categories' \
                or current_url == 'get_products' or current_url == 'get_subcategories' or \
                current_url == 'get_particular_product' or current_url == 'get_particular_subcategory' or \
                current_url == 'get_details':
            pass
        elif current_url == 'profile':
            token = request.META.get('HTTP_AUTHORIZATION')
            token = token.split()
            decoded = jwt.decode(token[1], "SECRET_KEY")
            time = str(decoded['time'])
            current_time = str(datetime.now()).split(' ')
            exact_time = current_time[1].split(':')
            actual_time = time.split(':')
            if int(actual_time[0]) <= int(exact_time[0]) and (int(exact_time[1]) - int(actual_time[1])) <= 15:
                pass
            else:
                data = {}
                data['message'] = 'Token expired'
                return return_response(request, data=data)