import json
import logging
import os
from logging.handlers import RotatingFileHandler

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            'timestamp': self.formatTime(record, '%Y-%m-%dT%H:%M:%S%z'),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        if hasattr(record, 'request_id'):
            payload['request_id'] = record.request_id
        return json.dumps(payload, ensure_ascii=False)

def configure_logging():
    level = getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper(), logging.INFO)
    root = logging.getLogger()
    if getattr(root, '_eventops_configured', False):
        return
    root.setLevel(level)
    formatter = JsonFormatter()
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)
    log_file = os.getenv('LOG_FILE', 'logs/eventops.log')
    try:
        os.makedirs(os.path.dirname(log_file) or '.', exist_ok=True)
        file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=5, encoding='utf-8')
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
    except OSError:
        # Container/serverless environments may expose only stdout/stderr.
        pass
    root._eventops_configured = True
