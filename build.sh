#!/usr/bin/env bash
# Exit immediately on error
set -o errexit

echo "=== 1. Upgrading Pip & Installing Dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== 2. Collecting Static Files with WhiteNoise ==="
python manage.py collectstatic --no-input

echo "=== 3. Applying Database Migrations ==="
python manage.py migrate --no-input

echo "=== 4. Seeding Market Universe & Demo Account ==="
python manage.py seed_stocks

echo "=== Build Completed Successfully ==="
