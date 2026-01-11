#!/bin/bash
set -euo pipefail

# Move to project root (script at crm/cron_jobs -> ../..)
cd "$(dirname "$0")/../.." || exit 1

# If a local virtualenv exists, activate it so Django and dependencies are available
if [ -f "./.venv/bin/activate" ]; then
	# shellcheck source=/dev/null
	source "./.venv/bin/activate"
fi

# Run a small Django script that deletes customers with no orders since one year ago
# and prints the number deleted to stdout as a single final line.
output=$(python manage.py shell <<'PY'
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max, Q
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.annotate(last_order=Max('orders__order_date')).filter(Q(last_order__lt=cutoff) | Q(last_order__isnull=True))
count = qs.count()
qs.delete()
print(count)
PY
)

# Extract the last printed line as the count (robust if any warnings appear earlier)
count=$(echo "$output" | tail -n 1)
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "$timestamp - Deleted $count inactive customers" >> /tmp/customer_cleanup_log.txt

exit 0
