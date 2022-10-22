# Web-microblog-App-with-Face-Recogntion-Authentification


Developping a Moicroblog Blog Web App where all principals admin and user rights and access are managed by a real time face recognition authentification system 

Nous concevons, développons et implémentons dans le cadre de ce projet un système de vision par ordinateur, orienté reconnaissance faciale, intégré subtilement au contrôle des accès et à la gestion des droits des utilisateurs d’un prototype d’application de microblogage (Partage d’informations entre salariés d’une entreprise) en mode fermé.

## Phase conception

### Détection de visage


Pour la phase de détection, le modèle utilisé est le HOG (Histogramme histogramme de gradient orienté), en anglais, histogram of oriented gradients) de Dlib que nous verrons dans les lignes suivantes.
Outil considérablement utilisé dans notre projet, Dlib est une bibliothèque logicielle multiplateforme à usage général écrite dans le langage de programmation C++. Il s'agit d'un logiciel open source publié sous une licence logicielle Boost.

Il contient des composants logiciels pour gérer la mise en réseau, les threads, les interfaces graphiques utilisateur, les structures de données, l'algèbre linéaire, l'apprentissage automatique (machine learning), le traitement d'images, l'exploration de données, l'analyse XML et de texte, l'optimisation numérique, les réseaux bayésiens et diverses autres tâches.

Comme cité plus haut, l’algorithme HOG de Dlib est l’outil utilisé pour notre phase de localisation de visage. Après l’avoir défini, nous présenterons le processus derrière cet algorithme et son implémentation.

<img width="720" alt="Capture d’écran 2022-10-22 à 07 44 57" src="https://user-images.githubusercontent.com/113049750/197323373-80747568-125e-4c2a-823b-3621ee956682.png">

