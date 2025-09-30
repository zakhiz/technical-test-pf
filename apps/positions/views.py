from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import PositionService
from .serializer import PositionSerializer


class PositionViewSet(APIView):
    def get(self, request):
        positions, error = PositionService.get_all_positions()
        if error:
            return Response({'error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)

    def post(self, request):
        position, error = PositionService.create_position(request.data)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PositionSerializer(position)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PositionDetailView(APIView):
    def get(self, request, pk):
        position, error = PositionService.get_position_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        serializer = PositionSerializer(position)
        return Response(serializer.data)

    def put(self, request, pk):
        position, error = PositionService.get_position_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        updated_position, update_error = PositionService.update_position(
            position, request.data)
        if update_error:
            return Response({'error': update_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PositionSerializer(updated_position)
        return Response(serializer.data)

    def delete(self, request, pk):
        position, error = PositionService.get_position_by_id(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)

        delete_error = PositionService.delete_position(position)
        if delete_error:
            return Response({'error': delete_error}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)
