from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import EmployeeService
from .serializer import EmployeeSerializer


class EmployeeViewSet(APIView):
    def get(self, request):
        employees, error = EmployeeService.get_all_employees()
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        employee, error = EmployeeService.create_employee(request.data)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmployeeDetailView(APIView):
    def get(self, request, pk):
        employee, error = EmployeeService.get_employee_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee, error = EmployeeService.get_employee_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        updated_employee, update_error = EmployeeService.update_employee(
            employee, request.data)
        if update_error:
            return Response({'error': update_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmployeeSerializer(updated_employee)
        return Response(serializer.data)

    def delete(self, request, pk):
        employee, error = EmployeeService.get_employee_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        delete_error = EmployeeService.delete_employee(employee)
        if delete_error:
            return Response({'error': delete_error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_204_NO_CONTENT)
