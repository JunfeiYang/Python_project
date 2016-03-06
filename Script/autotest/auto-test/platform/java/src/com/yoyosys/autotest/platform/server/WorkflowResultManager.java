/*
 * Copyright 2012 YoYo Systems, Inc.
 *
 * $ Id:$
 */

/*
 * -----------------------------------------------------------
 * file name  : WorkflowStoreI.java
 * creator    : wenxin(wen.xin@yoyosys.com)
 * created    : Wed 02 May 2012 04:49:28 PM CST
 *
 * modifications:
 *
 * -----------------------------------------------------------
 */
package com.yoyosys.autotest.platform.server;

import java.util.List;
import java.util.HashMap;

//TODO why give such name?
public interface WorkflowResultManager
{
  //TODO maybe AutotestException is better
  void init() throws Exception;

  /**
   * set workflow result
   *
   * @workflowId
   * @workflowResult
   */
  void setWorkflowResult(String workflowId, String workflowResult) throws Exception;

  /**
   * get workflow result
   *
   * @workflowId
   *
   */
  String getWorkflowResult(String workflowId) throws Exception;

  int getTotalResultNum() throws Exception;

  List<HashMap<String, String>> getFinishedWorkflows(int pageNum, int pageSize) throws Exception;

} // END: WorkflowStoreI
///:~

