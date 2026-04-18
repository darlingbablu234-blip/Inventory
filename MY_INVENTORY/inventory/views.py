from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db import transaction, models
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, F
from django.contrib.auth.mixins import LoginRequiredMixin
from chartjs.views.lines import BaseLineChartView
from django.http import HttpResponse
import csv
from datetime import datetime, timedelta, date
from .models import Item, StockMovement, Category, Supplier, ItemBatch, AuditLog
from .forms import ItemForm, StockMovementForm, CategoryForm, SupplierForm, ItemBatchForm

# Create your views here.

class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        return queryset

class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'inventory/item_detail.html'
    context_object_name = 'item'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object
        context['batches'] = item.batches.order_by('-received_date')
        context['recent_movements'] = item.stockmovement_set.order_by('-created_at')[:8]
        context['audit_history'] = AuditLog.objects.filter(item=item, user=self.request.user).order_by('-timestamp')[:8]
        context['expired_batches'] = item.batches.filter(expiry_date__lt=date.today())
        return context

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('item_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        form.fields['supplier'].queryset = Supplier.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('item_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        form.fields['supplier'].queryset = Supplier.objects.filter(user=self.request.user)
        return form

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'inventory/item_confirm_delete.html'
    success_url = reverse_lazy('item_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class StockMovementCreateView(LoginRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'inventory/stock_movement_form.html'
    success_url = reverse_lazy('item_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['item'].queryset = Item.objects.filter(user=self.request.user)
        return form

    def form_valid(self, form):
        with transaction.atomic():
            movement = form.save()
            item = movement.item
            if movement.movement_type == 'IN':
                item.quantity += movement.quantity
            elif movement.movement_type == 'OUT':
                if item.quantity >= movement.quantity:
                    item.quantity -= movement.quantity
                else:
                    form.add_error('quantity', 'Not enough stock')
                    return self.form_invalid(form)
            elif movement.movement_type == 'ADJ':
                item.quantity = movement.quantity  # adjust to this quantity
            item.save()
        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Item.objects.filter(user=self.request.user)
        categories = Category.objects.filter(user=self.request.user)
        suppliers = Supplier.objects.filter(user=self.request.user)
        
        total_items = items.count()
        total_value = sum(item.quantity * item.price for item in items)
        low_stock_count = items.filter(quantity__lt=10).count()
        recent_movements = StockMovement.objects.filter(item__user=self.request.user).order_by('-created_at')[:5]
        
        # For chart: value by category
        category_dict = {}
        for item in items:
            cat_name = item.category.name if item.category else 'Uncategorized'
            value = item.quantity * float(item.price)
            category_dict[cat_name] = category_dict.get(cat_name, 0) + value
        categories_chart = list(category_dict.keys())
        values = list(category_dict.values())
        
        context.update({
            'total_items': total_items,
            'total_value': total_value,
            'low_stock_count': low_stock_count,
            'total_categories': categories.count(),
            'total_suppliers': suppliers.count(),
            'recent_movements': recent_movements,
            'categories': categories_chart,
            'values': values,
        })
        return context

class ReportView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Item.objects.filter(user=self.request.user)
        total_value = sum(item.quantity * item.price for item in items)
        low_stock = items.filter(quantity__lt=10)
        item_values = [{'item': item, 'value': item.quantity * item.price} for item in items]
        movements = StockMovement.objects.filter(item__user=self.request.user).order_by('-created_at')[:20]  # recent movements
        context['item_values'] = item_values
        context['total_value'] = total_value
        context['low_stock'] = low_stock
        context['movements'] = movements
        return context

class InventoryChartView(LoginRequiredMixin, BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]

def export_items_csv(request):
    if not request.user.is_authenticated:
        return redirect('login')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_items.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Description', 'Quantity', 'Price', 'Category', 'Supplier', 'Created At', 'Updated At'])

    items = Item.objects.filter(user=request.user)
    for item in items:
        writer.writerow([
            item.name,
            item.description,
            item.quantity,
            item.price,
            item.category.name if item.category else '',
            item.supplier.name if item.supplier else '',
            item.created_at,
            item.updated_at,
        ])

    return response

# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'inventory/category_form.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'inventory/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

# Supplier Views
class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'inventory/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('supplier_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'inventory/supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

# Low Stock Alert View
class LowStockView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'inventory/low_stock.html'
    context_object_name = 'low_stock_items'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, quantity__lt=10).order_by('quantity')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add total value calculation for each item
        for item in context['low_stock_items']:
            item.total_value = item.quantity * item.price
        return context

# Reorder Alert View
class ReorderAlertView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'inventory/reorder_alert.html'
    context_object_name = 'reorder_items'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, quantity__lte=models.F('reorder_point')).order_by('quantity')

# Audit Log View
class AuditLogView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'inventory/audit_log.html'
    context_object_name = 'logs'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-timestamp')

# Item Batch Views
class ItemBatchListView(LoginRequiredMixin, ListView):
    model = ItemBatch
    template_name = 'inventory/batch_list.html'
    context_object_name = 'batches'
    paginate_by = 10

    def get_queryset(self):
        item_id = self.kwargs.get('item_id')
        if item_id:
            return ItemBatch.objects.filter(item__user=self.request.user, item_id=item_id).order_by('-received_date')
        return ItemBatch.objects.filter(item__user=self.request.user).order_by('-received_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs.get('item_id')
        if item_id:
            context['item'] = Item.objects.get(id=item_id, user=self.request.user)
        return context

class ItemBatchCreateView(LoginRequiredMixin, CreateView):
    model = ItemBatch
    form_class = ItemBatchForm
    template_name = 'inventory/batch_form.html'
    
    def get_success_url(self):
        return reverse_lazy('batch_list', kwargs={'item_id': self.object.item.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs.get('item_id')
        context['item'] = Item.objects.get(id=item_id, user=self.request.user)
        return context
    
    def form_valid(self, form):
        item_id = self.kwargs.get('item_id')
        form.instance.item = Item.objects.get(id=item_id, user=self.request.user)
        return super().form_valid(form)

class ItemBatchDeleteView(LoginRequiredMixin, DeleteView):
    model = ItemBatch
    template_name = 'inventory/batch_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('batch_list', kwargs={'item_id': self.object.item.id})
    
    def get_queryset(self):
        return super().get_queryset().filter(item__user=self.request.user)

# Helper function to create audit log entries
def create_audit_log(user, item, action, description, old_value=None, new_value=None):
    AuditLog.objects.create(
        user=user,
        item=item,
        action=action,
        description=description,
        old_value=old_value,
        new_value=new_value
    )
