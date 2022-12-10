# from django.conf import settings
# from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import UpdateView, ListView, DeleteView, DetailView, CreateView
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

import json
from aaa.models import Ads, Category, User, Location, Selection
from aaa.permissions import AdsUpdatePermission, SelectionUpdatePermission
from aaa.serializers import UserListSerializer, AdsListSerializer, \
    UserDetailSerializer, UserCreateSerializer, UserUpdateSerializer, UserDestroySerializer, CategorySerializer, \
    LocationSerializer, AdsDestroySerializer, AdsUpdateSerializer, AdsCreateSerializer, AdsDetailSerializer, \
    SelectionViewSerializer, SelectionDetailViewSerializer, SelectionCreateViewSerializer


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def index(request):
    return JsonResponse({'status': 'ok'}, status=200)


class AdsListView(ListAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsListSerializer

    def get(self, request, *args, **kwargs):
        cat = request.GET.get('cat', None)
        if cat:
            self.queryset = self.queryset.filter(
                category__id=cat
            )

        text = request.GET.get('text', None)
        if text:
            self.queryset = self.queryset.filter(
                name__contains=text
            )

        location = request.GET.get('location', None)
        if location:
            self.queryset = self.queryset.filter(
                author__locations__name__icontains=location
            )

        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        if price_from or price_to:
            self.queryset = self.queryset.filter(
                price__range=[price_from, price_to]
           )


        return super().get(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ["name", "author_id", "price", "description", "category_id"]
    def patch(self, request, *args, **kwargs):
        try:
            Ads.objects.get(pk=kwargs['pk'])
        except Ads.DoesNotExist:
            return JsonResponse({"error": "there is no such id in the ad"}, status=404)
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        self.object.name = ad_data["name"]
        self.object.author_id = User.objects.get(id=ad_data["author"])
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.category_id = Category.objects.get(id=ad_data["category"])

        self.object.save()

        return JsonResponse({
          "id": self.object.id,
          "name": self.object.name,
          "author_id": self.object.author_id,
          "author": User.objects.get(id=self.object.author_id_id).first_name,
          "price": self.object.price,
          "description": self.object.description,
          "is_published": self.object.is_published,
          "category_id": self.object.category_id,
          "image": self.object.image.url if self.object.image else ""

        }, safe=False, json_dumps_params={"ensure_ascii": True})

@method_decorator(csrf_exempt, name="dispatch")
class AdsDeleteView(DeleteView):
     model = Ads
     success_url = '/'
     def delete(self, request, *args, **kwargs):
         try:
             Ads.objects.get(pk=kwargs['pk'])
         except Ads.DoesNotExist:
             return JsonResponse({"error": "there is no such id in the ad"}, status=404)

         super().delete( request, *args, **kwargs)
         return JsonResponse({"status": "ok"}, status=200)

class AdsDetailView(RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsDetailSerializer
    permission_classes = [IsAuthenticated]

    # def get(self, request, *args, **kwargs):
    #     try:
    #       ad = Ads.objects.get(pk=kwargs['pk'])
    #     except Ads.DoesNotExist:
    #         return JsonResponse({"error": "there is no such id in the ad"}, status=404)
    #
    #     return JsonResponse({
    #         "id": ad.id,
    #         "name": ad.name,
    #         "author_id": ad.author_id,
    #         "author": User.objects.get(id=ad.author_id).first_name,
    #         "price": ad.price,
    #         "description": ad.description,
    #         "is_published": ad.is_published,
    #         "category_id": ad.category_id,
    #         "image": ad.image.url if ad.image else ""
    #        }, safe=False, json_dumps_params={"ensure_ascii": True})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def AdsCreateView(request, *args, **kwargs):
    ad_data = json.loads(request.body)
    author = User.objects.get(pk=ad_data["author_id"])
    category = Category.objects.get(pk=ad_data["category_id"])
    ad = Ads.objects.create(
        name=ad_data["name"],
        author=author,
        price=ad_data["price"],
        description=ad_data["description"],
        is_published=ad_data["is_published"],
        category=category
    )
    return JsonResponse({
        "status": "ok",
        "name": ad.name,
        "author": ad.author.first_name
    })



# @method_decorator(csrf_exempt, name="dispatch")
# class AdsCreateView(CreateView):
#      model = Ads
#      def post(self, request, *args, **kwargs):
#           ad_data = json.loads(request.body)
#           try:
#               author_obj = User.objects.get(id=ad_data["author_id"])
#           except User.DoesNotExist:
#               return JsonResponse({"error": "Users not"}, status=404)
#           try:
#               category_obj = Category.objects.get(id=ad_data["category_id"])
#           except Category.DoesNotExist:
#               return JsonResponse({"error": "Categories not"}, status=404)
#
#           ad = Ads.objects.create(
#               name = ad_data["name"],
#               author = author_obj,
#               price = ad_data["price"],
#               description = ad_data["description"],
#               is_published = ad_data["is_published"],
#               category = category_obj
#           )
#
#           return JsonResponse({
#               "id": ad.id,
#               "name": ad.name,
#               "author_id": ad.author_id,
#               "price": ad.price,
#               "description" : ad.description,
#               "is_published" : ad.is_published,
#               "category_id" : ad.category_id
#           }, safe=False, json_dumps_params={"ensure_ascii": True})



#
class AdsDetailView(RetrieveAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsDetailSerializer


class AdsCreateView(CreateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsCreateSerializer


class AdsUpdateView(UpdateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsUpdateSerializer
    permission_classes = [IsAuthenticated, AdsUpdatePermission]


class AdsDeleteView(DestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsDestroySerializer
    permission_classes = [IsAuthenticated, AdsUpdatePermission]


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ads
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        })


# class CatView(ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class CatDetailView(RetrieveAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class CatCreateView(CreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class CatUpdateView(UpdateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class CatDeleteView(DestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_queryset(self):
        return User.objects.annotate(total_ads=Count('ads', filter=Q(ads__is_published=True)))


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    # model = User
    def get_queryset(self):
        return User.objects.annotate(total_ads=Count('ads', filter=Q(ads__is_published=True)))


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer


# class UserElseView(ListView): # Выводит кол-во объявлений автора
#     model = User
#
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#         self.object_list = self.object_list.annotate(total_ads=Count('ads', filter=Q(ads__is_published=True)))
#
#         paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#
#         users = []
#         for user in page_obj:
#             users.append({
#                 "id": user.id,
#                 "username": user.username,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "role": user.role,
#                 "age": user.age,
#                 "locations": list(user.locations.all().values_list("name", flat=True)),
#                 "total_ads": user.total_ads
#                 })
#         response = {
#             "items": users,
#             "total":paginator.count,
#             "num_pages": paginator.num_pages
#         }
#
#         return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": True})


class SelectionView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionViewSerializer


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailViewSerializer


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateViewSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateViewSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateViewSerializer
    permission_classes = [IsAuthenticated, SelectionUpdatePermission]


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

