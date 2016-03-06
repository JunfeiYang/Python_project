package com.yoyosys.test.bitsflow;

import static com.yoyosys.test.TestCommon.*;
import com.yoyosys.test.*;
import com.yoyosys.test.TestCase.*;
import java.util.*;
import java.io.*;
import org.apache.log4j.Logger;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import com.yoyosys.bitsflow.api.*;
import com.yoyosys.bitsflow.api.impl.*;
import com.yoyosys.jcore.datanode.*;


public class TestBitsflowGroupClient extends TestCase
{
  static Logger logger = Logger.getLogger(TestBitsflowGroupClient.class);
  static final YoyoKey MESSAGE_LEN_KEY   = new YoyoKey("messageLength");
  static final YoyoKey INTERVAL_TIME_KEY = new YoyoKey("sendIntervalTime");
  static final YoyoKey MESSAGE_NUM_KEY   = new YoyoKey("sendMessageNum");
  static final YoyoKey AGENT_KEY         = new YoyoKey("agent");
  static final YoyoKey AGENT_SERVICE_KEY = new YoyoKey("agentService");
  static final YoyoKey GROUPID_KEY       = new YoyoKey("groupID");
  static final YoyoKey GROUP_SERVICE_KEY = new YoyoKey("groupService");

  static TestGroup sender;
  static TestGroup receiver;
  static HashMap<String, PeerInfo> peerInfoHash = new HashMap<String, PeerInfo>();

  class PeerInfo
  {
    public long currentMessageSeqNum;

    public PeerInfo(long msgSeqNum)
    {
      this.currentMessageSeqNum = msgSeqNum;
    }
  }

  public static synchronized void shutDownHandle()
  {
    logger.error("shutDownHandle enter==>");
    for (Map.Entry<String, PeerInfo> entry : peerInfoHash.entrySet()) {
      logger.error(entry.getKey() + " ==> " + entry.getValue().currentMessageSeqNum);
    }
  }

  class TestGroup extends BitsflowComm
  {
    long totalSendMessageNum;

    public TestGroup(String agent, String agentService,
                     String groupID, String groupService,
                     int threadRole, long totalSendMessageNum)
    {
      super(agent, agentService, groupID, groupService, threadRole, TestRole.CLIENT);
      if (threadRole == ROLE_SENDER) {
        this.totalSendMessageNum = totalSendMessageNum;
        init(null);
      } else {
        String[] subjects = new String[]{
        };
        init(subjects);
      }
    }

    public void run()
    {
      try {
        startup();
        TestBitsflowGroupClient.this.addActiveThread(1);
        TestBitsflowGroupClient.this.waitBegin();

        if (threadRole == ROLE_SENDER) {
          while ((!allExit.get()) && (!isExit) && (messageSeqNum.get() < totalSendMessageNum)) {
            sendGroupMessage(BitsFlowMessage.ORDERING_IMMEDIATE, messageSeqNum.getAndIncrement(), TestBitsflowGroupClient.this.content);
            if (TestBitsflowGroupClient.this.localSenderIntervalTime != 0) {
              sleep(TestBitsflowGroupClient.this.localSenderIntervalTime);
            }
          }
          synchronized (waitExit) {
            waitExit.notifyAll();
          }
          isExit = true;
        } else {
          synchronized (waitExit) {
            waitExit.wait();
          }
        }
      } catch (Exception ex) {
        logger.error(ex.getMessage(), ex);
        throw new RuntimeException(ex);
      }
    }

    public void onBlock(BitsFlowGroupComm comm, boolean done)
    {
      try {
        if (done) {
          logger.info("Blocking Off, there is " + groupPendingMsgQueue.size() + " groupPending messages to deliver");
          groupCommBlocked.set(false);
        } else {
          logger.info("Blocking on");
          groupCommBlocked.set(true);
          comm.block();
        }
      } catch (Exception ex) {
        logger.error(ex.getMessage(), ex);
        throw new RuntimeException(ex);
      }
    }

