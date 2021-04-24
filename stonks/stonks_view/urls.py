from django.urls import path, include
from stonks_view import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'company-earnings', views.CopmanyEarningsViewSet, basename="copmanyearnings")

# user_list

urlpatterns = [
    path('', include(router.urls)),
    # path('company-earnings1/<str:ticker>/', views.CopmanyEarningsView.as_view()),
]