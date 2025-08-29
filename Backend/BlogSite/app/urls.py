from django.urls import path,include
from .views import RegisterView,PostViewset,CommentViewset,CategoryViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts',PostViewset,basename= 'posts')
router.register(r'comments',CommentViewset,basename= 'comments')
router.register(r'category',CategoryViewset,basename= 'category')

urlpatterns = [
    path('', include(router.urls)),
    path('register/',RegisterView.as_view()),
    # path('login/',LoginView.as_view()),
]
