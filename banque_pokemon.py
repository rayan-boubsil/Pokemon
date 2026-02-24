"""
Classe BanquePokemon
Gère la collection de tous les Pokémon disponibles dans le jeu
"""
import json
import os
from pokemon import Pokemon

class BanquePokemon:
    """
    Classe gérant la banque de Pokémon disponibles
    
    Cette classe gère pokemon.json qui contient TOUS les Pokémon disponibles
    dans le jeu (contrairement au Pokédex qui contient les Pokémon rencontrés)
    """
    
    def __init__(self, fichier="pokemon.json"):
        """
        Initialise la banque de Pokémon
        
        Args:
            fichier (str): Nom du fichier JSON contenant les Pokémon disponibles
        """
        self.fichier = fichier
        self._pokemons_disponibles = []  # Liste privée (encapsulation)
        self._charger_pokemons()
    
    def _charger_pokemons(self):
        """
        Charge les Pokémon depuis le fichier pokemon.json
        Méthode privée (encapsulation)
        """
        if os.path.exists(self.fichier):
            try:
                with open(self.fichier, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._pokemons_disponibles = [Pokemon.from_dict(p) for p in data]
                    print(f"✓ Banque Pokémon chargée: {len(self._pokemons_disponibles)} Pokémon disponibles")
            except json.JSONDecodeError:
                print(f"Erreur lors de la lecture de {self.fichier}")
                self._pokemons_disponibles = []
                self._initialiser_pokemons_defaut()
        else:
            self._initialiser_pokemons_defaut()
    
    def _initialiser_pokemons_defaut(self):
        """
        Crée quelques Pokémon par défaut
        Méthode privée (encapsulation)
        """
        pokemons_defaut = [
            Pokemon("Salamèche", "Feu", 39, 52, 43, 5),
            Pokemon("Carapuce", "Eau", 44, 48, 65, 5),
            Pokemon("Bulbizarre", "Plante", 45, 49, 49, 5),
            Pokemon("Pikachu", "Électrik", 35, 55, 40, 5),
            Pokemon("Évoli", "Normal", 55, 55, 50, 5),
            Pokemon("Ronflex", "Normal", 160, 110, 65, 10),
            Pokemon("Dracaufeu", "Feu", 78, 84, 78, 36),
            Pokemon("Mewtwo", "Psy", 106, 110, 90, 70)
        ]
        self._pokemons_disponibles = pokemons_defaut
        self._sauvegarder()
        print(f"✓ Banque Pokémon initialisée avec {len(pokemons_defaut)} Pokémon")
    
    def _sauvegarder(self):
        """
        Sauvegarde les Pokémon dans le fichier pokemon.json
        Méthode privée (encapsulation)
        """
        try:
            with open(self.fichier, 'w', encoding='utf-8') as f:
                data = [p.to_dict() for p in self._pokemons_disponibles]
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    def ajouter_pokemon(self, pokemon):
        """
        Ajoute un nouveau Pokémon à la banque
        Vérifie les doublons avant d'ajouter
        
        Args:
            pokemon (Pokemon): Le Pokémon à ajouter
        
        Returns:
            tuple: (bool, str) - (Succès, Message)
        """
        # Vérifier si le Pokémon existe déjà
        if any(p.nom.lower() == pokemon.nom.lower() for p in self._pokemons_disponibles):
            return False, f"{pokemon.nom} existe déjà dans la banque!"
        
        self._pokemons_disponibles.append(pokemon)
        if self._sauvegarder():
            return True, f"{pokemon.nom} ajouté avec succès à la banque!"
        else:
            return False, "Erreur lors de la sauvegarde"
    
    def obtenir_pokemon(self, nom):
        """
        Récupère un Pokémon par son nom
        
        Args:
            nom (str): Nom du Pokémon
        
        Returns:
            Pokemon ou None: Le Pokémon trouvé ou None
        """
        for pokemon in self._pokemons_disponibles:
            if pokemon.nom.lower() == nom.lower():
                return pokemon
        return None
    
    def obtenir_liste_noms(self):
        """
        Retourne la liste des noms de Pokémon disponibles
        
        Returns:
            list: Liste des noms
        """
        return [p.nom for p in self._pokemons_disponibles]
    
    @property
    def pokemons(self):
        """
        Propriété retournant la liste des Pokémon (en lecture seule)
        Principe d'encapsulation: accès contrôlé aux données
        
        Returns:
            list: Copie de la liste des Pokémon
        """
        return self._pokemons_disponibles.copy()
    
    def __len__(self):
        """
        Surcharge de l'opérateur len()
        Principe du polymorphisme
        
        Returns:
            int: Nombre de Pokémon dans la banque
        """
        return len(self._pokemons_disponibles)
    
    def __str__(self):
        """
        Représentation en chaîne de la banque
        Principe du polymorphisme
        
        Returns:
            str: Description de la banque
        """
        return f"Banque Pokémon: {len(self._pokemons_disponibles)} Pokémon disponibles"
    
    def __repr__(self):
        """
        Représentation technique de la banque
        
        Returns:
            str: Représentation technique
        """
        return f"BanquePokemon(fichier='{self.fichier}', pokemons={len(self._pokemons_disponibles)})"
