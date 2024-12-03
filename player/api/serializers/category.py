from rest_framework import serializers

from player.models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'parent']

    def validate_parent(self, value):
        if self.instance:  # Ensure we're updating, not creating
            if value == self.instance:
                raise serializers.ValidationError('A category cannot be its own subcategory')
        return value

    def validate_title(self, value):
        if self.instance:  # Ensure we're updating, not creating
            if value == self.instance.title:
                raise serializers.ValidationError('The category title is already in use')
        return value

class NestedCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'children']
        read_only_fields = ['children']

    def get_children(self, obj):
        children = obj.children.all()
        if children:
            return NestedCategorySerializer(children, many=True).data
        return None