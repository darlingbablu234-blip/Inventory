# Inventory Management Application

A Django-based web application for managing inventory items with a modern, responsive UI. Features include adding, editing, deleting items, tracking stock movements, categorizing items, searching, pagination, generating detailed reports, multi-user support with authentication, and data visualization.

## Features

### Core Features
- **Dashboard**: Overview with total items, value, low stock count, categories, suppliers, and recent movements.
- **Item Management**: Add, edit, and delete inventory items with categories and suppliers.
- **Stock Tracking**: Record stock movements (in, out, adjustments) that automatically update quantities.
- **Search and Pagination**: Search items by name, description, or category; paginated lists.
- **Reports**: Detailed reports with total value, low stock alerts, and recent movements.
- **Modern UI**: Responsive design with clean styling, navigation bar, and card-based layout.

### Advanced Features
- **User Authentication**: Multi-user support with login/logout and user-specific data isolation.
- **Category Management**: Full CRUD operations for item categories.
- **Supplier Management**: Track suppliers and link them to items.
- **Low Stock Alerts**: Visual warnings and dedicated page for items below quantity threshold (10 units).
- **Data Visualization**: Interactive pie charts showing inventory value by category.
- **CSV Export**: Export all inventory items to CSV format.
- **Local SQLite Database**: Simple, file-based storage.

## Setup

1. Install Python 3.11+ and Django 5.2+.
2. Clone or download the project.
3. Create virtual environment: `python -m venv venv`
4. Activate virtual environment: `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run development server: `python manage.py runserver`
9. Open http://127.0.0.1:8000/ in your browser and log in.

## 📱 Mobile Warehouse Access

Ready to use your app on mobile while away from the office?

### Quick Deploy (Recommended)
→ See **`QUICK_START_DEPLOY.md`** - Choose your deployment option in 2 minutes

### Deployment Options

#### Option 1: Railway.app (EASIEST) ⭐
- Deploy anywhere in 10 minutes
- Free tier available
- Works from phone anywhere
- **Guide:** `RAILWAY_DEPLOYMENT.md`

#### Option 2: Cloudflare Pages + Railway (FASTEST)
- Ultra-fast CDN frontend
- Railway backend API
- Best performance for mobile
- **Guide:** `CLOUDFLARE_PAGES_SETUP.md`

#### Option 3: Docker Locally
- Access on same WiFi network
- No cloud needed
- **Guide:** `DEPLOYMENT.md`

**For warehouse use, start with Railway.** ⬆️


## Usage

- **Login**: Access the login page at `/accounts/login/`
- **Dashboard**: View summary statistics, inventory value charts, and recent activity.
- **Items**: Browse, search, and manage inventory items with categories and suppliers.
- **Stock Movement**: Record changes to item quantities with reasons.
- **Low Stock Alerts**: Monitor items below quantity threshold.
- **Categories**: Manage item categories.
- **Suppliers**: Manage supplier information.
- **Reports**: View comprehensive inventory reports with analytics.
- **Export**: Download inventory as CSV file.

## Models

- **Item**: Inventory items with quantity, price, category, supplier, and user association.
- **Category**: Item groupings with user association.
- **Supplier**: Supplier information with contact details and user association.
- **StockMovement**: Logs quantity changes with types (IN, OUT, ADJ) and reasons.

## Authentication

- Multi-user support with Django's built-in authentication.
- Each user sees only their own inventory data.
- Login required for all views except login/register pages.

## Dependencies

- Django 5.2.13
- django-chartjs 2.3.0
- Python 3.11+