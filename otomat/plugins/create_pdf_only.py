#_*_ coding: UTF-8 _*_
import sys,time,os,datetime
reload(sys)
sys.setdefaultencoding('utf8')

from otomat.conf import conf
from  otomat.logs  import log as logging

config =conf.otomat_conf('/etc/otomat/otomat.cnf')
logfile = config.pdf_log()
logdir = config.server_logdir()
graph_dir = config.graph_dir()

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)

os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')

pdfdir = config.pdf_dir()
if not os.path.exists(pdfdir):
        os.makedirs(pdfdir,0o755)

ISOFORMAT='%Y%m%d'
today = datetime.date.today()
today_dir = today.strftime(ISOFORMAT)
host = config.rrdtool_host()
os.chdir(pdfdir)
if not os.path.exists(today_dir):
	os.makedirs(today_dir,0o755)

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph,Spacer,Image,PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import copy
# 注册中文字体
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
import reportlab.pdfbase.pdfmetrics
import reportlab.pdfbase.ttfonts
reportlab.pdfbase.pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont('song', '/usr/share/fonts/wqy-microhei/wqy-microhei.ttc'))
# 修改默认字体
import reportlab.lib.fonts
reportlab.lib.fonts.ps2tt = lambda psfn: ('song', 0, 0)
reportlab.lib.fonts.tt2ps = lambda fn,b,i: 'song'
## for CJK Wrap
import reportlab.platypus
def wrap(self, availWidth, availHeight):
	# work out widths array for breaking
	self.width = availWidth
	leftIndent = self.style.leftIndent
	first_line_width = availWidth - (leftIndent+self.style.firstLineIndent) - self.style.rightIndent
	later_widths = availWidth - leftIndent - self.style.rightIndent
	try:
		self.blPara = self.breakLinesCJK([first_line_width, later_widths])
	except:
		self.blPara = self.breakLines([first_line_width, later_widths])
	self.height = len(self.blPara.lines) * self.style.leading
	return (self.width, self.height)
