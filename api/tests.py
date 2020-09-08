import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Employee, Department


class TestDepartment(TestCase):
    """Department test case."""

    client = APIClient()

    @classmethod
    def setUpClass(cls):
        super(TestDepartment, cls).setUpClass()

    def setUp(self):
        """Create departments to use in tests"""
        Department(code='arch', name='Architecture').save()
        Department(code='ecom', name='E-commerce').save()
        Department(code='mobi', name='Mobile').save()

    def tearDown(self):
        """Delete departments for test."""
        Department.objects.all().delete()

    def test_api_returns_departments_list(self):
        """Check if API returns department list with code and name."""
        departments = Department.objects.all()
        response = self.client.get(reverse('list'), format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        for department in departments:
            self.assertContains(response, department)


class TestEmployee(TestCase):
    """Employee test case."""

    client = APIClient()

    @classmethod
    def setUpClass(cls):
        super(TestEmployee, cls).setUpClass()

    def setUp(self):
        """Create departments to use in tests"""
        department_data = [('arch', 'Architecture'),
                           ('ecom', 'E-commerce'),
                           ('mobi', 'Mobile')]
        self.departments = []
        for department_info in department_data:
            department = Department(code=department_info[0],
                                    name=department_info[1])
            department.save()
            self.departments.append(department)

    def tearDown(self):
        """Delete departments for test."""
        Department.objects.all().delete()

    def test_model_can_add_an_employee(self):
        """Employee model test."""
        department = Department.objects.get(code='arch')
        employee = Employee(
            name='Arnaldo Pereira',
            email='arnaldo@luizalabs.com',
            department=department
        )
        employee.save()
        # Check if it's saved
        check_employee = Employee.objects.get(name='Arnaldo Pereira')
        self.assertIsNotNone(check_employee)

    def test_add_api_creates_employee(self):
        """Test to create an employee using the API."""
        response = self.client.post(
            reverse('add'),
            data={
                'name': 'Renato Pedigoni',
                'email': 'renato@luizalabs.com',
                'department': 'ecom'
            },
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_add_api_returns_400_if_department_doesnt_exist(self):
        """Check if API returns error if employee's department doesn't exist."""
        response = self.client.post(
            reverse('add'),
            data={
                'name': 'Fulano de Tal',
                'email': 'fulano@luizalabs.com',
                'department': '1234'
            },
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_api_returns_400_if_name_is_missing(self):
        """Check if API returns error if employee's name is missing."""
        response = self.client.post(
            reverse('add'),
            data={
                'email': 'fulano@luizalabs.com',
                'department': 'ecom'
            },
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_api_returns_400_if_email_is_missing(self):
        """Check if API returns error if employee's email is missing."""
        response = self.client.post(
            reverse('add'),
            data={
                'name': 'Fulano de Tal',
                'department': 'mobi'
            },
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_api_returns_employees_list(self):
        """Test to get employees list through API."""
        Employee(name='Arnaldo Pereira',
                 email='arnaldo@luizalabs.com',
                 department=self.departments[0]).save()
        Employee(name='Renato Pedigoni',
                 email='renato@luizalabs.com',
                 department=self.departments[1]).save()
        Employee(name='Thiago Catoto',
                 email='catoto@luizalabs.com',
                 department=self.departments[2]).save()
        response = self.client.get(reverse('list'), format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertIsNotNone(json.dumps(response.data))

    def test_remove_api_deletes_an_employee(self):
        """Test to delete an employee using the API."""
        employee = Employee(name='Arnaldo Pereira',
                            email='arnaldo@luizalabs.com',
                            department=self.departments[0])
        employee.save()
        response = self.client.delete(
            reverse('remove', kwargs={'pk': employee.pk}),
            format='json',
            follow=True
        )
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_api_returns_error_if_employee_doesnt_exist(self):
        """Test to delete an employee using the API."""
        response = self.client.delete(
            reverse('remove', kwargs={'pk': 12345}),
            format='json',
            follow=True
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
