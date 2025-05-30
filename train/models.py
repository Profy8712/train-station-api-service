from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Station(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="source_routes"
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="destination_routes"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} - {self.destination}"


class TrainType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField(default=0)
    places_in_cargo = models.IntegerField(default=0)
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE)

    @property
    def total_seats(self):
        if self.cargo_num is None or self.places_in_cargo is None:
            return 0
        return self.cargo_num * self.places_in_cargo

    def __str__(self):
        return f"{self.name} ({self.train_type})"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Journey(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    crews = models.ManyToManyField(Crew)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f"{self.route} at {self.departure_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id}"


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("journey", "cargo", "seat")

    def clean(self):
        if not (1 <= self.cargo <= self.journey.train.cargo_num):
            raise ValidationError(
                {"cargo": f"Cargo must be between 1 and {self.journey.train.cargo_num}"}
            )
        if not (1 <= self.seat <= self.journey.train.places_in_cargo):
            raise ValidationError(
                {"seat": f"Seat must be between 1 and {self.journey.train.places_in_cargo}"}
            )

    def __str__(self):
        return f"Ticket for {self.journey} (Cargo {self.cargo}, Seat {self.seat})"
