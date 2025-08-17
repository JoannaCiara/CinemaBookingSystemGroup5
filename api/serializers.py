from rest_framework import serializers
from .models import Movie, CinemaHall, Seat, Screening, Booking
from decimal import Decimal


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = "__all__"


class SeatSerializer(serializers.ModelSerializer):
    hall_name = serializers.ReadOnlyField(source="hall.name")

    class Meta:
        model = Seat
        fields = "__all__"


class ScreeningSerializer(serializers.ModelSerializer):
    movie_title = serializers.ReadOnlyField(source="movie.title")
    hall_name = serializers.ReadOnlyField(source="hall.name")
    end_time = serializers.ReadOnlyField()

    class Meta:
        model = Screening
        fields = "__all__"

    def validate(self, data):
        """
        Check for overlapping screenings in the same hall.
        """
        instance = Screening(**data)
        instance.full_clean()  # calls model clean() to check overlap
        return data


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['price', 'booked_at']
