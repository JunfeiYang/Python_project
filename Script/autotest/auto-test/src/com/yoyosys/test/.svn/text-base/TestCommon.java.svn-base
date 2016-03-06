package com.yoyosys.test;

public class TestCommon
{
  public static final String BASE_SUBJECT    = "YoyoTest.";
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
    M2S_HEARTBEAT, //pubsub

    M2C_HEARTBEAT, //pubsub
    M2C_GET,   //rpc
    M2C_SET,   //pubsub
    M2C_STOP,  //pubsub
    M2S_STOP,  //pubsub

    S2C_RUN,   //pubsub

    S2M_HEARTBEAT,   //pubsub

    C2S_GET_TASK,    //rpc
    C2S_READY,       //pubsub
    C2S_REPORT_TASK, //pubsub

    C2M_HEARTBEAT,   //pubsub
  }

  public enum M2CSetType
  {
    SET_PAYLOAD,
    SET_SEND_INTERVAL
  }

}
