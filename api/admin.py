from django.contrib import admin
from .models import Movie, CinemaHall, Seat, Screening, Booking
from .forms import BookingForm


# ----------------- Movie Admin -----------------
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_minutes', 'rating', 'release_date', 'created_at')
    search_fields = ('title', 'rating')
    list_filter = ('rating', 'language')

# ----------------- Cinema Hall Admin -----------------
@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_seats', 'description')
    search_fields = ('name',)

# ----------------- Seat Admin -----------------
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('hall', 'row', 'number', 'seat_type', 'is_active')
    list_filter = ('hall', 'seat_type', 'is_active')
    search_fields = ('row', 'number')

# ----------------- Screening Admin -----------------
@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'start_time', 'price', 'status')
    list_filter = ('status', 'hall', 'movie')
    search_fields = ('movie__title',)

# ----------------- Booking Admin with instant price -----------------
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'screening', 'seat', 'status', 'price', 'booked_at')
    readonly_fields = ('price',)
    form = BookingForm

    class Media:
        js = ('js/booking_price.js',)

