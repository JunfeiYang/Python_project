package com.yoyosys.test;

import com.yoyosys.jcore.datanode.*;
import org.apache.log4j.Logger;

public class TestUtil
{
  static Logger logger = Logger.getLogger(TestUtil.class);

  public static String getNodeValue(YoyoDataNode parent, YoyoKey key, String debug)
  {
    String val = getNodeValueWithDefault(parent, key, null);
    if (val == null) {
      throw new RuntimeException("missing " + debug + " node of datasource");
    }

    return val;
  }

  public static String getNodeValueWithDefault(YoyoDataNode parent, YoyoKey key, String defaultValue)
  {
    YoyoDataNode node = parent.getNode(key);
    if ((node != null) && (node.getDataAsString() != null)) {
      return node.getDataAsString();
    }
    return defaultValue;
  }
}

