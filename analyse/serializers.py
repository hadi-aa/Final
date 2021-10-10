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


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    organization_products = ProductSerializer
    # user = serializers.StringRelatedField()

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
                # 'user',
        ]
