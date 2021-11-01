-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 01, 2021 at 09:51 AM
-- Server version: 5.7.23-23
-- PHP Version: 7.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: ``
--

-- --------------------------------------------------------

--
-- Table structure for table `vidnovoz_cars`
--

CREATE TABLE `vidnovoz_cars` (
  `id_tel` int(11) NOT NULL DEFAULT '0',
  `plate` varchar(45) COLLATE utf32_unicode_ci DEFAULT '',
  `mark` varchar(45) COLLATE utf32_unicode_ci DEFAULT '',
  `model` varchar(45) COLLATE utf32_unicode_ci DEFAULT '',
  `seats` int(11) DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf32 COLLATE=utf32_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vidnovoz_routes`
--

CREATE TABLE `vidnovoz_routes` (
  `id` int(11) NOT NULL,
  `route_date` date DEFAULT NULL,
  `route_time` time DEFAULT NULL,
  `route_datetime` datetime DEFAULT NULL,
  `route_created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `from_city` varchar(45) COLLATE utf32_unicode_ci DEFAULT NULL,
  `from_street` varchar(45) COLLATE utf32_unicode_ci DEFAULT NULL,
  `from_house` varchar(45) COLLATE utf32_unicode_ci DEFAULT NULL,
  `to_city` varchar(45) COLLATE utf32_unicode_ci DEFAULT NULL,
  `to_street` varchar(45) COLLATE utf32_unicode_ci DEFAULT NULL,
  `to_house` varchar(45) COLLATE utf32_unicode_ci DEFAULT NULL,
  `id_tel_driver` int(11) DEFAULT '0',
  `id_tel_user` int(11) DEFAULT '0',
  `cost_rub` int(11) DEFAULT '0',
  `driver_comment` varchar(145) COLLATE utf32_unicode_ci DEFAULT NULL,
  `user_comment` varchar(145) COLLATE utf32_unicode_ci DEFAULT NULL,
  `driver_chat_id` int(11) DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf32 COLLATE=utf32_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vidnovoz_user`
--

CREATE TABLE `vidnovoz_user` (
  `id_tel` int(11) NOT NULL,
  `nick` varchar(45) COLLATE utf32_unicode_ci DEFAULT '',
  `phone` varchar(45) COLLATE utf32_unicode_ci DEFAULT ''
) ENGINE=MyISAM DEFAULT CHARSET=utf32 COLLATE=utf32_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `vidnovoz_cars`
--
ALTER TABLE `vidnovoz_cars`
  ADD PRIMARY KEY (`id_tel`);

--
-- Indexes for table `vidnovoz_routes`
--
ALTER TABLE `vidnovoz_routes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`);

--
-- Indexes for table `vidnovoz_user`
--
ALTER TABLE `vidnovoz_user`
  ADD PRIMARY KEY (`id_tel`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `vidnovoz_routes`
--
ALTER TABLE `vidnovoz_routes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
