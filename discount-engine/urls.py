from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from .discounts.views import DiscountViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/discounts/', DiscountViewSet.as_view(), name='discounts')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
