#_*_ coding: UTF-8 _*_
#
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import  ConfigParser

class otomat_conf:
        def __init__(self,filename):
                self.filename = filename
                self.conf = ConfigParser.ConfigParser()
                self.conf.read(self.filename)
                s = self.conf.sections()
	# server configure
        def server_port(self):
                s_port = self.conf.get("server","port")
                return s_port
        def server_host(self):
                s_host = self.conf.get("server","host")
                return s_host
        def server_worker(self):
                s_worker = self.conf.get("server","worker")
                return s_worker
        def server_log(self):
                s_log = self.conf.get("server","server_log")
                return s_log
        def report_log(self):
                r_log = self.conf.get("server","report_log")
                return r_log
        def pdf_log(self):
               	p_log = self.conf.get("server","pdf_log")
                return p_log
        def email_log(self):
                e_log = self.conf.get("server","email_log")
                return e_log
        def server_logdir(self):
                s_logdir = self.conf.get("server","log_dir")
                return s_logdir
        #  mysql database  configure
        def db_host(self):
                db_host = self.conf.get("database","host")
                return db_host
        def db_user(self):
                db_user = self.conf.get("database","user")
                return db_user
        def db_password(self):
                db_password = self.conf.get("database","password")
                return db_password
        def db_defaultdb(self):
                db_def = self.conf.get("database","defaultdb")
                return db_def
	# rrdtool configure
        def rrdtool_host(self):
                rrdtool_host = self.conf.get("rrdtool","host")
                return rrdtool_host
        def rrdtool_cpu(self):
                rrdtool_cpu  = self.conf.get("rrdtool","cpu")
                return rrdtool_cpu
        def rrdtool_mem(self):
               	rrdtool_mem  = self.conf.get("rrdtool","mem")
                return rrdtool_mem
        def rrdtool_disk(self):
                rrdtool_disk = self.conf.get("rrdtool","disk")
                return rrdtool_disk
        def rrdtool_nic(self):
                rrdtool_nic = self.conf.get("rrdtool","network")
                return rrdtool_nic
        def rrdtool_dir(self):
                rrdtool_dir = self.conf.get("rrdtool","dir")
                return rrdtool_dir
        def rrdtool_login(self):
                rrdtool_login = self.conf.get("rrdtool","login")
                return rrdtool_login
        # graph configure
        def graph_cpu(self):
                graph_cpu = self.conf.get("graph","cpu")
                return graph_cpu
        def graph_mem(self):
                graph_mem = self.conf.get("graph","mem")
                return graph_mem
        def graph_disk(self):
                graph_disk = self.conf.get("graph","disk")
                return graph_disk
        def graph_network(self):
                graph_network = self.conf.get("graph","network")
                return graph_network
        def graph_login(self):
                graph_login = self.conf.get("graph","login_user")
                return graph_login
        def graph_dir(self):
                graph_dir = self.conf.get("graph","graph_dir")
                return graph_dir
        # cleint agent configure
        def client_host(self):
                c_host = self.conf.get("client","host")
                return c_host
        def client_port(self):
                c_port = self.conf.get("client","port")
                return c_port
        def  nic_port(self):
                n_port = self.conf.get("client","nic")
                return n_port
        def client_log(self):
                c_log = self.conf.get("client","log")
                return c_log
        def client_logdir(self):
                c_logdir = self.conf.get("client","log_dir")
                return c_logdir
        def  email_local(self):
               email_local  = self.conf.get("email","local")
               return email_local
        def email_remote(self):
               email_remote = self.conf.get("email","remote")
               return email_remote
        # create pdf  configure
        def pdf_dir(self):
                dir = self.conf.get("pdf","pdf_dir")
                return dir
        def pdf_daily(self):
                day = self.conf.get("pdf","pdf_daily")
                return day
        def pdf_weekly(self):
                week = self.conf.get("pdf","pdf_weekly")
                return week
        def pdf_monthly(self):
                month = self.conf.get("pdf","pdf_monthly")
                return month
