
import pygame
from pokedex import Pokedex
from pokemon import Pokemon
from jeu import Jeu

class Menu:
    """Classe gérant le menu principal"""
    
    # États du menu
    ETAT_PRINCIPAL = 0
    ETAT_JEU = 1
    ETAT_AJOUTER = 2
    ETAT_POKEDEX = 3
    
    def __init__(self, ecran):
        """
        Initialise le menu
        """
        self.ecran = ecran
        self.largeur = ecran.get_width()
        self.hauteur = ecran.get_height()
        self.etat = self.ETAT_PRINCIPAL
        
        # Polices
        self.police_titre = pygame.font.Font(None, 64)
        self.police_menu = pygame.font.Font(None, 36)
        self.police_texte = pygame.font.Font(None, 28)
        
        # Couleurs
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.ROUGE = (220, 50, 50)
        self.BLEU = (50, 120, 220)
        self.VERT = (50, 200, 50)
        self.GRIS = (150, 150, 150)
        self.JAUNE = (255, 220, 0)
        
        # Options du menu principal
        self.options_menu = [
            "Lancer une partie",
            "Ajouter un Pokémon",
            "Accéder au Pokédex",
            "Quitter"
        ]
        self.option_selectionnee = 0
        
        # Pokédex
        self.pokedex = Pokedex()
        
        # Jeu
        self.jeu = None
        
        # Pour l'ajout de Pokémon
        self.champs_formulaire = {
            "nom": "",
            "type": "",
            "pv": "",
            "attaque": "",
            "defense": "",
            "niveau": ""
        }
        self.champ_actif = "nom"
        self.ordre_champs = ["nom", "type", "pv", "attaque", "defense", "niveau"]
        self.message_formulaire = ""
        
        # Scroll pour le Pokédex
        self.scroll_pokedex = 0
    
    def gerer_evenement(self, event):
        """
        Gère les événements (clavier, souris)
        
        Args:
            event: Événement Pygame
        """
        if self.etat == self.ETAT_PRINCIPAL:
            self._gerer_menu_principal(event)
        elif self.etat == self.ETAT_JEU:
            if self.jeu:
                self.jeu.gerer_evenement(event)
                if self.jeu.retour_menu:
                    self.etat = self.ETAT_PRINCIPAL
                    self.jeu = None
        elif self.etat == self.ETAT_AJOUTER:
            self._gerer_formulaire(event)
        elif self.etat == self.ETAT_POKEDEX:
            self._gerer_pokedex(event)
    
    def _gerer_menu_principal(self, event):
        """Gère les événements du menu principal"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.option_selectionnee = (self.option_selectionnee - 1) % len(self.options_menu)
            elif event.key == pygame.K_DOWN:
                self.option_selectionnee = (self.option_selectionnee + 1) % len(self.options_menu)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._executer_option()
    
    def _gerer_formulaire(self, event):
        """Gère les événements du formulaire d'ajout de Pokémon"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.etat = self.ETAT_PRINCIPAL
                self._reinitialiser_formulaire()
            elif event.key == pygame.K_TAB:
                # Passer au champ suivant
                index_actuel = self.ordre_champs.index(self.champ_actif)
                self.champ_actif = self.ordre_champs[(index_actuel + 1) % len(self.ordre_champs)]
            elif event.key == pygame.K_RETURN:
                self._soumettre_formulaire()
            elif event.key == pygame.K_BACKSPACE:
                self.champs_formulaire[self.champ_actif] = self.champs_formulaire[self.champ_actif][:-1]
            else:
                # Ajouter le caractère
                if event.unicode.isprintable():
                    self.champs_formulaire[self.champ_actif] += event.unicode
    
    def _gerer_pokedex(self, event):
        """Gère les événements de l'affichage du Pokédex"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.etat = self.ETAT_PRINCIPAL
            elif event.key == pygame.K_UP:
                self.scroll_pokedex = max(0, self.scroll_pokedex - 1)
            elif event.key == pygame.K_DOWN:
                self.scroll_pokedex = min(len(self.pokedex.pokemons) - 1, self.scroll_pokedex + 1)
    
    def _executer_option(self):
        """Exécute l'option sélectionnée du menu"""
        if self.option_selectionnee == 0:  # Lancer une partie
            self.jeu = Jeu(self.ecran, self.pokedex)
            self.etat = self.ETAT_JEU
        elif self.option_selectionnee == 1:  # Ajouter un Pokémon
            self.etat = self.ETAT_AJOUTER
            self._reinitialiser_formulaire()
        elif self.option_selectionnee == 2:  # Pokédex
            self.etat = self.ETAT_POKEDEX
            self.scroll_pokedex = 0
        elif self.option_selectionnee == 3:  # Quitter
            pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def _soumettre_formulaire(self):
        """Soumet le formulaire d'ajout de Pokémon"""
        try:
            nom = self.champs_formulaire["nom"].strip()
            type_pokemon = self.champs_formulaire["type"].strip()
            pv = int(self.champs_formulaire["pv"])
            attaque = int(self.champs_formulaire["attaque"])
            defense = int(self.champs_formulaire["defense"])
            niveau = int(self.champs_formulaire["niveau"]) if self.champs_formulaire["niveau"] else 1
            
            if not nom or not type_pokemon:
                self.message_formulaire = "Le nom et le type sont obligatoires!"
                return
            
            if pv <= 0 or attaque <= 0 or defense <= 0:
                self.message_formulaire = "Les stats doivent être positives!"
                return
            
            nouveau_pokemon = Pokemon(nom, type_pokemon, pv, attaque, defense, niveau)
            
            if self.pokedex.ajouter_pokemon(nouveau_pokemon):
                self.message_formulaire = f"{nom} ajouté avec succès!"
                # Retour au menu après 2 secondes
                pygame.time.set_timer(pygame.USEREVENT, 2000)
            else:
                self.message_formulaire = f"{nom} existe déjà dans le Pokédex!"
        
        except ValueError:
            self.message_formulaire = "Erreur: Vérifiez les valeurs numériques!"
    
    def _reinitialiser_formulaire(self):
        """Réinitialise le formulaire"""
        for cle in self.champs_formulaire:
            self.champs_formulaire[cle] = ""
        self.champ_actif = "nom"
        self.message_formulaire = ""
    
    def mettre_a_jour(self):
        """Met à jour l'état du menu"""
        if self.etat == self.ETAT_JEU and self.jeu:
            self.jeu.mettre_a_jour()
        
        # Gérer le timer pour retour au menu après ajout
        for event in pygame.event.get(pygame.USEREVENT):
            if self.etat == self.ETAT_AJOUTER and self.message_formulaire:
                self.etat = self.ETAT_PRINCIPAL
                self._reinitialiser_formulaire()
    
    def afficher(self):
        """Affiche le menu ou l'écran actuel"""
        if self.etat == self.ETAT_PRINCIPAL:
            self._afficher_menu_principal()
        elif self.etat == self.ETAT_JEU:
            if self.jeu:
                self.jeu.afficher()
        elif self.etat == self.ETAT_AJOUTER:
            self._afficher_formulaire()
        elif self.etat == self.ETAT_POKEDEX:
            self._afficher_pokedex()
    
    def _afficher_menu_principal(self):
        """Affiche le menu principal"""
        self.ecran.fill(self.BLEU)
        
        # Titre
        titre = self.police_titre.render("JEU POKÉMON", True, self.JAUNE)
        rect_titre = titre.get_rect(center=(self.largeur // 2, 100))
        self.ecran.blit(titre, rect_titre)
        
        # Options du menu
        y_start = 250
        for i, option in enumerate(self.options_menu):
            couleur = self.JAUNE if i == self.option_selectionnee else self.BLANC
            texte = self.police_menu.render(option, True, couleur)
            rect = texte.get_rect(center=(self.largeur // 2, y_start + i * 60))
            self.ecran.blit(texte, rect)
            
            # Indicateur pour l'option sélectionnée
            if i == self.option_selectionnee:
                pygame.draw.rect(self.ecran, self.JAUNE, rect, 3)
        
        # Instructions
        instruction = self.police_texte.render("↑↓: Naviguer | ENTRÉE: Sélectionner", True, self.BLANC)
        rect_inst = instruction.get_rect(center=(self.largeur // 2, self.hauteur - 50))
        self.ecran.blit(instruction, rect_inst)
    
    def _afficher_formulaire(self):
        """Affiche le formulaire d'ajout de Pokémon"""
        self.ecran.fill(self.VERT)
        
        # Titre
        titre = self.police_titre.render("AJOUTER UN POKÉMON", True, self.BLANC)
        rect_titre = titre.get_rect(center=(self.largeur // 2, 60))
        self.ecran.blit(titre, rect_titre)
        
        # Formulaire
        y_start = 150
        labels = {
            "nom": "Nom:",
            "type": "Type:",
            "pv": "PV:",
            "attaque": "Attaque:",
            "defense": "Défense:",
            "niveau": "Niveau:"
        }
        
        for i, champ in enumerate(self.ordre_champs):
            y = y_start + i * 60
            
            # Label
            label = self.police_texte.render(labels[champ], True, self.BLANC)
            self.ecran.blit(label, (150, y))
            
            # Champ de saisie
            couleur_champ = self.JAUNE if champ == self.champ_actif else self.BLANC
            rect_champ = pygame.Rect(300, y - 5, 350, 40)
            pygame.draw.rect(self.ecran, couleur_champ, rect_champ, 2)
            
            # Texte saisi
            texte = self.police_texte.render(self.champs_formulaire[champ], True, self.BLANC)
            self.ecran.blit(texte, (310, y))
        
        # Message
        if self.message_formulaire:
            couleur_msg = self.ROUGE if "Erreur" in self.message_formulaire or "existe" in self.message_formulaire else self.JAUNE
            message = self.police_texte.render(self.message_formulaire, True, couleur_msg)
            rect_msg = message.get_rect(center=(self.largeur // 2, y_start + 380))
            self.ecran.blit(message, rect_msg)
        
        # Instructions
        instructions = [
            "TAB: Champ suivant | ENTRÉE: Valider | ESC: Annuler"
        ]
        for i, inst in enumerate(instructions):
            texte = self.police_texte.render(inst, True, self.BLANC)
            rect = texte.get_rect(center=(self.largeur // 2, self.hauteur - 50 + i * 30))
            self.ecran.blit(texte, rect)
    
    def _afficher_pokedex(self):
        """Affiche le Pokédex"""
        self.ecran.fill(self.ROUGE)
        
        # Titre
        titre = self.police_titre.render("POKÉDEX", True, self.JAUNE)
        rect_titre = titre.get_rect(center=(self.largeur // 2, 60))
        self.ecran.blit(titre, rect_titre)
        
        # Nombre de Pokémon
        info = self.police_texte.render(f"{len(self.pokedex)} Pokémon disponibles", True, self.BLANC)
        self.ecran.blit(info, (50, 120))
        
        # Liste des Pokémon
        y_start = 180
        max_affichage = 8
        debut = max(0, self.scroll_pokedex - max_affichage // 2)
        fin = min(len(self.pokedex.pokemons), debut + max_affichage)
        
        for i in range(debut, fin):
            pokemon = self.pokedex.pokemons[i]
            y = y_start + (i - debut) * 45
            
            # Fond pour le Pokémon sélectionné
            if i == self.scroll_pokedex:
                pygame.draw.rect(self.ecran, self.JAUNE, (40, y - 5, self.largeur - 80, 40))
            
            # Informations du Pokémon
            couleur = self.NOIR if i == self.scroll_pokedex else self.BLANC
            texte = self.police_texte.render(
                f"{pokemon.nom} - {pokemon.type} | PV: {pokemon.pv_max} | ATT: {pokemon.attaque} | DEF: {pokemon.defense}",
                True, couleur
            )
            self.ecran.blit(texte, (50, y))
        
        # Instructions
        instruction = self.police_texte.render("↑↓: Naviguer | ESC/ENTRÉE: Retour", True, self.BLANC)
        rect_inst = instruction.get_rect(center=(self.largeur // 2, self.hauteur - 50))
        self.ecran.blit(instruction, rect_inst)
