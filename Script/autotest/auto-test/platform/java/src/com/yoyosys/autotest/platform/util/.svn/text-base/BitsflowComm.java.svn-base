package com.yoyosys.autotest.platform.util;

//import com.yoyosys.test.*;
import static com.yoyosys.autotest.platform.util.TestCommon.*;
import static com.yoyosys.autotest.platform.util.TestCommon.MessageType.*;
import com.yoyosys.bitsflow.api.*;
import com.yoyosys.bitsflow.api.impl.*;
import org.apache.log4j.Logger;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.concurrent.locks.*;

public abstract class BitsflowComm extends Thread
  implements ChannelListener, MessageListener, GroupCommListener, BitsFlowRPCHandler
{
  static Logger logger = Logger.getLogger(BitsflowComm.class);
  private boolean reconnect = true;
  protected static Object getIDLock = new Object();
  protected String agent;
  protected String agentService;
  protected String groupService;
  protected String groupID;

  protected static long timeout = 50000000; //unit: us

  protected static BitsFlowEnv bitsflowEnv;
  protected BitsFlowMessaging messaging;
  protected BitsFlowChannel   pubSubChannel;
  protected BitsFlowListener  pubSubListener;
  protected BitsFlowSender    pubSubSender;
  protected BitsFlowChannel   groupChannel;
  protected BitsFlowSender    groupSender;
  protected BitsFlowGroupComm groupComm;
  protected GroupCommListener grouplistener;
  protected static Queue<BitsFlowMessage> groupPendingMsgQueue = new ConcurrentLinkedQueue();
  protected static AtomicBoolean groupCommBlocked = new AtomicBoolean(false);

  public static String localTestID;
  protected String testRole;

  //threadRole:  1--sender(only send message)   2--receiver(send and receive message)
  protected int threadRole = ROLE_SENDER;

  protected AtomicLong messageSeqNum = new AtomicLong(0);
  static Object waitExit = new Object();
  static AtomicBoolean allExit = new AtomicBoolean(false);
  boolean isExit;

  protected void reinitializeGroupComm() throws Exception
  {
    if (groupComm != null) {
      logger.info("Destroying old group comm");
      groupComm.destroy();
      groupComm = null;
    }
    logger.info("Joining group " + groupID);
    groupComm = pubSubChannel.createGroupComm(groupID, 0, localTestID.getBytes("UTF-8"));
    groupComm.addGroupCommListener(this);
    groupComm.start();
  }

  protected void startup()
  {
    try {
      pubSubChannel.setReconnect(10000, 1000000L);
      pubSubChannel.start();
      pubSubListener.start();
      pubSubSender.start();
      if (groupService != null) {
        groupChannel.setReconnect(10000, 1000000L);
        groupChannel.start();
        messaging.setGroupdChannel(groupChannel);
        groupSender.start();
        reinitializeGroupComm();
        logger.info(groupID + " is started.");
      }
      //pubSubChannel.sendSubscription();

      synchronized (getIDLock) {
        if (localTestID == null) {
          String ip = BitsFlowUtils.getClientAddr(pubSubSender, 0);
          localTestID = testRole + "_" + ip + "_" + UUID.randomUUID().toString();
        }
      }

    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }

  public void init(String[] subjects)
  {
    try {
      if (messaging == null) {
        bitsflowEnv = BitsFlowEnv.getInstance();
        messaging = bitsflowEnv.getDefaultMessaging();
      }

      logger.info("agent-service ==> " + agent + "-" + agentService);
      pubSubChannel  = messaging.createChannel(agent, agentService);
      pubSubSender   = pubSubChannel.createSender();
      pubSubListener = messaging.createListener();
      if (groupService != null) {
        groupChannel = messaging.createChannel(agent, groupService);
        groupSender  = groupChannel.createSender();
      }

      if (threadRole == TestCommon.ROLE_RECEIVER) {
        for (String subject : subjects) {
          pubSubListener.subscribe(pubSubChannel, subject);
          logger.info("subject is " + subject);
        }
        pubSubListener.addMessageListener(this);
        //pubSubChannel.addChannelListener(this);
      }
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }

  public BitsflowComm(String agent, String agentService, String groupID, String groupService, int threadRole, TestRole testRole)
  {
    this.agent = agent;
    this.agentService = agentService;
    this.groupID = groupID;
    this.groupService = groupService;
    this.threadRole = threadRole;
    this.testRole = (testRole == TestRole.SERVER ? "server" : (testRole == TestRole.CLIENT ? "client" : "manager"));
  }

  public BitsflowComm(String agent, String agentService, int threadRole, TestRole testRole)
  {
    this.agent = agent;
    this.agentService = agentService;
    this.threadRole = threadRole;
    this.testRole = (testRole == TestRole.SERVER ? "server" : (testRole == TestRole.CLIENT ? "client" : "manager"));
  }

  public void onMessage(BitsFlowListener listener, BitsFlowMessage msg)
  {
  }
  public void onMessage(BitsFlowGroupComm comm, BitsFlowMessage msg)
  {
  }

  public class ChannelWatchDog extends Thread
  {
    BitsFlowChannel channel;
    public ChannelWatchDog(BitsFlowChannel channel)
    {
      this.channel = channel;
    }

    public void run()
    {
      setName("ChannelWatchDog thread started");
      while (true) {
        /* reconnect channel */
        try {
          channel.setReconnect(10000, 1000000L);
          channel.start();
          logger.info("channel is recovered, stopping channel watchdog");
          break;
        } catch (BitsFlowException ex) {
          logger.warn("channel is still not connected");
          try {
            sleep(1000);
          } catch (Exception e) {
            logger.warn(e.getMessage(), e);
          }
        }
      }
    }
  }
  public class NetworkWatchDog extends Thread
  {
    public NetworkWatchDog()
    {
    }

    public void run()
    {
      setName("NetworkWatchDog thread started for group " + groupID);
      while (true) {
        /* recreate groupComm */
        try {
          reinitializeGroupComm();
          logger.debug("Network is recovered, terminating watch dog");
          break;
        } catch (Exception ex) {
          logger.warn(ex.getMessage(), ex);
          logger.warn("Network is still not connected");
          try {
            sleep(1000);
          } catch (Exception e) {
            logger.warn(e.getMessage(), e);
          }
        }
      }
    }
  }

  public void onDisconnect(BitsFlowChannel channel)
  {
    logger.warn("Channel is disconnected, starting channel watch dog for channel reconnection");
    ChannelWatchDog watchDog = new ChannelWatchDog(channel);
    watchDog.start();
  }

  public void onBlock(BitsFlowGroupComm comm, boolean done)
  {
  }

  public void onView(BitsFlowGroupComm comm)
  {
  }

  public void onAdvisory(BitsFlowGroupComm comm, BitsFlowAdvisory advisory)
  {
    logger.warn("The groupChannel received a advisory message");
  }

  public void onAdvisory(BitsFlowChannel channel, BitsFlowAdvisory adv)
  {
    logger.warn("The channel received a advisory message");
    if (adv.getSeverity() == BitsFlowAdvisory.ERROR) {
      reconnect = false;
    }
  }

  public void onReplyRecv(BitsFlowSender sender, BitsFlowMessage replyMsg)
  {
  }

  public void publishMessage(String subject, Object...datas)
  {
    publishMessage(true, subject, datas);
  }
  public void publishMessage(boolean blocking, String subject, Object...datas)
  {
    try {
      BitsFlowMessage pubSubMsg = createMessage(subject, datas);
      publishMessage(blocking, pubSubMsg);
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }
  public void publishMessage(boolean blocking, BitsFlowMessage pubSubMsg) throws BitsFlowException
  {
    pubSubSender.publish(pubSubMsg, blocking);
  }

  public BitsFlowMessage createMessage(String subject, Object...datas) throws Exception
  {
    BitsFlowMessage message = messaging.createMessage(subject);
    message.append(localTestID);
    logger.debug("createMessage ==>");
    logger.debug("  subject:" + subject);
    logger.debug("  localTestID:" + localTestID);
    for (Object data : datas) {
      if (data != null) {
        message.append(data);
        logger.debug("  element:" + data);
      } else {
        logger.warn("createMessage found a null data");
      }
    }
    return message;
  }

  public void procSyncRPCResult(BitsFlowMessage result)
  {
  }

  public void invokeRPCSyncMessage(String subject, Object...datas)
  {
    try {
      BitsFlowMessage rpcMsg = createMessage(subject, datas);
      BitsFlowMessage result = pubSubSender.invokeRPC(rpcMsg, timeout);
      if (result == null) {
        logger.error("sendRPC timeout.");
      } else {
        this.procSyncRPCResult(result);
      }
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }

  public void invokeRPCAsyncMessage(BitsFlowSender rpcSender, String subject, Object...datas)
  {
    try {
      BitsFlowMessage rpcMsg = createMessage(subject, datas);
      rpcSender.invokeRPCAsync(rpcMsg, this);
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }

  public void sendRPCReplyMessage(boolean blocking, BitsFlowMessage requestMsg, String subject, Object...datas)
  {
    try {
      BitsFlowMessage replyMsg = pubSubSender.createReplyMessage(requestMsg, subject);
      replyMsg.append(localTestID);
      for (Object data : datas) {
        if (data != null) {
          replyMsg.append(data);
        } else {
          logger.warn("sendRPCReplyMessage found a null data");
        }
      }
      pubSubSender.publish(replyMsg, blocking);
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }

  public void sendGroupMessage(int flags, Object...datas)
  {
    try {
      BitsFlowMessage groupMsg = messaging.createMessage();
      groupMsg.setFlags(flags);
      groupMsg.append(localTestID);
      for (Object data : datas) {
        if (data != null) {
          groupMsg.append(data);
        } else {
          logger.warn("sendGroupMessage found a null data");
        }
      }

      //logger.info("sendGroupMessage");
      if (groupCommBlocked.get()) {
        groupPendingMsgQueue.offer(groupMsg);
        logger.info("group comm is blocked, push message to pending queue[" + groupPendingMsgQueue.size() + "]");
      } else {
        if (groupPendingMsgQueue.size() > 0) {
          for (BitsFlowMessage msg : groupPendingMsgQueue) {
            try {
              groupComm.send(msg, false);
              groupPendingMsgQueue.remove(msg);
            } catch (BitsFlowException ex) {
              logger.info(ex.getMessage(), ex);
              groupPendingMsgQueue.offer(groupMsg);
              logger.info("group comm is blocked, can't send pending messages");
              return;
            }
          }
        }
        try {
          groupComm.send(groupMsg, false);
        } catch (BitsFlowException ex) {
          //logger.error(ex.getMessage(), ex);
          groupPendingMsgQueue.offer(groupMsg);
          logger.info("group comm is blocked, push message to pending queue[" + groupPendingMsgQueue.size() + "].");
        }
      }
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }

  public void unsubscribe(String subject)
  {
    try {
      pubSubListener.unsubscribe(pubSubChannel, subject);
      pubSubChannel.sendSubscription();
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }

  public void destroy()
  {
    try {
      isExit = true;
      if (groupComm != null) {
        groupComm.stop();
        groupComm.destroy();
        //groupComm.stopAsync();
        groupChannel.destroy();
        groupComm = null;
      }
      if (pubSubChannel != null) {
        pubSubChannel.destroy();
        pubSubChannel = null;
      }
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }

  public void destroyMessaging()
  {
    try {
      if (messaging != null) {
        bitsflowEnv.releaseDefaultMessaging();
        messaging = null;
      }
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
    }
  }
}
