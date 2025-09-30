from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import TaskService
from .serializer import TaskSerializer
from apps.common.decorators import (
    task_list_schema,
    task_create_schema,
    task_detail_schema,
    task_update_schema,
    task_delete_schema,
    task_status_update_schema
)


class TaskViewSet(APIView):
    @task_list_schema()
    def get(self, request):

        employee_id = request.query_params.get('employee_id', None)
        status_filter = request.query_params.get('status', None)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))

        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 10

        if employee_id:
            tasks, error = TaskService.get_tasks_by_employee(employee_id)
        else:
            tasks, error = TaskService.get_all_tasks()

        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if status_filter:
            tasks = tasks.filter(status=status_filter)

        total = tasks.count()
        start = (page - 1) * page_size
        end = start + page_size
        tasks_page = tasks[start:end]

        serializer = TaskSerializer(tasks_page, many=True)

        return Response({
            'data': serializer.data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': (total + page_size - 1) // page_size
            }
        })

    @task_create_schema()
    def post(self, request):

        task, error = TaskService.create_task(request.data)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailView(APIView):
    @task_detail_schema()
    def get(self, request, pk):
        task, error = TaskService.get_task_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @task_update_schema()
    def put(self, request, pk):

        task, error = TaskService.get_task_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        updated_task, update_error = TaskService.update_task(
            task, request.data)
        if update_error:
            return Response({'error': update_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(updated_task)
        return Response(serializer.data)

    @task_delete_schema()
    def delete(self, request, pk):

        task, error = TaskService.get_task_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        _, delete_error = TaskService.delete_task(task)
        if delete_error:
            return Response({'error': delete_error}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': 'Task deleted successfully'
        }, status=status.HTTP_200_OK)


class TaskStatusUpdateView(APIView):
    @task_status_update_schema()
    def patch(self, request, pk):
        task, error = TaskService.get_task_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if not new_status:
            return Response({
                'error': 'status field is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        valid_statuses = ['open', 'blocked', 'inprogress', 'qa', 'done']
        if new_status not in valid_statuses:
            return Response({
                'error': f'Invalid status. Must be one of: {valid_statuses}'
            }, status=status.HTTP_400_BAD_REQUEST)

        updated_task, update_error = TaskService.update_task(
            task, {'status': new_status})
        if update_error:
            return Response({'error': update_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(updated_task)
        return Response(serializer.data)
