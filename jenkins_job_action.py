# !/usr/bin/env python
# --*-- coding:utf-8 -*-
#  Author: Andre Yang
#  Email: yangjunfei2146@gmail.com
#  File Name:
#  Description:
#  Edit History:
# ==================================================
import jenkins,json
import sys,os

reload(sys)
sys.setdefaultencoding('utf8')

jenkins_url = "http://172.16.36.252:8080" 
username = "admin"
password = "yjf&2018Y"

server = jenkins.Jenkins(jenkins_url,username=username, password=password)

job_config_xml = '''<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.24">
  <actions>
    <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction plugin="pipeline-model-definition@1.3.1"/>
    <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction plugin="pipeline-model-definition@1.3.1">
      <jobProperties/>
      <triggers/>
      <parameters/>
    </org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction>
  </actions>
  <description>序列对比工具</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.54">
    <script>pipeline {
    agent any
     environment { 
        K8SfileRemote = &apos;/root/SXYF_YAML/raceseq/raceseq-mode-job.yml&apos;
        K8SfileLocal = &apos;raceseq-mode-job.yml&apos;
    }
    
    stages {
        stage(&quot;ssh-agent&quot;) {
            steps {
                    sh &apos;scp -o StrictHostKeyChecking=no  root@172.16.36.1:${K8SfileRemote} ./${K8SfileLocal}&apos;
            }
        }
        stage(&quot;clear old data&quot;) {
            steps {
               sh &apos;kubectl delete -f ${K8SfileLocal}&apos;
            }
        }
        stage(&apos;Run a job name is aln &apos;) {
            steps {
                sh &apos;kubectl create -f ${K8SfileLocal}&apos;
            }
        }
        stage(&apos;list all file&apos;) {
            steps {
                sh &apos;ls -l&apos;
            }
       }
        stage(&apos;Run kubectl get job&apos;) {
            steps {
                sh &quot;kubectl get job -n sxyf&quot;
            }
        }
    }
    post {
        always {
            echo &apos;One way or another, I have finished&apos;
            /*deleteDir() /* clean up our workspace */
        }
        success {
            echo &apos;I succeeeded!&apos;
        }
        unstable {
            echo &apos;I am unstable :/&apos;
        }
        failure {
            echo &apos;I failed :(&apos;
        }
        changed {
            echo &apos;Things were different before...&apos;
        }
    }    
}</script>
    <sandbox>true</sandbox>
  </definition>
  <triggers/>
  <authToken>jobrunning</authToken>
  <disabled>false</disabled>
</flow-definition>
'''
view_config_xml = '''<?xml version="1.1" encoding="UTF-8"?>
<hudson.model.ListView>
  <name>生信研发-raceseq</name>
  <filterExecutors>false</filterExecutors>
  <filterQueue>false</filterQueue>
  <properties class="hudson.model.View$PropertyList"/>
  <jobNames>
    <comparator class="hudson.util.CaseInsensitiveComparator"/>
    <string>shengxin_developer-aln-job-02</string>
    <string>shengxin_developer-qc-job-01</string>
    <string>shengxin_developer-var-GATK-job-03</string>
    <string>shengxin_developer-var-py-job-04</string>
  </jobNames>
  <jobFilters/>
  <columns>
    <hudson.views.StatusColumn/>
    <hudson.views.WeatherColumn/>
    <hudson.views.JobColumn/>
    <hudson.views.LastSuccessColumn/>
    <hudson.views.LastFailureColumn/>
    <hudson.views.LastDurationColumn/>
    <hudson.views.BuildButtonColumn/>
    <hudson.plugins.favorite.column.FavoriteColumn plugin="favorite@2.3.2"/>
  </columns>
  <recurse>true</recurse>
  <statusFilter>true</statusFilter>
</hudson.model.ListView>
'''


def get_all_jobs():
    '''
    获得 全部 Jenkins job 信息
    '''
    #job_name="shengxin_developer-aln-job-02"
    #server = jenkins.Jenkins("http://172.16.36.252:8080",username="admin", password='fsz&2018Y')
    jobs = server.get_jobs() 
    js = json.dumps(jobs, sort_keys=True, indent=4, separators=(',' ':'))
    return  js

