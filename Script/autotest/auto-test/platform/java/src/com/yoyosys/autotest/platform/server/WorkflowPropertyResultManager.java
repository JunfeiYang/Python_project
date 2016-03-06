/*
 * Copyright 2012 YoYo Systems, Inc.
 *
 * $ Id:$
 */

/*
 * -----------------------------------------------------------
 * file name  : WorkflowPropertyResultManager.java
 * creator    : wenxin(wen.xin@yoyosys.com)
 * created    : Wed 02 May 2012 04:56:53 PM CST
 *
 * modifications:
 *
 * -----------------------------------------------------------
 */
package com.yoyosys.autotest.platform.server;

import java.util.Properties;
import java.util.List;
import java.util.Set;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Collections;
import java.util.Comparator;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import com.google.gson.Gson;
//import com.google.gson.reflect.TypeToken;

public class WorkflowPropertyResultManager implements WorkflowResultManager
{

  private Properties prop = new Properties();
  private String resultFile = "result.properties";

  /**
   * default constructor.
   */
  public WorkflowPropertyResultManager()
  {

  } // END: WorkflowPropertyResultManager

  public synchronized void init() throws Exception
  {
    File f = new File(resultFile);
    if (!f.exists()) {
      f.createNewFile();
    }

    this.prop.load(new FileInputStream(resultFile));
  }

  public synchronized void setWorkflowResult(String workflowId, String workflowResult) throws Exception
  {
    this.prop.setProperty(workflowId, workflowResult);
    this.prop.store(new FileOutputStream(resultFile), null);
  }

  public synchronized String getWorkflowResult(String workflowId) throws Exception
  {
    String result = "";

    result = this.prop.getProperty(workflowId, "");

    return result;
  }

  public synchronized int getTotalResultNum() throws Exception
  {
    return this.prop.size();
  }

  public synchronized List<HashMap<String, String>> getFinishedWorkflows(int pageNum, int pageSize) throws Exception
  {
    List<HashMap<String, String>> finishedWorkflows = new ArrayList<HashMap<String, String>>();
    List<HashMap<String, String>> resultWorkflows = new ArrayList<HashMap<String, String>>();
    Gson gson = new Gson();

    Set<String> workflowSet = this.prop.stringPropertyNames();
    for (String workflowId : workflowSet) {
      HashMap<String, String> workflowInfoMap = new HashMap<String, String>();
      String workflowInfo = this.prop.getProperty(workflowId);
      //System.out.println("workflowId: " + workflowInfo);
      HashMap workflowMap = gson.fromJson(workflowInfo, HashMap.class);

      workflowInfoMap.put("startTime", "" + workflowMap.get("startTime"));
      workflowInfoMap.put("endTime", "" + workflowMap.get("endTime"));
      workflowInfoMap.put("suiteName", "" + workflowMap.get("suiteName"));
      workflowInfoMap.put("user", "" + workflowMap.get("user"));
      workflowInfoMap.put("suiteId", workflowId);

      finishedWorkflows.add(workflowInfoMap);
    }

    Collections.sort(finishedWorkflows, new Comparator<HashMap<String, String>>() {
      public int compare(HashMap<String, String> o1, HashMap<String, String> o2)
      {
        return Double.compare(Double.parseDouble(o2.get("endTime")),  Double.parseDouble(o1.get("endTime")));
      }
    });

    for (int i = pageSize * (pageNum - 1); i < pageSize * pageNum && i < finishedWorkflows.size(); i++) {
      resultWorkflows.add(finishedWorkflows.get(i));
    }

    return resultWorkflows;
  }

} // END: WorkflowPropertyResultManager
///:~

