/*
 * Copyright 2012 YoYo Systems, Inc.
 *
 * $ Id:$
 */

/*
 * -----------------------------------------------------------
 * file name  : AutotestServer.java
 * creator    : wenxin(wen.xin@yoyosys.com)
 * created    : Thu 26 Apr 2012 09:14:17 PM CST
 *
 * modifications:
 *
 * -----------------------------------------------------------
 */
package com.yoyosys.autotest.platform.server;

import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.*;

import org.apache.log4j.Logger;
import com.google.gson.Gson;

import com.yoyosys.bitsflow.api.*;
import com.yoyosys.autotest.platform.util.BitsflowComm;
import com.yoyosys.autotest.platform.util.DschedHelper;
import com.yoyosys.autotest.platform.util.WorkflowHelper;
import static com.yoyosys.autotest.platform.util.TestCommon.*;
import static com.yoyosys.autotest.platform.util.TestCommon.MessageType.*;


public class AutotestServer extends BitsflowComm
{

  private static Logger logger = Logger.getLogger(AutotestServer.class);

  private DschedHelper dschedHelper;
  private WorkflowHelper workflowHelper;

  public static String installSoftwareJob = "InstallSoftwareJob";
  public static String doCaseJob = "DoCaseJob";
  public static String autotestCpn = "auto_test_cpn";

  private int pageSize = 10;

  private static Object waitExit   = new Object();
  private BlockingQueue<Runnable> msgQueue;
  private ThreadPoolExecutor msgExecutor;

  /**
   * default constructor.
   */
  public AutotestServer(String agent, String service)
  {
    super(agent, service, ROLE_RECEIVER, TestRole.SERVER);
    msgQueue    = new LinkedBlockingQueue<Runnable>();
    msgExecutor = new ThreadPoolExecutor(2, 12, 60, TimeUnit.DAYS, msgQueue);
  } // END: AutotestServer

  public class AutotestWorker implements Runnable
  {
    private BitsFlowMessage message;

    public void run()
    {
      try {
        String user = (String) message.getField(0);
        String msgType = (String) message.getField(1);

        logger.debug("receive message[" + msgType + "] from " + user);
        if ("runTest".equals(msgType)) {
          String testSuiteXml = (String) message.getField(2);
          String workflowId = runTest(testSuiteXml, user);
          sendRPCReplyMessage(false, message, CLIENT_SUBJECT, 0, workflowId);
        } else if ("getTestResult".equals(msgType)) {
          String workflowId = (String) message.getField(2);
          //TODO getTestResult maybe return null
          String testResult = getTestResult(workflowId);
          sendRPCReplyMessage(false, message, CLIENT_SUBJECT, 0, testResult);
        } else if ("listHost".equals(msgType)) {
          String testResult = listHost();
          sendRPCReplyMessage(false, message, CLIENT_SUBJECT, 0, testResult);
        } else if ("listRunningTestSuite".equals(msgType)) {
          String testSuites = listRunningTestSuite();
          sendRPCReplyMessage(false, message, CLIENT_SUBJECT, 0, testSuites);
        } else if ("listFinishedTestSuite".equals(msgType)) {
          int pageNum = ((Integer) message.getField(2)).intValue();
          String testSuites = listFinishedTestSuite(pageNum);
          sendRPCReplyMessage(false, message, CLIENT_SUBJECT, 0, testSuites);
        } else {
          logger.warn("Unknown msgType " + msgType);
          sendRPCReplyMessage(false, message, CLIENT_SUBJECT, 1, "Error: Unknown msgType " + msgType);
        }

      } catch (Exception ex) {
        logger.error(ex.getMessage(), ex);
        try {
          sendRPCReplyMessage(false, message, CLIENT_SUBJECT, 1, ex.getMessage());
        } catch (Exception ex1) {
          logger.error(ex1.getMessage(), ex1);
        }
      }
    }

    public AutotestWorker(BitsFlowMessage message)
    {
      this.message = message;
    }
  }

  public void run()
  {
    try {
      String[] subjects = new String[]{SERVER_SUBJECT};
      init(subjects);
      startup();
      initServer();
      synchronized (waitExit) {
        waitExit.wait();
      }
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
    }
  }

  public void onMessage(BitsFlowListener listener, BitsFlowMessage msg)
  {
    try {
      msgExecutor.execute(new AutotestWorker(msg));
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
    }
  }

