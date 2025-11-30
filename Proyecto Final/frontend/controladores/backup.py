import os, json, threading, requests
from datetime import datetime
from pathlib import Path

API_URL = os.getenv('API_URL', 'http://127.0.0.1:8000/api')
INTERVAL_ENV = 'INTERVALO_BACKUP_SEG'
DEFAULT_INTERVAL = 600
BASE_DIR = Path(__file__).resolve().parents[1]
BACKUP_DIR = BASE_DIR / 'backups'
CONFIG = BASE_DIR / 'config.json'

def read_interval():
    val = os.getenv(INTERVAL_ENV)
    if val:
        try:
            ival = int(val)
            if ival>0: return ival
        except: pass
    if CONFIG.exists():
        try:
            c = json.load(open(CONFIG,'r',encoding='utf-8'))
            ival = int(c.get('INTERVALO_BACKUP_SEG', DEFAULT_INTERVAL))
            if ival>0: return ival
        except: pass
    return DEFAULT_INTERVAL

def read_api():
    val = os.getenv('API_URL')
    if val: return val
    if CONFIG.exists():
        try:
            c = json.load(open(CONFIG,'r',encoding='utf-8'))
            return c.get('API_URL','http://127.0.0.1:8000/api')
        except: pass
    return 'http://127.0.0.1:8000/api'

def fetch_all(timeout=8):
    api = read_api().rstrip('/')
    r1 = requests.get(f"{api}/herramientas/", timeout=timeout); r1.raise_for_status()
    r2 = requests.get(f"{api}/prestamos/", timeout=timeout); r2.raise_for_status()
    return {'herramientas': r1.json(), 'prestamos': r2.json()}

def write_backup(data):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    fname = BACKUP_DIR / f"backup_{ts}.json"
    with open(fname,'w',encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    with open(BACKUP_DIR / 'backup_latest.json','w',encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    return fname

def backup_worker(stop_event, status_queue=None):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    while not stop_event.is_set():
        interval = read_interval()
        try:
            data = fetch_all()
            fname = write_backup(data)
            if status_queue is not None:
                status_queue.put(('ok', fname.name, interval))
        except Exception as e:
            try:
                with open(BACKUP_DIR / 'backup.log','a',encoding='utf-8') as lf:
                    lf.write(f"{datetime.utcnow().isoformat()} - ERROR - {repr(e)}\n")
            except: pass
            if status_queue is not None:
                status_queue.put(('error', str(e), interval))
        stop_event.wait(interval)

def start_backup_thread(status_queue=None):
    stop_event = threading.Event()
    t = threading.Thread(target=backup_worker, args=(stop_event, status_queue), daemon=True)
    t.start()
    return stop_event, t
