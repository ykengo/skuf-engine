"""
Menu system for visual novel game
Handles menu creation, rendering and user interaction
"""

import pygame
import os
pygame.init()
defF = os.path.join("font", "DejaVuSans.ttf")

class Menu:
    """
    Individual menu item that can be selected/hovered
    """
    hovered = False
    
    def __init__(self, text, pos, font_size=30):
        """Initialize menu item with text and position"""
        self.text = text  # Text to display
        self.pos = pos    # (x,y) position  
        self.font = pygame.font.Font(defF, font_size)
        self.set_rect()
        self.set_rend()
    
    def draw(self, surface):
        """Draw menu item to surface"""
        surface.blit(self.rend, self.rect)

    def set_rend(self):
        """Update rendered text surface"""
        self.rend = self.font.render(self.text, True, self.get_color())
        
    def get_color(self):
        """Get color based on hover state"""
        return (255, 255, 255) if self.hovered else (65, 105, 255)
            
    def set_rect(self):
        """Update text rectangle position"""
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

def generate_menu(screen, menu_items, background_image=None):
    """
    Generate and handle menu system
    Args:
        screen: Pygame surface to draw on
        menu_items: List of menu item texts
        background_image: Optional background image
    Returns:
        Selected menu item text or None
    """
    try:
        # Create menu items
        menus = []
        y_pos = 205  # Starting Y position
        
        # Create menu items with increasing Y positions
        for item in menu_items:
            menus.append(Menu(item, (340, y_pos)))
            y_pos += 50
            
        running = True
        
        # Main menu loop
        while running:
            # Draw background if provided
            if background_image:
                screen.blit(background_image, (0, 0))
                
            pygame.event.pump()
            
            # Update and draw menu items
            for menu in menus:
                # Check for mouse hover
                if menu.rect.collidepoint(pygame.mouse.get_pos()):
                    menu.hovered = True
                else:
                    menu.hovered = False
                menu.draw(screen)
                
            pygame.display.flip()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check for clicked menu item
                    for menu in menus:
                        if menu.hovered:
                            return menu.text
                            
            pygame.time.Clock().tick(30)  # Cap framerate
            
    except Exception as e:
        logging.error(f"Menu generation error: {str(e)}")
        return None