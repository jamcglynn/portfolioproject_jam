#make this so not having front end piece-just json/insomnia use
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from rest_framework.decorators import api_view

# Create your views here.
# def index(request):
#     return render(request, "tutorials/index.html")


def index(request):
    print("------------------------- I AM HERE")
    queryset = Recipe.objects.all()
    return render(request, "recipes/index.html", {'recipes': queryset})


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'recipes/index.html'

    def get(self, request):
        queryset = Recipe.objects.all()
        return Response({'recipes': queryset})


class list_all_recipes(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'recipes/recipe_list.html'
    #something with HTML here

    def get(self, request):
        queryset = Recipe.objects.all()
        return Response({'recipes': queryset})


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def recipe_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.all()

        recipe_name = request.GET.get('recipe name', None)
        if recipe_name is not None:
            recipes = recipes.filter(recipe_name__icontains=recipe_name)

        recipes_serializer = RecipeSerializer(recipes, many=True)
        return JsonResponse(recipes_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        recipe_data = JSONParser().parse(request)
        recipe_serializer = RecipeSerializer(data=recipe_data)
        if recipe_serializer.is_valid():
            recipe_serializer.save()
            return JsonResponse(recipe_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(recipe_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Recipe.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Recipes were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def recipe_detail(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return JsonResponse({'message': 'The recipe does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        recipe_serializer = RecipeSerializer(recipe)
        return JsonResponse(recipe_serializer.data)

    elif request.method == 'PUT':
        recipe_data = JSONParser().parse(request)
        recipe_serializer = RecipeSerializer(recipe, data=recipe_data)
        if recipe_serializer.is_valid():
            recipe_serializer.save()
            return JsonResponse(recipe_serializer.data)
        return JsonResponse(recipe_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        recipe.delete()
        return JsonResponse({'message': 'Recipe was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def recipe_list_published(request):
    recipes = Recipe.objects.filter(published=True)

    if request.method == 'GET':
        recipes_serializer = RecipeSerializer(recipes, many=True)
        return JsonResponse(recipes_serializer.data, safe=False)
