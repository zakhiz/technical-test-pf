from ..models import Position
from ..serializer import PositionSerializer
from apps.common.constants import ERROR_MESSAGES


class PositionService:
    @staticmethod
    def get_all_positions():
        try:
            positions = Position.objects.all()
            return positions, None
        except Exception as e:
            return None, f"Error getting all positions: {e}"

    @staticmethod
    def get_position_by_id(position_id):
        try:
            position = Position.objects.get(
                id=position_id)
            return position, None
        except Position.DoesNotExist:
            return None, ERROR_MESSAGES['position']['not_found']
        except Exception as e:
            return None, f"Error getting position by id: {e}"

    @staticmethod
    def create_position(data):
        try:
            serializer = PositionSerializer(data=data)
            if serializer.is_valid():
                position = serializer.save()
                return position, None
            return None, serializer.errors
        except Exception as e:
            return None, f"Error creating position: {str(e)}"

    @staticmethod
    def update_position(position, data):
        try:
            serializer = PositionSerializer(position, data=data, partial=True)
            if serializer.is_valid():
                updated_position = serializer.save()
                return updated_position, None
            return None, serializer.errors
        except Exception as e:
            return None, f"Error updating position: {str(e)}"

    @staticmethod
    def delete_position(position):
        try:
            if position.employee_set.exists():
                return False, ERROR_MESSAGES['position']['has_employees']
            position.delete()
            return True, None
        except Exception as e:
            return None, f"Error deleting position: {str(e)}"
