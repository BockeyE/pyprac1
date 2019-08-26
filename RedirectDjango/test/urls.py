from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns


# b
from test import views

urlpatterns = [

    url(r'^test', views.test),



]
print("url ========")
urlpatterns = format_suffix_patterns(urlpatterns)
