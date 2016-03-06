package com.yoyosys.test;

import com.yoyosys.test.bitsflow.BitsflowComm;
import static com.yoyosys.test.TestCommon.*;
import static com.yoyosys.test.TestCommon.MessageType.*;
import java.util.*;
import java.io.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import org.apache.log4j.Logger;
import java.lang.reflect.*;
import com.yoyosys.jcore.datanode.*;
import com.yoyosys.bitsflow.api.*;
import com.yoyosys.bitsflow.api.impl.*;

public class TestClient extends BitsflowComm
{
  static Logger logger = Logger.getLogger(TestClient.class);
  static int currentCaseID = -1;
  static Object waitStart = new Object();
  static String caseName;
  static String className;
  static String caseConfig;
  static TestCase testCase;

  public void procSyncRPCResult(BitsFlowMessage result)
  {
    try {
      String srcTestID  = (String) result.getField(0);
      currentCaseID = (Integer) result.getField(1);
      if (currentCaseID < 0) {
        logger.info("Test finished");
        System.exit(0);
      }
      caseName   = (String) result.getField(2);
      className  = (String) result.getField(3);
      caseConfig = (String) result.getField(4);
      logger.info("caseID: "     + currentCaseID);
      logger.info("caseName: "   + caseName);
      logger.info("className: "  + className);
      logger.info("caseConfig: " + caseConfig);
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
    }
  }

  public void getTask()
  {
    invokeRPCSyncMessage(SERVER_SUBJECT, C2S_GET_TASK, currentCaseID);
  }

  public void createTask() throws Exception
  {
    Class  classInstance;
    Method createMethod;
    Class[] args = new Class[]{YoyoDataNode.class};

    YoyoDataNode node = YoyoDataLoader.loadFromXML(new StringReader(caseConfig));
    classInstance = Class.forName(className);
    createMethod = classInstance.getMethod("createTest", args);
    testCase = (TestCase) createMethod.invoke(
      classInstance, node);
  }

  public void run()
  {
    try {
      startup();

      while (true) {
        /* step1: get a task from server */
        logger.info("\n\n==== step1: get a task ====");
        getTask();

        /* step2: create task */
        logger.info("==== step2: create task ====");
        createTask();
        C2SPublishReady(true, currentCaseID);

        /* step3: wait to all testID ready */
        logger.info("==== step3: wait to start ====");
        synchronized (waitStart) {
          waitStart.wait();
        }

        /* step4: begin test and wait to stop  */
        logger.info("==== step4: begin test and wait to stop ====");
        testCase.notifyBegin();
        testCase.waitStop();

        /* step5: report the result  */
        logger.info("==== step5: report the result ====");
        C2SPublishReport(true, currentCaseID, testCase.errorCode, testCase.errorInfo);

      }
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    } finally {
      logger.info("==== test over ====");
    }
  }

  public void onMessage(BitsFlowListener listener, BitsFlowMessage msg)
  {
    try {
      String subject = msg.getSubject();
      String srcTestID = (String) msg.getField(0);

      if (srcTestID.equals(localTestID)) {
        return;
      }

      MessageType msgType = (MessageType) msg.getField(1);
      logger.debug("\n==== receive " + msgType + " from " + srcTestID + " ====");
      switch (msgType) {
      case M2C_HEARTBEAT:
        C2MPublishHeartbeat(false);
        break;

      case S2C_RUN:
      synchronized (waitStart) {
        waitStart.notifyAll();
      }
        break;

      case M2C_GET:
        sendRPCReplyMessage(false,
                            msg,
                            MANAGER_SUBJECT,
                            testCase.createGetResponse());

        break;

      case M2C_SET:
        M2CSetType paramType = (M2CSetType) msg.getField(2);
        String param = (String) msg.getField(3);

        switch (paramType) {
        case SET_PAYLOAD:
          testCase.localMessageLength = Integer.valueOf(param);
          testCase.content = new byte[testCase.localMessageLength];
          break;

        case SET_SEND_INTERVAL:
          testCase.localSenderIntervalTime = Integer.valueOf(param);
          break;

        default:
          logger.error("unknown parameter: " + paramType);
          break;
        }
        break;

      case M2C_STOP:
        System.exit(0);
        break;

      default:
        logger.error("unknown S2CMessageType " + msgType);
        break;
      }

    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }

  public TestClient(String agent, String service)
  {
    super(agent, service, ROLE_RECEIVER, TestRole.CLIENT);
    String[] subjects = new String[] {CLIENT_SUBJECT};
    init(subjects);
  }

  public void printStackTrace()
  {
    for (StackTraceElement e : Thread.currentThread().getStackTrace()) {
      logger.error(e);
    }
  }
  public static void main(String [] args) throws Exception
  {
    if (args.length != 2) {
      logger.error("Usage: TestClient agent:port managment-service");
      return;
    }

    Runtime.getRuntime().addShutdownHook(new Thread() {
      public void run()
      {
        try {
          logger.error("shutDownHandle enter.");

        } catch (Exception ex) {
          logger.error(ex.getMessage(), ex);
        }
      }
    });

    String agent   = args[0];
    String service = args[1];
    TestClient client = new TestClient(agent, service);
    client.setName("TestClient");
    client.start();
    client.join();
  }
}
