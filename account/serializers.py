from django.contrib.auth.models import User
from rest_framework import serializers

from account.models import Category, Worker_cardImages, Comment, Worker_card
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs.get('password') != password2:
            raise serializers.ValidationError(
                'Passwords did not match!')
        if not attrs.get('password').isalnum():
            raise serializers.ValidationError(
                'Password field must be contain alpha and nums!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs



class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=30, required=True)
    code = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=4,required=True)
    password2 = serializers.CharField(min_length=4, required=True)

    def validate(self, attrs,):
        password = attrs['password']
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords does not match')

        email = attrs['email']
        try:
           user=User.objects.get(email=email)
        except User.DoesNotExcist:
            raise  serializers.ValidationError('User with this email does not exists')

        code = attrs['code']
        if user.activation_code != code:
            raise serializers.ValidationError('Code is incorrect')
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        user = data['user']

        user.set_password(data['password'])
        user.activation_code = ''
        user.save()

        return user

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=25,required=True)





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class Worker_cardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker_cardImages
        exclude = ('id',)


class Worker_cardSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(
        source='owner.username'
    )
    images = Worker_cardImageSerializer(many=True, read_only=False, required=False)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Worker_card
        fields = (
            'id', 'first_name', 'last_name', 'body',
            'owner', 'category', 'phone_number', 'images',
            'comments', 'location',
        )

    def create(self, validated_data):
        print('validated data: ', validated_data)
        request = self.context.get('request')
        print('FILES', request.FILES)
        images_data = request.FILES
        created_card = Worker_card.objects.create(**validated_data)
        images_objects = [Worker_cardImages(card=created_card, image=image) for image in images_data.getlist('images')]
        Worker_cardImages.objects.bulk_create(images_objects)
        return created_card

    def is_liked(self, card):
        user = self.context.get('request').user
        return user.liked.filter(card=card).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments_detail'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['images'] = Worker_cardImageSerializer(instance.card.all(), many=True).data
        user = self.context.get('request').user
        if user.is_authenticated:
            representation['is_liked'] = self.is_liked(instance)

        representation['likes_count'] = instance.likes.count()
        return representation


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'owner', 'card')