#!/usr/bin/env bash
set -o errexit  # agar error aaye to turant ruk jaaye

pip install -r requirements.txt      # sab required libraries install karega
python manage.py collectstatic --no-input   # static files ek jaga collect karega
python manage.py migrate             # database migrations apply karega
