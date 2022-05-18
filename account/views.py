
from rest_auth.views import LogoutView
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import status
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from account import serializers
from account.serializers import Worker_cardSerializer
from account.models import Worker_card, Category, Comment, Likes
from account.permissions import IsAuthor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView
from .send_email import send_confirmation_email, send_reset_password

from . import serializers


User = get_user_model()

class StandartPaginationClass(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class RegistrationApiView(APIView):
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg':'Successfully activated!'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg':'Link expired!'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer


class NewPasswordVew(APIView):
   def post(self, request):
       serializer = serializers.CreateNewPasswordSerializer(data=request.data)
       if serializer.is_valid(raise_exception=True):


           serializer.save()
           return Response('Password changed')


class ResetPasswordView(APIView):

    def post(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user = User.objects.get(email=serializer.data.get('email'))
            user.create_activation_code()
            user.save()
            send_reset_password(user)
            return Response('Chek your email')

#
# class UserRegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.RegisterSerializer
#
#
# class CustomLogoutView(LogoutView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#
# class UserListView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#
#
# class UserDetailView(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserDetailSerializer


# class PostCreateView(generics.CreateAPIView):
#     serializer_class = serializers.PostSerializer

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# class PostListView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer

# class PostDetailView(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer

# class PostUpdateView(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer

# class PostDeleteView(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer



class Worker_cardViewSet(ModelViewSet):
    class Meta:
        model = Worker_card
        fields = '__all__'

    queryset = Worker_card.objects.all()
    serializer_class = serializers.Worker_cardSerializer
    pagination_class = StandartPaginationClass
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category', 'owner',)
    search_fields = ('firstname','location', 'category',)

    def perform_create(self, serializer):
        # print(serializer.data)
        return serializer.save(owner=self.request.user)

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        card = self.get_object()
        comments = card.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        card = self.get_object()
        if request.user.liked.filter(card=card).exists():
            return Response('Вы уже лайкали этот пост', status=status.HTTP_400_BAD_REQUEST)
        Likes.objects.create(card=card, user=request.user)
        return Response('Вы поставили лайк', status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def remove_from_liked(self, request, pk):
        card = self.get_object()
        if not request.user.liked.filter(card=card).exists():
            return Response('Вы не лайкали пост', status=status.HTTP_400_BAD_REQUEST)
        request.user.liked.filter(card=card).delete()
        Likes.objects.create(card=card, user=request.user)
        return Response('Ваш лайк удален', status=status.HTTP_204_NO_CONTENT)

    # @action(['POST'], detail=True)
    # def add_to_rating(self, request, pk):
    #     card = self.get_object()
    #     if request.user.ratinged.filter(card=card).exists():
    #         return Response('Вы уже лайкали этот пост', status=status.HTTP_400_BAD_REQUEST)
    #     .objects.create(card=card, user=request.user)
    #     return Response('Вы поставили лайк', status=status.HTTP_201_CREATED)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    # api/v1/posts/1/comments/


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# class PostView(APIView):
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True,)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)


# class PostDetailView(APIView):
#     @staticmethod
#     def get_object(pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Exception("Not found")

#     def get(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors)

#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response("Deleted", status=204)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer



