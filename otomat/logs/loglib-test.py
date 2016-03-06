#!/bin/python
import log

log.set_logger(filename = '/tmp/yyy.log', mode = 'w')
log.debug("Houston, we have a %s", "thorny problem", exc_info=1)
log.error('this is error log for otomat')
