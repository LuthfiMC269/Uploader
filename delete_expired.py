import os, time
from datetime import datetime, timedelta
FOLDER = 'static/uploads'
EXPIRATION = 3 * 60 * 60  # 3 jam

now = time.time()
for f in os.listdir(FOLDER):
    path = os.path.join(FOLDER, f)
    if os.path.isfile(path) and (now - os.path.getmtime(path)) > EXPIRATION:
        os.remove(path)
