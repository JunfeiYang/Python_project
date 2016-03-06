/*
 * Copyright 2012 YoYo Systems, Inc.
 *
 * $ Id:$
 */

/*
 * -----------------------------------------------------------
 * file name  : DschedHelper.java
 * creator    : wenxin(wen.xin@yoyosys.com)
 * created    : Thu 26 Apr 2012 09:50:22 PM CST
 *
 * modifications:
 *
 * -----------------------------------------------------------
 */
package com.yoyosys.autotest.platform.util;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.InputStream;

import org.apache.log4j.Logger;

import com.yoyosys.dsched.client.api.*;

public class DschedHelper implements NotificationListener
{

  private static Logger logger = Logger.getLogger(DschedHelper.class);

  private String agent;
  private String service;

  private DSchedClient client;
  /**
   * default constructor.
   */
  public DschedHelper(String agent, String service) throws DSchedClientException
  {
    this.agent = agent;
    this.service = service;

    this.startClient();
  } // END: DschedHelper

  public void onNotification(Notification notification)
  {
    NotificationType type = notification.getType();
    System.out.println("NotificationType is " + notification.getType());

    switch (type) {
    case JOB_STATUS:
      JobStatusNotification jobStatus = (JobStatusNotification) notification;
      logger.debug("jobId: " + jobStatus.getJobId());
      logger.debug("status: " + jobStatus.getStatus());
      break;
    default:
      if (type != null) {
        logger.debug("Unknown notification type: " + type);
      } else {
        logger.debug("Notification type is NULL");
      }
    }
  }

  public int getMask()
  {
    int mask = 0xFFFFFFFF;
    return mask;
  }


  public void startClient() throws DSchedClientException
  {
    this.client = DSchedClientFactory.createDSchedClient(agent, service);
    this.client.addNotificationListener(this);
    this.client.start();
  }

  public void stopClient() throws DSchedClientException
  {
    this.client.destroy();
  }

  public void createJobSpec(InputStream stream) throws Exception
  {
    BufferedReader in = new BufferedReader(new InputStreamReader(stream));
    StringBuffer buffer = new StringBuffer();
    String line = null;
    while ((line = in.readLine()) != null) {
      buffer.append(line);
      buffer.append("\n");
    }

    this.client.createJobSpec(buffer.toString());
  }

  public boolean isJobSpecExists(String jobSpecName) throws DSchedClientException
  {
    boolean found = false;
    String[] specList = this.client.getAllJobSpecName();
    for (String spec : specList) {
      if (jobSpecName.equals(spec)) {
        found = true;
        break;
      }
    }

    return found;
  }

  public String getAgent()
  {
    return this.agent;
  }

  public String getService()
  {
    return this.service;
  }

} // END: DschedHelper
///:~

