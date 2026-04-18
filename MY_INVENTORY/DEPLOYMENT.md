# Deployment Guide - Mobile Warehouse Access

This guide explains how to deploy the inventory management application so you can access it on mobile devices while away from the office.

## Option 1: Local Network (Fastest for LAN)

**Best for**: Quick warehouse access on the same local network

### Setup
1. Get your machine's IP address:
   - Windows: Open Command Prompt and run `ipconfig`, find IPv4 Address
   - Mac/Linux: Open Terminal and run `ifconfig`

2. Update Django allowed hosts in `myinventory/settings.py`:
   ```python
   ALLOWED_HOSTS = ['192.168.1.100', 'localhost', '127.0.0.1']  # Use your IP
   ```

3. Run the server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

4. On your phone, open browser and visit: `http://192.168.1.100:8000`

## Option 2: Docker on Local Machine

**Best for**: Easy management and production-like environment

### Prerequisites
- Install Docker Desktop: https://www.docker.com/products/docker-desktop

### Setup
1. Build and run:
   ```bash
   docker-compose up -d
   ```

2. Create database:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. Create admin user:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. Access at: `http://localhost:8000` (on same machine)
   Or: `http://your-ip:8000` (from other devices)

## Option 3: Cloud Deployment (Remote Access)

**Best for**: Access from anywhere, always online

### Services (Recommended)
- **Railway.app** - Easiest setup (free tier available)
- **Heroku** - Popular but paid
- **PythonAnywhere** - Simple Python hosting
- **AWS/Azure/Google Cloud** - Full control, more complex

### Quick Railway Deployment
1. Create account at https://railway.app
2. Connect GitHub repository
3. Set environment variables:
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app.railway.app`
   - `SECRET_KEY=generate-random-key`
4. Deploy and get public URL
5. Access from anywhere: `https://your-app.railway.app`

### Quick PythonAnywhere Deployment
1. Upload project to https://www.pythonanywhere.com
2. Set up virtual environment
3. Configure web app with Django settings
4. Enable HTTPS
5. Access from anywhere: `https://yourusername.pythonanywhere.com`

## Option 4: AWS EC2 (Advanced)

**Best for**: Enterprise deployment, full control

### Basic Steps
1. Launch EC2 instance (Ubuntu 22.04)
2. Install Docker and Docker Compose
3. Clone project: `git clone <repo>`
4. Run: `docker-compose up -d`
5. Allocate Elastic IP for stable domain
6. Configure security groups to allow HTTP/HTTPS
7. Set up domain name or use IP directly

## Mobile Optimization Tips

- The app is fully responsive for mobile screens
- All tables convert to card view on narrow screens
- Forms are touch-friendly with proper spacing
- Navigation menu collapses on small screens

## Security Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Set `DEBUG=False` on deployed version
- [ ] Use HTTPS (SSL/TLS certificate)
- [ ] Configure strong admin password
- [ ] Regularly backup database
- [ ] Keep dependencies updated
- [ ] Use environment variables for sensitive data

## Troubleshooting

**Can't connect from mobile?**
- Check firewall settings
- Ensure server IP is correct
- Verify ALLOWED_HOSTS includes the IP

**Database locked?**
- Restart Docker: `docker-compose restart`
- Check disk space

**Slow performance?**
- Increase gunicorn workers in docker-compose.yml
- Consider upgrading server resources

## Support

For more Django deployment info: https://docs.djangoproject.com/en/5.2/howto/deployment/
Docker docs: https://docs.docker.com/
