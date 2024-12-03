from rest_framework.routers import DefaultRouter

from player.api.views.category import CategoryViewSet
from player.api.views.music import MusicViewSet

router = DefaultRouter()
router.register(r'musics', MusicViewSet, basename='musics')
# router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [

              ] + router.urls
