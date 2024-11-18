#!/usr/bin/env bash
# Exit on error
set -o errexit

# Set the DJANGO_SETTINGS_MODULE environment variable
export DJANGO_SETTINGS_MODULE="iihc_website_portal.settings"  # Replace with your actual project name

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Create a superuser
echo "Creating a superuser..."
USERNAME="pixel"
EMAIL="pixelmain13@gmail.com"
PASSWORD="Pixel!@#$%12345"

# Create the superuser using Django's manage.py shell
python manage.py createsuperuser --noinput --username "$USERNAME" --email "$EMAIL"

# Set the password for the superuser
echo "Setting password for the superuser..."
python -c "from django.contrib.auth import get_user_model; from django.conf import settings; settings.configure(); User = get_user_model(); user = User.objects.get(username='$USERNAME'); user.set_password('$PASSWORD'); user.save()"

# Apply any outstanding database migrations
python manage.py migrate