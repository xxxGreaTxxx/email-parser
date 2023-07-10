from sites import Sites
from time import sleep
from log import Log, Levels

sites = Sites()
log = Log(__name__)
timeout = 300
while True:
    sites.send()
    log.add(Levels.info, f'Распрделение лидов закончено, следующее распределение через {timeout} секунд')
    sleep(timeout)
