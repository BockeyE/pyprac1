from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from interface import views

# zdz
urlpatterns = [
    # web
    url(r'^test$',views.test),
    url(r'^handle_tx$', views.handle_tx),

]
print("url ========")
urlpatterns = format_suffix_patterns(urlpatterns)
