from django.urls import path, include
from stonks_view import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'company-earnings', views.CompanyEarningsViewSet, basename="companyearnings")
router.register(r'company-balance', views.CompanyBalanceViewSet)
router.register(r'company-cash-flow', views.CompanyCashFlowViewSet)
router.register(r'watch-list', views.WatchListViewSet)
router.register(r'watch-items', views.WatchItemsViewSet)
from pprint import pprint
pprint(router.urls)
pprint(router.get_default_basename(views.WatchItemsViewSet))
pprint(router.get_default_basename(views.WatchListViewSet))


# user_list

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserCreate.as_view()),
]