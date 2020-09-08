from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.schemas import SchemaGenerator
from rest_framework_swagger import renderers
from .views import DepartmentListView, EmployeeCreateView, EmployeeDeleteView

class JSONOpenAPIRender(renderers.OpenAPIRenderer):
    media_type = 'application/json'


def get_swagger_view(title=None, url=None, patterns=None, urlconf=None):
    """
    Returns schema view which renders Swagger/OpenAPI.
    """
    class SwaggerSchemaView(APIView):
        _ignore_model_permissions = True
        exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = [
            CoreJSONRenderer,
            JSONOpenAPIRender,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]

        def get(self, request):
            generator = SchemaGenerator(
                title=title,
                url=url,
                patterns=patterns,
                urlconf=urlconf
            )
            schema = generator.get_schema(request=request)

            if not schema:
                raise exceptions.ValidationError(
                    'The schema generator did not return a schema Document'
                )

            return Response(schema)

    return SwaggerSchemaView.as_view()


schema_view = get_swagger_view(title='Farm Employee Management API' ,url='/docs')

urlpatterns = {
    url(r'department', DepartmentListView.as_view(), name='list'),
    url(r'^employee+1', EmployeeCreateView.as_view(), name='add'),
    url(r'employeeview', EmployeeCreateView.as_view(), name='list'),
    url(r'employee(?P<pk>[0-9]+)/$', EmployeeDeleteView.as_view(), name='remove'),
    url(r'docs', schema_view),
}

urlpatterns = format_suffix_patterns(urlpatterns)
