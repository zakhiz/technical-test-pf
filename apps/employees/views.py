from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import EmployeeService
from .serializer import EmployeeSerializer


class EmployeeViewSet(APIView):
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))

        employees, error = EmployeeService.get_employees_with_filters(
            request.query_params, page, page_size)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(employees)

    def post(self, request):
        employee, error = EmployeeService.create_employee(request.data)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(employee, status=status.HTTP_201_CREATED)


class EmployeeDetailView(APIView):
    def get(self, request, pk):
        employee, error = EmployeeService.get_employee_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        return Response(employee)

    def put(self, request, pk):
        updated_employee, update_error = EmployeeService.update_employee(
            pk, request.data)
        print(updated_employee)
        if update_error:
            return Response({'error': update_error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_employee)

    def delete(self, request, pk):
        employee, error = EmployeeService.get_employee_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        replacement_employee_id = request.data.get('replacement_employee_id')
        if not replacement_employee_id:
            return Response({
                'error': 'replacement_employee_id is required for deletion'
            }, status=status.HTTP_400_BAD_REQUEST)

        success, delete_error = EmployeeService.delete_employee(
            employee.data, replacement_employee_id)
        if not success:
            return Response({'error': delete_error}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': 'Employee deleted successfully',
            'replacement_employee_id': replacement_employee_id,
            'deleted_at': employee.deleted_at
        }, status=status.HTTP_200_OK)


class SalaryReportView(APIView):

    def get(self, request):
        report, error = EmployeeService.get_salary_report()
        print(report)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(report)
