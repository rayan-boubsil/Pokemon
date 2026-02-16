# Jeu Pokémon avec Pygame

## Description
Jeu Pokémon développé en Python avec Pygame utilisant la programmation orientée objet.

## Fonctionnalités

### Menu Principal
- **Lancer une partie** : Démarre un combat Pokémon
- **Ajouter un Pokémon** : Ajoute un nouveau Pokémon dans le fichier `pokemon.json`
- **Accéder au Pokédex** : Consulte la liste de tous les Pokémon disponibles
- **Quitter** : Ferme le jeu

### Système de Combat
- Sélection du Pokémon du joueur
- Combat au tour par tour contre un adversaire aléatoire
- Affichage des statistiques (PV, attaque, défense)
- Messages de combat dynamiques

## Structure du Projet

```
pokemon_game/
├── main.py          # Point d'entrée du jeu
├── pokemon.py       # Classe Pokemon
├── pokedex.py       # Classe Pokedex (gestion des Pokémon)
├── menu.py          # Classe Menu (interface du menu)
├── jeu.py           # Classe Jeu (logique de combat)
├── pokemon.json     # Base de données des Pokémon (créé automatiquement)
└── README.md        # Ce fichier
```

## Classes

### Pokemon (`pokemon.py`)
Représente un Pokémon avec ses attributs :
- `nom` : Nom du Pokémon
- `type` : Type (Feu, Eau, Plante, etc.)
- `pv_max` et `pv_actuel` : Points de vie
- `attaque` : Points d'attaque
- `defense` : Points de défense
- `niveau` : Niveau du Pokémon

**Méthodes principales :**
- `attaquer(cible)` : Attaque un autre Pokémon
- `recevoir_degats(degats)` : Reçoit des dégâts
- `est_ko()` : Vérifie si le Pokémon est KO
- `soigner()` : Restaure les PV au maximum

### Pokedex (`pokedex.py`)
Gère la collection de Pokémon disponibles :
- Chargement/sauvegarde depuis `pokemon.json`
- Ajout de nouveaux Pokémon
- Recherche de Pokémon par nom

### Menu (`menu.py`)
Gère l'interface utilisateur :
- Menu principal avec navigation
- Formulaire d'ajout de Pokémon
- Affichage du Pokédex
- Transition vers le jeu

### Jeu (`jeu.py`)
Gère la logique de combat :
- Sélection du Pokémon
- Combat au tour par tour
- Gestion des victoires/défaites

## Installation

### Prérequis
- Python 3.7 ou supérieur
- Pygame

### Installation de Pygame
```bash
pip install pygame
```

## Utilisation

### Lancer le jeu
```bash
python main.py
```

### Commandes

#### Menu Principal
- **↑/↓** : Naviguer dans le menu
- **ENTRÉE** : Sélectionner une option

#### Ajout de Pokémon
- **TAB** : Passer au champ suivant
- **ENTRÉE** : Valider le formulaire
- **ESC** : Annuler

#### Pokédex
- **↑/↓** : Naviguer dans la liste
- **ENTRÉE/ESC** : Retour au menu

#### Combat
- **↑/↓** : Sélectionner un Pokémon
- **←/→** : Choisir une action
- **ENTRÉE** : Confirmer
- **ESC** : Retour au menu

## Fichier pokemon.json

Le fichier `pokemon.json` est créé automatiquement avec des Pokémon par défaut. Vous pouvez l'éditer manuellement ou utiliser l'option "Ajouter un Pokémon" du menu.

Format :
```json
[
  {
    "nom": "Salamèche",
    "type": "Feu",
    "pv": 39,
    "attaque": 52,
    "defense": 43,
    "niveau": 5
  },
  ...
]
```

## Personnalisation

### Ajouter plus de Pokémon
Utilisez l'option du menu ou éditez `pokemon.json` directement.

### Modifier les couleurs
Les couleurs sont définies dans les classes `Menu` et `Jeu`.

### Ajouter de nouvelles fonctionnalités
Le code est modulaire et facile à étendre :
- Ajoutez de nouveaux types de Pokémon
- Implémentez des capacités spéciales
- Créez un système d'évolution
- Ajoutez des objets et des potions

## Améliorations possibles

1. **Système d'évolution** : Les Pokémon évoluent après plusieurs victoires
2. **Capacités multiples** : Chaque Pokémon a plusieurs attaques
3. **Multiplicateurs de types** : Les types ont des avantages/désavantages
4. **Système d'expérience** : Gain d'XP et montée de niveau
5. **Sauvegarde de partie** : Sauvegarder la progression
6. **Interface graphique améliorée** : Sprites et animations
7. **Musique et sons** : Effets sonores et musique de fond
8. **Mode multijoueur** : Combat contre un autre joueur

## Auteur
Projet développé avec Python et Pygame

## Licence
Projet éducatif libre d'utilisation
