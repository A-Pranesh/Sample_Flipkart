import json
import re
import jwt

from django.db.models import F
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import User_Registration, Product, SubCategory, Category
from datetime import datetime

def return_response(request, data):
    return JsonResponse(data, safe=False)

@api_view(['POST'])
def registration(request):
    password_regex = re.compile('(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d][A-Za-z\d!@#$%^&*()_+]{7,19}$')
    name_regex = re.compile('[a-zA-Z]+')
    try:
        data = json.loads(request.body.decode('utf-8'))
        if not re.search(password_regex, data['Password']):
            data1 = {}
            data1['message'] = 'See the password conditions'
            return return_response(request, data=data1)
        if not re.search(name_regex, data['Name']):
            data1 = {}
            data1['message'] = 'Invalid Name'
            return return_response(request, data=data1)
        if data['Email'] == '':
            data1 = {}
            data1['message'] = 'Email must be entered'
            return return_response(request, data=data1)
        user_object = User_Registration()
        user_object.Username = data['Username']
        user_object.Name = data['Name']
        user_object.Email = data['Email']
        user_object.Password = data['Password']
        user_object.Age = data['Age']
        user_object.DOB = data['DOB']
        user_object.Gender = data['Gender']
        user_object.Address = data['Address']
        user_object.save()
        data ['message'] = 'Successfully Registered'
        return return_response(request, data=data)
    except:
        data = {}
        data['message'] = 'Unable to register Username/Email must be unique'
        return return_response(request, data=data)

@api_view(['GET'])
def profile(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    token = token.split()
    decoded = jwt.decode(token[1], "SECRET_KEY")
    username = decoded['Username']
    try:
        user_obj = User_Registration.objects.get(Username=username)
        data = {}
        data['Username'] = user_obj.Username
        data['Name'] = user_obj.Name
        data['Email'] = user_obj.Email
        data['Password'] = user_obj.Password
        data['Age'] = user_obj.Age
        data['DOB'] = user_obj.DOB
        data['Gender'] = user_obj.Gender
        data['Address'] = user_obj.Address
        return return_response(request, data=data)
    except:
        data = {}
        data['message'] = 'User not found'
        return return_response(request, data=data)

@api_view(['POST'])
def login(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        user_object = User_Registration.objects.get(Username=data['Username'])
        if not user_object.Password == data['Password']:
            data1 = {}
            data1['message'] = 'Invalid Password'
            return return_response(request, data=data1)
    except:
        data1 = {}
        data1['message'] = 'Invalid Username'
        return return_response(request, data=data1)
    time = str(datetime.now()).split(' ')
    data['time'] = time[1]
    jwt_token = {'token': jwt.encode(data, "SECRET_KEY")}
    data['token'] = str(jwt_token['token'])
    return return_response(request, data=data)

@api_view(['GET'])
def refresh_token(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    token = token.split()
    decoded = jwt.decode(token[1], "SECRET_KEY")
    Username = decoded['Username']
    try:
        User_Registration.objects.get(Username=Username)
        time = str(datetime.now()).split(' ')
        decoded['time'] = time[1]
        jwt_token = {'token': jwt.encode(decoded, "SECRET_KEY")}
        decoded['token'] = str(jwt_token['token'])
        return return_response(request, data=decoded)
    except:
        data = {}
        data['message'] = 'Invalid User'
        return return_response(request, data=data)

@api_view(['POST'])
def create_category(request):
    data = json.loads(request.body.decode('utf-8'))
    if data['Name']:
        try:
            category_object = Category()
            category_object.Name = data['Name']
            category_object.save()
            data['message'] = 'Category  created successfully'
            return return_response(request, data=data)
        except:
            data1 = {}
            data1['message'] = 'Category already created'
            return return_response(request, data=data1)
    else:
        data1 = {}
        data1['message'] = 'Please enter a value'
        return return_response(request, data=data1)

@api_view(['POST'])
def create_subcategory(request):
    data = json.loads(request.body.decode('utf-8'))
    if data['Name']:
        try:
            subcategory_object = SubCategory()
            name = data['product_category']
            try:
                type_id = Category.objects.get(Name=name)
                subcategory_object.product_category = type_id
                subcategory_object.Name = data['Name']
                subcategory_object.save()
                data['message'] = 'SubCategory created successfully'
                return return_response(request, data=data)
            except:
                data1 = {}
                data1['message'] = 'There is no such category'
                return return_response(request, data=data1)
        except:
            data1 = {}
            data1['message'] = 'SubCategory already created'
            return return_response(request, data=data1)
    else:
        data1 = {}
        data1['message'] = 'Please enter a value'
        return return_response(request, data=data1)

@api_view(['POST'])
def create_product(request):
    data = json.loads(request.body.decode('utf-8'))
    if data['Name']:
        try:
            product_object = Product()
            name = data['product_subcategory']
            try:
                type_id = SubCategory.objects.get(Name=name)
                print(type_id)
                product_object.product_subcategory = type_id
                product_object.Name = data['Name']
                product_object.model = data['model']
                product_object.features = data['features']
                product_object.save()
                data['message'] = 'Product created successfully'
                return return_response(request, data=data)
            except:
                data1 = {}
                data1['message'] = 'There is no such subcategory'
                return return_response(request, data=data1)
        except:
            data1 = {}
            data1['message'] = 'Product already created'
            return return_response(request, data=data1)
    else:
        data1 = {}
        data1['message'] = 'Please enter a value'
        return return_response(request, data=data1)

@api_view(['GET'])
def get_users(request):
    users_object = list(User_Registration.objects.values())
    return return_response(request, data=users_object)

@api_view(['GET'])
def get_categories(request):
    users_object = list(Category.objects.values())
    return return_response(request, data=users_object)

@api_view(['GET'])
def get_subcategories(request):
    users_object = list(SubCategory.objects.annotate(category=F('product_category__Name'))
                        .values('category', 'id', 'Name'))
    return return_response(request, data=users_object)

@api_view(['GET'])
def get_products(request):
    users_object = list(Product.objects.annotate(subcategory=F('product_subcategory__Name'))
                        .values('subcategory', 'id', 'Name', 'model', 'features'))
    return return_response(request, data=users_object)

@api_view(['GET'])
def get_particular_subcategory(request, id):
    data = list(SubCategory.objects.annotate(category=F('product_category__Name')).filter(product_category_id=id)
                .values('category', 'id', 'Name'))
    if len(data) > 0:
        return return_response(request, data=data)
    data1 = {}
    data1['message'] = 'There is no such Category/Empty Subcategory'
    return return_response(request, data=data1)

@api_view(['GET'])
def get_particular_product(request, id):
    data = list(Product.objects.annotate(subcategory=F('product_subcategory__Name')).filter(product_subcategory_id=id)
                .values('subcategory', 'id', 'Name', 'model', 'features'))
    if len(data) > 0:
        return return_response(request, data=data)
    data1 = {}
    data1['message'] = 'There is no such SubCategory/Empty products'
    return return_response(request, data=data1)

@api_view(['GET'])
def get_details(request):
    li=[]
    data = Category.objects.all()
    for i in data:
        data1 = list(SubCategory.objects.filter(product_category_id=i.id).values('id','Name'))
        for j in data1:
            data2 = list(Product.objects.filter(product_subcategory_id=j['id']).values('Name','model','Name',
                                                                                       'features'))
            result = {}
            result['category'] = i.Name
            result['subcategory'] = j['Name']
            result['products'] = data2
            li.append(result)
    return return_response(request, data=li)