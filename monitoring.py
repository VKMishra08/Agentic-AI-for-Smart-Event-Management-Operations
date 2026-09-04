import os
import time
from datetime import datetime, timezone

START_TIME = time.time()
REQUEST_COUNT = 0
REQUEST_ERRORS = 0
TOTAL_REQUEST_TIME = 0.0

try:
    import psutil
except ImportError:  # pragma: no cover
    psutil = None

def record_request(duration: float, status_code: int):
    global REQUEST_COUNT, REQUEST_ERRORS, TOTAL_REQUEST_TIME
    REQUEST_COUNT += 1
    TOTAL_REQUEST_TIME += duration
    if status_code >= 500:
        REQUEST_ERRORS += 1

def metrics():
    avg_ms = (TOTAL_REQUEST_TIME / REQUEST_COUNT * 1000) if REQUEST_COUNT else 0
    data = {
        'service': 'eventops-backend',
        'status': 'healthy',
        'uptime_seconds': round(time.time() - START_TIME, 2),
        'request_count': REQUEST_COUNT,
        'error_count': REQUEST_ERRORS,
        'error_rate_percent': round((REQUEST_ERRORS / REQUEST_COUNT * 100), 2) if REQUEST_COUNT else 0,
        'average_request_ms': round(avg_ms, 2),
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }
    if psutil:
        process = psutil.Process(os.getpid())
        data['cpu_percent'] = process.cpu_percent(interval=None)
        data['memory_mb'] = round(process.memory_info().rss / 1024 / 1024, 2)
    return data
