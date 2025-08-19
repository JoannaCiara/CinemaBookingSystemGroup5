from datetime import timedelta, time
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

# ----- small choice sets -----
RATING_CHOICES = [
    ("G", "G"),
    ("PG", "PG"),
    ("PG-13", "PG-13"),
    ("R", "R"),
]

SEAT_TYPE_CHOICES = [
    ("REG", "Regular"),
    ("VIP", "VIP"),
]

SCREENING_STATUS = [
    ("SCHEDULED", "Scheduled"),
    ("CANCELLED", "Cancelled"),
]

BOOKING_STATUS = [
    ("PENDING", "Pending"),
    ("CONFIRMED", "Confirmed"),
    ("CANCELLED", "Cancelled"),
]


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    rating = models.CharField(max_length=6, choices=RATING_CHOICES, default="G")
    release_date = models.DateField(null=True, blank=True)
    language = models.CharField(max_length=50, default="English")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CinemaHall(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Seat(models.Model):
    hall = models.ForeignKey(CinemaHall, related_name="seats", on_delete=models.CASCADE)
    row = models.CharField(max_length=3)
    number = models.PositiveIntegerField()
    seat_type = models.CharField(max_length=3, choices=SEAT_TYPE_CHOICES, default="REG")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("hall", "row", "number")
        ordering = ["row", "number"]

    def __str__(self):
        return f"{self.hall.name} {self.row}{self.number}"


class Screening(models.Model):
    movie = models.ForeignKey(Movie, related_name="screenings", on_delete=models.CASCADE)
    hall = models.ForeignKey(CinemaHall, related_name="screenings", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=7, decimal_places=2, help_text="Base price per seat")
    status = models.CharField(max_length=12, choices=SCREENING_STATUS, default="SCHEDULED")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} @ {self.hall.name} on {self.start_time}"

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.movie.duration_minutes)

    def clean(self):
        overlapping = []
        for s in Screening.objects.filter(hall=self.hall).exclude(pk=self.pk):
            s_end = s.start_time + timedelta(minutes=s.movie.duration_minutes)
            if (self.start_time < s_end) and (self.end_time > s.start_time):
                overlapping.append(s)
        if overlapping:
            raise ValidationError("This screening overlaps with an existing screening in the same hall.")


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    screening = models.ForeignKey('Screening', on_delete=models.CASCADE)
    seat = models.ForeignKey(
        'Seat',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    customer_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    booked_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, editable=False, default=0.00)
    discount_code = models.CharField(max_length=20, blank=True, null=True)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)  # NEW

    def clean(self):
        if self.seat and Booking.objects.filter(screening=self.screening, seat=self.seat).exclude(pk=self.pk).exists():
            raise ValidationError("This seat is already booked for this screening.")

    def calculate_price(self):
        price = Decimal("850")  # base standard price

        # VIP surcharge
        if self.seat and self.seat.seat_type == "VIP":
            price *= Decimal("1.5")

        # Late screening surcharge (after 12 PM)
        if self.screening.start_time.time() >= time(12, 0):
            price += Decimal("100")

        # Hall-based pricing
        if self.seat and self.seat.hall.total_seats > 100:
            price *= Decimal("1.1")

        # Discount codes
        if self.discount_code:
            code = self.discount_code.upper()
            if code == "STUDENT10":
                price *= Decimal("0.9")
            elif code == "VIP20":
                price *= Decimal("0.8")
            elif code == "FREE":
                price = Decimal("0")

        return round(price, 2)

    def generate_qr(self):
        qr_data = (
            f"Booking ID: {self.id}\n"
            f"Movie: {self.screening.movie.title}\n"
            f"Hall: {self.screening.hall.name}\n"
            f"Seat: {self.seat}\n"
            f"Time: {self.screening.start_time}\n"
            f"Price: {self.price}"
        )
        qr_img = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        file_name = f"booking_{self.id}_qr.png"
        self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

    def send_confirmation_email(self):
        if self.email:
            send_mail(
                subject="Your Booking Confirmation",
                message=(
                    f"Hello {self.customer_name},\n\n"
                    f"Your booking is confirmed:\n"
                    f"Movie: {self.screening.movie.title}\n"
                    f"Hall: {self.screening.hall.name}\n"
                    f"Seat: {self.seat}\n"
                    f"Time: {self.screening.start_time}\n"
                    f"Price: {self.price}\n\n"
                    f"Thank you for booking with us!"
                ),
                from_email="noreply@cinemabooking.com",
                recipient_list=[self.email],
                fail_silently=True,
            )

    def save(self, *args, **kwargs):
        self.price = self.calculate_price()
        super().save(*args, **kwargs)  # save once (to get ID)
        self.generate_qr()
        super().save(update_fields=["qr_code"])  # save QR
        self.send_confirmation_email()

    def __str__(self):
        return f"{self.customer_name} - {self.screening} - {self.seat}"
