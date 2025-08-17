from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Movie, CinemaHall, Seat, Screening, Booking
from .serializers import (
    MovieSerializer,
    CinemaHallSerializer,
    SeatSerializer,
    ScreeningSerializer,
    BookingSerializer,
)

# Public endpoints
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]  # Public


class ScreeningViewSet(viewsets.ModelViewSet):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer
    permission_classes = [AllowAny]  # Public

# Protected endpoints (login required)
class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = [IsAuthenticated]


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Seat

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        screening_id = self.request.query_params.get("screening")
        if screening_id:
            queryset = queryset.filter(screening_id=screening_id)
        return queryset

    @action(detail=False, methods=['get'], url_path='available-seats')
    def available_seats(self, request):
        """Get list of available seats for a given screening."""
        screening_id = request.query_params.get("screening")
        if not screening_id:
            return Response({"error": "Please provide ?screening=<id>"}, status=400)

        booked_seats = Booking.objects.filter(screening_id=screening_id).values_list('seat_id', flat=True)
        available_seats = Seat.objects.exclude(id__in=booked_seats).values('id', 'seat_number', 'seat_type')
        return Response(available_seats)
