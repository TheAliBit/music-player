from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from player.api.serializers.music import MusicSerializer, ListMusicSerializer
from player.models import Music


class MusicViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Music.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ListMusicSerializer
        return MusicSerializer