  public void initServer() throws Exception
  {
    this.dschedHelper   = new DschedHelper(this.agent, this.agentService);
    //TODO get type from xml
    this.workflowHelper = new WorkflowHelper(this.agent, this.agentService, ManagerType.DB);

    // Check Install Software Job Exists
    if (!this.dschedHelper.isJobSpecExists(installSoftwareJob)) {
      // Create Install Software Job
      this.dschedHelper.createJobSpec(this.getClass().getResourceAsStream("/install_software_job.xml"));
    } else {
      logger.debug(installSoftwareJob  + " is exists!");
    }

    // Check Do Case Job Exists
    if (!this.dschedHelper.isJobSpecExists(doCaseJob)) {
      // Create Do Case Job
      this.dschedHelper.createJobSpec(this.getClass().getResourceAsStream("/do_case_job.xml"));
    } else {
      logger.debug(doCaseJob + " is exists!");
    }

    // Check Auto Test CPN Exists
    if (!this.workflowHelper.isCpnExists(autotestCpn)) {
      // Create Auto Test CPN
      this.workflowHelper.createCPN(this.getClass().getResourceAsStream("/auto_test_cpn.xml"));
    } else {
      logger.debug(autotestCpn + " is exists!");
    }

    this.workflowHelper.handleUnStoredWorkflows(autotestCpn);
  }

  public String runTest(String testXml, String user) throws Exception
  {
    String workflowId = null;

    // Parse test xml
    TestSuite ts = new TestSuite(testXml, user);

    // Create and Start Workflow
    workflowId = this.workflowHelper.createWorkflow(autotestCpn);
    this.workflowHelper.startWorkflow(workflowId);

    // Eval Expression
    this.workflowHelper.evalExpressions(workflowId, ts.getEvalExpressions());

    // Place Start Token
    this.workflowHelper.placeToken(workflowId, "Start", "1");

    return workflowId;

  }

  public String getTestResult(String workflowId) throws Exception
  {
    return this.workflowHelper.getSuiteResult(workflowId);
  }

  public String listRunningTestSuite() throws Exception
  {
    List<HashMap<String, String>> testSuites = new ArrayList<HashMap<String, String>>();

    List<String> runningSuiteIds = this.workflowHelper.getWorkflowsByVar(autotestCpn, "suiteStatus", "1");
    for (String suiteId : runningSuiteIds) {
      String suiteName = this.workflowHelper.getVariableValue(suiteId, "suiteName");
      String user = this.workflowHelper.getVariableValue(suiteId, "user");
      HashMap<String, String> suiteMap = new HashMap<String, String>();
      suiteMap.put("suiteId", suiteId);
      suiteMap.put("suiteName", suiteName);
      suiteMap.put("user", user);
      testSuites.add(suiteMap);
    }

    Gson gson = new Gson();
    return gson.toJson(testSuites);
  }

  public String listFinishedTestSuite(int pageNum) throws Exception
  {

    Map finishedSuitesResult = new HashMap();

    int totalNum = this.workflowHelper.getFinishedWorkflowNum();

    List<HashMap<String, String>> finishedSuites = this.workflowHelper.getFinishedWorkflows(pageNum, this.pageSize);

    finishedSuitesResult.put("finishedSuites", finishedSuites);
    finishedSuitesResult.put("totalNum", totalNum);
    finishedSuitesResult.put("pageSize", this.pageSize);
    finishedSuitesResult.put("pageNum", pageNum);


    Gson gson = new Gson();
    return gson.toJson(finishedSuitesResult);

  }

  public String listHost() throws Exception
  {
    List<String[]> hostList = new ArrayList<String[]>();
    String[] host1 = {"node1", "Linux", "x86_64", "8Core", "4G Mem"};
    String[] host2 = {"node2", "Linux", "x86_64", "4Core", "4G Mem"};
    String[] host3 = {"node3", "Linux", "x86_64", "32Core", "4G Mem"};
    String[] host4 = {"node4", "Linux", "x86_64", "8Core", "16G Mem"};
    String[] host5 = {"node5", "Linux", "x86_64", "8Core", "32G Mem"};

    hostList.add(host1);
    hostList.add(host2);
    hostList.add(host3);
    hostList.add(host4);
    hostList.add(host5);

    Gson gson = new Gson();
    return gson.toJson(hostList);
  }

  public void stopServer() throws Exception
  {
    this.dschedHelper.stopClient();
    this.workflowHelper.stopClient();
  }

  public static void main(String[] args) throws Exception
  {
    if (args.length != 2) {
      logger.error("Usage: AutotestServer agent:port managment-service");
      return;
    }

    String agent   = args[0];
    String service = args[1];
    logger.debug("Autotest Server Starting...");
    AutotestServer server = new AutotestServer(agent, service);
    server.setName("AutotestServer");
    server.start();
    server.join();

  }
} // END: AutotestServer
///:~

