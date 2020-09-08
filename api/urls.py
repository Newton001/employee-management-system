from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view

from .views import DepartmentListView, EmployeeCreateView, EmployeeDeleteView


schema_view = get_swagger_view(title='Farm Employee Management API', url='/docs')

urlpatterns = {
    url(r'^department/$', DepartmentListView.as_view(), name='list'),
    url(r'^employee/$', EmployeeCreateView.as_view(), name='add'),
    url(r'^employee/$', EmployeeCreateView.as_view(), name='list'),
    url(r'^employee/(?P<pk>[0-9]+)/$', EmployeeDeleteView.as_view(), name='remove'),
    url(r'^docs/$', schema_view),
}

urlpatterns = format_suffix_patterns(urlpatterns)
