"""Serializers

Module to serialize models into JSON format.
"""
from rest_framework import serializers
from .models import Employee, Duty, Task


class DutySerializer(serializers.ModelSerializer):
    """Duty JSON serializer"""

    class Meta:
        model = Duty
        fields = ('code', 'name')


class EmployeeSerializer(serializers.ModelSerializer):
    """Employee JSON serializer"""

    class Meta:
        model = Employee
        fields = ('pk', 'name', 'email', 'duty')

    def create(self, validated_data):
        employee = Employee.objects.create(**validated_data)
        employee.save()
        return employee

class TaskSerializer(serializers.ModelSerializer):
    """Task JSON serializer"""

    class Meta:
        model = Task
        fields = ( 'name', 'pk',)

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        task.save()
        return task
