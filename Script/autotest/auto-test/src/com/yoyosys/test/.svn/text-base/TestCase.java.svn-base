package com.yoyosys.test;

import org.apache.log4j.Logger;
import com.yoyosys.bitsflow.api.*;
import com.yoyosys.bitsflow.api.impl.*;
import com.yoyosys.jcore.datanode.*;
import java.util.concurrent.atomic.*;
import com.yoyosys.test.bitsflow.BitsflowComm.*;

public abstract class TestCase
{
  public static Logger logger = Logger.getLogger(TestCase.class);
  public static int errorCode; //0: successful
  public static String errorInfo = "successful";
  public static int localSenderNum;
  public static int localReceiverNum;
  public static int localMessageLength;
  public static byte[] content = new byte[localMessageLength];
  public static AtomicLong totalRecvMessageNum = new AtomicLong(0);
  public static AtomicLong activeThreadNum = new AtomicLong(0);
  public static volatile int localSenderIntervalTime;

  public static Object testBegin = new Object();
  public static Object testEnd   = new Object();

  public static TestCase createTest(YoyoDataNode datasource)
  {
    throw new RuntimeException("TestCase.createTest must be implement.");
  }

  /* called by Test case(TestBitsflow***Client)  */
  public static void setActiveThread(long num)
  {
    activeThreadNum.set(num);
  }
  /* called by Test case(TestBitsflow***Client)  */
  public static long addActiveThread(long num)
  {
    return activeThreadNum.addAndGet(num);
  }

  public static long getActiveThread()
  {
    return activeThreadNum.get();
  }

  /* called by Test case(TestBitsflow***Client)  */
  public static void setReport(int code, String info)
  {
    errorCode = code;
    errorInfo = info;
  }

  /* called by Test case(TestBitsflow***Client)  */
  public void waitBegin() throws Exception
  {
    synchronized (testBegin) {
      testBegin.wait();
    }
  }

  /* called by TestClient */
  public void notifyBegin() throws Exception
  {
    synchronized (testBegin) {
      testBegin.notifyAll();
    }
  }

  /* called by TestClient */
  public void waitStop() throws Exception
  {
    synchronized (testEnd) {
      testEnd.wait();
    }
  }

  /* called by Test case(TestBitsflow***Client)  */
  public void notifyStop() throws Exception
  {
    synchronized (testEnd) {
      testEnd.notifyAll();
    }
  }

  public String createGetResponse()
  {
    StringBuffer buf = new StringBuffer();
    buf.append("SenderNum:           "     + localSenderNum);
    buf.append("\r\nReceiverNum:         " + localReceiverNum);
    buf.append("\r\nMessageLength:         " + localMessageLength);
    buf.append("\r\nSenderIntervalTime:  " + localSenderIntervalTime);
    buf.append("\r\ntotalRecvMessageNum: " + totalRecvMessageNum.get());
    return buf.toString();
  }
}

