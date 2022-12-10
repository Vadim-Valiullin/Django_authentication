from rest_framework import serializers

from aaa.models import Ads, User, Location, Category, Selection


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AdsListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), required=False, slug_field='first_name')
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), required=False, slug_field='name')
    class Meta:
        model = Ads
        fields = ['id', 'name', 'author', 'price', 'category']


class AdsDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='first_name')
    # category = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Ads
        fields = ['id', 'name', 'author_id', 'author', 'price', 'description', 'is_published', 'category_id', 'image' ]


class AdsCreateSerializer(serializers.ModelSerializer):
    # is_published = serializers.BooleanField(validators=[NotTrueValidator()])
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Ads
        fields = '__all__'


class AdsUpdateSerializer(serializers.ModelSerializer):
    # is_published = serializers.BooleanField(validators=[NotTrueValidator()])
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Ads
        fields = '__all__'


class AdsDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
        # exclude = ['author']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(queryset=Location.objects.all(), many=True, required=False,
                                             slug_field='name')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'role', 'age', 'age', 'locations']
        # exclude = ['password']


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')


    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(required=False, many=True, queryset=Location.objects.all(),
                                             slug_field='name')
    # email = serializers.EmailField(validators=[CheckRamblerEmail()])

    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'first_name', 'last_name', 'username', 'password','role', 'age', 'age', 'locations']
        # exclude = ["id"]

    # def is_valid(self, raise_exception=False):
    #     self._locations = self.initial_data.pop("locations")
    #     return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = super().create(validated_data)

        user.set_password(user.password)

        # for locations in self._locations:
        #     obj, _ = Location.objects.get_or_create(name=locations)
        #     user.locations.add(obj)

        # user.set_password(validated_data["password"])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(required=False, many=True, queryset=Location.objects.all(),
                                             slug_field='name')
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        # fields = ['id', 'first_name', 'last_name', 'username', 'password', 'role', 'age', 'age', 'locations']
        exclude = ["id"]
    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()

        for locations in self._locations:
            obj, _ = Location.objects.get_or_create(name=locations)
            user.locations.add(obj)
        user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class SelectionDetailViewSerializer(serializers.ModelSerializer):
    items = AdsDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateViewSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        required=False,
        many=True,
        slug_field='id',
        queryset=Ads.objects.all())
    owner = serializers.SlugRelatedField(required=False, slug_field='id', queryset=User.objects.all())

    class Meta:
        model = Selection
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._items = self.initial_data.pop("items")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        request = self.context.get('request', None)
        selection = Selection.objects.create(**validated_data, owner_id=request.user.id)

        for item in self._items:
            item_obj, _ = Ads.objects.get_or_create(pk=item)
            selection.items.add(item_obj)
        selection.save()
        return selection

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.items.clear()
        for item in self._items:
            item_obj, _ = Ads.objects.get_or_create(pk=item)
            instance.items.add(item_obj)
        instance.save()
        return instance


class SelectionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']
