/*
 * Copyright 2012 YoYo Systems, Inc.
 *
 * $ Id:$
 */

/*
 * -----------------------------------------------------------
 * file name  : WorkflowDBResultManager.java
 * creator    : wenxin(wen.xin@yoyosys.com)
 * created    : Wed 02 May 2012 04:56:53 PM CST
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

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
//import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;

import org.apache.log4j.Logger;
import com.google.gson.Gson;
//import com.google.gson.reflect.TypeToken;

public class WorkflowDBResultManager implements WorkflowResultManager
{
  private static Logger logger = Logger.getLogger(WorkflowDBResultManager.class);

  private String resultDBFile = "testsuite_result";
  private Connection conn;

  /**
   * default constructor.
   */
  public WorkflowDBResultManager()
  {

  } // END: WorkflowDBResultManager

  public synchronized void init() throws Exception
  {
    //File f = new File(resultDBFile);
    Class.forName("org.hsqldb.jdbcDriver");
    conn = DriverManager.getConnection("jdbc:hsqldb:" + resultDBFile, "yoyoadm", "yoyosys");
    try {
      // make an empty table
      // by declaring the id column IDENTITY, the db will automatically
      // generate unique values for new rows- useful for row keys
      this.update(
        "CREATE TABLE result ( suite_id VARCHAR(36), suite_name VARCHAR(128), start_time VARCHAR(64), end_time VARCHAR(64), suite_user VARCHAR(128), suite_result VARCHAR(4094) )");
    } catch (SQLException ex2) {
      ex2.printStackTrace();  // second time we run program
    }
  }

  private int update(String expression) throws Exception
  {
    logger.debug("expression: " + expression);
    Statement st = null;
    st = conn.createStatement();    // statements
    int ret = st.executeUpdate(expression);    // run the query
    st.close();

    return ret;
  }

  public synchronized void setWorkflowResult(String workflowId, String workflowResult) throws Exception
  {
    Gson gson = new Gson();
    HashMap workflowMap = gson.fromJson(workflowResult, HashMap.class);

    String startTime =  "" + workflowMap.get("startTime");
    String endTime =  "" + workflowMap.get("endTime");
    String suiteName = "" + workflowMap.get("suiteName");
    String user =  "" + workflowMap.get("user");
    String caseResultList = gson.toJson(workflowMap.get("caseResultList"));
    //logger.debug("caseResultList1:" + gson.toJson(workflowMap.get("caseResultList")));
    //logger.debug("caseResultList2:" + caseResultList);
    String expression = String.format("INSERT INTO result(suite_id, suite_name, start_time, end_time, suite_user, suite_result) VALUES('%s', '%s', '%s', '%s', '%s', '%s')", workflowId, suiteName, startTime, endTime, user, caseResultList);
    this.update(expression);
  }

  public synchronized String getWorkflowResult(String workflowId) throws Exception
  {
    //TODO it's very dangerous -- SQL inject
    String expression = "SELECT * from result where suite_id='" + workflowId + "'";
    String result = null;

    Statement st = null;
    ResultSet rs = null;
    st = conn.createStatement();
    rs = st.executeQuery(expression);
    if (rs.next()) {
      Map<String, String> workflowMap = new HashMap<String, String>();
      workflowMap.put("suiteId", rs.getString(1));
      workflowMap.put("suiteName", rs.getString(2));
      workflowMap.put("startTime", rs.getString(3));
      workflowMap.put("endTime", rs.getString(4));
      workflowMap.put("user", rs.getString(5));
      workflowMap.put("caseResultList", rs.getString(6));

      Gson gson = new Gson();
      result = gson.toJson(workflowMap);
    }
    st.close();

    return result;
  }

  public synchronized int getTotalResultNum() throws Exception
  {
    String expression = "SELECT COUNT(*) from result";
    int count = 0;

    Statement st = null;
    ResultSet rs = null;
    st = conn.createStatement();
    rs = st.executeQuery(expression);
    if (rs.next()) {
      count = Integer.parseInt(rs.getString(1));
    }
    st.close();

    return count;

  }

  public synchronized List<HashMap<String, String>> getFinishedWorkflows(int pageNum, int pageSize) throws Exception
  {
    List<HashMap<String, String>> finishedWorkflows = new ArrayList<HashMap<String, String>>();
    List<HashMap<String, String>> resultWorkflows = new ArrayList<HashMap<String, String>>();

    if (pageNum < 1) {
      pageNum = 1;
    }

    String expression = String.format("SELECT limit %d %d * from result order by end_time desc", (pageNum - 1) * pageSize, pageSize);
    String result = null;

    Statement st = null;
    ResultSet rs = null;
    st = conn.createStatement();
    rs = st.executeQuery(expression);
    while (rs.next()) {
      HashMap<String, String> workflowMap = new HashMap<String, String>();
      workflowMap.put("suiteId", rs.getString(1));
      workflowMap.put("suiteName", rs.getString(2));
      workflowMap.put("startTime", rs.getString(3));
      workflowMap.put("endTime", rs.getString(4));
      workflowMap.put("user", rs.getString(5));

      //finishedWorkflows.add(workflowInfoMap);
      resultWorkflows.add(workflowMap);
    }
    st.close();


    /*
    for (int i = pageSize * (pageNum - 1); i < pageSize * pageNum && i < finishedWorkflows.size(); i++) {
      resultWorkflows.add(finishedWorkflows.get(i));
    }
    */

    return resultWorkflows;
  }

} // END: WorkflowDBResultManager
///:~

