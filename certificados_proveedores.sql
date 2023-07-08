-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-04-2023 a las 14:59:10
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `certificados_tributarios`
--
CREATE DATABASE IF NOT EXISTS `certificados_tributarios` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `certificados_tributarios`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administradores`
--

CREATE TABLE `administradores` (
  `Tipo_Doc` varchar(30) NOT NULL,
  `Num_Doc` int(15) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` longblob NOT NULL,
  `Cargo` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documentos`
--

CREATE TABLE `documentos` (
  `Id_Documento` int(20) NOT NULL,
  `Tipo_Doc` varchar(30) NOT NULL,
  `Num_Proveedor` int(15) NOT NULL,
  `Nombre_RazonSocial` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Tipo_Certificado` int(11) NOT NULL,
  `Documento` varchar(70) NOT NULL,
  `Year` year(4) NOT NULL,
  `Num_Solicitudes` int(11) NOT NULL,
  `Fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `Tipo_Doc` varchar(25) NOT NULL,
  `Num_Proveedor` int(15) NOT NULL,
  `Nombre_RazonSocial` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Telefono` varchar(12) NOT NULL,
  `Direccion` varchar(50) NOT NULL,
  `Num_Solicitudes` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `solicitudes`
--

CREATE TABLE `solicitudes` (
  `Id_Solicitud` int(20) NOT NULL,
  `Tipo_Doc` varchar(25) NOT NULL,
  `Num_Proveedor` int(15) NOT NULL,
  `Nombre_RazonSocial` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Id_Documento` int(20) NOT NULL,
  `Documento` varchar(50) NOT NULL,
  `Fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_certificado`
--

CREATE TABLE `tipo_certificado` (
  `Tipo_Certificado` int(11) NOT NULL,
  `Nombre_Certificado` varchar(50) NOT NULL,
  `Fecha` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administradores`
--
ALTER TABLE `administradores`
  ADD PRIMARY KEY (`Num_Doc`);

--
-- Indices de la tabla `documentos`
--
ALTER TABLE `documentos`
  ADD PRIMARY KEY (`Id_Documento`) USING BTREE,
  ADD KEY `Tipo_Doc` (`Tipo_Doc`,`Num_Proveedor`),
  ADD KEY `tipo_certificado` (`Tipo_Certificado`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`Tipo_Doc`,`Num_Proveedor`) USING BTREE,
  ADD KEY `Num_Solicitudes` (`Num_Solicitudes`);

--
-- Indices de la tabla `solicitudes`
--
ALTER TABLE `solicitudes`
  ADD PRIMARY KEY (`Id_Solicitud`),
  ADD KEY `Tipo_Doc` (`Tipo_Doc`,`Num_Proveedor`),
  ADD KEY `Id_Documento` (`Id_Documento`);

--
-- Indices de la tabla `tipo_certificado`
--
ALTER TABLE `tipo_certificado`
  ADD PRIMARY KEY (`Tipo_Certificado`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `documentos`
--
ALTER TABLE `documentos`
  MODIFY `Id_Documento` int(0) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `solicitudes`
--
ALTER TABLE `solicitudes`
  MODIFY `Id_Solicitud` int(0) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_certificado`
--
ALTER TABLE `tipo_certificado`
  MODIFY `Tipo_Certificado` int(0) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `documentos`
--
ALTER TABLE `documentos`
  ADD CONSTRAINT `documentos_ibfk_1` FOREIGN KEY (`Tipo_Doc`,`Num_Proveedor`) REFERENCES `proveedores` (`Tipo_Doc`, `Num_Proveedor`) ON UPDATE CASCADE,
  ADD CONSTRAINT `documentos_ibfk_2` FOREIGN KEY (`Tipo_Certificado`) REFERENCES `tipo_certificado` (`Tipo_Certificado`) ON DELETE NO ACTION ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
