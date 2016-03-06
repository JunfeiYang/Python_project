#_*_ coding: UTF-8 _*_
import sys,time,os
reload(sys)
sys.setdefaultencoding('utf8')
import time,datetime
from otomat.conf import conf
from  otomat.logs  import log as logging
from  otomat.plugins  import rrdtool_data_collector
from  otomat.plugins  import rrdtool_drafting
from otomat.plugins import shell_cmd as shell

config =conf.otomat_conf('/etc/otomat/otomat.cnf')
logfile = config.report_log()
logdir = config.server_logdir()

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)

os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')

def main(argv=sys.argv[1:]):
	t = rrdtool_data_collector.rrdtool_collector(argv)
	garph_day = rrdtool_drafting.graph_rrdtool(argv)
	garph_week = rrdtool_drafting.graph_rrdtool(argv)
	garph_month = rrdtool_drafting.graph_rrdtool(argv)
	logging.info(("The otomat-report-server has been launched successfully !!!"))
	while True:
		t.rrdb()
		t.rrdb_update()
		# now is 0
		n = time.localtime(time.time())
		now = str(n.tm_hour)+str(n.tm_min)
		print "This is test hours:%s" % (now)
		# week is 6
		cmd = 'date +%w'
		day = shell.shell_cmd(cmd)
		day_week = day[0].split()[0]
		print "This is test day_week:%s" % (day_week)
		# day is 1
		day_month = str(datetime.date.today().day)
		# Beginning of month
		if (now == '01' or now == '02' or now == '03' or now == '04' or now == '05') and (day_week == '6'):
			garph_day.graph_rrdtool('-1d')
			garph_week.graph_rrdtool('-1w')
			print 'weekend'
		if (now == '01' or now == '02' or now == '03' or now == '04' or now == '05') and (day_month == '1'):
			garph_day.graph_rrdtool('-1d')
			garph_week.graph_rrdtool('-1M')
			print 'month end'
		if (now == '01' or now == '02' or now == '03' or now == '04' or now == '05'):
			garph_day.graph_rrdtool('-1d')
			print 'day end'
		
		print "This is test end !!" 
		time.sleep(300)
		continue
if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))

