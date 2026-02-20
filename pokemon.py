"""
Classe Pokemon
Représente un Pokémon avec ses caractéristiques
"""

class Pokemon:
    """Classe représentant un Pokémon"""
    
    def __init__(self, nom, type_pokemon, pv, attaque, defense, niveau=1):
        """
        Initialise un Pokémon
        
        Args:
            nom (str): Nom du Pokémon
            type_pokemon (str): Type du Pokémon (Feu, Eau, Plante, etc.)
            pv (int): Points de vie
            attaque (int): Points d'attaque
            defense (int): Points de défense
            niveau (int): Niveau du Pokémon (par défaut 1)
        """
        self.nom = nom
        self.type = type_pokemon
        self.pv_max = pv
        self.pv_actuel = pv
        self.attaque = attaque
        self.defense = defense
        self.niveau = niveau
    
    def attaquer(self, cible):
        """
        Attaque un autre Pokémon
        
        Args:
            cible (Pokemon): Le Pokémon à attaquer
        
        Returns:
            int: Les dégâts infligés
        """
        degats = max(1, self.attaque - cible.defense // 2)
        cible.recevoir_degats(degats)
        return degats
    
    def recevoir_degats(self, degats):
        """
        Reçoit des dégâts
        
        Args:
            degats (int): Nombre de points de dégâts
        """
        self.pv_actuel = max(0, self.pv_actuel - degats)
    
    def est_ko(self):
        """
        Vérifie si le Pokémon est KO
        
        Returns:
            bool: True si le Pokémon est KO
        """
        return self.pv_actuel <= 0
    
    def soigner(self):
        """Soigne complètement le Pokémon"""
        self.pv_actuel = self.pv_max
    
    def to_dict(self):
        """
        Convertit le Pokémon en dictionnaire pour la sauvegarde
        
        Returns:
            dict: Dictionnaire contenant les informations du Pokémon
        """
        return {
            "nom": self.nom,
            "type": self.type,
            "pv": self.pv_max,
            "attaque": self.attaque,
            "defense": self.defense,
            "niveau": self.niveau
        }
    
    @staticmethod
    def from_dict(data):
        """
        Crée un Pokémon à partir d'un dictionnaire
        
        Args:
            data (dict): Dictionnaire contenant les informations
        
        Returns:
            Pokemon: Un nouveau Pokémon
        """
        return Pokemon(
            data["nom"],
            data["type"],
            data["pv"],
            data["attaque"],
            data["defense"],
            data.get("niveau", 1)
        )
    
    def __str__(self):
        """
        Représentation en chaîne du Pokémon
        
        Returns:
            str: Description du Pokémon
        """
        return f"{self.nom} (Niv.{self.niveau}) - Type: {self.type} - PV: {self.pv_actuel}/{self.pv_max}"