reportlab.platypus.Paragraph.wrap = wrap
###########
class create_pdf_report:
	def __init__(self):
		global config
		day = '1d_'
		week = '1w_'
		month = '1m_'
		self.cpu = config.graph_cpu()
		self.mem = config.graph_mem()
		self.network =  config.graph_network() 
		self.disk = config.graph_disk()
		self.login = config.graph_login()
		self.day_file = day+self.cpu,day+self.mem,day+self.network,day+self.disk,day+self.login 
		self.week_file = week+self.cpu,week+self.mem,week+self.network,week+self.disk,week+self.login 
		self.month_file = month+self.cpu,month+self.mem,month+self.network,month+self.disk,month+self.login 
        def report_hostname(self,ip):
		global config
		host = config.rrdtool_host()
		#print host
		#print ip
		db_ip = config.db_host()
		#===================
		graph_dir = config.graph_dir()
                os.chdir(graph_dir)
                os.chdir(ip)
		sql_host = "select distinct hostname,host_ip  from login_user \
                	where Time > date_sub(now(),interval 12 HOUR) and Time< now();"
		import  MySQLdb
		user = config.db_user()
		passwd = config.db_password()
		db = config.db_defaultdb()
		conn = MySQLdb.connect(db_ip,user,passwd,db)
		cur = conn.cursor()
		cur.execute(sql_host)
		rows = int(cur.rowcount)
		#print os.getcwd()
		for l in xrange(rows):
			row = cur.fetchone()
			#print row[1]
			#print i
			for i in list(host.split(',')):
				if ( row[1] == i):
					hostname = row[0]
					#print 'This is create pdf name: %s' % dst_file
					#print 'This is create pdf hostname: %s' % hostname
		conn.close()
		return hostname


	def ptext_template(self,flag):
		global pdfdir,today_dir,graph_dir
		styles=getSampleStyleSheet()
                #styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
		normalStyle = copy.deepcopy(styles['Normal'])
		normalStyle.fontName ='song'
		normalStyle.fontSize = 12
		# 设置行距
		normalStyle.leading = 20
		##首行缩进
		normalStyle.firstLineIndent = 32
		day = '1d_'
		week = '1w_'
		month = '1m_'
		k = '/'

		Story = []
		if (flag == 'day'):
			#magName = "北京壹号车云计算部系统日报"
			title = "北京壹号车云计算部系统日报"
			#cpu = '1d_cpu.png'
			cpu = day+self.cpu
			#mem = '1d_mem.png'
			mem = day+self.mem
			#disk = '1d_disk.png'
			disk = day+self.disk
			#network = '1d_nic.png'
			network = day+self.network
			#login = '1d_login_user.png'
			login = day+self.login
			pdf_name = config.pdf_daily()
			dst_file = pdfdir+k+today_dir+k+pdf_name
		elif (flag == 'week'):
			#magName = "北京壹号车云计算部系统周报"
			title = "北京壹号车云计算部系统周报"
			#cpu = '1w_cpu.png'
			cpu = week+self.cpu
			#mem = '1w_mem.png'
			mem = week+self.mem
			#disk = '1w_disk.png'
			disk = week+self.disk
			#network = '1w_nic.png'
			network = week+self.network
			#login = '1w_login_user.png'
			login = week+self.login
			pdf_name = config.pdf_weekly()
			dst_file = pdfdir+k+today_dir+k+pdf_name
		elif (flag == 'month'):
			#magName = "北京壹号车云计算部系统月报"
			title = "北京壹号车云计算部系统月报"
			#cpu = '1m_cpu.png'
			cpu = month+self.cpu
			#mem = '1m_mem.png'
			mem = month+self.mem
			#disk = '1m_disk.png'
			disk = month+self.disk
			#network = '1m_nic.png'
			network = month+self.network
			#login = '1m_login_user.png'
			login = month+self.login
			pdf_name = config.pdf_monthly()
			dst_file = pdfdir+k+today_dir+k+pdf_name
			
		issueNum = 12
		subPrice = "99.00"
		limitedDate = "03/25/2015"
		freeGift = "tin foil hat"
                doc = SimpleDocTemplate(dst_file,pagesize=letter,
 			rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=18)

		formatted_time = time.ctime()
		print dst_file
		#=============================
		#hostname = 'jumpclient02'
		#ip = '172.172.0.8'
		#ip = ip
		#==================================
		#cpu = '1d_cpu.png'
		#mem = '1d_mem.png'
		#disk = '1d_disk.png'
		#network = '1d_nic.png'
		#login = '1d_login_user.png'
		#ptext = '<font size=12>%s</font>' % formatted_time
		ptext = '<font size=20>%s</font>' % title

		Story.append(Paragraph(ptext, normalStyle))
		Story.append(Spacer(1, 12))

		# Create return address
		ptext = '<font size=14>日期：%s</font>' % formatted_time
		Story.append(Spacer(1, 24))
		Story.append(Paragraph(ptext, normalStyle))

		ptext = '<font size=14 color=#ff0000>目的：通过日报、周报与月报可以直观的了解操作系统的重要参数，\
			通过这些我们可以判断系统资源是否长期闲置以及遇到瓶颈。比如：当内存使用\
			长期在80%以上，内存上遇到了瓶颈。CPU idle 长期在20%，CPU使用率过高，\
			需要优化系统或者增加CPU。</font>'
		Story.append(Paragraph(ptext, normalStyle))
		Story.append(Spacer(1, 24))

		ptext = '以下是各个节点的监控指标，具体包括cpu，内存，磁盘，网络与登陆终端的数量。'
		Story.append(Paragraph(ptext, normalStyle))
		Story.append(Spacer(1, 48))
		host = config.rrdtool_host()
		for ip in list(host.split(',')):
			os.chdir(graph_dir)
			os.chdir(ip)
			print today_dir
			hostname = self.report_hostname(ip)
			#print hostname  
			ptext = '<font size=12>主机名：%s</font>' % hostname
			Story.append(Paragraph(ptext, normalStyle))
			Story.append(Spacer(1, 12))
			ptext = '<font size=12>IP地址：%s</font>' % ip
			Story.append(Paragraph(ptext, normalStyle))
			Story.append(Spacer(1, 12))
			print os.getcwd()
			# cpu
			os.chdir(today_dir)
			ptext = '<font size=12>一：CPU使用率的监控</font>'
			Story.append(Paragraph(ptext, normalStyle))
			Story.append(Spacer(1, 12))
			im = Image(os.getcwd()+k+cpu,4*inch,2*inch)
			Story.append(im)
			print os.getcwd()
			# mem
			ptext = '<font size=12>二：内存使用状况的监控</font>'
			Story.append(Paragraph(ptext, normalStyle))
			Story.append(Spacer(1, 12))
			im = Image(os.getcwd()+k+mem,4*inch,2*inch)
			Story.append(im)
			print os.getcwd()
			# disk
			ptext = '<font size=12>三：磁盘使用情况的监控</font>'
			Story.append(Paragraph(ptext, normalStyle))
			Story.append(Spacer(1, 12))
			im = Image(os.getcwd()+k+disk,4*inch,2*inch)
			Story.append(im)
			print os.getcwd()
			# network
			ptext = '<font size=12>四：网络流量的监控</font>'
			Story.append(Paragraph(ptext, normalStyle))
			Story.append(Spacer(1, 12))
			im = Image(os.getcwd()+k+network,4*inch,2*inch)
			Story.append(im)
			print os.getcwd()
			# login
			ptext = '<font size=12>五：登陆终端数量的监控</font>'
			Story.append(Paragraph(ptext, normalStyle))
			Story.append(Spacer(1, 12))
			im = Image(os.getcwd()+k+login,4*inch,2*inch)
			print login
			Story.append(im)
			Story.append(Spacer(1, 48))
			print os.getcwd()
			time.sleep(1)

		ptext = '<font size=12>真诚的感谢,</font>'
		Story.append(Paragraph(ptext, normalStyle))
		Story.append(Spacer(1, 24))

		ptext = '<font size=12>Openstack 团队</font>'
		Story.append(Paragraph(ptext, normalStyle))
		Story.append(Spacer(1, 12))
		Story.append(PageBreak())
		doc.build(Story)

