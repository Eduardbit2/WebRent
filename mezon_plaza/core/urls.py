from django.urls import path
from .views import (
    unit_list, tenant_detail, unit_detail, add_comment,
    add_contact, unit_create
)

app_name = 'core'

urlpatterns = [
    path('', unit_list, name='unit_list'),  # доступно по /units/
    path('tenant/<int:tenant_id>/', tenant_detail, name='tenant_detail'),
    path('unit/<int:unit_id>/', unit_detail, name='unit_detail'),
    path('tenant/<int:tenant_id>/comment/', add_comment, name='add_comment_tenant'),
    path('unit/create/', unit_create, name='unit_create'),
    path('unit/<int:unit_id>/comment/', add_comment, name='add_comment_unit'),
    path('tenant/<int:tenant_id>/add_contact/', add_contact, name='add_contact'),
]
