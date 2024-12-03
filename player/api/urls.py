from rest_framework.routers import DefaultRouter

from player.api.views.music import MusicViewSet

router = DefaultRouter()
router.register(r'musics', MusicViewSet, basename='musics')

urlpatterns = [

              ] + router.urls
