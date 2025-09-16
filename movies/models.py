from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/', blank=True, null=True)

    # NEW: must be at class indent level (not inside a method)
    amount_left = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Optional. Leave blank for unlimited."
    )

    def is_available(self) -> bool:
        """Visible to shoppers?"""
        return self.amount_left is None or self.amount_left > 0

    def decrease_amount(self, qty: int = 1):
        """Reduce stock after purchase."""
        if self.amount_left is not None and self.amount_left > 0:
            self.amount_left = max(0, self.amount_left - max(1, qty))
            self.save(update_fields=["amount_left"])

    def __str__(self):
        return f"{self.id} - {self.name}"


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} - {self.movie.name}"
