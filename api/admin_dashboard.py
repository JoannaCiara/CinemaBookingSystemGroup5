from django.contrib import admin
from django.db.models import Count, Sum
from django.urls import path
from django.http import HttpResponse
from .models import Booking, Screening, Movie

class AnalyticsAdmin(admin.ModelAdmin):
    change_list_template = "admin/analytics_dashboard.html"

    def changelist_view(self, request, extra_context=None):
        stats = {
            "total_bookings": Booking.objects.count(),
            "total_revenue": Booking.objects.aggregate(Sum("price"))["price__sum"] or 0,
            "most_booked_movie": Movie.objects.annotate(num=Count("screenings__booking"))
                                .order_by("-num").first(),
        }
        extra_context = {"stats": stats}
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Booking, AnalyticsAdmin)
