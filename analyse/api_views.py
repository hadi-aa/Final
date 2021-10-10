from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from analyse import permissions as analyse_permissions

from analyse.models import Organization, Product
from analyse.serializers import OrganizationSerializer, ProductSerializer


class OrganizationViewSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [analyse_permissions.IsUserorReadOnly]

    def get_queryset(self):
        queryset = Organization.objects.filter(user_id=self.request.user.pk)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [analyse_permissions.IsUserorReadOnly]
    queryset = Product.objects.all()
