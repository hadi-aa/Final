from rest_framework import serializers

from analyse.models import Organization, Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = [
            'pk',
            'name',
            'description',
        ]

        read_only_fields = [
            'pk',
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    organization_products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    logo = serializers.ImageField(default='default.jpg')

    class Meta:
        model = Organization
        fields = [
            'pk',
            'name',
            'country',
            'logo',
            'employees_count',
            'organization_products',
            'repr_name',
            'repr_num',
            'repr_email',
        ]
        read_only_fields = [
            'pk',
        ]
