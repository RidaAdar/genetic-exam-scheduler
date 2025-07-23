#  Génération d’emplois du temps d’examen par algorithme génétique (Python)
<p align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1400/1*91TZsf7mZidi68IOzMY6ew.png" width="300" alt="Genetic Algorithm Logo"/>
</p>

## Présentation

Ce projet automatise la création d’emplois du temps d’examens grâce à un **algorithme génétique**, un type d’algorithme évolutionniste largement utilisé pour résoudre des problèmes complexes d’optimisation sous contraintes.  
L’objectif est de générer un planning respectant :  
- la disponibilité des enseignants,
- l’absence de conflits pour chaque étudiant,
- l’équité dans la répartition des épreuves.

---

## Fonctionnalités principales

- **Modélisation complète** des enseignants, étudiants, emplois du temps, et “gènes” (épreuves individuelles)
- **Gestion automatique des contraintes** :
  - Un enseignant ne peut surveiller deux examens en même temps
  - Un enseignant ne peut surveiller un examen hors de ses disponibilités
  - Un étudiant ne peut avoir deux examens simultanés
- **Optimisation évolutive** :  
  - Initialisation aléatoire d’une population de plannings
  - Sélection par roulette, croisement uniforme, mutation pour explorer le maximum de solutions valides
  - Fonction objectif avec pénalités ajustables pour chaque type de contrainte
- **Paramétrage flexible** :  
  - Taille de population, taux de mutation/croisement, pondération des contraintes, nombre de générations, etc.
- **Exemples de résultats** sur différents jeux de données (petit et gros clusters)

---

## Fichiers du projet

- `classes.py` : Définitions des classes : Teacher, Student, Schedule, gene
- `functions.py` : Fonctions principales : chargement des données, génération, croisement, mutation, calcul de fitness, etc.
- `main.py` : Script de lancement, configuration des paramètres et exécution de l’algorithme
- `[rapport_projet][TPP].pdf` : Rapport détaillé (explications théoriques, structure, résultats, analyse)
- `Profs/` & `Students/` : Répertoires contenant les fichiers d’entrée (à créer avec tes propres données)

---

## Exécution rapide


1. **Ouvrez le dossier `/TPP` dans votre terminal** (il contient `main.py`, `classes.py` et `functions.py`).
2. **Dans `main.py`,** modifiez les variables `teacher_directory` et `student_directory` avec le chemin de vos dossiers `Profs` et `Students` (utilisez le préfixe `r` pour les chemins Windows, ex :  
   `r"C:\Users\mon_nom\Downloads\Data Cluster Projet Math-app\Students"`).
3. **(Optionnel)** Adaptez les paramètres de l’algorithme dans la fonction `main()` (`pop_size`, `mutation_rate`, `crossover_rate`, `student_coeff`, etc.).
4. **Exécutez le projet** en tapant dans le terminal :
   ```bash
   python3 main.py
