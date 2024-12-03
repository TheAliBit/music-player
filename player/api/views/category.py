from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from player.api.serializers.category import CategoryListSerializer, NestedCategorySerializer
from player.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action == 'nested':
            return NestedCategorySerializer
        return CategoryListSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='nested')
    def nested(self, request):
        categories = Category.objects.filter(parent=None)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
