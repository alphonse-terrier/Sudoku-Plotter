# Sudoku-Plotter

Tous les fichiers permettant la réalisation d' un bras mécanique travaillant en coordonnées polaires, permettant d’écrire un sudoku ou d’en résoudre un et à terme d’écrire tout type d’information.

Au niveau informatique, le bras doit identifier une grille de sudoku tracée sur une feuille, résoudre cette dernière par différentes méthodes de résolution. Ces méthodes doivent permettre éventuellement de créer des grilles de sudoku à compléter. Une fois le sudoku résolu, le stylo présent sur le bras doit pouvoir se déplacer pour écrire la solution de celui-ci (ou écrire un sudoku que l’utilisateur devra lui-même compléter). Le bras doit pouvoir également recopier tout type de document en noir et blanc.

La structure du bras sera réalisée en Makerbeam, tiges en métal se rapprochant dans leur utilisation des meccanos. Le pivotement du bras sera assuré par un moteur pas-à-pas dont le pignon sera en liaison appui-plan avec un roue dentée fixe. Ainsi la mise en mouvement du moteur entrainera sa rotation - et celle de toute la structure - autour de cette roue. Le stylo sera fixé sur une structure qui pourra se déplacer le long de deux tiges en métal. Cette structure sera mise en mouvement par un deuxième moteur pas-à-pas qui entrainera une courroie fixée à ses extrémités à celle-ci. Le stylo pourra être mis en contact avec la feuille grâce à un servomoteur.

La résolution d'un sudoku peut se faire par l'éxécution du fichier main.py dans un interpréteur Python 3.
