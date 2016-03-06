package com.yoyosys.test;

import static com.yoyosys.test.TestCommon.*;
import static com.yoyosys.test.TestCommon.MessageType.*;
import com.yoyosys.test.bitsflow.BitsflowComm;
import java.util.*;
import java.io.*;
import org.apache.log4j.Logger;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import com.yoyosys.bitsflow.api.*;
import com.yoyosys.bitsflow.api.impl.*;
import com.yoyosys.jcore.datanode.*;

public class TestManager extends BitsflowComm
{
  static Logger logger = Logger.getLogger(TestManager.class);
  static long waitTime = 2000; // ms

  private HashMap<String, PeerInfo> peerOnlineHash = new HashMap<String, PeerInfo>();

  public void print(String string)
  {
    System.out.print(string);
  }

  public void println(String string)
  {
    System.out.println(string);
  }

  public void printSyncRPCResult(BitsFlowMessage result)
  {
    try {
      String srcTestID = (String)  result.getField(0);
      String response  = (String)  result.getField(1);
      println("======== " + srcTestID + " ========");
      println(response);
      println("==================================");
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
    }
  }
  public void printHelp()
  {
    println("Command List:\n\t"
          + "0: show this help\n\t"
          + "1: show online servers\n\t"
          + "2: show a server's details\n\t"
          + "3: show online servers' details\n\t"
          + "4: stop test\n\t"
          + "5: set servers' parameters\n\t"
          + "6: set client's RPC timeout(default:20000000 microseconds)\n\t"
          + "7: set client's scanning time(default:2000 milliseconds)");
  }

  class PeerInfo
  {
    public PeerInfo()
    {
    }
  }

  public void scanTester()
  {
    try {
      peerOnlineHash.clear();
      M2SPublishHeartbeat(true);
      M2CPublishHeartbeat(true);
      Thread.sleep(waitTime);
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
    }
  }

  public void pressZero()
  {
    printHelp();
  }
  public void pressOne()
  {
    scanTester();
    println("  Online Tester number is: " + peerOnlineHash.size());
  }
  public void pressTwo(String input)
  {
    getDetails(input);
  }
  public void pressThree()
  {
    scanTester();
    println("  Online Tester number is: " + peerOnlineHash.size());
    for (Map.Entry entry : peerOnlineHash.entrySet()) {
      println("    TestID: " + entry.getKey());
    }
  }
  public void pressFour(String input)
  {
    if ("all".equals(input)) {
      stopAllTest();
    } else {
      stopTest(input);
    }
  }
  public void pressFive(String target, String paramType, String param)
  {
    M2CSetType type;
    if ("0".equals(paramType)) {
      type = M2CSetType.SET_PAYLOAD;
    } else {
      type = M2CSetType.SET_SEND_INTERVAL;
    }

    if ("all".equals(target)) {
      setAllParameter(type, param);
    } else {
      setParameter(target, type, param);
    }
  }

  public void run()
  {
    try {
      startup();
      printHelp();
      BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
      String input = null;
      String target = null;
      String paramType = null;
      String param = null;
      while (true) {
        print("Enter your choose: ");
        input = br.readLine();
        if ("0".equals(input)) {
          pressZero();
        } else if ("1".equals(input)) {
          pressOne();
        } else if ("2".equals(input)) {
          print("  Enter the server's TestID: ");
          input = br.readLine();
          pressTwo(input);
        } else if ("3".equals(input)) {
          pressThree();
        } else if ("4".equals(input)) {
          print("  all: stop all test\n  TestID: stop the TestID\n  Your choose: ");
          input = br.readLine();
          pressFour(input);
        } else if ("5".equals(input)) {
          print("  all: set all servers\n  TestID: set the given server\n  Your choose: ");
          target = br.readLine();
          print("  0: set payload size(Byte), not safe\n  1: set sender's interval time(ms)\n  Your choose: ");
          paramType = br.readLine();
          print("  Enter the value: ");
          param = br.readLine();
          pressFive(target, paramType, param);
        } else if ("6".equals(input)) {
          print("  Enter the timeout value(microseconds): ");
          input = br.readLine();
          timeout = Long.valueOf(input);
        } else if ("7".equals(input)) {
          print("  Enter the timeout value(milliseconds): ");
          input = br.readLine();
          waitTime = Long.valueOf(input);
        } else {
          logger.error("Unsupport command.");
        }
      }
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
    }
  }

  public void onMessage(BitsFlowListener listener, BitsFlowMessage msg)
  {
    try {
      int caseID;
      PeerInfo peer;
      String subject   = msg.getSubject();
      String srcTestID = (String) msg.getField(0);
      if (srcTestID.equals(localTestID)) {
        return;
      }

      MessageType msgType = (MessageType) msg.getField(1);

      logger.info("\n==== receive " + msgType + " from " + srcTestID + " ====");
      switch (msgType) {
      case S2M_HEARTBEAT:
      case C2M_HEARTBEAT:
        peer = peerOnlineHash.get(srcTestID);
        if (peer == null) {
          peerOnlineHash.put(srcTestID, new PeerInfo());
        }
        break;

      default:
        logger.warn("Unknown msgType " + msgType);
        break;
      }

    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
    }
  }
  public void getDetails(String targetTestID)
  {
    logger.info("send getDetails-message");
    invokeRPCSyncMessage(CLIENT_SUBJECT + targetTestID, M2C_GET, localTestID);
  }

  public void stopAllTest()
  {
    logger.info("send stop-message to all");
    publishMessage(CLIENT_SUBJECT, M2C_STOP, localTestID);
  }

  public void stopTest(String targetTestID)
  {
    logger.info("send stop-message to " + targetTestID);
    publishMessage(CLIENT_SUBJECT + targetTestID, M2C_STOP, localTestID);
  }

  public void setAllParameter(M2CSetType paramType, String param)
  {
    logger.info("send set-message to all");
    publishMessage(CLIENT_SUBJECT, M2C_SET, localTestID, paramType, param);
  }

  public void setParameter(String targetTestID, M2CSetType paramType, String param)
  {
    logger.info("send set-message to " + targetTestID);
    publishMessage(CLIENT_SUBJECT + targetTestID, M2C_SET, localTestID, paramType, param);
  }

  public TestManager(String agent, String service)
  {
    super(agent, service, ROLE_RECEIVER, TestRole.MANAGER);

    String[] subjects = new String[]{MANAGER_SUBJECT};
    init(subjects);
  }

  public static void main(String [] args) throws Exception
  {
    if (args.length != 2) {
      logger.error("Usage: TestManager agent:port managment-service");
      return;
    }

    String agent   = args[0];
    String service = args[1];
    TestManager server = new TestManager(agent, service);
    server.setName("TestManager");
    server.start();
    server.join();
  }
}
