from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.html import format_html  # Added import format_html
from .models import (
    Station,
    Route,
    TrainType,
    Train,
    Crew,
    Journey,
    Order,
    Ticket
)


User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2"),
        }),
    )


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance")
    list_filter = ("source", "destination")
    search_fields = ("source__name", "destination__name")


@admin.register(TrainType)
class TrainTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ("name", "train_type", "cargo_num", "places_in_cargo", "capacity")
    list_filter = ("train_type",)
    search_fields = ("name",)
    fields = ("name", "train_type", "cargo_num", "places_in_cargo", "capacity")
    readonly_fields = ("capacity",)

    def capacity(self, obj):
        seats = obj.total_seats
        return f"{seats} seats" if seats > 0 else "Not specified"

    capacity.short_description = "Total Capacity"


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "full_name")
    search_fields = ("first_name", "last_name")
    list_filter = ("first_name", "last_name")


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = ("journey", "order", "cargo", "seat")
    can_delete = False


@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ("route", "train", "departure_time", "arrival_time")
    list_filter = ("route", "train", "departure_time")
    search_fields = ("route__source__name", "route__destination__name")
    filter_horizontal = ("crews",)
    inlines = [TicketInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("user__email",)
    date_hierarchy = "created_at"


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("journey", "order_user", "seat_info", "purchase_date", "validation_status")
    list_filter = ("journey__route", "cargo")
    search_fields = ("order__user__email", "journey__route__source__name")
    readonly_fields = ("purchase_date", "seat_info", "validation_status")

    fieldsets = (
        (None, {
            'fields': ('journey', 'order', 'cargo', 'seat'),
            'description': 'Fill in all required fields for the ticket'
        }),
        ('Validation Info', {
            'fields': ('validation_status',),
            'classes': ('collapse',),
            'description': 'Automatic validation results'
        }),
    )

    def order_user(self, obj):
        return obj.order.user.email if obj.order and obj.order.user else "No user"

    order_user.short_description = "Passenger"
    order_user.admin_order_field = "order__user__email"

    def seat_info(self, obj):
        if obj.cargo and obj.seat:
            return f"Cargo {obj.cargo}, Seat {obj.seat}"
        return "Not assigned"

    seat_info.short_description = "Seat Assignment"

    def purchase_date(self, obj):
        return obj.order.created_at if obj.order else "No order"

    purchase_date.short_description = "Purchase Date"
    purchase_date.admin_order_field = "order__created_at"

    def validation_status(self, obj):
        try:
            obj.clean()
            return format_html('<span style="color: green;">✓ Valid</span>')
        except ValidationError as e:
            return format_html('<span style="color: red;">✗ Error: {}</span>', e)

    validation_status.short_description = "Validation Status"


# Registering a custom admin panel for a user
admin.site.register(User, CustomUserAdmin)