-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-08-2025 a las 06:36:05
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `control_vacunas_v2`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `niños`
--

CREATE TABLE `niños` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido_paterno` varchar(50) NOT NULL,
  `apellido_materno` varchar(50) NOT NULL,
  `fecha_nacimiento` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `niños`
--

INSERT INTO `niños` (`id`, `nombre`, `apellido_paterno`, `apellido_materno`, `fecha_nacimiento`) VALUES
(1, 'Mateo', 'Quispe', 'Mendoza', '2024-01-15'),
(2, 'Sofia', 'Mamani', 'Rojas', '2023-11-20'),
(3, 'Sebastian', 'Cruz', 'Vargas', '2024-03-10'),
(4, 'Camila', 'Choque', 'Gutiérrez', '2023-09-05');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personal_vacunador`
--

CREATE TABLE `personal_vacunador` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `rol` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `personal_vacunador`
--

INSERT INTO `personal_vacunador` (`id`, `nombre`, `rol`) VALUES
(1, 'Lic. Maria Elena Morales', 'Enfermera'),
(2, 'Dr. Carlos Fernando López', 'Pediatra'),
(3, 'Lic. Juan Pablo Durán', 'Enfermero');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `responsables`
--

CREATE TABLE `responsables` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `carnet_identidad` varchar(20) NOT NULL,
  `celular` varchar(15) DEFAULT NULL,
  `parentesco` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `responsables`
--

INSERT INTO `responsables` (`id`, `nombre`, `carnet_identidad`, `celular`, `parentesco`) VALUES
(1, 'Ana Laura Rojas', '9876543 CB', '77788899', 'Madre'),
(2, 'Jorge Luis Poma', '8765432 LP', '65432109', 'Padre'),
(3, 'Carla Andrea Villarroel', '7654321 SC', '71234567', 'Tía'),
(4, 'Mario Alejandro Quispe', '6543210 CH', '79876543', 'Padre');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipos_vacuna`
--

CREATE TABLE `tipos_vacuna` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipos_vacuna`
--

INSERT INTO `tipos_vacuna` (`id`, `nombre`) VALUES
(1, 'BCG'),
(11, 'DPT'),
(9, 'Fiebre amarilla'),
(2, 'Hepatitis'),
(7, 'Influenza'),
(5, 'Neumococo'),
(3, 'Pentavalente'),
(4, 'Polio'),
(6, 'Rotavirus'),
(8, 'SRP'),
(10, 'Varicela');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vacunas_aplicadas`
--

CREATE TABLE `vacunas_aplicadas` (
  `id` int(11) NOT NULL,
  `id_niño` int(11) NOT NULL,
  `id_responsable` int(11) NOT NULL,
  `id_vacuna` int(11) NOT NULL,
  `id_personal` int(11) NOT NULL,
  `fecha_aplicacion` date NOT NULL,
  `dosis` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vacunas_aplicadas`
--

INSERT INTO `vacunas_aplicadas` (`id`, `id_niño`, `id_responsable`, `id_vacuna`, `id_personal`, `fecha_aplicacion`, `dosis`) VALUES
(1, 1, 4, 1, 1, '2024-02-15', 1),
(2, 2, 1, 2, 2, '2023-12-25', 1),
(3, 3, 2, 3, 3, '2024-04-10', 1),
(4, 4, 3, 2, 1, '2023-10-05', 1),
(6, 1, 4, 2, 1, '2024-03-15', 1),
(7, 2, 1, 6, 3, '2024-01-20', 1),
(8, 3, 2, 7, 2, '2024-04-25', 1),
(9, 4, 1, 6, 2, '2025-08-22', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `niños`
--
ALTER TABLE `niños`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `personal_vacunador`
--
ALTER TABLE `personal_vacunador`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `responsables`
--
ALTER TABLE `responsables`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `carnet_identidad` (`carnet_identidad`);

--
-- Indices de la tabla `tipos_vacuna`
--
ALTER TABLE `tipos_vacuna`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `vacunas_aplicadas`
--
ALTER TABLE `vacunas_aplicadas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_niño` (`id_niño`),
  ADD KEY `id_responsable` (`id_responsable`),
  ADD KEY `id_vacuna` (`id_vacuna`),
  ADD KEY `id_personal` (`id_personal`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `niños`
--
ALTER TABLE `niños`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `personal_vacunador`
--
ALTER TABLE `personal_vacunador`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `responsables`
--
ALTER TABLE `responsables`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `tipos_vacuna`
--
ALTER TABLE `tipos_vacuna`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `vacunas_aplicadas`
--
ALTER TABLE `vacunas_aplicadas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `vacunas_aplicadas`
--
ALTER TABLE `vacunas_aplicadas`
  ADD CONSTRAINT `vacunas_aplicadas_ibfk_1` FOREIGN KEY (`id_niño`) REFERENCES `niños` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `vacunas_aplicadas_ibfk_2` FOREIGN KEY (`id_responsable`) REFERENCES `responsables` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `vacunas_aplicadas_ibfk_3` FOREIGN KEY (`id_vacuna`) REFERENCES `tipos_vacuna` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `vacunas_aplicadas_ibfk_4` FOREIGN KEY (`id_personal`) REFERENCES `personal_vacunador` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
