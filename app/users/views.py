from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import BadHeaderError
from django.template import loader

# Create your views here.
User = get_user_model()

def register(request):
    next = request.GET.get('next', '/')
    try:
        username = request.POST['username']
        password = request.POST['password']
        auth_user = authenticate(request, username=username, password=password)
        try:
            login(request, auth_user)
            return HttpResponseRedirect(next)
        except:
            messages.error(request, 'Invalid credentials')
            return HttpResponseRedirect(next)
    except (KeyError):
        messages.error(request, 'Invalid credentials')
        return render(request, '/', { 'message': "Invalid username or password. Please try again." })


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        email = request.POST['email']

        print("----------------- register called")
        print(username)
        print(password)
        print(first_name)
        print(email)

         #try:
             #user = get_object_or_404(User, username=username)
         #except:
             #pass

        messages.success(request,
                         'Your account has been created! You can now login!')
        return redirect('login')
    else:
        return render(request, 'users/register.html')

from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer
from rest_framework.decorators import api_view

# Create your views here.
# def index(request):
#     return render(request, "tutorials/index.html")


#def index(request):
    #print("------------------------- I AM HERE")
    #queryset = User.objects.all()
    #return render(request, "users/index.html", {'users': queryset})


class login(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users/login.html'

    def get(self, request):
        queryset = User.objects.all()
        return Response({'users': queryset})

class logout(APIView):
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'users/logout.html'


class register(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users/register.html'
    #something with HTML here

    def get(self, request):
        queryset = User.objects.all()
        return Response({'users': queryset})
        


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def username(request):
    if request.method == 'GET':
        users = User.objects.all()

        user_name = request.GET.get('username', None)
        if user_name is not None:
            users = users.filter(user_name__icontains=user_name)

        user_serializer = UserSerializer(users, many=True)
        return JsonResponse(user_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = User.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Users were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'message': 'The user does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data)

    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def user_list_published(request):
    users = User.objects.filter(published=True)

    if request.method == 'GET':
        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
