-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : sam. 17 déc. 2022 à 22:03
-- Version du serveur : 10.4.24-MariaDB
-- Version de PHP : 7.1.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `bdplanning`
--

-- --------------------------------------------------------

--
-- Structure de la table `groupe_salle`
--

CREATE TABLE `groupe_salle` (
  `id_groupe` int(11) NOT NULL,
  `nom_groupe` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `groupe_salle`
--

INSERT INTO `groupe_salle` (`id_groupe`, `nom_groupe`) VALUES
(1, 'ENSIBS'),
(2, 'DSEG'),
(3, 'LORIENT');

-- --------------------------------------------------------

--
-- Structure de la table `relation_groupe_salle`
--

CREATE TABLE `relation_groupe_salle` (
  `id_groupe_salle` int(11) NOT NULL,
  `id_salle` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `relation_groupe_salle`
--

INSERT INTO `relation_groupe_salle` (`id_groupe_salle`, `id_salle`) VALUES
(1, 176),
(1, 157),
(1, 158),
(1, 159),
(2, 1),
(2, 2),
(2, 11),
(3, 21),
(3, 22),
(3, 24),
(2, 12),
(2, 4),
(2, 5),
(1, 1),
(1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `salle`
--

CREATE TABLE `salle` (
  `id_salle` int(11) NOT NULL,
  `nom` text NOT NULL,
  `tauxAlerte` int(11) NOT NULL DEFAULT 50
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `salle`
--

INSERT INTO `salle` (`id_salle`, `nom`, `tauxAlerte`) VALUES
(1, 'A 101 V-DSEG (100)', 50),
(2, 'A 102 V-DSEG (100)', 32),
(3, 'EAD-2D1', 0),
(4, 'S 202 V-DSEG (30)', 0),
(5, 'S 209 V-DSEG (30)', 0),
(6, 'S 315 V-DSEG (40)', 0),
(7, 'V-B 414', 0),
(8, 'V-B 020', 0),
(9, 'V-B 216', 0),
(10, '', 0),
(11, 'A 103 V-DSEG (100)', 0),
(12, 'A 104 V-DSEG (3è etage) (100)', 0),
(13, 'A 150 V-DSEG (150)', 0),
(14, 'A 250 V-DSEG (250)', 0),
(15, 'A 500 V-DSEG (500)', 0),
(16, 'Amphi Joker 1', 0),
(17, 'Amphi joker 2', 0),
(18, 'Hall 1er étage DSEG', 0),
(19, 'Hall Rez de chaussée DSEG', 0),
(20, 'Joker Info 1 GEA', 0),
(21, 'L-ENSIBS- S 105 Multimedia (20)', 0),
(22, 'L-ENSIBS- S 303 Réunion : visio (12)', 0),
(23, 'L-ENSIBS- S 304 Réunion (12)', 0),
(24, 'L-ENSIBS- S 401 Conseil : visio (24)', 0),
(25, 'Moodle/Teams/Via', 0),
(26, 'NEGO', 0),
(27, 'S 203 V-DSEG (30)', 0),
(28, 'S 204 V-DSEG (50)', 0),
(29, 'S 205 V-DSEG (56)', 0),
(30, 'S 206 V-DSEG (30)', 0),
(31, 'S 207 V-DSEG (54)', 0),
(32, 'S 208 V-DSEG (54)', 0),
(33, 'S 210 V-DSEG (39)', 0),
(34, 'S 211 V-DSEG (80)', 0),
(35, 'S 212U V-DSEG (30)', 0),
(36, 'S 213 V-DSEG (30)', 0),
(37, 'S 214 V-DSEG (32)', 0),
(38, 'S 215 V-DSEG (40)', 0),
(39, 'S 216 V-DSEG (30)', 0),
(40, 'S 301 V-DSEG (30)', 0),
(41, 'S 302 V-DSEG (59)', 0),
(42, 'S 303 V-DSEG (56)', 0),
(43, 'S 305 V-DSEG (50)', 0),
(44, 'S 307 V-DSEG (46)', 0),
(45, 'S 308 V-DSEG (46)', 0),
(46, 'S 309 V-DSEG (30) Réservée ENSIBS', 0),
(47, 'S 310 V-DSEG (30) Réservée ENSIBS', 0),
(48, 'S 311 V-DSEG (46)', 0),
(49, 'S 312 V-DSEG (46)', 0),
(50, 'S 313 V-DSEG (54)', 0),
(51, 'S 314 V-DSEG (52)', 0),
(52, 'S 316 V-DSEG (40)', 0),
(53, 'Salle fictive', 0),
(54, 'Salle non réservée', 0),
(55, 'TD', 0),
(56, 'Teams', 0),
(57, 'V-A joker', 0),
(58, 'V-A010', 0),
(59, 'V-A012', 0),
(60, 'V-A016', 0),
(61, 'V-A106 (IUP Tohannic )', 0),
(62, 'V-Amphi A', 0),
(63, 'V-Amphi B', 0),
(64, 'V-Amphi B (Info)', 0),
(65, 'V-Amphi C', 0),
(66, 'V-B 003', 0),
(67, 'V-B 005', 0),
(68, 'V-B 015', 0),
(69, 'V-B 017', 0),
(70, 'V-B 018', 0),
(71, 'V-B 022', 0),
(72, 'V-B 024', 0),
(73, 'V-B 025', 0),
(74, 'V-B 027', 0),
(75, 'V-B 028', 0),
(76, 'V-B 029', 0),
(77, 'V-B 030', 0),
(78, 'V-B 035', 0),
(79, 'V-B 037', 0),
(80, 'V-B 118', 0),
(81, 'V-B 120', 0),
(82, 'V-B 121', 0),
(83, 'V-B 122', 0),
(84, 'V-B 124', 0),
(85, 'V-B 126', 0),
(86, 'V-B 141', 0),
(87, 'V-B 145', 0),
(88, 'V-B 201', 0),
(89, 'V-B 201 bis', 0),
(90, 'V-B 202', 0),
(91, 'V-B 203', 0),
(92, 'V-B 204', 0),
(93, 'V-B 205', 0),
(94, 'V-B 207', 0),
(95, 'V-B 209', 0),
(96, 'V-B 214', 0),
(97, 'V-B 301', 0),
(98, 'V-B 302', 0),
(99, 'V-B 303', 0),
(100, 'V-B 304', 0),
(101, 'V-B 305', 0),
(102, 'V-B 307', 0),
(103, 'V-B 309', 0),
(104, 'V-B 311', 0),
(105, 'V-B 314', 0),
(106, 'V-B 316', 0),
(107, 'V-B 401', 0),
(108, 'V-B 402', 0),
(109, 'V-B 403', 0),
(110, 'V-B 404', 0),
(111, 'V-B 405', 0),
(112, 'V-B 407', 0),
(113, 'V-B 409', 0),
(114, 'V-B 411', 0),
(115, 'V-B 416', 0),
(116, 'V-B joker', 0),
(117, 'V-B-Joker 1', 0),
(118, 'V-B-Joker 2', 0),
(119, 'V-B-Joker 3', 0),
(120, 'V-BU', 0),
(121, 'V-I-Joker 1', 0),
(122, 'V-I-Joker 2', 0),
(123, 'V-I-Joker 3', 0),
(124, 'V-I-Joker 4', 0),
(125, 'V-Info Jok tc1', 0),
(126, 'V-Info Jok tc2', 0),
(127, 'V-Info Jok tc3', 0),
(128, 'V-JOK TC n°1', 0),
(129, 'V-JOK TC n°2', 0),
(130, 'V-Jocker 1 LP', 0),
(131, 'V-Jocker 2 LP', 0),
(132, 'V-Jocker Info 2', 0),
(133, 'V-Jocker-info 1', 0),
(134, 'V-Joker 01', 0),
(135, 'V-Joker 02', 0),
(136, 'V-Joker 03', 0),
(137, 'V-Joker 04', 0),
(138, 'V-Joker 05', 0),
(139, 'V-Joker 06', 0),
(140, 'V-Joker 07', 0),
(141, 'V-Joker 08', 0),
(142, 'V-Joker 09', 0),
(143, 'V-Joker 1', 0),
(144, 'V-Joker 10', 0),
(145, 'V-Joker 11', 0),
(146, 'V-Joker 12', 0),
(147, 'V-Joker 13', 0),
(148, 'V-Joker 14', 0),
(149, 'V-Joker 15', 0),
(150, 'V-Joker 16', 0),
(151, 'V-Joker 17', 0),
(152, 'V-Joker 2', 0),
(153, 'V-Joker 3', 0),
(154, 'V-Joker 4', 0),
(155, 'V-Phoning 314 bis', 0),
(156, 'V-TO-BU-SCD', 0),
(157, 'V-TO-ENSIBS - A102 (TBI) (30)', 0),
(158, 'V-TO-ENSIBS - A103 (30)', 0),
(159, 'V-TO-ENSIBS - A104 (30)', 0),
(160, 'V-TO-ENSIBS - A105-107 (60)', 0),
(161, 'V-TO-ENSIBS - A106 (30)', 0),
(162, 'V-TO-ENSIBS - B001 amphi (250)', 0),
(163, 'V-TO-ENSIBS - B002 (C4-Pro)', 0),
(164, 'V-TO-ENSIBS - B003', 0),
(165, 'V-TO-ENSIBS - C4', 0),
(166, 'V-TO-ENSIBS - D001 (30)', 0),
(167, 'V-TO-ENSIBS - D003 (30)', 0),
(168, 'V-TO-ENSIBS - D005 (42)', 0),
(169, 'V-TO-ENSIBS - D009 (42)', 0),
(170, 'V-TO-ENSIBS - D010 (90)', 0),
(171, 'V-TO-ENSIBS - D101 (26)', 0),
(172, 'V-TO-ENSIBS - D105 (28)', 0),
(173, 'V-TO-ENSIBS - D107 (VirtualLab-AIDN) (26)', 0),
(174, 'V-TO-ENSIBS - D111 (CyberLab-SAIM) (26)', 0),
(175, 'V-TO-ENSIBS - D113 (28)', 0),
(176, 'V-TO-ENSIBS - Grande Salle Virtuelle', 0),
(177, 'V-TO-ENSIBS - Info-TMP', 0),
(178, 'V-TO-ENSIBS - Salle Info Virtuelle', 0),
(179, 'V-TO-ENSIBS - Salle TD Virtuelle', 0),
(180, 'V-TO-ENSIBS - TD-TMP', 0),
(181, 'V-TO-YC-A104', 0),
(182, 'V-TO-YC-AMPHI (150)', 0),
(183, 'V-TO-YC-D070 (40)', 0),
(184, 'V-TO-YC-D071 (IGREC) (26)', 0),
(185, 'V-TO-YC-D072 (32)', 0),
(186, 'V-TO-YC-D073 (IGREC) (18)', 0),
(187, 'V-TO-YC-D074 (52)', 0),
(188, 'V-TO-YC-D075 (56)', 0),
(189, 'V-TO-YC-D076 (62)', 0),
(190, 'V-TO-YC-D077-VBI (64)', 0),
(191, 'V-TO-YC-D079-TBI (56)', 0),
(192, 'V-TO-YC-D170 (21)', 0),
(193, 'V-TO-YC-D171 (21)', 0),
(194, 'V-TO-YC-D172 (21)', 0),
(195, 'V-TO-YC-D173 (21)', 0),
(196, 'V-TO-YC-D174 (50)', 0),
(197, 'V-TO-YC-D176 (40)', 0),
(198, 'V-TO-YC-D177', 0),
(199, 'V-TO-YC-E081', 0),
(200, 'V-TO-YC-E083', 0),
(201, 'V-TO-YC-E084', 0),
(202, 'V-TO-YC-E181D', 0),
(203, 'V-TO-YC-E182', 0),
(204, 'V-TO-YC-E184', 0),
(205, 'V-TO-YC-E187', 0),
(206, 'V-TO-YC-F092', 0),
(207, 'V-TO-YC-F097', 0),
(208, 'V-TO-YC-F191 (langues) (21)', 0),
(209, 'V-TO-YC-F193 (langues) (21)', 0),
(210, 'V-TO-YC-F195 (21)', 0),
(211, 'Y-TO-ENSIBS - D106 (14)', 0),
(212, 'salle joker à distance', 0),
(213, 'L-ENSIBS- S 302 (20)', 0);

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `id_user` int(11) NOT NULL,
  `nom_user` text NOT NULL,
  `prenom_user` text NOT NULL,
  `role` enum('lecteur','superviseur','administrateur') NOT NULL DEFAULT 'lecteur',
  `mail` text NOT NULL,
  `n_etudiant` text NOT NULL,
  `Acontacter` enum('oui','non') NOT NULL DEFAULT 'oui'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`id_user`, `nom_user`, `prenom_user`, `role`, `mail`, `n_etudiant`, `Acontacter`) VALUES
(1, 'horlaville', 'pierre', 'administrateur', 'horlaville.e0000003@univ-ubs.fr', 'e0000003', 'oui'),
(2, 'hidoux', 'cassio', 'superviseur', 'hidoux.e0000001@etud.univ-ubs.fr', 'e0000001', 'oui'),
(14, 'chap', 'lucas', 'lecteur', 'chap.e0000002@etud.univ-ubs.fr', 'e0000002', 'non'),
(15, 'cay', 'vincent', 'lecteur', 'cay.e0000004@etud.univ-ubs.fr', 'e0000004', 'non');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `groupe_salle`
--
ALTER TABLE `groupe_salle`
  ADD PRIMARY KEY (`id_groupe`);

--
-- Index pour la table `relation_groupe_salle`
--
ALTER TABLE `relation_groupe_salle`
  ADD KEY `id_groupe_salle` (`id_groupe_salle`),
  ADD KEY `id_salle` (`id_salle`);

--
-- Index pour la table `salle`
--
ALTER TABLE `salle`
  ADD PRIMARY KEY (`id_salle`);

--
-- Index pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `groupe_salle`
--
ALTER TABLE `groupe_salle`
  MODIFY `id_groupe` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT pour la table `salle`
--
ALTER TABLE `salle`
  MODIFY `id_salle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=214;

--
-- AUTO_INCREMENT pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `relation_groupe_salle`
--
ALTER TABLE `relation_groupe_salle`
  ADD CONSTRAINT `id_groupe_salle` FOREIGN KEY (`id_groupe_salle`) REFERENCES `groupe_salle` (`id_groupe`),
  ADD CONSTRAINT `id_salle` FOREIGN KEY (`id_salle`) REFERENCES `salle` (`id_salle`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
