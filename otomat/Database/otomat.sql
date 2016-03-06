-- MySQL  (x86_64)
--
-- Host: Mysql-server    Database: otomat
-- ------------------------------------------------------
-- Server version	5.1.73

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cpu`
--

DROP TABLE IF EXISTS `cpu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cpu` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Hostname` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Host_ip` varchar(16) CHARACTER SET utf8 DEFAULT NULL,
  `Time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `CPU_Loadavg` varchar(20) DEFAULT NULL,
  `CPU_User` decimal(6,2) DEFAULT NULL,
  `CPU_Nice` decimal(6,2) DEFAULT NULL,
  `CPU_System` decimal(8,7) DEFAULT NULL,
  `CPU_Iowait` decimal(6,2) DEFAULT NULL,
  `CPU_Steal` decimal(6,2) DEFAULT NULL,
  `CPU_Idel` decimal(6,4) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `mem`
--

DROP TABLE IF EXISTS `mem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mem` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Hostname` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Host_ip` varchar(16) CHARACTER SET utf8 DEFAULT NULL,
  `Time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `MEM_Total` bigint(6) DEFAULT NULL,
  `MEM_Freed` bigint(6) DEFAULT NULL,
  `MEM_Used` bigint(6) DEFAULT NULL,
  `MEM_Buffers_Freed` bigint(6) DEFAULT NULL,
  `MEM_Buffers_Used` bigint(6) DEFAULT NULL,
  `MEM_Used_Percent` decimal(6,4) DEFAULT NULL,
  `SWAP_Total` bigint(6) DEFAULT NULL,
  `SWAP_Freed` bigint(6) DEFAULT NULL,
  `SWAP_Used` bigint(6) DEFAULT NULL,
  `SWAP_Used_Percent` decimal(6,4) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `disk`
--

DROP TABLE IF EXISTS `disk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `disk` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Hostname` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Host_ip` varchar(16) CHARACTER SET utf8 DEFAULT NULL,
  `Time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `DISK_Total` bigint(6) DEFAULT NULL,
  `DISK_Used` bigint(6) DEFAULT NULL,
  `DISK_Freed` bigint(6) DEFAULT NULL,
  `Disk_Used_Percent` decimal(17,15) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `network`
--

DROP TABLE IF EXISTS `network`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `network` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Hostname` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Host_ip` varchar(16) CHARACTER SET utf8 DEFAULT NULL,
  `Time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `Networktraffic_recv` bigint(6) DEFAULT NULL,
  `Networktraffic_recv_err` bigint(6) DEFAULT NULL,
  `Networktraffic_sent` bigint(6) DEFAULT NULL,
  `Networktraffic_sent_err` bigint(6) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `network`
--

DROP TABLE IF EXISTS `login_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_user` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Hostname` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `Host_ip` varchar(16) CHARACTER SET utf8 DEFAULT NULL,
  `Time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `User_num` bigint(6) DEFAULT NULL,
  `User_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

-- Dump completed on 2014-11-29 20:57:07
