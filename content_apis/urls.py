from django.urls import path, include
from rest_framework import routers

from .views import ContentAPIViewset

apiRouter = routers.DefaultRouter()
apiRouter.register(r"content",
                    ContentAPIViewset,
                    basename="content_api_viewset"
                )

urlpatterns = [
    path("", include(apiRouter.urls), name="content_apis")
]
