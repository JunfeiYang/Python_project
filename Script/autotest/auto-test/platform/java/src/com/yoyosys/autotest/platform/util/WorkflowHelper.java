/*
 * Copyright 2012 YoYo Systems, Inc.
 *
 * $ Id:$
 */

/*
 * -----------------------------------------------------------
 * file name  : WorkflowHelper.java
 * creator    : wenxin(wen.xin@yoyosys.com)
 * created    : Thu 26 Apr 2012 11:37:08 PM CST
 *
 * modifications:
 *
 * -----------------------------------------------------------
 */
package com.yoyosys.autotest.platform.util;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.InputStream;
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;

import org.apache.log4j.Logger;

import com.yoyosys.workflow.client.api.*;
import com.yoyosys.autotest.platform.server.*;

public class WorkflowHelper implements NotificationListener
{

  private static Logger logger = Logger.getLogger(WorkflowHelper.class);

  private String agent;
  private String service;

  private WorkflowClient client;

  private WorkflowResultManager resultManager;

  /**
   * default constructor.
   */
  public WorkflowHelper(String agent, String service, ManagerType type) throws Exception
  {
    this.agent = agent;
    this.service = service;
    switch (type) {
    case PROPERTY:
      this.resultManager = new WorkflowPropertyResultManager();
      break;
    case DB:
      this.resultManager = new WorkflowDBResultManager();
      break;
    default:
      throw new IllegalArgumentException("unknown type.");
    }
    this.resultManager.init();
    this.startClient();

  } // END: WorkflowHelper

  public void onNotification(Notification notification)
  {
    NotificationType type = notification.getType();
    logger.debug("NotificationType is " + notification.getType());

    switch (type) {
    case TRANSITION_COMPLETE:
      String execId = ((TransitionCompleteNotification) notification).getExecutionId();
      String transitionId = ((TransitionCompleteNotification) notification).getTransitionId();
      String workflowId = notification.getWorkflowId();
      if ("DoReport".equals(transitionId)) {
        WorkflowWorker worker = new WorkflowWorker();
        worker.workflowId = workflowId;
        worker.start();
      }
      break;
    default:
      break;
    }
  }

  public int getMask()
  {
    return 0xFFFFFFFF;
  }

  public void startClient() throws WorkflowClientException
  {
    this.client = WorkflowClientFactory.createWorkflowClient(agent, service);
    this.client.addNotificationListener(this);
    this.client.start();
  }

  public void stopClient() throws WorkflowClientException
  {
    this.client.destroy();
  }

  public void createCPN(InputStream stream) throws Exception
  {
    BufferedReader in = new BufferedReader(new InputStreamReader(stream));
    StringBuffer buffer = new StringBuffer();
    String line = null;
    while ((line = in.readLine()) != null) {
      buffer.append(line);
      buffer.append("\n");
    }

    this.client.createCPN(buffer.toString());
  }

  public boolean isCpnExists(String cpnName) throws WorkflowClientException
  {
    boolean found = false;
    String[] cpnList = this.client.getAllCPNId();
    for (String cpn : cpnList) {
      if (cpnName.equals(cpn)) {
        found = true;
        break;
      }
    }

    return found;
  }

  public String createWorkflow(String cpnName) throws WorkflowClientException
  {
    String workflowId = this.client.createWorkflow(cpnName);
    return workflowId;
  }

  public void startWorkflow(String workflowId) throws WorkflowClientException
  {
    this.client.startWorkflow(workflowId, true);
  }

  public void closeWorkflow(String workflowId) throws WorkflowClientException
  {
    this.client.stopWorkflow(workflowId);
    this.client.deleteWorkflow(workflowId);
  }

  public void evalExpressions(String workflowId, List<String> evalList) throws Exception
  {
    for (String eval : evalList) {
      this.client.runStatement(workflowId, eval);
    }
  }

  public String getVariableValue(String workflowId, String variable) throws Exception
  {
    return this.client.evaluateExpression(workflowId, variable, ReturnType.JSON);
  }

  public void placeToken(String workflowId, String place, String value) throws WorkflowClientException
  {
    Token[] tokens = new Token[] {
      WorkflowClientFactory.createToken(place, value), };
    this.client.placeTokens(workflowId, tokens);
  }

  public List<String> getWorkflowsByVar(String cpnId, String varName, String expectValue) throws Exception
  {
    List<String> workflowList = new ArrayList<String>();
    String[] workflowIds = this.client.getCPNAllWorkflowId(cpnId);
    for (String workflowId : workflowIds) {
      String value = this.getVariableValue(workflowId, varName);
      if (expectValue.equals(value)) {
        workflowList.add(workflowId);
      }
    }

    return workflowList;

  }

  public int getFinishedWorkflowNum() throws Exception
  {
    return this.resultManager.getTotalResultNum();
  }

  public List<HashMap<String, String>> getFinishedWorkflows(int pageNum, int pageSize) throws Exception
  {
    return this.resultManager.getFinishedWorkflows(pageNum, pageSize);
  }

  public String getSuiteResult(String workflowId) throws Exception
  {
    String result = "";
    result = this.resultManager.getWorkflowResult(workflowId);
    //if ("".equals(result)) {
    //  result = this.getVariableValue(workflowId, "suiteResult");
    //}
    return result;
  }

  public void handleUnStoredWorkflows(String autotestCpn) throws Exception
  {
    List<String> testSuites = this.getWorkflowsByVar(autotestCpn, "suiteStatus", "2");;
    for (String suiteId : testSuites) {
      this.handleFinishedWorkflow(suiteId);
    }
  }

  public void handleFinishedWorkflow(String workflowId) throws Exception
  {
    String resultStr = getVariableValue(workflowId, "suiteResult");
    logger.debug("workflow result: " + resultStr);
    resultManager.setWorkflowResult(workflowId, resultStr);
    closeWorkflow(workflowId);
  }

  public String getAgent()
  {
    return this.agent;
  }

  public String getService()
  {
    return this.service;
  }

  class WorkflowWorker extends Thread
  {

    public String workflowId;

    public void run()
    {
      logger.debug("Workflow: " + this.workflowId + " DoReport!");
      try {
        handleFinishedWorkflow(this.workflowId);
      } catch (Exception ex) {
        ex.printStackTrace();
      }
    }
  }

} // END: WorkflowHelper
///:~

