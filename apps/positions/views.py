from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import PositionService
from .serializer import PositionSerializer


class PositionViewSet(APIView):
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))

        positions, error = PositionService.get_all_positions(
            request.query_params, page, page_size)
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(positions)

    def post(self, request):
        position, error = PositionService.create_position(request.data)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(position, status=status.HTTP_201_CREATED)


class PositionDetailView(APIView):
    def get(self, request, pk):
        position, error = PositionService.get_position_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        return Response(position)

    def put(self, request, pk):
        updated_position, update_error = PositionService.update_position(
            pk, request.data)
        if update_error:
            return Response({'error': update_error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_position)

    def delete(self, request, pk):

        delete_response, delete_error = PositionService.delete_position(pk)
        if delete_error:
            return Response({'error': delete_error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(delete_response, status=status.HTTP_204_NO_CONTENT)
