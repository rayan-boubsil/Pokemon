"""
Classe Pokedex
Gère la collection de Pokémon rencontrés par le dresseur
"""
import json
import os
from pokemon import Pokemon
from datetime import datetime

class Pokedex:
    """
    Classe gérant le Pokédex du dresseur
    
    Le Pokédex est un outil indispensable qui enregistre les informations
    des Pokémon combattus (nom, type, défense, puissance d'attaque et points de vie).
    Les Pokémon sont sauvegardés dans pokedex.json avec vérification des doublons.
    
    Principes POO appliqués:
    - Encapsulation: Les données sont protégées et accessibles via des méthodes
    - Abstraction: Interface simple pour gérer les Pokémon rencontrés
    - Responsabilité unique: Gère uniquement les Pokémon rencontrés en combat
    """
    
    def __init__(self, fichier_pokedex="pokedex.json"):
        """
        Initialise le Pokédex du dresseur
        
        Args:
            fichier_pokedex (str): Fichier JSON pour les Pokémon rencontrés
        """
        self.fichier_pokedex = fichier_pokedex
        self._pokemons_rencontres = []  # Liste privée (encapsulation)
        self._charger_pokedex()
    
    def _charger_pokedex(self):
        """
        Charge les Pokémon rencontrés depuis le fichier pokedex.json
        Méthode privée (encapsulation)
        """
        if os.path.exists(self.fichier_pokedex):
            try:
                with open(self.fichier_pokedex, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._pokemons_rencontres = [self._dict_vers_pokemon(p) for p in data]
                    print(f"✓ Pokédex chargé: {len(self._pokemons_rencontres)} Pokémon")
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Nouveau Pokédex créé")
                self._pokemons_rencontres = []
                self._sauvegarder()
        else:
            print("Nouveau Pokédex initialisé")
            self._pokemons_rencontres = []
            self._sauvegarder()
    
    def _sauvegarder(self):
        """
        Sauvegarde les Pokémon rencontrés dans pokedex.json
        Méthode privée (encapsulation)
        """
        try:
            with open(self.fichier_pokedex, 'w', encoding='utf-8') as f:
                data = [self._pokemon_vers_dict(p) for p in self._pokemons_rencontres]
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du Pokédex: {e}")
            return False
    
    def _pokemon_vers_dict(self, pokemon):
        """
        Convertit un Pokémon en dictionnaire avec métadonnées
        Méthode privée (encapsulation)
        
        Args:
            pokemon (Pokemon): Le Pokémon à convertir
        
        Returns:
            dict: Dictionnaire avec infos du Pokémon et métadonnées
        """
        return {
            "nom": pokemon.nom,
            "type": pokemon.type,
            "pv": pokemon.pv_max,
            "attaque": pokemon.attaque,
            "defense": pokemon.defense,
            "niveau": pokemon.niveau,
            "date_rencontre": pokemon.date_rencontre if hasattr(pokemon, 'date_rencontre') else datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nombre_combats": pokemon.nombre_combats if hasattr(pokemon, 'nombre_combats') else 1
        }
    
    def _dict_vers_pokemon(self, data):
        """
        Crée un Pokémon depuis un dictionnaire
        Méthode privée (encapsulation)
        
        Args:
            data (dict): Dictionnaire contenant les données
        
        Returns:
            Pokemon: Instance de Pokemon
        """
        pokemon = Pokemon(
            data["nom"],
            data["type"],
            data["pv"],
            data["attaque"],
            data["defense"],
            data.get("niveau", 1)
        )
        pokemon.date_rencontre = data.get("date_rencontre", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        pokemon.nombre_combats = data.get("nombre_combats", 1)
        return pokemon
    
    def _pokemon_existe(self, nom):
        """
        Vérifie si un Pokémon existe déjà dans le Pokédex
        Méthode privée pour la vérification des doublons (encapsulation)
        
        Args:
            nom (str): Nom du Pokémon à vérifier
        
        Returns:
            tuple: (bool, index) - True si existe avec son index, sinon (False, -1)
        """
        for i, pokemon in enumerate(self._pokemons_rencontres):
            if pokemon.nom.lower() == nom.lower():
                return True, i
        return False, -1
    
    def enregistrer_pokemon(self, pokemon):
        """
        Enregistre un Pokémon rencontré en combat dans le Pokédex
        Effectue une vérification pour éviter les doublons
        
        Args:
            pokemon (Pokemon): Le Pokémon à enregistrer
        
        Returns:
            tuple: (bool, str) - (Succès, Message)
        """
        existe, index = self._pokemon_existe(pokemon.nom)
        
        if existe:
            # Le Pokémon existe déjà, on incrémente le nombre de combats
            self._pokemons_rencontres[index].nombre_combats += 1
            self._sauvegarder()
            return True, f"{pokemon.nom} déjà dans le Pokédex ! Nombre de combats: {self._pokemons_rencontres[index].nombre_combats}"
        else:
            # Nouveau Pokémon, on l'ajoute
            pokemon.date_rencontre = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pokemon.nombre_combats = 1
            self._pokemons_rencontres.append(pokemon)
            self._sauvegarder()
            return True, f"Nouveau Pokémon enregistré dans le Pokédex: {pokemon.nom}!"
    
    def afficher_pokedex(self):
        """
        Affiche l'ensemble des Pokémon rencontrés ainsi que leur nombre
        
        Returns:
            str: Représentation textuelle du Pokédex
        """
        if not self._pokemons_rencontres:
            return "Votre Pokédex est vide. Combattez des Pokémon pour le remplir !"
        
        resultat = f"\n{'='*60}\n"
        resultat += f"POKÉDEX DU DRESSEUR - {len(self._pokemons_rencontres)} Pokémon rencontrés\n"
        resultat += f"{'='*60}\n\n"
        
        for i, pokemon in enumerate(self._pokemons_rencontres, 1):
            resultat += f"{i}. {pokemon.nom} (Niv.{pokemon.niveau})\n"
            resultat += f"   Type: {pokemon.type}\n"
            resultat += f"   PV: {pokemon.pv_max} | Attaque: {pokemon.attaque} | Défense: {pokemon.defense}\n"
            resultat += f"   Combats: {pokemon.nombre_combats} | Rencontré le: {pokemon.date_rencontre}\n"
            resultat += f"   {'-'*56}\n"
        
        resultat += f"\n{'='*60}\n"
        resultat += f"Total: {len(self._pokemons_rencontres)} Pokémon différents\n"
        resultat += f"{'='*60}\n"
        
        return resultat
    
    def obtenir_pokemon(self, nom):
        """
        Récupère un Pokémon du Pokédex par son nom
        
        Args:
            nom (str): Nom du Pokémon
        
        Returns:
            Pokemon ou None: Le Pokémon trouvé ou None
        """
        for pokemon in self._pokemons_rencontres:
            if pokemon.nom.lower() == nom.lower():
                return pokemon
        return None
    
    def obtenir_statistiques(self):
        """
        Retourne des statistiques sur le Pokédex
        
        Returns:
            dict: Statistiques (nombre total, types rencontrés, etc.)
        """
        if not self._pokemons_rencontres:
            return {
                "total": 0,
                "types": {},
                "total_combats": 0
            }
        
        types = {}
        total_combats = 0
        
        for pokemon in self._pokemons_rencontres:
            # Compter les types
            if pokemon.type in types:
                types[pokemon.type] += 1
            else:
                types[pokemon.type] = 1
            
            # Compter les combats
            total_combats += pokemon.nombre_combats
        
        return {
            "total": len(self._pokemons_rencontres),
            "types": types,
            "total_combats": total_combats
        }
    
    @property
    def nombre_pokemon(self):
        """
        Propriété retournant le nombre de Pokémon rencontrés
        Utilise le principe de l'encapsulation (property)
        
        Returns:
            int: Nombre de Pokémon
        """
        return len(self._pokemons_rencontres)
    
    @property
    def pokemons_rencontres(self):
        """
        Propriété retournant la liste des Pokémon (en lecture seule)
        Principe d'encapsulation: accès contrôlé aux données
        
        Returns:
            list: Copie de la liste des Pokémon
        """
        return self._pokemons_rencontres.copy()
    
    def __len__(self):
        """
        Surcharge de l'opérateur len()
        Principe du polymorphisme
        
        Returns:
            int: Nombre de Pokémon dans le Pokédex
        """
        return len(self._pokemons_rencontres)
    
    def __str__(self):
        """
        Représentation en chaîne du Pokédex
        Principe du polymorphisme
        
        Returns:
            str: Description du Pokédex
        """
        return f"Pokédex du dresseur: {len(self._pokemons_rencontres)} Pokémon rencontrés"
    
    def __repr__(self):
        """
        Représentation technique du Pokédex
        
        Returns:
            str: Représentation technique
        """
        return f"Pokedex(fichier='{self.fichier_pokedex}', pokemons={len(self._pokemons_rencontres)})"
