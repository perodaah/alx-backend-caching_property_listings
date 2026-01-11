# CRM Celery Setup Guide

## Prerequisites

### Install Redis

Redis is required as the message broker for Celery.

- **macOS (using Homebrew):**

  ```
  brew install redis
  brew services start redis
  ```

- **Ubuntu/Debian:**

  ```
  sudo apt update
  sudo apt install redis-server
  sudo systemctl start redis-server
  sudo systemctl enable redis-server
  ```

- **Windows:**
  Download and install Redis from https://redis.io/download
  Start Redis server.

### Install Dependencies

Install the required Python packages:

```
pip install -r requirements.txt
```

## Setup Steps

### 1. Run Migrations

Apply database migrations:

```
python manage.py migrate
```

### 2. Start Celery Worker

Start the Celery worker to process tasks:

```
celery -A crm worker -l info
```

### 3. Start Celery Beat

Start Celery Beat to schedule periodic tasks:

```
celery -A crm beat -l info
```

## Verification

### Check Logs

The CRM report will be generated weekly on Mondays at 6:00 AM and logged to `/tmp/crm_report_log.txt`.

To verify the logs:

```
cat /tmp/crm_report_log.txt
```

You should see entries like:

```
2026-01-13 06:00:00 - Report: 10 customers, 25 orders, 1500.00 revenue
```
