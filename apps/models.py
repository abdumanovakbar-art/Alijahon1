import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import CharField, DecimalField, Model, CASCADE, ForeignKey, ImageField, TextField, DateTimeField, \
    IntegerField, SlugField, TextChoices


class CustomUserManager(UserManager):

    def _create_user_object(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone_number, password, **extra_fields):
        """
        Create and save a user with the given  phone_number, and password.
        """
        user = self._create_user_object(phone_number, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


    phone_number = CharField(unique=True, max_length=20)
    balance = DecimalField(max_digits=10, decimal_places=0, default=0)
    coins = DecimalField(max_digits=10, decimal_places=0, default=0)
    api_key = CharField(max_length=255, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    password = CharField(max_length=255, null=True, blank=True)

    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    telegram_id = CharField(max_length=50, null=True, blank=True, default="")
    description = TextField(null=True, blank=True, default="")

    def generate_api_key(self):
        self.api_key = str(uuid.uuid4()).replace('-', '')
        self.save()

    referred_by = ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals'
    )
    referral_id = models.IntegerField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name() or self.phone_number}"



    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.phone_number

    @property
    def referral_count(self):
        """Get referral count"""
        return self.referrals.count()


class Transaction(Model):
    class TransactionType(TextChoices):
        MONEY = 'money', 'Money'
        COIN = 'coin', 'Coin'

    class TransactionStatus(TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESS = 'success', 'Success'
        REJECTED = 'rejected', 'Rejected'

    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='transactions')
    card_number = CharField(max_length=16)
    amount = DecimalField(max_digits=10, decimal_places=0)
    type = CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.MONEY)
    status = CharField(max_length=10, choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.phone_number} - {self.amount} {self.type}"


class Category(Model):
    title = CharField(max_length=255)
    image = ImageField(upload_to='products/')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(Model):
    title = CharField(max_length=50)
    price = DecimalField(max_digits=10, decimal_places=0)
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='products')
    description = TextField()
    amount = IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = ImageField(upload_to='products/')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Order(Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('waiting', 'Waiting'),
        ('delivering', 'Delivering'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled'),
    ]

    product = ForeignKey(Product, CASCADE, null=True)
    full_name = CharField(max_length=100)
    phone_number = CharField(max_length=20)
    quantity = IntegerField()
    total_price = IntegerField()
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class Stream(Model):
    amount = IntegerField(blank=True, null=True)
    title = CharField(max_length=255)
    discount = DecimalField(max_digits=10, decimal_places=0, default=0)
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='streams')
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='user_streams')
    created_at = DateTimeField(auto_now_add=True)

    visit = IntegerField(default=0)
    new_order = IntegerField(default=0)
    packing = IntegerField(default=0)
    delivering = IntegerField(default=0)
    delivered = IntegerField(default=0)
    waiting = IntegerField(default=0)
    returned = IntegerField(default=0)
    cancelled = IntegerField(default=0)
    hold = IntegerField(default=0)
    archived = IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.user.phone_number}"


class District(Model):
    title = CharField(max_length=255)

    def __str__(self):
        return self.title


class WishList(Model):
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='wishlists')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='wishlists')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.phone_number} - {self.product.title}"



class Competition(Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='competition/', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title


class CompetitionResult(Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='results')
    seller_name = models.CharField(max_length=255)
    sold_amount = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f"{self.rank}. {self.seller_name}"

