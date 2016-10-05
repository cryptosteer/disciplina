from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
# from website.views import TaskViewSet


# router = routers.DefaultRouter()
# router.register(r'tasks', TaskViewSet)

urlpatterns = [
    url(r'^', include('website.urls')),
    url(r'^admin/', admin.site.urls),
    # url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
