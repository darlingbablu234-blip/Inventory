from django import forms
from .models import Item, StockMovement, Category, Supplier, ItemBatch

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'sku', 'description', 'quantity', 'price', 'unit', 'image', 'reorder_point', 'reorder_quantity', 'category', 'supplier']

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['item', 'quantity', 'movement_type', 'reason']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_info']

class ItemBatchForm(forms.ModelForm):
    class Meta:
        model = ItemBatch
        fields = ['batch_number', 'quantity', 'expiry_date']