-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mar. 18 mars 2025 à 04:12
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `universite`
--

-- --------------------------------------------------------

--
-- Structure de la table `annee_academique`
--

CREATE TABLE `annee_academique` (
  `id` int(11) NOT NULL,
  `annee` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `annee_academique`
--

INSERT INTO `annee_academique` (`id`, `annee`) VALUES
(1, '2023-2024'),
(2, '2024-2025');

-- --------------------------------------------------------

--
-- Structure de la table `annee_etude`
--

CREATE TABLE `annee_etude` (
  `id` int(11) NOT NULL,
  `code` varchar(20) NOT NULL,
  `niveau` int(11) NOT NULL,
  `filiere_id` int(11) DEFAULT NULL,
  `grade_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `annee_etude`
--

INSERT INTO `annee_etude` (`id`, `code`, `niveau`, `filiere_id`, `grade_id`) VALUES
(1, 'GL_Licence_1', 1, 1, 1),
(2, 'GL_Licence_2', 2, 1, 1),
(3, 'GL_Licence_3', 3, 1, 1),
(4, 'GL_Master_1', 1, 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `ecue`
--

CREATE TABLE `ecue` (
  `id` int(11) NOT NULL,
  `code` varchar(100) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `ue_id` int(11) DEFAULT NULL,
  `enseignant_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `ecue`
--

INSERT INTO `ecue` (`id`, `code`, `nom`, `ue_id`, `enseignant_id`) VALUES
(10, 'EC101', 'Algèbre Linéaire', 1, 1),
(11, 'EC102', 'Analyse Mathématique', 1, 1),
(12, 'EC103', 'Programmation C', 2, 5),
(13, 'EC104', 'Structures de Données', 2, 5),
(14, 'EC105', 'Introduction à la Microéconomie', 3, 6),
(15, 'EC106', 'Mécanique Générale', 4, 2),
(16, 'EC107', 'Optique Géométrique', 4, 2),
(17, 'EC108', 'Statistiques Descriptives', 5, 6),
(18, 'EC109', 'Expression Écrite et Orale', 6, 8),
(19, 'EC201', 'Modélisation des BD', 7, 5),
(20, 'EC202', 'SQL et Normalisation', 7, 5),
(21, 'EC203', 'Équations Différentielles', 8, 1),
(22, 'EC204', 'Comptabilité Analytique', 9, 6),
(23, 'EC205', 'Circuits Logiques', 10, 2),
(24, 'EC206', 'Introduction au Droit', 11, 7),
(25, 'EC207', 'Anglais Professionnel', 12, 8),
(26, 'EC301', 'Méthodologie UML', 13, 5),
(27, 'EC302', 'Programmation Objet', 13, 5),
(28, 'EC303', 'Architecture Réseaux', 14, 5),
(29, 'EC304', 'Économie Monétaire', 15, 6),
(30, 'EC305', 'Systèmes UNIX/Linux', 16, 5),
(31, 'EC306', 'Tests Statistiques', 17, 1),
(32, 'EC307', 'Négociation et Leadership', 18, 9),
(33, 'EC401', 'Machine Learning', 19, 5),
(34, 'EC402', 'Réseaux Sécurisés', 20, 5),
(35, 'EC403', 'Gestion Agile', 21, 6),
(36, 'EC404', 'Cryptanalyse', 22, 5),
(37, 'EC405', 'E-Commerce et Digitalisation', 23, 6),
(38, 'EC406', 'Frameworks JS (React, Vue)', 24, 5),
(39, 'EC501', 'Data Mining', 25, 5),
(40, 'EC502', 'Virtualisation', 26, 5),
(41, 'EC503', 'Administration Systèmes', 27, 5),
(42, 'EC504', 'Droit Numérique', 28, 7),
(43, 'EC505', 'Audit Financier', 29, 6),
(44, 'EC506', 'Business Model Canvas', 30, 9),
(45, 'EC601', 'Smart Contracts', 31, 5),
(46, 'EC602', 'Sécurité Offensive', 32, 5),
(47, 'EC603', 'Innovation Technologique', 33, 5),
(48, 'EC604', 'Éthique et Vie Privée', 34, 10),
(49, 'EC605', 'Marketing Digital', 35, 6),
(50, 'EC606', 'Rédaction du Mémoire', 36, 8);

-- --------------------------------------------------------

--
-- Structure de la table `enseignant`
--

CREATE TABLE `enseignant` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telephone` varchar(15) DEFAULT NULL,
  `specialite` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `enseignant`
--

INSERT INTO `enseignant` (`id`, `nom`, `prenom`, `email`, `telephone`, `specialite`) VALUES
(1, 'ADJOVI', 'Jean', 'jean.adjovi@example.com', '22961000001', 'Mathématiques Appliquées'),
(2, 'HOUNGBÉDJI', 'Alice', 'alice.houngbedji@example.com', '22961000002', 'Physique Quantique'),
(3, 'TOSSOU', 'Bernard', 'bernard.tossou@example.com', '22961000003', 'Chimie Organique'),
(4, 'GNACADJA', 'Clémentine', 'clementine.gnacadja@example.com', '22961000004', 'Biologie Moléculaire'),
(5, 'AGOSSOU', 'David', 'david.agossou@example.com', '22961000005', 'Intelligence Artificielle'),
(6, 'ZINSOU', 'Estelle', 'estelle.zinsou@example.com', '22961000006', 'Économie et Finance'),
(7, 'AHOLLOU', 'Franck', 'franck.ahollou@example.com', '22961000007', 'Droit International'),
(8, 'GUÉDÉGBÉ', 'Grace', 'grace.guedegbe@example.com', '22961000008', 'Histoire des Civilisations'),
(9, 'AVOCÈ', 'Henri', 'henri.avoce@example.com', '22961000009', 'Philosophie Politique'),
(10, 'HOUNKPATI', 'Isabelle', 'isabelle.hounkpati@example.com', '22961000010', 'Sociologie du Développement');

-- --------------------------------------------------------

--
-- Structure de la table `etudiant`
--

CREATE TABLE `etudiant` (
  `matricule` varchar(20) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `date_naissance` date NOT NULL,
  `sexe` enum('M','F') NOT NULL,
  `email` varchar(100) NOT NULL,
  `telephone` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `etudiant`
--

INSERT INTO `etudiant` (`matricule`, `nom`, `prenom`, `date_naissance`, `sexe`, `email`, `telephone`) VALUES
('10012345', 'DIARRA', 'Chloé Marie', '2001-10-30', 'F', 'chloe.diara@gmail.com', '+229 0102030406'),
('10012398', 'SISSE', 'Léa Mariama', '2000-08-19', 'F', 'lea.sisse@gmail.com', '+229 0203040508'),
('10012399', 'DAOUDA', 'Sarah Mariame', '1999-06-08', 'F', 'sarah.daouda@gmail.com', '+229 0304050610'),
('10120400', 'MALIK', 'François Kader', '1999-09-24', 'M', 'francois.malik@gmail.com', '+229 0304050609'),
('10123400', 'FOFANA', 'Nicolas Michel', '2000-11-04', 'M', 'nicolas.fofana@gmail.com', '+229 0203040507'),
('10123456', 'KOUASSI', 'Jean Pierre', '2000-01-15', 'M', 'jean.kouassi@gmail.com', '+229 0102030405'),
('10234510', 'TRAORE', 'Marie Claire', '1999-12-09', 'F', 'marie.traore@gmail.com', '+229 0304050608'),
('10234511', 'DIABATE', 'Alice Binta', '2001-10-29', 'F', 'alice.diabate@gmail.com', '+229 0405060710'),
('10234567', 'ADJAHO', 'Sophie Marguerite', '2000-02-20', 'F', 'sophie.adjaho@gmail.com', '+229 0203040506'),
('10345621', 'TOURE', 'Antoine Kouadio', '2000-01-14', 'M', 'antoine.toure@gmail.com', '+229 0405060709'),
('10345622', 'KATENDE', 'Louis Kalifa', '2000-11-03', 'M', 'louis.katende@gmail.com', '+229 0506070811'),
('10345678', 'DIOP', 'Pierre Alain', '1999-03-25', 'M', 'pierre.diop@gmail.com', '+229 0304050607'),
('10456732', 'KONE', 'Laura Salima', '2000-02-19', 'F', 'laura.kone@gmail.com', '+229 0506070810'),
('10456733', 'KIMBA', 'Camille Kadiatu', '1999-12-08', 'F', 'camille.kimba@gmail.com', '+229 0607080912'),
('10456789', 'NGUESSAN', 'Claire Mélanie', '2001-04-30', 'F', 'claire.nguessan@gmail.com', '+229 0405060708'),
('10567843', 'OUEDRAOGO', 'Alexandre Moussa', '1999-03-24', 'M', 'alexandre.ouedraogo@gmail.com', '+229 0607080911'),
('10567844', 'FENI', 'Etienne Saliou', '2000-01-13', 'M', 'etienne.feni@gmail.com', '+229 0708091013'),
('10567890', 'KAMARA', 'Lucas Antoine', '2000-05-05', 'M', 'lucas.kamara@gmail.com', '+229 0506070809'),
('10678901', 'MBOGO', 'Emma Nadia', '1999-06-10', 'F', 'emma.mbogo@gmail.com', '+229 0607080910'),
('10678954', 'SANOGO', 'Justine Mamou', '2001-04-29', 'F', 'justine.sanogo@gmail.com', '+229 0708091012'),
('10678955', 'TRAORE', 'Élodie Souad', '2000-02-18', 'F', 'elodie.traore@gmail.com', '+229 0809101114'),
('10789012', 'SOW', 'Thomas Benjamin', '2000-07-15', 'M', 'thomas.sow@gmail.com', '+229 0708091011'),
('10789065', 'COULIBALY', 'Martin Mahmoud', '2000-05-04', 'M', 'martin.coulibaly@gmail.com', '+229 0809101113'),
('10789066', 'KOUYATE', 'Maxime Kamal', '1999-03-23', 'M', 'maxime.kouyate@gmail.com', '+229 0901011123'),
('10890123', 'SACKO', 'Alice Rose', '2000-08-20', 'F', 'alice.sacko@gmail.com', '+229 0809101112'),
('10890176', 'N’DIAYE', 'Juliette Rama', '1999-06-09', 'F', 'juliette.ndiaye@gmail.com', '+229 0901011122'),
('10890177', 'YAO', 'Lucie Sanou', '2001-04-28', 'F', 'lucie.yao@gmail.com', '+229 0102030408'),
('10901234', 'KOUADIO', 'Julien Laurent', '1999-09-25', 'M', 'julien.kouadio@gmail.com', '+229 0901011121'),
('10901287', 'BA', 'Victor Koulibaly', '2000-07-14', 'M', 'victor.ba@gmail.com', '+229 0102030407'),
('10901288', 'TAPSOBA', 'Olivier Diaby', '2000-05-03', 'M', 'olivier.tapsoba@gmail.com', '+229 0203040509');

-- --------------------------------------------------------

--
-- Structure de la table `filiere`
--

CREATE TABLE `filiere` (
  `id` int(11) NOT NULL,
  `code` varchar(100) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `mention` varchar(100) DEFAULT NULL,
  `domaine` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `filiere`
--

INSERT INTO `filiere` (`id`, `code`, `nom`, `mention`, `domaine`) VALUES
(1, 'GL', 'Génie Logiciel', 'Informatique', 'Science et Technologie'),
(2, 'SI', 'Sécurité Informatique', 'Informatique', 'Science et Technologie'),
(3, 'IM', 'Internet et Multimédia', 'Informatique', 'Science et Technologie');

-- --------------------------------------------------------

--
-- Structure de la table `grade`
--

CREATE TABLE `grade` (
  `id` int(11) NOT NULL,
  `nom` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `grade`
--

INSERT INTO `grade` (`id`, `nom`) VALUES
(1, 'Licence'),
(2, 'Master');

-- --------------------------------------------------------

--
-- Structure de la table `membre_administratif`
--

CREATE TABLE `membre_administratif` (
  `id` int(11) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `role` enum('Admin','Secrétaire','Enseignant') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `membre_administratif`
--

INSERT INTO `membre_administratif` (`id`, `nom`, `prenom`, `email`, `mot_de_passe`, `role`) VALUES
(1, 'DJEGO', 'Marie-Julio', 'mariejuliobricedjego@gmail.com', '$2b$12$gj9thKNn5M1W7Gc1LuBNX.rVKfXh2bsYurn7tN8It3/yMT.3/RLwW', 'Admin');

-- --------------------------------------------------------

--
-- Structure de la table `moyenne_ue`
--

CREATE TABLE `moyenne_ue` (
  `id` int(11) NOT NULL,
  `etudiant_matricule` varchar(20) DEFAULT NULL,
  `ue_id` int(11) DEFAULT NULL,
  `annee_academique_id` int(11) DEFAULT NULL,
  `moyenne` decimal(5,2) DEFAULT NULL CHECK (`moyenne` between 0 and 20),
  `verdict` enum('Validé','Non validé') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `note`
--

CREATE TABLE `note` (
  `id` int(11) NOT NULL,
  `ecue_id` int(11) DEFAULT NULL,
  `parcours_etudiant_id` int(11) DEFAULT NULL,
  `note` decimal(5,2) DEFAULT NULL CHECK (`note` between 0 and 20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `parcours_etudiant`
--

CREATE TABLE `parcours_etudiant` (
  `id` int(11) NOT NULL,
  `etudiant_matricule` varchar(20) DEFAULT NULL,
  `annee_etude_id` int(11) DEFAULT NULL,
  `annee_academique_id` int(11) DEFAULT NULL,
  `decision` enum('Admis','Redoublant','Enjambement') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `parcours_etudiant`
--

INSERT INTO `parcours_etudiant` (`id`, `etudiant_matricule`, `annee_etude_id`, `annee_academique_id`, `decision`) VALUES
(1, '10012345', 1, 1, 'Redoublant'),
(2, '10012398', 1, 1, 'Admis'),
(3, '10012399', 2, 1, 'Admis'),
(4, '10120400', 3, 1, 'Redoublant'),
(5, '10123400', 1, 1, 'Admis'),
(6, '10123456', 1, 1, 'Enjambement'),
(7, '10012398', 1, 2, 'Admis'),
(8, '10012399', 2, 2, 'Enjambement'),
(9, '10123400', 1, 2, 'Admis'),
(10, '10123456', 1, 2, 'Admis');

-- --------------------------------------------------------

--
-- Structure de la table `ue`
--

CREATE TABLE `ue` (
  `id` int(11) NOT NULL,
  `code` varchar(100) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `annee_etude_id` int(11) DEFAULT NULL,
  `coefficient` int(11) NOT NULL,
  `semestre` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `ue`
--

INSERT INTO `ue` (`id`, `code`, `nom`, `annee_etude_id`, `coefficient`, `semestre`) VALUES
(1, 'UE101', 'Mathématiques fondamentales', 1, 6, 1),
(2, 'UE102', 'Programmation et Algorithmique', 1, 5, 1),
(3, 'UE103', 'Économie Générale', 1, 4, 1),
(4, 'UE104', 'Physique appliquée', 1, 5, 1),
(5, 'UE105', 'Statistiques', 1, 5, 1),
(6, 'UE106', 'Expression et Communication', 1, 5, 1),
(7, 'UE201', 'Bases de Données', 1, 6, 2),
(8, 'UE202', 'Analyse et Algèbre', 1, 5, 2),
(9, 'UE203', 'Comptabilité Générale', 1, 4, 2),
(10, 'UE204', 'Électronique Numérique', 1, 5, 2),
(11, 'UE205', 'Droit des Affaires', 1, 5, 2),
(12, 'UE206', 'Anglais Technique', 1, 5, 2),
(13, 'UE301', 'Génie Logiciel', 2, 5, 1),
(14, 'UE302', 'Réseaux Informatiques', 2, 5, 1),
(15, 'UE303', 'Microéconomie', 2, 5, 1),
(16, 'UE304', 'Systèmes d’Exploitation', 2, 5, 1),
(17, 'UE305', 'Méthodes Statistiques', 2, 5, 1),
(18, 'UE306', 'Techniques de Communication', 2, 5, 1),
(19, 'UE401', 'Intelligence Artificielle', 2, 6, 2),
(20, 'UE402', 'Sécurité Informatique', 2, 5, 2),
(21, 'UE403', 'Gestion de Projet', 2, 4, 2),
(22, 'UE404', 'Cryptographie', 2, 5, 2),
(23, 'UE405', 'Économie Numérique', 2, 5, 2),
(24, 'UE406', 'Développement Web Avancé', 2, 5, 2),
(25, 'UE501', 'Big Data', 3, 6, 1),
(26, 'UE502', 'Cloud Computing', 3, 5, 1),
(27, 'UE503', 'Management des Systèmes', 3, 5, 1),
(28, 'UE504', 'Droit de l’Informatique', 3, 4, 1),
(29, 'UE505', 'Analyse Financière', 3, 5, 1),
(30, 'UE506', 'Entrepreneuriat Numérique', 3, 5, 1),
(31, 'UE601', 'Blockchain et Cryptomonnaies', 3, 6, 2),
(32, 'UE602', 'Cybersécurité Avancée', 3, 5, 2),
(33, 'UE603', 'Innovation Technologique', 3, 5, 2),
(34, 'UE604', 'Éthique et Numérique', 3, 4, 2),
(35, 'UE605', 'Stratégies Digitales', 3, 5, 2),
(36, 'UE606', 'Mémoire et Projet de Fin d’Études', 3, 5, 2);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `annee_academique`
--
ALTER TABLE `annee_academique`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `annee` (`annee`);

--
-- Index pour la table `annee_etude`
--
ALTER TABLE `annee_etude`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `filiere_id` (`filiere_id`),
  ADD KEY `grade_id` (`grade_id`);

--
-- Index pour la table `ecue`
--
ALTER TABLE `ecue`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `ue_id` (`ue_id`),
  ADD KEY `enseignant_id` (`enseignant_id`);

--
-- Index pour la table `enseignant`
--
ALTER TABLE `enseignant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `telephone` (`telephone`);

--
-- Index pour la table `etudiant`
--
ALTER TABLE `etudiant`
  ADD PRIMARY KEY (`matricule`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `telephone` (`telephone`);

--
-- Index pour la table `filiere`
--
ALTER TABLE `filiere`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Index pour la table `grade`
--
ALTER TABLE `grade`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nom` (`nom`);

--
-- Index pour la table `membre_administratif`
--
ALTER TABLE `membre_administratif`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Index pour la table `moyenne_ue`
--
ALTER TABLE `moyenne_ue`
  ADD PRIMARY KEY (`id`),
  ADD KEY `etudiant_matricule` (`etudiant_matricule`),
  ADD KEY `ue_id` (`ue_id`),
  ADD KEY `annee_academique_id` (`annee_academique_id`);

--
-- Index pour la table `note`
--
ALTER TABLE `note`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ecue_id` (`ecue_id`),
  ADD KEY `parcours_etudiant_id` (`parcours_etudiant_id`);

--
-- Index pour la table `parcours_etudiant`
--
ALTER TABLE `parcours_etudiant`
  ADD PRIMARY KEY (`id`),
  ADD KEY `etudiant_matricule` (`etudiant_matricule`),
  ADD KEY `annee_etude_id` (`annee_etude_id`),
  ADD KEY `annee_academique_id` (`annee_academique_id`);

--
-- Index pour la table `ue`
--
ALTER TABLE `ue`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `annee_etude_id` (`annee_etude_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `annee_academique`
--
ALTER TABLE `annee_academique`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `annee_etude`
--
ALTER TABLE `annee_etude`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `ecue`
--
ALTER TABLE `ecue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT pour la table `enseignant`
--
ALTER TABLE `enseignant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT pour la table `filiere`
--
ALTER TABLE `filiere`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `grade`
--
ALTER TABLE `grade`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `membre_administratif`
--
ALTER TABLE `membre_administratif`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `moyenne_ue`
--
ALTER TABLE `moyenne_ue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `note`
--
ALTER TABLE `note`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `parcours_etudiant`
--
ALTER TABLE `parcours_etudiant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT pour la table `ue`
--
ALTER TABLE `ue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `annee_etude`
--
ALTER TABLE `annee_etude`
  ADD CONSTRAINT `annee_etude_ibfk_1` FOREIGN KEY (`filiere_id`) REFERENCES `filiere` (`id`),
  ADD CONSTRAINT `annee_etude_ibfk_2` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`);

--
-- Contraintes pour la table `ecue`
--
ALTER TABLE `ecue`
  ADD CONSTRAINT `ecue_ibfk_1` FOREIGN KEY (`ue_id`) REFERENCES `ue` (`id`),
  ADD CONSTRAINT `ecue_ibfk_2` FOREIGN KEY (`enseignant_id`) REFERENCES `enseignant` (`id`);

--
-- Contraintes pour la table `moyenne_ue`
--
ALTER TABLE `moyenne_ue`
  ADD CONSTRAINT `moyenne_ue_ibfk_1` FOREIGN KEY (`etudiant_matricule`) REFERENCES `etudiant` (`matricule`),
  ADD CONSTRAINT `moyenne_ue_ibfk_2` FOREIGN KEY (`ue_id`) REFERENCES `ue` (`id`),
  ADD CONSTRAINT `moyenne_ue_ibfk_3` FOREIGN KEY (`annee_academique_id`) REFERENCES `annee_academique` (`id`);

--
-- Contraintes pour la table `note`
--
ALTER TABLE `note`
  ADD CONSTRAINT `note_ibfk_1` FOREIGN KEY (`ecue_id`) REFERENCES `ecue` (`id`),
  ADD CONSTRAINT `note_ibfk_2` FOREIGN KEY (`parcours_etudiant_id`) REFERENCES `parcours_etudiant` (`id`);

--
-- Contraintes pour la table `parcours_etudiant`
--
ALTER TABLE `parcours_etudiant`
  ADD CONSTRAINT `parcours_etudiant_ibfk_1` FOREIGN KEY (`etudiant_matricule`) REFERENCES `etudiant` (`matricule`),
  ADD CONSTRAINT `parcours_etudiant_ibfk_2` FOREIGN KEY (`annee_etude_id`) REFERENCES `annee_etude` (`id`),
  ADD CONSTRAINT `parcours_etudiant_ibfk_3` FOREIGN KEY (`annee_academique_id`) REFERENCES `annee_academique` (`id`);

--
-- Contraintes pour la table `ue`
--
ALTER TABLE `ue`
  ADD CONSTRAINT `ue_ibfk_2` FOREIGN KEY (`annee_etude_id`) REFERENCES `annee_etude` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
