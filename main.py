import pygame
from menu import Menu

def main():
    """Fonction principale du jeu"""
    pygame.init()
    
    # Configuration de la fenêtre
    LARGEUR = 800
    HAUTEUR = 600
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Jeu Pokémon")
    
    # Horloge pour contrôler les FPS
    horloge = pygame.time.Clock()
    
    # Créer le menu
    menu = Menu(ecran)
    
    # Boucle principale
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            
            # Gérer les événements du menu
            menu.gerer_evenement(event)
        
        # Mettre à jour et afficher
        menu.mettre_a_jour()
        menu.afficher()
        
        pygame.display.flip()
        horloge.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
