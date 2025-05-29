from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    TrainType,
    Train,
    Station,
    Route,
    Crew,
    Journey,
    Ticket,
    Order
)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2"),
        }),
    )


@admin.register(TrainType)
class TrainTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ("name", "train_type", "cargo_num", "places_in_cargo")
    list_filter = ("train_type",)
    search_fields = ("name",)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance")
    search_fields = ("source__name", "destination__name")


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0


@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ("route", "train", "departure_time", "arrival_time")
    list_filter = ("route", "train", "departure_time")
    inlines = [TicketInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "user")
    list_filter = ("created_at", "user")
    search_fields = ("user__email",)


admin.site.register(Ticket)
