/*
 * Copyright 2012 YoYo Systems, Inc.
 *
 * $ Id:$
 */

/*
 * -----------------------------------------------------------
 * file name  : TestSuite.java
 * creator    : wenxin(wen.xin@yoyosys.com)
 * created    : Fri 27 Apr 2012 12:22:23 AM CST
 *
 * modifications:
 *
 * -----------------------------------------------------------
 */
package com.yoyosys.autotest.platform.server;

import java.util.List;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.InputStreamReader;

import org.w3c.dom.*;
import com.google.gson.Gson;

import com.yoyosys.workflow.client.util.XMLUtils;

public class TestSuite
{

  public String suitePolicy;
  public String suiteName;
  public String user;
  public List<String> testPolicyList;
  public List<ArrayList<String>> testHostList;
  public List<String> testSoftwareList;
  public List<ArrayList<String>> caseScriptList;
  public List<ArrayList<String>> caseNameList;

  /**
   * default constructor.
   */
  public TestSuite()
  {
  }

  public TestSuite(String testSuiteXml, String user) throws Exception
  {
    this.user = user;
    this.loadXml(testSuiteXml);
  } // END: TestSuite

  public void loadXml(String testSuiteXml) throws Exception
  {
    Node testSuiteNode = XMLUtils.loadFromXMLString(testSuiteXml);
    suitePolicy = XMLUtils.getAttribute(testSuiteNode, "policy");
    suiteName = XMLUtils.getAttribute(testSuiteNode, "name");

    NodeList testNodes = ((Element) testSuiteNode).getElementsByTagName("test");

    testPolicyList = new ArrayList<String>();
    testHostList = new ArrayList<ArrayList<String>>();
    testSoftwareList = new ArrayList<String>();
    caseScriptList = new ArrayList<ArrayList<String>>();
    caseNameList = new ArrayList<ArrayList<String>>();

    for (int i = 0; i < testNodes.getLength(); i++) {
      Node testNode = testNodes.item(i);
      Element testNodeElement = (Element) testNode;

      String testPolicy = XMLUtils.getAttribute(testNode, "policy");
      testPolicyList.add(testPolicy);


      ArrayList<String> hostList = new ArrayList<String>();

      Node hostsNode = testNodeElement.getElementsByTagName("hosts").item(0);
      NodeList hostNodes = ((Element) hostsNode).getElementsByTagName("host");
      for (int j = 0; j < hostNodes.getLength(); j++) {
        Node hostNode = hostNodes.item(j);
        String hostId = XMLUtils.getAttribute(hostNode, "id");
        hostList.add(hostId);
      }

      testHostList.add(hostList);



      StringBuffer softwareBuffer = new StringBuffer();

      Node softwaresNode = testNodeElement.getElementsByTagName("software").item(0);
      NodeList yoyopkgNodes = ((Element) softwaresNode).getElementsByTagName("yoyopkg");
      for (int j = 0; j < yoyopkgNodes.getLength(); j++) {
        Node yoyopkgNode = yoyopkgNodes.item(j);
        String yoyopkgType = XMLUtils.getAttribute(yoyopkgNode, "type");
        String yoyopkgData = XMLUtils.getData(yoyopkgNode);
        if ("tag".equals(yoyopkgType)) {
          softwareBuffer.append("yoyopkg install --tag " + yoyopkgData);
        } else {
          softwareBuffer.append("yoyopkg install " + yoyopkgData);
        }
        softwareBuffer.append("\n");
      }

      testSoftwareList.add(softwareBuffer.toString());


      ArrayList<String> scriptList = new ArrayList<String>();

      Node scriptsNode = testNodeElement.getElementsByTagName("script").item(0);
      Node startNode = ((Element) scriptsNode).getElementsByTagName("start").item(0);
      String startScript = XMLUtils.getData(startNode);
      scriptList.add(startScript.trim());
      caseScriptList.add(scriptList);

      ArrayList<String> caseList = new ArrayList<String>();

      Node casesNode = testNodeElement.getElementsByTagName("cases").item(0);
      NodeList caseNodes = ((Element) casesNode).getElementsByTagName("case");
      for (int j = 0; j < caseNodes.getLength(); j++) {
        Node caseNode = caseNodes.item(j);
        String caseName = XMLUtils.getData(caseNode);
        caseList.add(caseName);
      }

      caseNameList.add(caseList);



    }

  }

  public List<String> getEvalExpressions()
  {
    List<String> evalList = new ArrayList<String>();

    evalList.add(String.format("suitePolicy='%s'", this.suitePolicy));
    evalList.add(String.format("suiteName='%s'", this.suiteName));
    evalList.add(String.format("currentCase=0", this.suitePolicy));
    evalList.add(String.format("currentTest=0", this.suitePolicy));
    evalList.add(String.format("installRetryNum=3", this.suitePolicy));

    Gson gson = new Gson();
    evalList.add(String.format("caseScriptList=%s", gson.toJson(this.caseScriptList)));
    evalList.add(String.format("testPolicyList=%s", gson.toJson(this.testPolicyList)));
    evalList.add(String.format("caseNameList=%s", gson.toJson(this.caseNameList)));
    evalList.add(String.format("softwareList=%s", gson.toJson(this.testSoftwareList)));
    evalList.add(String.format("hostIds=%s", gson.toJson(this.testHostList)));
    evalList.add(String.format("user='%s'", this.user));

    return evalList;
  }

  public String getTestXmlExample() throws Exception
  {
    StringBuffer suiteBuffer = new StringBuffer();
    BufferedReader in = new BufferedReader(new InputStreamReader(this.getClass().getResourceAsStream("/test_spec_example.xml")));
    String line = null;
    while ((line = in.readLine()) != null) {
      suiteBuffer.append(line);
      suiteBuffer.append("\n");
    }
    return suiteBuffer.toString();

  }


} // END: TestSuite
///:~

