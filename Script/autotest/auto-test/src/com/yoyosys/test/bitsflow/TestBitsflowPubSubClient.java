package com.yoyosys.test.bitsflow;

import com.yoyosys.test.*;
import static com.yoyosys.test.TestCommon.*;
import java.util.*;
import java.io.*;
import org.apache.log4j.Logger;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import com.yoyosys.bitsflow.api.*;
import com.yoyosys.bitsflow.api.impl.*;
import com.yoyosys.jcore.datanode.*;

public class TestBitsflowPubSubClient extends TestCase
{
  static Logger logger = Logger.getLogger(TestBitsflowPubSubClient.class);
  static final YoyoKey SUBJECT_KEY    = new YoyoKey("subject");
  static final YoyoKey MESSAGE_LEN_KEY   = new YoyoKey("messageLength");
  static final YoyoKey INTERVAL_TIME_KEY = new YoyoKey("sendIntervalTime");
  static final YoyoKey MESSAGE_NUM_KEY   = new YoyoKey("sendMessageNum");
  static final YoyoKey AGENT_KEY         = new YoyoKey("agent");
  static final YoyoKey AGENT_SERVICE_KEY = new YoyoKey("agentService");

  static TestPubSub sender;
  static TestPubSub receiver;
  HashMap<String, PeerInfo> peerInfoHash = new HashMap<String, PeerInfo>();

  String contentSubject;

  class PeerInfo
  {
    public long currentMessageSeqNum;

    public PeerInfo(long msgSeqNum)
    {
      this.currentMessageSeqNum = msgSeqNum;
    }
  }

  class TestPubSub extends BitsflowComm
  {
    long totalSendMessageNum;

    public TestPubSub(String agent, String agentService,
                      int threadRole, long totalSendMessageNum)
    {
      super(agent, agentService, threadRole, TestRole.CLIENT);
      if (threadRole == ROLE_SENDER) {
        this.totalSendMessageNum = totalSendMessageNum;
        init(null);
      } else {
        String[] subjects = new String[]{
          contentSubject,
        };
        init(subjects);
      }
    }

    public void run()
    {
      try {
        startup();
        TestBitsflowPubSubClient.this.addActiveThread(1);
        TestBitsflowPubSubClient.this.waitBegin();

        if (threadRole == ROLE_SENDER) {
          while ((!allExit.get()) && (!isExit) && (messageSeqNum.get() < totalSendMessageNum)) {
            publishContent(messageSeqNum.getAndIncrement(), TestBitsflowPubSubClient.this.content);
            if (TestBitsflowPubSubClient.this.localSenderIntervalTime != 0) {
              sleep(TestBitsflowPubSubClient.this.localSenderIntervalTime);
            }
          }
          synchronized (waitExit) {
            waitExit.notifyAll();
          }

          TestBitsflowPubSubClient.this.notifyStop();

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

    public void onMessage(BitsFlowListener listener, BitsFlowMessage msg)
    {
      try {
        String subject = msg.getSubject();
        String srcTestID = (String) msg.getField(0);

        totalRecvMessageNum.incrementAndGet();

        if (srcTestID.equals(localTestID) || (threadRole == ROLE_SENDER)) {
          return;
        }

        if (subject.equals(contentSubject)) {
          logger.debug("receive content message [" + contentSubject + "] from " + srcTestID);
          long recvSeqNum = (Long) msg.getField(1);
          PeerInfo peer = null;
          peer = peerInfoHash.get(srcTestID);
          if (peer == null) {
            peerInfoHash.put(srcTestID, new PeerInfo(recvSeqNum));
          } else {
            if (peer.currentMessageSeqNum == (recvSeqNum - 1)) {
              peer.currentMessageSeqNum++;
            } else if (peer.currentMessageSeqNum > 0 && recvSeqNum == 0) {
              logger.info(srcTestID + " had been restarted.");
              peer.currentMessageSeqNum = 0;
            } else {
              throw new RuntimeException("message sequence number error[" + contentSubject + "]: expected[" + (peer.currentMessageSeqNum + 1) + "], but received[" + recvSeqNum + "] (from " + srcTestID + ")");
            }
          }

        } else {
          logger.error("unknown subject");
        }
      } catch (Exception ex) {
        logger.error(ex.getMessage(), ex);
        setReport(-1, "PubSub onMessage error");
      }
    }

    public void publishContent(long msgSeqNum, byte[] content)
    {
      logger.debug("send content-message");
      publishMessage(contentSubject, msgSeqNum, content);
    }
  }

  public void waitStop() throws Exception
  {
    receiver.join();
    sender.join();
    receiver.unsubscribe(contentSubject);
    receiver.destroy();
    sender.destroy();
    TestCase.setActiveThread(0);
  }

  public TestBitsflowPubSubClient(YoyoDataNode datasource)
  {
    try {
      String agent        = TestUtil.getNodeValue(datasource, AGENT_KEY, "agent");
      String agentService = TestUtil.getNodeValue(datasource, AGENT_SERVICE_KEY, "agentService");
      contentSubject      = TestUtil.getNodeValue(datasource, SUBJECT_KEY, "subject");
      long messageNum     = Long.valueOf(TestUtil.getNodeValue(datasource, MESSAGE_NUM_KEY, "sendMessageNum"));
      localMessageLength  = Integer.valueOf(TestUtil.getNodeValue(datasource, MESSAGE_LEN_KEY, "messageLength"));
      localSenderIntervalTime = Integer.valueOf(TestUtil.getNodeValue(datasource, INTERVAL_TIME_KEY, "sendIntervalTime"));

      receiver = new TestPubSub(agent, agentService, ROLE_RECEIVER, messageNum);
      receiver.setName("receiver");
      receiver.start();

      sender = new TestPubSub(agent, agentService, ROLE_SENDER, messageNum);
      sender.setName("sender");
      sender.start();
    } catch (Exception ex) {
      setReport(-2, "PubSub test error");
    }
  }

  public static TestCase createTest(YoyoDataNode datasource)
  {
    try {
      TestCase pubsubCase = new TestBitsflowPubSubClient(datasource);
      while (2 != TestCase.getActiveThread()) {
        Thread.sleep(100);
      }
      return pubsubCase;
    } catch (Exception ex) {
      setReport(-3, "Create Pubsub test error");
      return null;
    }
  }
}
