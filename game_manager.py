"""
Game Manager Module for Visual Novel Engine

Coordinates dialog and menu systems, manages game state and screen rendering.
Acts as a facade for the dialog and menu subsystems.

Classes:
    GameManager: Main coordinator class for game systems
"""

import pygame
from dialog import Dialog
from menu import Menu, generate_menu
import logging
from typing import List, Optional

class GameManager:
    """
    Coordinates dialog and menu systems for the visual novel engine
    
    Handles:
    - Dialog box display and progression
    - Menu generation and interaction
    - Background management
    - Screen state coordination
    
    Attributes:
        screen: Main pygame surface for rendering
        dialog: Dialog system instance
    """
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize game manager
        
        Args:
            screen: Pygame surface to render game elements on
        """
        self.screen = screen
        self.dialog = Dialog(screen)
        
    def show_dialogs(self, dialog_list: List[str], background: Optional[object] = None):
        """
        Display a sequence of dialog messages
        
        Args:
            dialog_list: List of dialog messages to display
            background: Optional background object to render behind dialogs
        """
        # Draw background if provided
        if background:
            background.back()
            
        # Process each dialog message
        for message in dialog_list:
            self.dialog.message = (message,)
            self.dialog.show = True
            self.dialog.sndNext()
            
    def show_menu(self, menu_items: List[str], background_image: Optional[pygame.Surface] = None):
        """
        Display menu and handle selection
        
        Args:
            menu_items: List of menu options to display
            background_image: Optional background image for menu
            
        Returns:
            str: Selected menu item text or None if no selection
        """
        return generate_menu(self.screen, menu_items, background_image)