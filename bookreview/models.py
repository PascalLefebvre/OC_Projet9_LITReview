from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.db.models import CheckConstraint, F, Q
from PIL import Image


RATING_CHOICES = (
    (0, '- 0'),
    (1, '- 1'),
    (2, '- 2'),
    (3, '- 3'),
    (4, '- 4'),
    (5, '- 5'),
)



class Ticket(models.Model):
    """ A ticket for asking reviews. """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    
    IMAGE_SIZE = (80, 160)

    def resize_image(self):
        image = Image.open(self.image)
        image.resize(self.IMAGE_SIZE, Image.ANTIALIAS)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        self.resize_image()
        super().save(*args, **kwargs)

    def __str__(self):
        """ Return a string representation of the model. """
        return self.title


class Review(models.Model):
    """ A review in response to a ticket. """
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(blank=False, default=3, choices=RATING_CHOICES,
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ Return a simple string representing the review. """
        return f"{self.headline[:50]}"


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by")

    class Meta:
        # ensures we don't get multiple UserFollows instances for unique user-user_followed pairs
        unique_together = (
            "user",
            "followed_user",
        )
        constraints = [ CheckConstraint(name='not_same', check=~Q(user=F('followed_user'))) ]
        verbose_name_plural = "User follows"
    
    def __str__(self):
        """ Return a pair of usernames. """
        return f"{self.user.username} / {self.followed_user.username}"