Selon Wikipédia, un histogramme de gradient orienté (en anglais, histogram of oriented gradients ou HOG) est une caractéristique utilisée en vision par ordinateur pour la détection d'objet. Il est basé sur le calcul d’histogrammes locaux de l'orientation du gradient sur une grille dense (zones régulièrement réparties sur l'image) et est particulièrement efficace pour la détection de personnes.



Navneet Dalal et Bill Triggs, chercheurs à l'INRIA de Grenoble, sont les auteurs de ce procédé.

Les 5 étapes du descripteur de fonctionnalité HOG :
Le prétraitement (normalisation gamma/couleur et redimensionnement).
Le calcul des gradients de l’orientation de l’image.
Division de l'image en cellules et construction des histogrammes de l’orientation des gradients.
Normalisation des blocs.
Obtention du vecteur de caractéristiques HOG.

##### Étape 1 : Le prétraitement
Le prétraitement des images (normalisation des couleurs, redimensionnement) sont typiques de toutes les tâches de vision par ordinateur. Le redimensionnement de l'image et la normalisation des valeurs de pixels constituent des étapes très importantes aussi bien dans l’application de méthodes traditionnelles que d’apprentissage en profondeur (deep learning).
 
Dans l’application du descripteur de caractéristiques HOG, la taille d'image la plus courante est de 64 × 128 (largeur x hauteur) pixels. Les travaux de Dalal et Triggs portaient principalement sur la reconnaissance et la détection humaines et révèlent que 64×128 est la taille d'image idéale, bien qu’il soit tout à fait possible d’utiliser n'importe quelles autres dimensions d'image tant que le ratio largeur /hauteur est 1 : 2 (128×256 ou 256×512).
 
On procède ensuite à l’application d’échelles de couleurs ou de normalisation des couleurs. Selon les auteurs les deux espaces colorimétriques RVB et LAB fonctionnent de manière identique. L’utilisation d'images en niveaux de gris, cependant réduit les performances (le descripteur de fonction HOG donne de meilleurs résultats sur les images colorées).

##### Étape 2 : Calcul des gradients de l’orientation de l’image

Lors de l’étape du calcul du gradient, on recourt couramment à l’application d’un filtre dérivatif 1-D centré, dans les directions horizontales et verticales. Les masques utilisés sont les suivants : 
Gradient vertical :   [−1,0,1]
Gradient horizontal : [−1,0,1] T
En règle générale, le calcul des gradients de l’orientation d'une image en vision par ordinateur, révèle les emplacements où les intensités des gradients de pixels changent. Cela conduit à l’extraction des informations utiles. Les images suivantes représentent dans l’ordre l’image de départ, celle après l’application des masques horizontal et celle après l’application du masque vertical.

##### Étape 3 : Division de l'image en cellules et construction des histogrammes de l’orientation des gradients
L’objectif à ce niveau est la création des histogrammes de l'orientation des gradients. Ceci est fait dans des cellules carrées de petite taille (de 4x4 à 12x12 pixels). On divise ici l'image en cellules de 8 × 8. On calcule par la suite, les gradients pour toutes les cellules. 
Chaque pixel de la cellule vote alors pour une classe de l'histogramme, en fonction de l'orientation du gradient à ce point. Le vote du pixel est pondéré par l'intensité du gradient en ce point.  


Dans la mesure où l’image est de dimension 64 × 128, on obtient 8 cellules dans le sens horizontal pour chaque ligne et 16 cellules dans le sens vertical pour chaque colonne. 
Chaque cellule a 8x8x3 = 192 pixels. Et le gradient de chaque cellule possède une magnitude et une direction (2 valeurs). Chaque cellule possède alors 8x8x2 = 128 valeurs comme informations de gradient. 
Les magnitudes des gradients et les directions sont chacun des blocs 8 × 8 contenants des nombres. Ils sont représentés à l'aide de 9 bacs d'orientation (9 valeurs pour une cellule).

On obtient donc 128 histogrammes de ces 9 valeurs correspondant aux 128 cellules dans l'image. La plupart des bacs sont vides sur l’image pour la simple et bonne raison qu’ils représentent la première cellule de la grille, où l'image ne contient pas beaucoup d'informations sur le gradient.


##### Étape 4 : Normalisation des blocs

Nous avons vu, lors de l’étape précédente, que nous divisons l'image en grilles de cellules de 8*8 pixels et nous calculons ensuite les gradients pour chaque cellule. 
Selon les travaux des auteurs, les valeurs de gradient peuvent varier en fonction de l'éclairage et du contraste du premier plan et de l'arrière-plan.
 	Pour pallier à ce problème, on procède à la normalisation de blocs de cellules. Dans de tels cas, la normalisation par bloc tend à être plus performante que celle par cellule unique. On regroupe donc quelques cellules en un bloc et on normalise les valeurs de gradient de chaque bloc de cellules groupées.



Nous avons regroupé 4 cellules pour former un bloc. On parle de normalisation de bloc 2 × 2. Il est également possible d’utiliser une normalisation de bloc 3 × 3 (regrouper 9 cellules ensemble). Selon les auteurs, les normalisations de bloc 2 × 2 et la normalisation de bloc 3 × 3 sont toutes les deux performantes.


##### Étape 5 : Obtention du vecteur de caractéristiques HOG

Lors de la dernière étape, on procède à l’établissement du vecteur de caractéristiques HOG.
Après tous les calculs de normalisations de bloc, ils sont concaténés en un seul vecteur pour former le vecteur de caractéristiques final. A ce niveau, il existe 7 vecteurs horizontaux et 15 vecteurs verticaux. 105 vecteurs au total qui sont concaténés pour obtenir le vecteur de caractéristiques final.
Nous pouvons par la suite utiliser un algorithme d'apprentissage automatique (classificateur supervisé) tel que Linear SVM pour poursuivre la reconnaissance d’image (classification). Cette étape ne fait pas partie de la définition du descripteur HOG à proprement parler et différents types de classifieurs peuvent être utilisés. Dalal et Triggs, choisissent volontairement un classificateur simple, un SVM à noyau linéaire, afin de mesurer essentiellement l'apport des HOG.

Une fois que nous avons correctement organisé nos données et nos étiquettes, nous devons initialiser un objet Linear SVM et appeler la méthode fit () avec les images et les étiquettes en tant qu'arguments pour entrainer le SVM linéaire sur les caractéristiques HOG que nous avons obtenues plus haut.


Ces deux outils (Dlib's HOG + Linear SVM face detector) sont combinés à l’intérieur de la méthode get_frontal_face_detector() de Dlib. C’est le détecteur de visage qu’il nous faut charger au préalable pour effectuer la phase de détection.


### Extraction des caractéristiques

Au cours de cette phase, le système extrait de l’image du visage détecté, les caractéristiques (informations utiles), et les représente sous la forme d’un vecteur de 128 dimensions qui est stocké dans la base de données pour être utilisé plus tard lors de la phase de décision (ici, vérification).

<img width="360" alt="extrac carac" src="https://user-images.githubusercontent.com/113049750/197323399-7bfb01b9-994b-411c-8ae9-9b78e543adb3.png">

Nous avons besoin, à ce niveau de charger au préalable tous les modèles dont nous avons besoin : 
Un prédicteur de forme pour trouver des repères de visage afin de pouvoir localiser précisément le visage, et enfin 
Le modèle de reconnaissance faciale.

### Le prédicteur de forme

Il permet d’effectuer l’alignement du visage qui est une étape cruciale dans la plupart des systèmes d’analyse de visages car il facilite la détection des caractéristiques, donc la reconnaissance du visage. 
Il est nécessaire pour cela de d’abord déterminer les points clés appelés points de repère au nombre de 68 avec le prédicteur de forme de visage.
Nous utilisons dans ce projet le ‘shape_predictor_68_face_landmarks.dat’ qui permet de prédire la forme ou bien la pose de visage.

<img width="363" alt="face3" src="https://user-images.githubusercontent.com/113049750/197323400-61fdfb14-fcb9-49bb-8611-8358ce6d0de3.png">

Il a été entrainé sur le jeu de données ibug 300-W (300 faces In-the-wild challenge : Database and results) de C. Sagonas, E. Antonakos, G, Tzimiropoulos, S. Zafeiriou, M. Pantic.


Ce prédicteur de forme retourne au modèle de reconnaissance un dictionnaire de liste contenant les coordonnées des parties caractéristiques du visage à savoir le menton, les deux sourcils, yeux, lèvres, l’arête et le bout du nez.


<img width="770" alt="face4" src="https://user-images.githubusercontent.com/113049750/197323401-309e4616-cee0-4143-91a3-7f7b0f08354d.png">

Ces coordonnées d’alignement du visage seront sous la forme de (150, 150, 3) et sont placées en entrée du modèle de reconnaissance pour le reste de la reconnaissance.

### Le modèle de reconnaissance

Ce modèle est un réseau ResNet avec 29 couches de conversion. Il s'agit essentiellement d'une version du réseau ResNet-34 de l'article Deep Residual Learning for Image Recognition de He, Zhang, Ren et Sun avec quelques couches supprimées et le nombre de filtres par couche réduit de moitié par l’auteur Davis King.

 <img width="794" alt="face5" src="https://user-images.githubusercontent.com/113049750/197323402-06755576-a30f-4c82-b483-20fe8bb4fafe.png">


Le réseau a été entrainé de zéro sur un ensemble de données d'environ 3 millions de visages. Cet ensemble de données est dérivé d'un certain nombre d'ensembles de données : l'ensemble de données Face Scrub, l’ensemble de données VGG Dataset et un large ensemble un grand nombre d'images récupérées sur Internet. 
L'ensemble de données a été nettoyé au mieux, en supprimant les erreurs d'étiquetage, grâce à l'entrainement répétitif d’un CNN (réseau de neurone convolutif) de reconnaissance faciale, puis des méthodes de classification par Graph Clustering et de nombreuses révisions manuelles . Environ la moitié des images proviennent de VGG et de Scrub Face. Le nombre total d'identités individuelles dans l'ensemble de données est de 7485.
L’entrainement du modèle a commencé avec des poids initialisés de manière aléatoire et un seuil (threshold) de 0,6. Le modèle résultant obtient une erreur moyenne de 0,993833 avec un écart type de 0,00272732 sur le benchmark LFW.
Il prend en entrées 150x150x3 (les données issues de la phase précédente) et représente les images de visage sous forme de vecteurs 128 dimensions. Il a obtenu une précision de 99,38% tandis que les êtres humains ont à peine un score de 97,53 % sur le même ensemble de données. 
Cela signifie que le modèle de reconnaissance faciale dlib peut rivaliser avec les autres modèles de reconnaissance faciale à la pointe de la technologie et avec les êtres humains.

Ce vecteur de 128 dimensions est donc stocké dans la base de données pour être utilisé lors de la phase de vérification.

### Vérification d’identité 

La dernière étape de vérification de notre système est celle où le système compare le vecteur obtenu à partir de l’image de l’utilisateur, grâce aux étapes précédentes, avec celui stocké au préalable dans la base de données pour l’individu prétendu. Elle se base sur l’application du calcul de la Distance Euclidienne.
Nous nous intéressons au calcul de la distance euclidienne entre des vecteurs représentant l’image d’entrée et l’image stockée dans la base de données afin de déterminer leurs similitudes.
Soient m ∈ 𝑁 ∗ , x= (𝑥1,...,𝑥𝑚) ∈ R, et y= (𝑦1,...,𝑦𝑚) ∈ R, la loi de calcul de la distance euclidienne comme ce suit : 

<img width="542" alt="face6" src="https://user-images.githubusercontent.com/113049750/197323404-5051b4a8-821c-413b-9df6-46c0ae8c071c.png">

Nous déterminons la distance entre leurs représentations vectorielles pour décider si deux photos faciales sont identiques. Ces deux photos de visage sont classées comme représentant une même personne si la distance est inférieure à une valeur seuil. Le seuil utilisé ici est 0,6 qui est la valeur ayant permis d’obtenir les meilleurs résultats (99,38 % de précision). 
Cette précision signifie que, lorsqu'il est présenté avec une paire de visages, le modèle identifiera correctement si la paire appartient au même personne ou provient de personnes différentes 99,38 % du temps.


## Description de la phase implémentation


Dans le cadre de ce projet nous avons développé une application de microblogage XFact pour l’échange d’informations entre les employés d’une société XFact fictive. L’application, inspirée du système de publications de Twitter, est privatisée. 

Cette application n’est en aucun cas une copie de Twitter et présente donc uniquement quelques fonctionnalités nous permettant de mettre en œuvre l’intégration et la mise en exergue de notre système en mode gestion des accès/ surveillance temps réel.  

Contrairement à une application classique, aucun rôle ou profile d’accès, outre que celui de l’admin, n’a été défini dans la partie administration de l’application. Toute l’architecture de gestion des accès et de rôles (gestion des droits des utilisateurs) est basée sur la reconnaissance faciale. 

### Les acteurs

- L’administrateur ou le super-utilisateur. Il ou elle possède tous les droits d’un utilisateur classique. En plus il dispose du droit d’accéder à la partie administration (base de données) de l’application pour exercer différents droits vis-à-vis des utilisateurs, publications et profiles. 
- Les utilisateurs qui disposent des droits de création de publications, de modification et de suppression de publications dont ils sont les auteurs.

### La présentation

Page d'acceuil

<img width="732" alt="Capture d’écran 2022-10-22 à 08 06 43" src="https://user-images.githubusercontent.com/113049750/197323396-a51a5538-f857-4f35-b471-e6c3950c3775.png">

Pages présentant les publications

Ces publications sont ordonnées de la plus récente à la plus ancienne, à chaque rafraichissement de la page grâce à la date de publication avec la vue PostListView 

<img width="732" alt="Capture d’écran 2022-10-22 à 08 06 43" src="https://user-images.githubusercontent.com/113049750/197323397-6a8ca4f8-f4e8-4a68-adf0-d38336a9505e.png">

 Exemple de Profil
 
<img width="732" alt="Capture d’écran 2022-10-22 à 08 06 43" src="https://user-images.githubusercontent.com/113049750/197323398-b9a6b324-f11d-4adb-ad19-c7a7538b4180.png">

### Fonctionnement

La fonction facedetect() permet d'évaluer en temps réel un vecteur représentant l'identité de l'utilisateur courant et de le comparer avec un vecteur représentant l'identité du profile utilisateur présent au préalable dans la base de données.

#### Succès de la reconnaissance

En cas de succès du processus d’authentification à double facteur, l’utilisateur est connecté et le message suivant s’affiche :

<img width="789" alt="Capture d’écran 2022-10-22 à 08 04 24" src="https://user-images.githubusercontent.com/113049750/197323380-b2039d8b-4d61-43cc-af1f-e395c5fc83da.png">

Il peut donc accéder au contenu de l’application comme son profile, les publications des utilisateurs, ou encore la page de création d’un nouveau post à publier.


#### Échec d'authentification et message d'alerte

<img width="852" alt="Capture d’écran 2022-10-22 à 08 00 17" src="https://user-images.githubusercontent.com/113049750/197323376-116ede65-3ce7-46a5-b421-1c703dcae111.png">

Le système envoie instantanément à l’administrateur du blog ainsi un mail d’alerte lui indiquant non seulement la phase du processus d’authentification qui a échoué mais aussi une image (capture) de l’individu à l’origine de la tentative de violation.

<img width="732" alt="Capture d’écran 2022-10-22 à 08 06 43" src="https://user-images.githubusercontent.com/113049750/197323384-650900cf-4967-4b1f-9bca-03828362ae13.png">


<img width="718" alt="vue  auth" src="https://user-images.githubusercontent.com/113049750/197323406-2635c862-2748-48b9-ac9e-31753f005357.png">

La fonction mailing pour l'envoi des messages d'alertes à l'admin et au propriétaire.

<img width="721" alt="mess al" src="https://user-images.githubusercontent.com/113049750/197323405-323a75a5-16df-463b-bb4e-1be2503feb03.png">

<img width="732" alt="Capture d’écran 2022-10-22 à 08 06 14" src="https://user-images.githubusercontent.com/113049750/197323383-d934e8b3-3f3e-45cd-8ec3-157eb60fc312.png">

<img width="732" alt="Capture d’écran 2022-10-22 à 08 06 06" src="https://user-images.githubusercontent.com/113049750/197323382-08fb7707-6489-4d77-8b71-09983059259c.png">  

Le rendu est le suivant :

<img width="852" alt="Capture d’écran 2022-10-22 à 07 58 44" src="https://user-images.githubusercontent.com/113049750/197323374-c160cf5a-3567-4448-b92c-a6ea56f79717.png">

Cette phrase clôture la partie authentification de notre application.

L’application de notre système à la gestion des accès intervient aussi lors d’une tentative de modification ou de suppression du contenu d’un utilisateur (modification ou suppression d’une publication).


S'il décide de consulter une publication de l’utilisateur Millie_1. Après clic, il est dirigé vers la page suivante :

<img width="840" alt="Capture d’écran 2022-10-22 à 08 02 32" src="https://user-images.githubusercontent.com/113049750/197323377-83644a3b-c56b-4b18-869f-1979d0721aef.png">

Il ne peut donc (puisque le système se base sur son profile pour la gestion des accès) que consulter la publication.

<img width="848" alt="Capture d’écran 2022-10-22 à 08 04 01" src="https://user-images.githubusercontent.com/113049750/197323379-2c828f5c-0923-44d8-98ff-5805899d7d15.png">

## Conclusion 

Le présent projet est satisfaisant dans l’ensemble car il met bien en évidence, comme l’était notre intention, l’idée de substituer la définition des droits et la gestion des accès classique avec une approche basée sur l’utilisation de la vision par ordinateur (plus précisément la reconnaissance faciale).
Il regroupe toutes les étapes d’implémentation du dit système ainsi qu’une présentation de son fonctionnement dans l’environnement de l’application pour les taches d’authentification pour l’accès à l’application initialement, mais également lors des tentatives d’altérations d’informations à l’intérieur de la base de données (publications, utilisateurs et profiles) comme la modification ou la suppression du contenu utilisateur. 

Comme précisé plus haut, aucune définition de droits ou de privilèges en dehors de ceux qui définissent primitivement l’admin n’a été incluse lors de la conception et de l’implémentation. Toute la gestion des accès et des droits est basée uniquement sur le résultat de l’authentification comme implémenté dans les extraits de code python insérés dans la présentation des vues. 

Toutes les autorisations d’accès de l’application sont complètement centrées sur la reconnaissance faciale de l’utilisateur connecté, même après succès de la phase d’authentification. 

