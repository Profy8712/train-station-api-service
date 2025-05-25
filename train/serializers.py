from rest_framework import serializers
from .models import (
    Station,
    Route,
    TrainType,
    Train,
    Crew,
    Journey,
    Ticket,
    Order
)


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ["id", "name", "latitude", "longitude"]


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()

    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]


class RouteListSerializer(RouteSerializer):
    source = StationSerializer()
    destination = StationSerializer()


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ["id", "name"]


class TrainSerializer(serializers.ModelSerializer):
    train_type = TrainTypeSerializer()

    class Meta:
        model = Train
        fields = ["id", "name", "cargo_num", "places_in_cargo", "train_type"]


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name", "full_name"]


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ["id", "route", "train", "departure_time", "arrival_time"]


class JourneyListSerializer(JourneySerializer):
    route = RouteListSerializer()
    train = TrainSerializer()
    crews = CrewSerializer(many=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Journey
        fields = [
            "id",
            "route",
            "train",
            "crews",
            "departure_time",
            "arrival_time",
            "tickets_available"
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "cargo", "seat", "journey"]

    def validate(self, attrs):
        data = super().validate(attrs)
        journey = attrs["journey"]
        train = journey.train

        if not (1 <= attrs["cargo"] <= train.cargo_num):
            raise serializers.ValidationError(
                {"cargo": f"Cargo number must be between 1 and {train.cargo_num}"}
            )

        if not (1 <= attrs["seat"] <= train.places_in_cargo):
            raise serializers.ValidationError(
                {"seat": f"Seat number must be between 1 and {train.places_in_cargo}"}
            )

        return data


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ["id", "created_at", "tickets"]

    def create(self, validated_data):
        with serializers.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ["id", "created_at", "user", "tickets"]