    public void onView(BitsFlowGroupComm comm)
    {
      StringBuilder sb = new StringBuilder();
      sb.append("New view:\n");
      try {
        if (comm.getRank() == -1) {
          if (isExit) {
            return;
          }
          logger.error("Network is down, watch dog start detecting network");

          NetworkWatchDog watchDog = new NetworkWatchDog();
          watchDog.start();
          return;
        }

        int groupSize = comm.getGroupSize();
        for (int i = 0; i < groupSize; i++) {
          BitsFlowGroupMember member = comm.getMember(i);
          // test if the context is in bootstrap mode for this
          sb.append(i);
          sb.append(".");
          sb.append(member.getInbox());
          if (i == comm.getRank()) {
            sb.append(" (<-- Me)");
          }
          sb.append("\n");
        }
      } catch (Exception ex) {
        logger.error(ex.getMessage(), ex);
        throw new RuntimeException(ex);
      } finally {
        logger.info(sb.toString());
      }
    }

    public void onMessage(BitsFlowGroupComm comm, BitsFlowMessage msg)
    {
      try {
        String subject = msg.getSubject();
        String srcTestID = (String) msg.getField(0);

        totalRecvMessageNum.incrementAndGet();

        if (srcTestID.equals(localTestID)) {
          return;
        }

        logger.debug("receive groupComm message from " + srcTestID);

        long recvSeqNum = (Long) msg.getField(1);
        PeerInfo peer = peerInfoHash.get(srcTestID);
        if (peer == null) {
          peerInfoHash.put(srcTestID, new PeerInfo(recvSeqNum));
        } else {
          if (peer.currentMessageSeqNum == (recvSeqNum - 1)) {
            peer.currentMessageSeqNum++;
          } else if (peer.currentMessageSeqNum > 0 && recvSeqNum == 0) {
            logger.info(srcTestID + " had been restarted.");
            peer.currentMessageSeqNum = 0;
          } else {
            throw new RuntimeException("message sequence number error. expected seq is " + (peer.currentMessageSeqNum + 1) + ", but this seq is" + recvSeqNum + " (from " + srcTestID + ")");
          }
        }

      } catch (Exception ex) {
        logger.error(ex.getMessage(), ex);
        setReport(-1, "Group onMessage error");
      }
    }
  }

  public void waitStop() throws Exception
  {
//    receiver.join();
//    receiver.destroy();
    sender.join();
    sender.destroy();
    TestCase.setActiveThread(0);
  }

  public TestBitsflowGroupClient(YoyoDataNode datasource)
  {
    try {
      String agent        = String.valueOf(TestUtil.getNodeValue(datasource, AGENT_KEY, "agent"));
      String agentService = String.valueOf(TestUtil.getNodeValue(datasource, AGENT_SERVICE_KEY, "agentService"));
      String groupID      = String.valueOf(TestUtil.getNodeValue(datasource, GROUPID_KEY, "groupID"));
      String groupService = String.valueOf(TestUtil.getNodeValue(datasource, GROUP_SERVICE_KEY, "groupService"));
      long messageNum     = Long.valueOf(TestUtil.getNodeValue(datasource, MESSAGE_NUM_KEY, "sendMessageNum"));
      localMessageLength  = Integer.valueOf(TestUtil.getNodeValue(datasource, MESSAGE_LEN_KEY, "messageLength"));
      localSenderIntervalTime = Integer.valueOf(TestUtil.getNodeValue(datasource, INTERVAL_TIME_KEY, "sendIntervalTime"));

/*
      receiver = new TestGroup(agent, agentService,
                               groupID, groupService,
                               "receiver", BitsflowComm.ROLE_RECEIVER, messageNum);
      receiver.setName("receiver");
      receiver.start();
*/
      sender = new TestGroup(agent, agentService,
                             groupID, groupService,
                             ROLE_SENDER, messageNum);
      sender.setName("sender");
      sender.start();
    } catch (Exception ex) {
      setReport(-2, "Group test error");
    }
  }

  public static TestCase createTest(YoyoDataNode datasource)
  {
    try {
      TestCase groupCase = new TestBitsflowGroupClient(datasource);
      while (1 != TestCase.getActiveThread()) {
        Thread.sleep(100);
      }
      return groupCase;
    } catch (Exception ex) {
      setReport(-3, "Create Group test error");
      return null;
    }
  }
}
