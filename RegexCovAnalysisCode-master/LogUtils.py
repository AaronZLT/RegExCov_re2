import logging

def createLog(filename):
#     print("log------------------------")
    log = logging.getLogger(filename)
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
                fmt='%(asctime)s %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
                )
    fh.setFormatter(formatter)
    log.addHandler(fh)
#     print("log------------------------")
    return log,fh

def closeLog(log,fh):
    log.removeHandler(fh)
    del fh,log