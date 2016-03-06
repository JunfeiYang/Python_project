package com.yoyosys.autotest.platform.util;

public class TestCommon
{
  public static final String BASE_SUBJECT    = "YoyoAutoTest.";
  public static final String SERVER_SUBJECT  = BASE_SUBJECT + "server";
  public static final String CLIENT_SUBJECT  = BASE_SUBJECT + "client";
  public static final String MANAGER_SUBJECT = BASE_SUBJECT + "manager";
  public static final String NULL_TESTID     = "NULL";

  /* thread role  */
  public static final int ROLE_SENDER     = 1;
  public static final int ROLE_RECEIVER   = 2;

  public enum TestRole
  {
    SERVER,
    CLIENT,
    MANAGER,
  }

  /* S2C: server --> client
  *  C2S: client --> server
  *  M2C: manager --> client
  *  M2S: manager --> server
  * */
  public enum MessageType
  {
    RUN_TEST,
  }

  public enum M2CSetType
  {
    SET_PAYLOAD,
    SET_SEND_INTERVAL
  }

}
