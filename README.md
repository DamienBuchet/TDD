# TDD

TP sur le TDD, avec pour sujet la gestion d'une bibliothèque, de ses livres, membres et réservations.

On commencera par installer Python, si ce n'est pas déjà fait. Il suffit d'aller sur https://www.python.org/, et de suivre les étapes pour télécharger et installer Python sur son OS.

Puis, on installe les modules nécessaires à l'aide du fichier requirements.txt (il ne contient que deux modules, les autres sont normalement préinstallés lors d'une installation normale de Python), comme suit : 

```bash
python -m pip install -r requirements.txt
```
Ensuite, il faudra lancer un serveur local pour avoir une base de données (ici, on utilise phpMyAdmin, avec MySQL, avec pour hôte : localhost, utilisateur : root, pas de mot de passe, et un nom de base de données : tdd). Il est possible de créer la base de données en utilisant le fichier bdd.sql, qui contient les instructions nécessaires à cette tâche, en important ce fichier dans phpMyAdmin (exemple ci-dessous).
#
 
![Image](https://i.goopics.net/ygo7c5.png)

#

Une fois tout ceci effectué, on peut lancer le fichier Python, depuis le cmd : 
```bash
python doc.py
```
ou à partir de n'importe quel éditeur pouvant faire fonctionner des programmes en Python.

Une fois le programme lancé, on a normalement les résultats au bout de quelques secondes : 

![Image](https://i.goopics.net/17jic3.png)

Si des erreurs ont lieu, il sera affiché sous les résultats : (errors: x, failures: x), ainsi que les problèmes rencontrés.
