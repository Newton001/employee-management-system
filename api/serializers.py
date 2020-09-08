"""Serializers

Module to serialize models into JSON format.
"""
from rest_framework import serializers
from .models import Employee, Department


class DepartmentSerializer(serializers.ModelSerializer):
    """Department JSON serializer"""

    class Meta:
        model = Department
        fields = ('code', 'name')


class EmployeeSerializer(serializers.ModelSerializer):
    """Employee JSON serializer"""

    class Meta:
        model = Employee
        fields = ('pk', 'name', 'email', 'department')

    def create(self, validated_data):
        employee = Employee.objects.create(**validated_data)
        employee.save()
        return employee
