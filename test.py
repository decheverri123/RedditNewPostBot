

from datetime import datetime
import calendar
import time 

unix = time.time()

dt = datetime.fromtimestamp((unix))

print(dt)