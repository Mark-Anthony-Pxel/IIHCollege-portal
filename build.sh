#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python -m gunicorn iihc_website_portal.asgi:django_asgi_app -k uvicorn.workers.UvicornWorker
#  -k uvicorn.workers.UvicornWorker