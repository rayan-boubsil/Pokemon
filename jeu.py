"""
Classe Jeu
Gère la logique du jeu (combat entre Pokémon)
"""
import pygame
import random
from pokemon import Pokemon

class Jeu:
    """Classe gérant une partie de jeu"""
    
    # États du jeu
    ETAT_SELECTION = 0
    ETAT_COMBAT = 1
    ETAT_VICTOIRE = 2
    ETAT_DEFAITE = 3
    
    def __init__(self, ecran, pokedex):
        """
        Initialise une partie
        
        Args:
            ecran: Surface Pygame pour l'affichage
            pokedex: Instance du Pokédex
        """
        self.ecran = ecran
        self.largeur = ecran.get_width()
        self.hauteur = ecran.get_height()
        self.pokedex = pokedex
        
        # Polices
        self.police_titre = pygame.font.Font(None, 48)
        self.police_texte = pygame.font.Font(None, 32)
        self.police_petite = pygame.font.Font(None, 24)
        
        # Couleurs
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        self.ROUGE = (220, 50, 50)
        self.BLEU = (50, 120, 220)
        self.VERT = (50, 200, 50)
        self.GRIS = (150, 150, 150)
        self.JAUNE = (255, 220, 0)
        
        # État du jeu
        self.etat = self.ETAT_SELECTION
        self.retour_menu = False
        
        # Pokémon du joueur et adversaire
        self.pokemon_joueur = None
        self.pokemon_adversaire = None
        
        # Sélection
        self.liste_pokemons = self.pokedex.pokemons.copy()
        self.selection_index = 0
        
        # Combat
        self.message_combat = "Que voulez-vous faire ?"
        self.actions = ["Attaquer", "Retour au menu"]
        self.action_selectionnee = 0
        self.attente = False
        self.temps_attente = 0
    
    def gerer_evenement(self, event):
        """
        Gère les événements du jeu
        
        Args:
            event: Événement Pygame
        """
        if self.etat == self.ETAT_SELECTION:
            self._gerer_selection(event)
        elif self.etat == self.ETAT_COMBAT:
            self._gerer_combat(event)
        elif self.etat == self.ETAT_VICTOIRE or self.etat == self.ETAT_DEFAITE:
            self._gerer_fin(event)
    
    def _gerer_selection(self, event):
        """Gère la sélection du Pokémon"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.retour_menu = True
            elif event.key == pygame.K_UP:
                self.selection_index = (self.selection_index - 1) % len(self.liste_pokemons)
            elif event.key == pygame.K_DOWN:
                self.selection_index = (self.selection_index + 1) % len(self.liste_pokemons)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._demarrer_combat()
    
    def _gerer_combat(self, event):
        """Gère les actions pendant le combat"""
        if self.attente:
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.action_selectionnee = (self.action_selectionnee - 1) % len(self.actions)
            elif event.key == pygame.K_RIGHT:
                self.action_selectionnee = (self.action_selectionnee + 1) % len(self.actions)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.action_selectionnee == 0:  # Attaquer
                    self._executer_tour_combat()
                elif self.action_selectionnee == 1:  # Retour
                    self.retour_menu = True
    
    def _gerer_fin(self, event):
        """Gère la fin de partie"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                self.retour_menu = True
    
    def _demarrer_combat(self):
        """Démarre un combat"""
        # Créer une copie du Pokémon sélectionné pour le joueur
        pokemon_original = self.liste_pokemons[self.selection_index]
        self.pokemon_joueur = Pokemon(
            pokemon_original.nom,
            pokemon_original.type,
            pokemon_original.pv_max,
            pokemon_original.attaque,
            pokemon_original.defense,
            pokemon_original.niveau
        )
        
        # Choisir un adversaire aléatoire (différent du joueur)
        adversaires_possibles = [p for p in self.liste_pokemons 
                                 if p.nom != pokemon_original.nom]
        if adversaires_possibles:
            pokemon_adv_original = random.choice(adversaires_possibles)
            self.pokemon_adversaire = Pokemon(
                pokemon_adv_original.nom,
                pokemon_adv_original.type,
                pokemon_adv_original.pv_max,
                pokemon_adv_original.attaque,
                pokemon_adv_original.defense,
                pokemon_adv_original.niveau
            )
        else:
            # Si un seul Pokémon, créer un clone
            self.pokemon_adversaire = Pokemon(
                pokemon_original.nom + " Sauvage",
                pokemon_original.type,
                pokemon_original.pv_max,
                pokemon_original.attaque,
                pokemon_original.defense,
                pokemon_original.niveau
            )
        
        self.etat = self.ETAT_COMBAT
        self.message_combat = f"Un {self.pokemon_adversaire.nom} sauvage apparaît !"
    
    def _executer_tour_combat(self):
        """Exécute un tour de combat"""
        self.attente = True
        self.temps_attente = pygame.time.get_ticks()
        
        # Le joueur attaque
        degats_joueur = self.pokemon_joueur.attaquer(self.pokemon_adversaire)
        self.message_combat = f"{self.pokemon_joueur.nom} inflige {degats_joueur} dégâts !"
        
        # Vérifier si l'adversaire est KO
        if self.pokemon_adversaire.est_ko():
            self.etat = self.ETAT_VICTOIRE
            self.message_combat = f"{self.pokemon_adversaire.nom} est K.O. ! Vous avez gagné !"
            return
        
    def mettre_a_jour(self):
        """Met à jour l'état du jeu"""
        if self.attente:
            temps_actuel = pygame.time.get_ticks()
            if temps_actuel - self.temps_attente > 1500:  # Attendre 1.5 secondes
                # L'adversaire riposte
                if not self.pokemon_adversaire.est_ko():
                    degats_adversaire = self.pokemon_adversaire.attaquer(self.pokemon_joueur)
                    self.message_combat = f"{self.pokemon_adversaire.nom} riposte et inflige {degats_adversaire} dégâts !"
                    
                    # Vérifier si le joueur est KO
                    if self.pokemon_joueur.est_ko():
                        self.etat = self.ETAT_DEFAITE
                        self.message_combat = f"{self.pokemon_joueur.nom} est K.O. ! Vous avez perdu..."
                    else:
                        self.message_combat = "Que voulez-vous faire ?"
                
                self.attente = False
    
    def afficher(self):
        """Affiche l'écran de jeu"""
        if self.etat == self.ETAT_SELECTION:
            self._afficher_selection()
        elif self.etat == self.ETAT_COMBAT:
            self._afficher_combat()
        elif self.etat == self.ETAT_VICTOIRE:
            self._afficher_victoire()
        elif self.etat == self.ETAT_DEFAITE:
            self._afficher_defaite()
    
    def _afficher_selection(self):
        """Affiche l'écran de sélection"""
        self.ecran.fill(self.BLEU)
        
        # Titre
        titre = self.police_titre.render("CHOISISSEZ VOTRE POKÉMON", True, self.JAUNE)
        rect_titre = titre.get_rect(center=(self.largeur // 2, 50))
        self.ecran.blit(titre, rect_titre)
        
        # Liste des Pokémon
        y_start = 150
        for i, pokemon in enumerate(self.liste_pokemons):
            y = y_start + i * 60
            
            # Fond pour le Pokémon sélectionné
            if i == self.selection_index:
                pygame.draw.rect(self.ecran, self.JAUNE, (50, y - 5, self.largeur - 100, 50))
            
            # Informations
            couleur = self.NOIR if i == self.selection_index else self.BLANC
            texte = self.police_texte.render(str(pokemon), True, couleur)
            self.ecran.blit(texte, (60, y))
        
        # Instructions
        instruction = self.police_petite.render("↑↓: Choisir | ENTRÉE: Valider | ESC: Retour", True, self.BLANC)
        rect_inst = instruction.get_rect(center=(self.largeur // 2, self.hauteur - 40))
        self.ecran.blit(instruction, rect_inst)
    
    def _afficher_combat(self):
        """Affiche l'écran de combat"""
        self.ecran.fill(self.VERT)
        
        # Titre
        titre = self.police_titre.render("COMBAT POKÉMON", True, self.BLANC)
        rect_titre = titre.get_rect(center=(self.largeur // 2, 40))
        self.ecran.blit(titre, rect_titre)
        
        # Pokémon du joueur (en bas à gauche)
        self._afficher_pokemon_combat(self.pokemon_joueur, 100, 400, True)
        
        # Pokémon adversaire (en haut à droite)
        self._afficher_pokemon_combat(self.pokemon_adversaire, 500, 150, False)
        
        # Message de combat
        pygame.draw.rect(self.ecran, self.BLANC, (50, 300, self.largeur - 100, 80))
        pygame.draw.rect(self.ecran, self.NOIR, (50, 300, self.largeur - 100, 80), 3)
        texte_msg = self.police_texte.render(self.message_combat, True, self.NOIR)
        self.ecran.blit(texte_msg, (70, 320))
        
        # Actions disponibles (si pas en attente)
        if not self.attente:
            y_actions = 500
            for i, action in enumerate(self.actions):
                x = 150 + i * 250
                couleur = self.JAUNE if i == self.action_selectionnee else self.BLANC
                pygame.draw.rect(self.ecran, couleur, (x, y_actions, 200, 50))
                pygame.draw.rect(self.ecran, self.NOIR, (x, y_actions, 200, 50), 3)
                
                texte = self.police_texte.render(action, True, self.NOIR)
                rect_texte = texte.get_rect(center=(x + 100, y_actions + 25))
                self.ecran.blit(texte, rect_texte)
            
            # Instructions
            instruction = self.police_petite.render("←→: Choisir action | ENTRÉE: Confirmer", True, self.BLANC)
            rect_inst = instruction.get_rect(center=(self.largeur // 2, 570))
            self.ecran.blit(instruction, rect_inst)
    
    def _afficher_pokemon_combat(self, pokemon, x, y, est_joueur):
        """
        Affiche un Pokémon pendant le combat
        
        Args:
            pokemon (Pokemon): Le Pokémon à afficher
            x (int): Position X
            y (int): Position Y
            est_joueur (bool): True si c'est le Pokémon du joueur
        """
        # Cadre
        largeur_cadre = 250
        hauteur_cadre = 120
        pygame.draw.rect(self.ecran, self.BLANC, (x, y, largeur_cadre, hauteur_cadre))
        pygame.draw.rect(self.ecran, self.NOIR, (x, y, largeur_cadre, hauteur_cadre), 3)
        
        # Nom
        texte_nom = self.police_texte.render(pokemon.nom, True, self.NOIR)
        self.ecran.blit(texte_nom, (x + 10, y + 10))
        
        # Type
        texte_type = self.police_petite.render(f"Type: {pokemon.type}", True, self.NOIR)
        self.ecran.blit(texte_type, (x + 10, y + 40))
        
        # Barre de PV
        texte_pv = self.police_petite.render(f"PV: {pokemon.pv_actuel}/{pokemon.pv_max}", True, self.NOIR)
        self.ecran.blit(texte_pv, (x + 10, y + 65))
        
        # Barre de PV graphique
        ratio_pv = pokemon.pv_actuel / pokemon.pv_max
        couleur_barre = self.VERT if ratio_pv > 0.5 else (self.JAUNE if ratio_pv > 0.2 else self.ROUGE)
        pygame.draw.rect(self.ecran, self.GRIS, (x + 10, y + 90, 230, 20))
        pygame.draw.rect(self.ecran, couleur_barre, (x + 10, y + 90, int(230 * ratio_pv), 20))
        pygame.draw.rect(self.ecran, self.NOIR, (x + 10, y + 90, 230, 20), 2)
    
    def _afficher_victoire(self):
        """Affiche l'écran de victoire"""
        self.ecran.fill(self.VERT)
        
        # Message de victoire
        titre = self.police_titre.render("VICTOIRE !", True, self.JAUNE)
        rect_titre = titre.get_rect(center=(self.largeur // 2, 200))
        self.ecran.blit(titre, rect_titre)
        
        message = self.police_texte.render(self.message_combat, True, self.BLANC)
        rect_msg = message.get_rect(center=(self.largeur // 2, 300))
        self.ecran.blit(message, rect_msg)
        
        # Instruction
        instruction = self.police_petite.render("Appuyez sur ENTRÉE pour retourner au menu", True, self.BLANC)
        rect_inst = instruction.get_rect(center=(self.largeur // 2, 400))
        self.ecran.blit(instruction, rect_inst)
    
    def _afficher_defaite(self):
        """Affiche l'écran de défaite"""
        self.ecran.fill(self.ROUGE)
        
        # Message de défaite
        titre = self.police_titre.render("DÉFAITE...", True, self.BLANC)
        rect_titre = titre.get_rect(center=(self.largeur // 2, 200))
        self.ecran.blit(titre, rect_titre)
        
        message = self.police_texte.render(self.message_combat, True, self.BLANC)
        rect_msg = message.get_rect(center=(self.largeur // 2, 300))
        self.ecran.blit(message, rect_msg)
        
        # Instruction
        instruction = self.police_petite.render("Appuyez sur ENTRÉE pour retourner au menu", True, self.BLANC)
        rect_inst = instruction.get_rect(center=(self.largeur // 2, 400))
        self.ecran.blit(instruction, rect_inst)
