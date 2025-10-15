from ..models import Position
from ..serializer import PositionSerializer
from apps.common.constants import ERROR_MESSAGES


class PositionService:
    @staticmethod
    def get_all_positions(filters=None, page=1, page_size=10):
        try:
            if page < 1:
                page = 1
            if page_size < 1 or page_size > 100:
                page_size = 10

            query = {}

            if filters and filters.get('name'):
                query['name__icontains'] = filters['name']

            total = Position.objects(**query).count()
            total_pages = (total + page_size - 1) // page_size
            offset = (page - 1) * page_size

            positions = Position.objects(**query).skip(offset).limit(page_size)

            formated_positions = []

            for position in positions:
                position_data = {
                    "id": str(position.id),
                    "name": position.name,
                    "description": position.description,
                }
                formated_positions.append(position_data)
            return {
                'success': True,
                'message': 'Positions fetched successfully',
                'data': formated_positions,
                'total_positions': total,
                'total_pages': total_pages,
                'current_page': page,
            }, None
        except Exception as e:
            return None, f"Error getting all positions: {e}"

    @staticmethod
    def get_position_by_id(position_id):
        try:
            position = Position.objects.get(
                id=position_id)
            serializer = PositionSerializer(position)
            return {
                'success': True,
                'message': 'Position fetched successfully',
                'data': serializer.data
            }, None
        except Position.DoesNotExist:
            return None, ERROR_MESSAGES['position']['not_found']
        except Exception as e:
            return None, f"Error getting position by id: {e}"

    @staticmethod
    def create_position(data):
        try:
            serializer = PositionSerializer(data=data)
            if serializer.is_valid():
                new_position = serializer.save()
                return {
                    'success': True,
                    'message': 'Position created successfully',
                    'data': {
                        'id': str(new_position.id),
                    }
                }, None
            return None, serializer.errors
        except Exception as e:
            return None, f"Error creating position: {str(e)}"

    @staticmethod
    def update_position(pk, data):
        try:
            position = Position.objects.get(id=pk)
            serializer = PositionSerializer(position, data=data, partial=True)
            if serializer.is_valid():
                updated_position = serializer.save()
                return {
                    'success': True,
                    'message': 'Position updated successfully',
                    'data': {
                        'id': str(updated_position.id),
                    }
                }, None
            return None, serializer.errors
        except Exception as e:
            return None, f"Error updating position: {str(e)}"

    @staticmethod
    def delete_position(pk):
        try:
            position = Position.objects.get(id=pk)
            if not position:
                return None, ERROR_MESSAGES['position']['not_found']
            position.delete()
            return {
                'success': True,
                'message': 'Position deleted successfully',
            }, None
        except Position.DoesNotExist:
            return None, ERROR_MESSAGES['position']['not_found']
        except Exception as e:
            return None, f"Error deleting position: {str(e)}"
