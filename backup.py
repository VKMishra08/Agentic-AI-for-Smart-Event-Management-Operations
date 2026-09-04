"""Database backup and recovery utility.

SQLite is backed up using SQLite's online backup API. PostgreSQL uses pg_dump/pg_restore.
Usage:
  python backup.py backup
  python backup.py restore <backup_file>
"""
import argparse
import os
import shutil
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

DB_URL = os.getenv('DATABASE_URL', 'sqlite:///./event_operations.db')
BACKUP_DIR = Path(os.getenv('BACKUP_DIR', './backups'))
BACKUP_RETENTION = int(os.getenv('BACKUP_RETENTION', '7'))

def backup_sqlite():
    source = Path(DB_URL.replace('sqlite:///', '', 1))
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    target = BACKUP_DIR / f'event_operations_{datetime.now():%Y%m%d_%H%M%S}.db'
    src = sqlite3.connect(source)
    dst = sqlite3.connect(target)
    try:
        src.backup(dst)
    finally:
        dst.close(); src.close()
    for old in sorted(BACKUP_DIR.glob('event_operations_*.db'), key=lambda p: p.stat().st_mtime, reverse=True)[BACKUP_RETENTION:]:
        old.unlink(missing_ok=True)
    for old in sorted(BACKUP_DIR.glob('event_operations_*.dump'), key=lambda p: p.stat().st_mtime, reverse=True)[BACKUP_RETENTION:]:
        old.unlink(missing_ok=True)
    print(f'Backup created: {target}')
    return target

def backup_postgres():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    target = BACKUP_DIR / f'event_operations_{datetime.now():%Y%m%d_%H%M%S}.dump'
    subprocess.run(['pg_dump', DB_URL, '-Fc', '-f', str(target)], check=True)
    print(f'Backup created: {target}')
    return target

def backup():
    if DB_URL.startswith('sqlite:///'):
        return backup_sqlite()
    if DB_URL.startswith(('postgresql://', 'postgres://')):
        return backup_postgres()
    raise ValueError('Unsupported DATABASE_URL. Use SQLite or PostgreSQL.')

def restore(backup_file):
    source = Path(backup_file)
    if not source.exists():
        raise FileNotFoundError(source)
    if DB_URL.startswith('sqlite:///'):
        target = Path(DB_URL.replace('sqlite:///', '', 1))
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        print(f'SQLite database restored to: {target}')
    elif DB_URL.startswith(('postgresql://', 'postgres://')):
        subprocess.run(['pg_restore', '--clean', '--if-exists', '--dbname', DB_URL, str(source)], check=True)
        print('PostgreSQL database restored.')
    else:
        raise ValueError('Unsupported DATABASE_URL.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['backup', 'restore'])
    parser.add_argument('file', nargs='?')
    args = parser.parse_args()
    if args.command == 'backup': backup()
    elif not args.file: parser.error('restore requires a backup file')
    else: restore(args.file)
