from rest_framework import serializers

from music_player.validators import validate_image_file, validate_audio_file
from player.models import Music


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = [
            'title', 'description', 'image', 'music'
        ]

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError('Title is required')
        if Music.objects.filter(title=value).exists():
            raise serializers.ValidationError('Title already exists')
        return value

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError('Description is required')

        if len(value) > 500:
            raise serializers.ValidationError('Description too long')
        return value

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError('Image is required')

        validate_image_file(value)

        return value

    def validate_music(self, value):
        if not value:
            raise serializers.ValidationError('Music is required')
        validate_audio_file(value)
        return value


class ListMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = [
            'id', 'title', 'image'
        ]