def get_job_name(job_name):
    '''
    获得某个job配置信息
    '''
    job = server.get_job_config(job_name)
    return job

def create_job(create_job_name, job_config_xml, replace_str):
    '''
    创建一个job需要两个参数，名字和配置文件文本,
    下面是一个最简单的例子，配置都是默认后期需要
     用户自己添加
    server.create_job("abcddd",jenkins.RECONFIG_XML)
    '''
    job_exist = server.job_exists(create_job_name)
    if job_exist:
        print "%s already exist." % create_job_name 
    else:
       job_config_xml = job_config_xml.replace("raceseq-mode-job.yml", replace_str)
       job = server.create_job(create_job_name,job_config_xml)
    return job

def del_job(job_name):
    '''
    删除一个job
    '''
    job = server.delete_job(job_name)
    return job

def get_all_views():
    '''
    获得 全部 视图 信息
    '''
    views = server.get_views()
    js = json.dumps(views, sort_keys=True, indent=4, separators=(',' ':'))
    return js

def get_view_name(view_name):
    '''
    获得某个视图的配置信息
    '''
    view = server.get_view_config(view_name)
    return view

def create_view(create_view_name, view_config_xml):
    '''
    创建一个视图需要两个参数，视图名字和配置文本
    '''
    view_exist = server.view_exists(create_view_name)
    if view_exist:
        print "%s already exist." % create_view_name
    else:
        view = server.create_view(create_view_name,view_config_xml)
    return view

def del_view(view_name):
    '''
    删除一个视图
    '''
    view = server.delete_view(view_name)
    return view

def job_join_view(job_name,view_name, view_config_xml):
    '''
     把一个job添加到一个视图view，注意：这一个步骤包含，创建视图，不需要执行创建视图；
    '''
    import os
    ls = os.linesep
    insert_str = "    <string>"+job_name+"</string>"+ls
    pos = view_config_xml.find("  </jobNames>")
    content = view_config_xml[:pos] + insert_str + view_config_xml[pos:]
    view_exist = server.view_exists(view_name)
    if view_exist:
        server.reconfig_view(view_name,content)
    else:
        create_view(view_name,content)

    
    

def usage():
    usages='''
Usage:
    python jenkins_aciton.py <get_all_jobs|get_job_name|crete_job|get_all_views|get_view_name|create_view> name
Example:
    get info:
    python jenkins_action.py get_all_jobs
    python jenkins_action.py get_job_name abc
    python jenkins_action.py get_all_views
    python jenkins_action.py get_view_name abc
    creat :
    python jenkins_action.py create_job abc
    python jenkins_action.py create_view abc
    delete:
    python jenkins_action.py del_job abc
    python jenkins_action.py del_view abc
    join：
    python jenkins_action.py job_join_view  abc  aaaa # abc is job ; aaaa is view

    '''
    print usages,


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "get_all_jobs":
            print get_all_jobs()
        elif sys.argv[1] == "get_all_views":
            print get_all_views()
        else:
            usage() 
    elif len(sys.argv) == 3:
        if sys.argv[1] == "get_job_name":
            print get_job_name(sys.argv[2])
        elif sys.argv[1] == "get_view_name":
            print get_view_name(sys.argv[2])
        elif sys.argv[1] == "create_job":
            create(sys.argv[2],job_config_xml,replace_str)
        elif sys.argv[1] == "create_view":
            create_view(sys.argv[2], view_config_xml)
        elif sys.argv[1] == "del_job":
            del_job(sys.argv[2])
        elif sys.argv[1] == "del_view":
            del_view(sys.argv[2])
        else:
            usage()
    elif len(sys.argv) == 4:
        if sys.argv[1] == "job_join_view":
            job_join_view(sys.argv[2],sys.argv[3],view_config_xml)
        else:
            usage()
    else:
        usage()
