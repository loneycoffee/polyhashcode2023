# Projet Polyhash2023 Team S - CupSTeam

## L'équipe

- Théo M.
- Loïc W.
- Amedeo C.

## Descriptif général du projet

Projet de développement logiciel IDIA3 sur le problème
du [google-hash-code 2016](https://storage.googleapis.com/coding-competitions.appspot.com/HC/2016/hashcode2016_qualification_task.pdf)  
Réalisation de 3 algorithmes différents dans le but de générer des solutions au problème.  
L'objectif est de contrôler une flotte de drones pour livrer des commandes dont les produits sont stockés dans des
entrepôts.

Vidéo explicative :

![](https://justalternate.fr/polyhash.mp4)

## Prérequis / Procédure d'installation

- Python (>= 3.11.6 sous un environnement Linux)

```sh
sudo apt install python
```

- pip

```sh
python -m ensurepip --upgrade
```

- Dépendances

```sh
make install
```

## Procédure d'exécution

### Utilisation avec `make`

Afin d'utiliser notre projet, nous vous conseillons vivement d'**utiliser notre Makefile** avec la commande `make`.  
Celle-ci devrait permettre de faire tout ce que vous avez besoin.

- Pour installer les dépendances du projet et créer l'environnement python :

```shell
make install
```

- Pour générer toutes les solutions du dossier `challenges` avec un algorithme (polyhash.py) :

```sh
make generate theo|loic|amedeo
```

Les solutions seront écrites dans le dossier `solutions`

- Pour lancer notre module de tests (polytests.py) :

```sh
make tests
```

- Pour lancer nos tests de formatage (pep8 et flake8) :

```sh
make lint
```

- Pour lancer un benchmark (polybench.py) :
  (les arguments entre crochets sont optionnels)

```sh
make bench every #Pour lancer les benchmarks de a_example, b_busy_day, c_redundancy et d_mother_of_all_warehouses avec toutes nos solutions
make bench every every #Pour lancer les benchmarks sur l'ensemble du dossier challenges/ avec toutes nos solutions
make every|theo|loic|amedeo [every|challenges/map.in]
```

- Pour lancer tous nos tests (linter et polytests) :

```sh
make all
```

- Pour supprimer les fichiers non essentiels :

```sh
make clean
```

### Utilisation sans `make`

Il est quand même possible d'utiliser notre projet sans utiliser le Makefile :  
Attention, il faut lancer les fichiers python depuis le dossier racine du projet.

- Pour générer toutes les solutions du dossier `challenges` avec un algorithme :

```sh
python src/polyhash.py theo|loic|amedeo
```

- Pour générer une solution en particulière avec un algorithme et spécifier le nom de sortie :

```sh
python src/polyhash.py theo|loic|amedeo challenges/a_example.in solutions/a_example.out
```

- Pour lancer notre module de tests :

```sh
python src/polytests.py
```

- Pour lancer notre module de benchmark :
  (les arguments entre crochets sont optionnels)

```sh
python src/polybench.py every|theo|loic|amedeo [every|challenges/a_example.in]
```

## Détail des stratégies mises en œuvre

### Stratégies algorithmiques

Explication implémentation des algorithmes :

#### **Algorithme Théo** :

- L'idée est de d'abord établir un classement des orders par poids total d'order, ce qui nous donne un weight_ranking.
- On fait ensuite des clusters de 2 orders (idéalement 2 et dans le cas contraire 1 si pas assez d'orders). Le critère
  pour faire ces clusters est la distance entre 2 orders. Donc si 2 orders sont proches on forme un cluster.
- Le cluster a un weight_ranking (qui est égal à la somme des weight_ranking des orders) et un dist_ranking qui est la
  distance par rapport au cluster actuel.
- Au début, on prend le cluster le plus proche de la warehouse 0.
- Ensuite, on prend chaque order du cluster.
- On utilise un drone que l'on essaye de remplir un maximum pour compléter l'order le plus rapidement possible.
- Une fois qu'on a complété les orders du cluster, on enlève le cluster des clusters à compléter.
- Puis, on regarde le meilleur cluster à faire après. On refait ainsi un classement des clusters avec la distance par
  rapport au cluster actuel. Le score global d'un cluster est pondéré par 90% de son poids total et 10% de sa distance
  avec le cluster actuel.
- Une fois le cluster choisi, on le traite comme précédemment.
- On refait ces opérations tant que l'on a des clusters.

#### **Algorithme Loïc** :

- On trie la liste des orders par distance par rapport à la position de la warehouse 0 dans un premier prétraitement.
- Pour chaque orders dans la liste des orders triée :
  - On cycle sur les produits un par un en assignant un drone par type de produit.
  - Quand il n'y a plus de drones disponibles, on livre les produits en faisant attention de toujours utiliser la
    warehouse la plus proche.

#### **Algorithme Amedeo** :

- On trie les commandes par poids pour ensuite choisir la commande qui peut être complétée le plus rapidement possible.
- On charge un drone au maximum avec des produits de plusieurs commandes. S'il est plein, on passe au drone suivant.
- Chaque drone peut se charger de plusieurs commandes à la fois.
- Lorsque tous les drones sont chargés, on va délivrer les produits pour les commandes concernées.

### Performances

#### Algorithme Théo

- a_example.in : 0 secondes, 0 MB

- b_busy_day.in : ~3 secondes, ~6 MB

- c_redundancy.in : ~4 secondes, ~13 MB

- d_mother_of_all_warehouses.in : ~2 secondes, 0 MB

#### Algorithme Loïc

- a_example.in : 0 secondes, 0 MB

- b_busy_day.in : ~0.07 secondes, 0 MB

- c_redundancy.in : ~0.16 secondes, 0.24 MB

- d_mother_of_all_warehouses.in : ~0.064 secondes, 0 MB

#### Algorithme Amedeo

- a_example.in : 0 secondes, ~0.12 MB

- b_busy_day.in : ~0.12 secondes, ~6 MB

- c_redundancy.in : ~0.37 secondes, ~12 MB

- d_mother_of_all_warehouses.in : ~0.17 secondes, 0 MB

## Description et organisation du code

### Organisation des fichiers

- **challenges/**  
  Dossier des fichiers d'entrée.
- **solutions/**
  - **solutions_amedeo/**  
    solutions générées par l'algorithme **polysolver_naive_amedeo.py**.
  - **solutions_loic/**  
    solutions générées par l'algorithme **polysolver_naive_loic.py**.
  - **solutions_theo/**  
    solutions générées par l'algorithme **polysolver_naive_theo.py**.
- **solutions_test/**  
  solutions prégénérées pour les comparaisons de nos tests **polytests.py**.
- **src/** : dossier contenant l'ensemble du code python du projet.
  - **Objects/** : dossier regroupant nos implémentations objets.
    - **Cluster.py** : cluster d'orders
    - **Drone.py**
    - **Map.py** : objet général qui contient l'ensemble des informations du problème.
    - **Order.py**
    - **Warehouse.py**
  - **polysolvers/** : dossier regroupant nos générateurs de solutions.
    - **polysolver_naive_theo** : Algorithme final de Théo.
    - **polysolver_naive_loic** : Algorithme naïf de Loïc.
    - **polysolver_naive_amedeo** : Algorithme naïf de Amedeo.
  - **polybench.py** : calculs de temps et mémoire des différents algorithmes.
  - **polyhash.py** : interface homme-machine qui génère des solutions.
  - **polyparser.py** : parse un fichier d'entrée du dossier **challenges/** en utilisant nos implémentations objets.
  - **polytests.py** : l'ensemble de nos tests sur les objets, méthodes d'objets, fonctions et modules du projet.
  - **polyvisualizer.py** : visualisation de fichier d'entrée de taille inférieure à 30x30.
  - **polywriter.py** : écrit des solutions dans un fichier **.out** et le place dans les dossiers **solutions/**.
  - **polyscoring.py** : prend un fichier d'entrée et un algorithme et renvoie le nombre de points de la solution
    générée.

### Limitations connues

- Le polyvisualizer ne fonctionne pas avec les autres challenges donnés autre que a_example_to_visu.in (nous n'avons pas
  implémenté une version qui permet d'afficher les grands challenges).

### Bugs connus

- Dans **Objects/Clusters.py ligne (56)** : la méthode **del_order_full_filled(order)** pourrait apparemment supprimer
  une order qui n'a pas été complétée.  
  Pourtant, lors de son utilisation, elle n'est pas censé le faire, en effet, on vérifie au préalable que l'order n'est
  pas considérée comme complétée.  
  **Conséquence :** des orders n'ont pas été complétées => Manque de point à gagner.

## Stratégie de développement

- Utilisation du **"[Tableau des tickets
  ](https://gitlab.univ-nantes.fr/E23B956N/polyhash2023/-/issues/?sort=created_date&state=all&first_page_size=100)"** de
  Gitlab pour la **gestion des tickets**, politique de **"[demande de fusion](https://gitlab.univ-nantes.fr/E23B956N/polyhash2023/-/merge_requests?scope=all&state=all)"** pour
  avoir un suivi de projet explicite, efficace, fonctionnel et **revue de code** par un autre membre de l'équipe à
  chaque demande de fusion.

- Ajout d'une **[CI](https://gitlab.univ-nantes.fr/E23B956N/polyhash2023/-/pipelines)** qui se lance à **chaque demande
  de fusion** afin de vérifier que le formatage de tous les fichiers du dossier `src` respectent les **règles pep8 et
  flake8**. Et que le nouveau code passe bien toujours nos **tests** `polytests.py`

## Répartition des tâches au sein de l'équipe

- Théo M. :

  - Réalisation **polysolver_naive_theo** (avec classe Cluster et fonctions utils respectives)
  - Contribution majoritaire aux **polytests**
  - Contributions à l'élaboration de solutions
  - Contribution majoritaire aux functs/utils.py
  - Gestion tableau des tickets GitLab
  - Participation à la refactorisation du code
  - Particpation au typing sur les fichiers
  - Participation au README.md
  - Contribution majoritaire pour la vidéo

- Loïc W. :

  - Réalisation **polysolver_naive_loic** (avec fonctions utils respectives)
  - Réalisation de la **CI** (dont création runner GitLab)
  - Réalisation du **Makefile**
  - Contributions à l'élaboration de solutions
  - Normalisation PEP8 et flake8
  - Gestion tableau des tickets GitLab
  - Création majoritaire de tickets sur GitLab
  - Organisation des fichiers du projet
  - Participation à la refactorisation du code
  - Participation à la réalisation des tests
  - Contribution majoritaire au README.md
  - Participation à la vidéo
  - A dissimulé des ASCII ART cuphead dans le projet

- Amedeo C. :
  - Réalisation **polysolver_naive_amedeo** (avec fonctions utils respectives)
  - Contributions à l'élaboration de solutions
  - Contribution majoritaire au typing
  - Participation à la refactorisation du code
  - Participation à la vidéo (élaboration premières versions diaporama)
  - Participation au README.md
  - Réalisation du polyscoring (non fini, mais visible dans la branche #34-polyscoring)
  - Réalisation du polyparser

## Autres informations

Quelques chiffres concernant notre projet :

- **54** tickets
- **41** merge requests
- **+40** branches
- ~ **1570** lignes de code
- **178** pipelines (sucess rate : 75%)
- **43** failed pipelines
- **318** jobs de CI

Il y a un total de 3 ASCII ART cuphead cachés dans le projet (code et repository), si vous les trouvez tous nous vous
offrons une chouquette :D

Assets et musiques du jeu CupHead :  
© 2022 StudioMDHR Entertainment Inc. All Rights Reserved.
