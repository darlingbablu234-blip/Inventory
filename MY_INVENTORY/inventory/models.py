from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    UNIT_CHOICES = [
        ('pc', 'Piece'),
        ('kg', 'Kilogram'),
        ('L', 'Liter'),
        ('m', 'Meter'),
        ('box', 'Box'),
        ('dozen', 'Dozen'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text="Stock Keeping Unit")
    quantity = models.IntegerField(default=0)
    reorder_point = models.IntegerField(default=10, help_text="Minimum quantity threshold")
    reorder_quantity = models.IntegerField(default=50, help_text="Suggested quantity to reorder")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='pc')
    image = models.ImageField(upload_to='items/', null=True, blank=True, help_text="Product image")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def needs_reorder(self):
        return self.quantity <= self.reorder_point
    
    @property
    def total_value(self):
        return self.quantity * self.price

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJ', 'Adjustment'),
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} {self.quantity} of {self.item.name}"

class ItemBatch(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=50)
    quantity = models.IntegerField()
    expiry_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('item', 'batch_number')
    
    def __str__(self):
        return f"{self.item.name} - Batch {self.batch_number}"
    
    @property
    def is_expired(self):
        if self.expiry_date:
            from datetime import date
            return self.expiry_date < date.today()
        return False

class AuditLog(models.Model):
    ACTION_TYPES = [
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Deleted'),
        ('STOCK_IN', 'Stock In'),
        ('STOCK_OUT', 'Stock Out'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
