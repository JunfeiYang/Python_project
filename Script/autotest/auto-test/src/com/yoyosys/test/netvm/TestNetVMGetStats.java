package com.yoyosys.test.netvm;

import com.yoyosys.test.*;
import static com.yoyosys.test.TestCommon.*;
import com.yoyosys.netvm.client.*;
import java.util.*;
import org.apache.log4j.Logger;
import com.yoyosys.jcore.datanode.*;

public class TestNetVMGetStats extends TestCase
{
  static Logger logger = Logger.getLogger(TestNetVMGetStats.class);
  static final YoyoKey AGENT_KEY         = new YoyoKey("agent");
  static final YoyoKey AGENT_SERVICE_KEY = new YoyoKey("agentService");
  static final YoyoKey GET_STATS_NUM_KEY = new YoyoKey("getStatsNum");
  static int getStatsNum;

  class TestNetVM extends NetVMComm
  {
    public TestNetVM(String agent, String agentService)
    {
      super(agent, agentService);
      init();
    }

    public void onSystemInfoRcvd(NetVMClient client, String hostId, String xml)
    {
      logger.info("onSystemInfoRcvd enter");
      logger.info("  hostId: " + hostId);
      logger.info("  xml: " + xml);
    }

    public void onMonitorEvent(NetVMClient paramNetVMClient, NetVMMonitorEvent paramNetVMMonitorEvent)
    {
      logger.info("onMonitorEvent enter");
      logger.info("  hostId: " + paramNetVMMonitorEvent.getHostId());
      logger.info("  typeName: " + paramNetVMMonitorEvent.getTypeName());
    }
    public void run()
    {
      try {
        startup();
        TestNetVMGetStats.this.addActiveThread(1);
        TestNetVMGetStats.this.waitBegin();
        while (getStatsNum-- > 0) {
          querySystemStats();
        }
        TestNetVMGetStats.this.notifyStop();
      } catch (Exception ex) {
        logger.error(ex.getMessage(), ex);
        throw new RuntimeException(ex);
      }
    }
  }

  public TestNetVMGetStats(YoyoDataNode datasource)
  {
    try {
      String agent        = TestUtil.getNodeValue(datasource, AGENT_KEY, "agent");
      String agentService = TestUtil.getNodeValue(datasource, AGENT_SERVICE_KEY, "agentService");
      getStatsNum = Integer.valueOf(TestUtil.getNodeValue(datasource, GET_STATS_NUM_KEY, "getStatsNum"));
      TestNetVM tester = new TestNetVM(agent, agentService);
      tester.setName("netVMGetStats");
      tester.start();
    } catch (Exception ex) {
      setReport(-2, "NetVMGetStats test error");
    }
  }

  public static TestCase createTest(YoyoDataNode datasource)
  {
    try {
      TestCase netvmCase = new TestNetVMGetStats(datasource);
      return netvmCase;
    } catch (Exception ex) {
      setReport(-3, "Create NetVMGetStats test error");
      return null;
    }
  }
}
