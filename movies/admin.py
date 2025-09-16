# movies/admin.py
from django.contrib import admin
from .models import Movie
# If you also added Review/Favorite models earlier, you can register them too:
# from .models import Review, Favorite

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # Columns shown in the changelist
    list_display = ("name", "price", "amount_left", "is_available_admin")
    list_filter = ("amount_left",)
    search_fields = ("name", "description")
    ordering = ("name",)

    # Fields shown on the edit page (order matters)
    fields = ("name", "description", "price", "image", "amount_left")

    def is_available_admin(self, obj):
        # mirrors your model helper but safe for admin display
        return (obj.amount_left is None) or (obj.amount_left > 0)
    is_available_admin.boolean = True
    is_available_admin.short_description = "Available?"

    def get_readonly_fields(self, request, obj=None):
        """
        Admin can set/update amount_left anytime EXCEPT when it is exactly 0.
        (They can still edit other fields.)
        """
        ro = list(super().get_readonly_fields(request, obj))
        if obj and obj.amount_left == 0:
            ro.append("amount_left")
        return ro


# Optional: if you want quick admin access to reviews/favorites
# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ("movie", "user", "rating", "created_at")
#     list_filter = ("rating", "created_at")
#     search_fields = ("movie__name", "user__username", "text")
#
# @admin.register(Favorite)
# class FavoriteAdmin(admin.ModelAdmin):
#     list_display = ("user", "movie", "created_at")
#     search_fields = ("user__username", "movie__name")
#     list_filter = ("created_at",)
