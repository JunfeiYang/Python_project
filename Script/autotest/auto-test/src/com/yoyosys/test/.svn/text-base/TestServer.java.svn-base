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

public class TestServer extends BitsflowComm
{
  static Logger logger = Logger.getLogger(TestServer.class);
  static final YoyoKey GLOBAL_KEY = new YoyoKey("global");
  static final YoyoKey CASE_KEY   = new YoyoKey("case");
  static final YoyoKey CLIENTNUM_KEY = new YoyoKey("global/Client-Num");
  private ArrayList<PeersInfo> caseInfoList  = new ArrayList<PeersInfo>();
  private ArrayList<String> caseNameList   = new ArrayList<String>();
  private ArrayList<String> caseConfigList = new ArrayList<String>();
  private ArrayList<String> classNameList  = new ArrayList<String>();
  static Object waitExit   = new Object();
  static int totalTester;
  static int totalCase;
  static int currentCaseID;

  public enum CLIENT_STATUS
  {
    GET_TASK,
    READY,
    REPORT,
  }

  class PeersInfo
  {
    int caseID;
    int getTaskNum;
    int readyNum;
    int reportNum;
    HashMap<String, CLIENT_STATUS> peerInfoHash = new HashMap<String, CLIENT_STATUS>();

    public PeersInfo(int caseID)
    {
      this.caseID = caseID;
    }

    public int addGetTaskPeer(String peerTestID)
    {
      CLIENT_STATUS status = peerInfoHash.get(peerTestID);
      if (status == null || status == CLIENT_STATUS.REPORT) {
        peerInfoHash.put(peerTestID, CLIENT_STATUS.GET_TASK);
        getTaskNum++;
        return 0;
      } else {
        logger.error(peerTestID + " status error[" + status + "]");
        return -1;
      }
    }
    public int addReadyPeer(String peerTestID)
    {
      CLIENT_STATUS status = peerInfoHash.get(peerTestID);
      if (status == CLIENT_STATUS.GET_TASK) {
        peerInfoHash.put(peerTestID, CLIENT_STATUS.READY);
        readyNum++;
        return 0;
      } else {
        logger.error(peerTestID + " status error[" + status + "]");
        return -1;
      }
    }
    public int addReportPeer(String peerTestID)
    {
      CLIENT_STATUS status = peerInfoHash.get(peerTestID);
      if (status == CLIENT_STATUS.READY) {
        peerInfoHash.put(peerTestID, CLIENT_STATUS.REPORT);
        reportNum++;
        return 0;
      } else {
        logger.error(peerTestID + " status error[" + status + "]");
        return -1;
      }
    }
    public int getGetTaskNum()
    {
      return getTaskNum;
    }
    public int getReadyNum()
    {
      return readyNum;
    }
    public int getReportNum()
    {
      return reportNum;
    }
  }

  public void run()
  {
    try {
      startup();
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
      int caseID;
      PeersInfo peers;
      String subject   = msg.getSubject();
      String srcTestID = (String) msg.getField(0);
      if (srcTestID.equals(localTestID)) {
        return;
      }

      MessageType msgType = (MessageType) msg.getField(1);

      logger.debug("\n==== receive " + msgType + " from " + srcTestID + " ====");

      switch (msgType) {
      case C2S_GET_TASK:
        int returnCaseID;
        caseID = (Integer) msg.getField(2);
        if (caseID == -1) {
          returnCaseID = currentCaseID;
        } else {
          returnCaseID = caseID + 1;
        }

        if (returnCaseID > (totalCase - 1)) {
          logger.info("Test finished, and return -1 to " + srcTestID);
          sendRPCReplyMessage(false, msg, CLIENT_SUBJECT, -1);

        } else {
          peers = caseInfoList.get(returnCaseID);
          if (peers.addGetTaskPeer(srcTestID) >= 0) {
            sendRPCReplyMessage(false, msg, CLIENT_SUBJECT,
                                returnCaseID,
                                caseNameList.get(returnCaseID),
                                classNameList.get(returnCaseID),
                                caseConfigList.get(returnCaseID));
          }
        }
        break;

      case C2S_READY:
        caseID = (Integer) msg.getField(2);
        logger.debug("caseID " + caseID + " is ready");
        if (caseID >= totalCase) {
          logger.error("caseID >= totalCase");
          return;
        }

        peers = caseInfoList.get(caseID);
        if (peers.addReadyPeer(srcTestID) >= 0) {
          if (peers.getReadyNum() == totalTester) {
            publishMessage(false, CLIENT_SUBJECT, S2C_RUN);
            logger.info("\n\n**** " + caseNameList.get(caseID) + " begin ****");
          }
        }
        break;

      case C2S_REPORT_TASK:
        caseID      = (Integer) msg.getField(2);
        int code    = (Integer) msg.getField(3);
        String info = (String) msg.getField(4);

        if (code != 0) {
          logger.error(srcTestID + " report "
                       + code
                       + "[" + info + "]");
        } else {
          logger.info(srcTestID + " report successful");
        }

        peers = caseInfoList.get(caseID);
        if (peers.addReportPeer(srcTestID) >= 0) {
          if (peers.getReportNum() == totalTester) {
            logger.info("\n**** " + caseNameList.get(caseID) + " end ****");
            if (totalCase == (caseID + 1)) {
              logger.info("#### Testsuite has finished ####\n\n");
            }
            currentCaseID++;
          }
        }
        break;

      case M2S_HEARTBEAT:
        S2MPublishHeartbeat(false);
        break;

      default:
        logger.warn("Unknown msgType " + msgType);
        break;
      }

    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
    }
  }

  public TestServer(String agent, String service)
  {
    super(agent, service, ROLE_RECEIVER, TestRole.SERVER);

    YoyoDataNode rootNode =
      YoyoDataLoader.loadFromXML(this.getClass().getResourceAsStream("/TestServer.xml"));

    List<YoyoDataNode> caseNodes = new ArrayList();
    rootNode.getNodeList(caseNodes, CASE_KEY);
    totalCase   = caseNodes.size();
    totalTester = Integer.valueOf(TestUtil.getNodeValue(rootNode, CLIENTNUM_KEY, "Client-Num"));
    String caseName;
    String className;
    String config;
    int tmpCaseID = 0;
    for (YoyoDataNode caseNode : caseNodes) {
      caseName  = caseNode.getAttributeAsString("name");
      className = caseNode.getAttributeAsString("class");
      config    = YoyoDataLoader.saveToXMLString(caseNode);
      caseNameList.add(caseName);
      classNameList.add(className);
      caseConfigList.add(config);
      caseInfoList.add(new PeersInfo(tmpCaseID++));
    }
    String[] subjects = new String[]{SERVER_SUBJECT};
    init(subjects);
  }

  public static void main(String [] args) throws Exception
  {
    if (args.length != 2) {
      logger.error("Usage: TestServer agent:port managment-service");
      return;
    }

    String agent   = args[0];
    String service = args[1];
    TestServer server = new TestServer(agent, service);
    server.setName("TestServer");
    server.start();
    server.join();
  }
}
