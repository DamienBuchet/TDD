# TDD

TP sur le TDD, avec pour sujet la gestion d'une bibliothèque, de ses livres, membres et réservations.

On commencera par installer Python, si ce n'est pas déjà fait. Il suffit d'aller sur https://www.python.org/, et de suivre les étapes pour télécharger et installer Python sur son OS.

Puis, on installe les modules nécessaires à l'aide du fichier requirements.txt (il ne contient qu'un seul module, les autres sont normalement préinstallés lors d'une installation normale de Python), comme suit : 

```bash
python -m pip install -r requirements.txt
```
ou alors, installer le module directement : 
```bash
pip install mysql-connector-python
```

Une fois tout ceci effectué, on peut lancer le fichier Python, depuis un terminal : 
```bash
python main.py
```

Une fois le programme lancé, on a normalement les résultats au bout de quelques secondes : 

![Image](https://i.goopics.net/wosm7m.png)

Si des erreurs ont lieu, il sera affiché sous les résultats : (errors: x, failures: x), ainsi que les problèmes rencontrés.
