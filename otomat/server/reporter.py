#_*_ coding: UTF-8 _*_
import sys,time,os
reload(sys)
sys.setdefaultencoding('utf8')
import time,datetime
from otomat.conf import conf
from  otomat.logs  import log as logging
from otomat.plugins import shell_cmd as shell
from otomat.plugins import create_pdf_only as pdf


config =conf.otomat_conf('/etc/otomat/otomat.cnf')
logfile = config.pdf_log()
logdir = config.server_logdir()

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)

os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')

def main(argv=sys.argv[1:]):
	create_pdf = pdf.create_pdf()
	logging.info(("The otomat-generate-pdf-server has been launched successfully !!!"))
	while True:
		# now is 0
		n = time.localtime(time.time())
		now = str(n.tm_hour)+str(n.tm_min)
		print "This is test hours:%s" % (now)
		# week is 6
		cmd = 'date +%w'
		day_today = shell.shell_cmd(cmd)
		day_week = day_today[0].split()[0]
		# day is 1
		day_month = str(datetime.date.today().day)
		# Beginning of month
		if (now == '10') and (day_week == '6'):
			create_pdf.create_pdf_report('day')
			create_pdf.create_pdf_report('week')
			logging.info((" System generated weekly to complete successfully !!!"))
			print 'weekend'
		if (now == '10') and (day_month == '1'):
			create_pdf.create_pdf_report('day')
			create_pdf.create_pdf_report('month')
			logging.info((" System generated monthly to complete successfully !!!"))
			print 'month end'
		if (now == '1030'):
			create_pdf.create_pdf_report('day')
			logging.info((" System generated daily to complete successfully !!!"))
			print 'day end'
		
		print "This is test end !!" 
		time.sleep(60)
		continue
if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))

