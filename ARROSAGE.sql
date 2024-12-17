-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : dim. 15 déc. 2024 à 14:43
-- Version du serveur : 10.6.18-MariaDB-0ubuntu0.22.04.1
-- Version de PHP : 8.1.2-1ubuntu2.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `ARROSAGE`
--

-- --------------------------------------------------------

--
-- Structure de la table `Event`
--

CREATE TABLE `Event` (
  `id_event` int(11) NOT NULL,
  `eventdate` datetime NOT NULL DEFAULT current_timestamp(),
  `val1` varchar(100) DEFAULT NULL,
  `val2` varchar(100) DEFAULT NULL,
  `val3` varchar(100) DEFAULT NULL,
  `val4` varchar(100) DEFAULT NULL,
  `val5` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `mesure`
--

CREATE TABLE `mesure` (
  `id` int(11) NOT NULL,
  `mesure_ts` timestamp NOT NULL DEFAULT current_timestamp(),
  `mesure` float NOT NULL,
  `id_sensor` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `mesure_last`
--

CREATE TABLE `mesure_last` (
  `id` int(11) NOT NULL,
  `id_sensor` int(11) NOT NULL,
  `mesure` float NOT NULL,
  `mesure_tm` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `mqtt`
--

CREATE TABLE `mqtt` (
  `id_mqtt` int(11) NOT NULL,
  `config_entitie` varchar(30) DEFAULT NULL,
  `config_device` varchar(50) DEFAULT NULL,
  `config_name` varchar(100) DEFAULT NULL,
  `device_identifiers` varchar(200) DEFAULT NULL,
  `device_manufacturer` varchar(200) DEFAULT NULL,
  `device_model` varchar(200) DEFAULT NULL,
  `device_name` varchar(200) DEFAULT NULL,
  `device_configuration_url` varchar(200) DEFAULT NULL,
  `device_sw_version` varchar(10) DEFAULT NULL,
  `device_hw_version` varchar(10) DEFAULT NULL,
  `entity_category` varchar(50) DEFAULT NULL,
  `device_class` varchar(50) DEFAULT NULL,
  `state_class` varchar(50) DEFAULT NULL,
  `object_id` varchar(100) DEFAULT NULL,
  `unique_id` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `availability_topic` varchar(200) DEFAULT NULL,
  `availability_mode` varchar(10) DEFAULT NULL,
  `command_topic` varchar(200) DEFAULT NULL,
  `state_topic` varchar(200) DEFAULT NULL,
  `min` varchar(10) DEFAULT NULL,
  `max` varchar(10) DEFAULT NULL,
  `step` varchar(10) DEFAULT NULL,
  `unit_of_measurement` varchar(10) DEFAULT NULL,
  `options` varchar(300) DEFAULT NULL,
  `optimistic` varchar(10) DEFAULT NULL,
  `retain` varchar(10) DEFAULT NULL,
  `mode` varchar(10) DEFAULT NULL,
  `qos` varchar(2) DEFAULT NULL,
  `payload_on` varchar(10) DEFAULT NULL,
  `payload_off` varchar(10) DEFAULT NULL,
  `payload_open` varchar(10) DEFAULT NULL,
  `payload_close` varchar(10) DEFAULT NULL,
  `payload_stop` varchar(10) DEFAULT NULL,
  `payload_press` varchar(10) DEFAULT NULL,
  `payload_available` varchar(10) DEFAULT NULL,
  `payload_not_available` varchar(10) DEFAULT NULL,
  `state_open` varchar(10) DEFAULT NULL,
  `state_opening` varchar(10) DEFAULT NULL,
  `state_closed` varchar(10) DEFAULT NULL,
  `state_closing` varchar(10) DEFAULT NULL,
  `state_on` varchar(10) DEFAULT NULL,
  `state_off` varchar(10) DEFAULT NULL,
  `reports_position` varchar(100) DEFAULT NULL,
  `active` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Mqtt_Queue`
--

CREATE TABLE `Mqtt_Queue` (
  `id_mqtt_queue` int(11) NOT NULL,
  `topic` varchar(200) NOT NULL,
  `payload` varchar(300) NOT NULL,
  `retain` tinyint(1) NOT NULL,
  `published` int(11) NOT NULL DEFAULT 0,
  `date_ajout` timestamp NOT NULL DEFAULT current_timestamp(),
  `date_publish` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Parameter`
--

CREATE TABLE `Parameter` (
  `id_parameter` int(11) NOT NULL,
  `mode` varchar(20) NOT NULL DEFAULT 'Auto',
  `source` varchar(100) DEFAULT NULL,
  `test` int(11) NOT NULL,
  `duree_test` int(11) NOT NULL,
  `gestion_cuve` int(11) NOT NULL DEFAULT 1,
  `sequence_demande` varchar(10) NOT NULL DEFAULT 'S1',
  `heure_demande` int(11) NOT NULL DEFAULT 0,
  `minute_demande` int(11) NOT NULL DEFAULT 0,
  `coef` int(11) NOT NULL,
  `pression_seuil_bas` float NOT NULL,
  `pression_seuil_haut` float DEFAULT NULL,
  `pression_canal_amont` float NOT NULL,
  `pression_canal_aval` float NOT NULL,
  `pression_cuve_amont` float NOT NULL,
  `pression_cuve_aval` float NOT NULL,
  `pression_ville` float NOT NULL,
  `pression_arrosage` float NOT NULL,
  `debitmetre_cuve` float NOT NULL,
  `debimetre_arrosage` float NOT NULL,
  `test_pression_cuve` int(11) NOT NULL,
  `test_pression_canal` int(11) NOT NULL,
  `test_pression_ville` int(11) NOT NULL,
  `hauteur_eau_cuve` int(11) NOT NULL,
  `test_hauteur_eau_cuve` int(11) NOT NULL,
  `delta_pression_filtre_max` float NOT NULL,
  `nb_cuve_ibc` int(11) NOT NULL,
  `nb_litre_cuve_ibc` int(11) NOT NULL,
  `seuil_min_capacite_cuve` int(11) NOT NULL,
  `seuil_max_capacite_cuve` int(11) NOT NULL,
  `seuil_capacite_remplissage_auto_cuve` int(11) NOT NULL,
  `gestion_pompe_cuve` int(11) NOT NULL DEFAULT 1,
  `gestion_pompe_canal` int(11) NOT NULL DEFAULT 1,
  `auto_coef` int(11) NOT NULL DEFAULT 0,
  `kpi_auto_coef` varchar(20) NOT NULL DEFAULT '90Percentile',
  `nb_max_sv` int(11) NOT NULL DEFAULT 3,
  `verif_nb_max_sv` int(11) NOT NULL DEFAULT 0,
  `precipitation` int(11) NOT NULL DEFAULT 0,
  `verif_seq_hour` int(11) NOT NULL DEFAULT 0,
  `nb_jour_precipitation` int(11) NOT NULL DEFAULT 3,
  `seuil_precipitation` int(11) NOT NULL DEFAULT 5,
  `cumul_precipitation` float NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `sensor`
--

CREATE TABLE `sensor` (
  `id` int(11) NOT NULL,
  `sensor` mediumtext NOT NULL,
  `description` mediumtext NOT NULL,
  `type` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Sequence`
--

CREATE TABLE `Sequence` (
  `seq` varchar(10) NOT NULL,
  `active` int(11) NOT NULL DEFAULT 1,
  `heure` int(11) NOT NULL,
  `minute` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `SequenceZone`
--

CREATE TABLE `SequenceZone` (
  `id_sequence` int(11) NOT NULL,
  `id_sv` int(11) DEFAULT NULL,
  `sv` varchar(10) DEFAULT NULL,
  `sequence` varchar(10) NOT NULL,
  `name` varchar(150) DEFAULT NULL,
  `order` int(11) DEFAULT NULL,
  `open` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `StartingDate` timestamp NULL DEFAULT NULL,
  `EndDate` timestamp NULL DEFAULT NULL,
  `planned` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Zone`
--

CREATE TABLE `Zone` (
  `id_sv` int(11) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'zone',
  `systeme` varchar(30) NOT NULL DEFAULT 'Tuyere',
  `sv` varchar(10) NOT NULL,
  `order` int(11) NOT NULL,
  `gpio` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `open` int(11) NOT NULL,
  `active` int(11) NOT NULL,
  `sequence` varchar(10) NOT NULL DEFAULT 'S1',
  `duration` int(11) NOT NULL,
  `test` int(11) NOT NULL DEFAULT 0,
  `even` int(11) NOT NULL,
  `odd` int(11) NOT NULL DEFAULT 0,
  `monday` int(11) NOT NULL,
  `tuesday` int(11) NOT NULL,
  `wednesday` int(11) NOT NULL,
  `thursday` int(11) NOT NULL,
  `friday` int(11) NOT NULL,
  `saturday` int(11) NOT NULL,
  `sunday` int(11) NOT NULL,
  `coef` int(11) NOT NULL,
  `rpi` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Event`
--
ALTER TABLE `Event`
  ADD PRIMARY KEY (`id_event`),
  ADD KEY `type_evenement` (`val5`);

--
-- Index pour la table `mesure`
--
ALTER TABLE `mesure`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `mesure_last`
--
ALTER TABLE `mesure_last`
  ADD KEY `id` (`id`);

--
-- Index pour la table `mqtt`
--
ALTER TABLE `mqtt`
  ADD PRIMARY KEY (`id_mqtt`);

--
-- Index pour la table `Mqtt_Queue`
--
ALTER TABLE `Mqtt_Queue`
  ADD PRIMARY KEY (`id_mqtt_queue`);

--
-- Index pour la table `Parameter`
--
ALTER TABLE `Parameter`
  ADD PRIMARY KEY (`id_parameter`);

--
-- Index pour la table `sensor`
--
ALTER TABLE `sensor`
  ADD UNIQUE KEY `id` (`id`);

--
-- Index pour la table `SequenceZone`
--
ALTER TABLE `SequenceZone`
  ADD KEY `ix_Sequence` (`id_sequence`) USING BTREE;

--
-- Index pour la table `Zone`
--
ALTER TABLE `Zone`
  ADD PRIMARY KEY (`id_sv`),
  ADD UNIQUE KEY `sv` (`sv`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Event`
--
ALTER TABLE `Event`
  MODIFY `id_event` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `mesure`
--
ALTER TABLE `mesure`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `mesure_last`
--
ALTER TABLE `mesure_last`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Mqtt_Queue`
--
ALTER TABLE `Mqtt_Queue`
  MODIFY `id_mqtt_queue` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Parameter`
--
ALTER TABLE `Parameter`
  MODIFY `id_parameter` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `sensor`
--
ALTER TABLE `sensor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `SequenceZone`
--
ALTER TABLE `SequenceZone`
  MODIFY `id_sequence` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `Zone`
--
ALTER TABLE `Zone`
  MODIFY `id_sv` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
