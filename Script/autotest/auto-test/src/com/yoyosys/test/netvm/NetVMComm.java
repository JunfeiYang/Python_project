package com.yoyosys.test.netvm;

import com.yoyosys.bitsflow.api.*;
import com.yoyosys.bitsflow.api.impl.*;
import com.yoyosys.netvm.client.*;
import org.apache.log4j.Logger;

public abstract class NetVMComm extends Thread implements NetVMClientListener
{
  static Logger logger = Logger.getLogger(NetVMComm.class);
  protected static Object initLock  = new Object();
  protected String agent;
  protected String agentService;
  protected static BitsFlowEnv bitsflowEnv;
  protected static BitsFlowMessaging messaging;
  protected static BitsFlowChannel channel;
  public static NetVMClient netvmClient;

  public void querySystemStats() throws Exception
  {
    netvmClient.querySystemStats(NetVMClient.ALL_HOSTS, NetVMClient.ALL_STATS);
  }

  public void onSystemInfoRcvd(NetVMClient client, String hostId, String xml)
  {
    System.err.println("Default onSystemInfoRcvd handler");
  }

  public void onMonitorEvent(NetVMClient paramNetVMClient, NetVMMonitorEvent paramNetVMMonitorEvent)
  {
    System.err.println("Default onMonitorEvent handler");
  }

  protected void startup()
  {
    try {
      channel.start();
      netvmClient = new NetVMClient(channel);
      netvmClient.addClientListener(this);
      netvmClient.configure(true);
      netvmClient.start();
    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }

  public void init()
  {
    try {
      synchronized (initLock) {
        if (messaging == null) {
          bitsflowEnv = BitsFlowEnv.getInstance();
          messaging = bitsflowEnv.getDefaultMessaging();
          logger.info("agent-service ==> " + agent + "-" + agentService);
          channel = messaging.createChannel(agent, agentService);
        }
      }

    } catch (Exception ex) {
      logger.error(ex.getMessage(), ex);
      throw new RuntimeException(ex);
    }
  }
  public NetVMComm(String agent, String agentService)
  {
    this.agent = agent;
    this.agentService = agentService;
  }
}
