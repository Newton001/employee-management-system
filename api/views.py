from rest_framework import generics, response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

from api.models import Department, Employee
from api.serializers import DepartmentSerializer, EmployeeSerializer

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





class SwaggerSchemaView(APIView):
    """Swagger Schema View"""
    permission_classes = [AllowAny]
    renderer_classes =  [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)
        return response.Response(schema)


class DepartmentListView(generics.ListAPIView):
    """Define service to get departments list"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeCreateView(generics.ListCreateAPIView):
    """
    get:
    Return a list of all employees.

    post:
    Create a new employee.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def post(self, request, *args, **kwargs):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDeleteView(generics.DestroyAPIView):
    """delete:
    Delete an employee.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
