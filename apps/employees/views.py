from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import EmployeeService
from .serializer import EmployeeSerializer


class EmployeeViewSet(APIView):
    def get(self, request):
        position_filter = request.query_params.get('position', None)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))

        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 10

        employees, error = EmployeeService.get_employees_with_filters(
            position_filter, page, page_size)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = EmployeeSerializer(employees['data'], many=True)
        return Response({
            'data': serializer.data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': employees['total'],
                'total_pages': employees['total_pages']
            }
        })

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


class SalaryReportView(APIView):

    def get(self, request):
        report, error = EmployeeService.get_salary_report()
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'report': report,
            'message': 'Salary report generated successfully',
            'requested_by': 'Nacho (CFO)',
            'purpose': 'Weekly budget planning'
        })
