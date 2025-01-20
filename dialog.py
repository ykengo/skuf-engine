"""
Dialog System Module for Visual Novel Game Engine

This module handles dialog boxes, text rendering, and dialog progression.
Supports optional character portraits and text animations.

Classes:
    Dialog: Main dialog box implementation with text rendering and animation
"""

import pygame
import os
import logging

pygame.init()
defF = os.path.join("font", "DejaVuSans.ttf")

class Dialog(pygame.sprite.Sprite):
    """
    Dialog box that displays text with optional character portraits
    
    Attributes:
        image: Dialog box background surface
        rect: Position rectangle for dialog box
        photo: Optional character portrait
        message: Tuple containing dialog text
        show: Boolean controlling dialog visibility
    """
    
    def __init__(self, screen, photo=None):
        """
        Initialize dialog box
        
        Args:
            screen: Pygame surface to render dialog on
            photo: Optional path to character portrait image
        """
        try:
            pygame.sprite.Sprite.__init__(self)
            # Load dialog box background
            self.image = pygame.image.load("image/49.png").convert()
        except pygame.error:
            logging.error("Could not load dialog background")
            # Fallback to black rectangle if image fails to load
            self.image = pygame.Surface((800, 200))
            self.image.fill((0, 0, 0))
        except Exception as e:
            logging.error(f"Dialog initialization error: {str(e)}")
            
        # Setup dialog box positioning
        self.rect = self.image.get_rect()
        self.rect.center = (400, 530)
        self.image.set_alpha(220)  # Set transparency
        
        # Load character portrait if provided
        if photo:
            self.photo = pygame.image.load(photo).convert_alpha()
        else:
            self.photo = None
            
        # Initialize text rendering
        self.dFont = pygame.font.Font(defF, 16)  # Dialog font
        self.message = ()
        self.screen = screen
        
        # Setup next page indicator
        self.nextImage = pygame.image.load('next.png').convert_alpha()
        self.nextImageRect = self.nextImage.get_rect()
        self.nextImageRect.right = 410
        self.nextImageRect.bottom = 120
        self.show = True

    def reset(self):
        """Reset dialog box state"""
        pass

    def sndNext(self):
        """
        Handle text progression and animation
        
        Controls text rendering, pagination and typing animation
        """
        if not self.message:
            return
            
        # Text progression variables
        outOfText = False      # Flag for text completion
        line = 0              # Current line being rendered
        lineCount = 0         # Total lines rendered
        startLine = 0         # First visible line
        nextPage = False      # Flag for next page
        text_pos = 0         # Character position in current text
        text = ""            # Current text being rendered
        delayTimer = 30      # Animation delay timer
        textSurf = None      # Text surface for rendering

        textImage = pygame.Surface(self.image.get_size())
        textImage.fill((0,0,0))
        textImage.set_colorkey((0,0,0))
        lastScreen = pygame.Surface(self.screen.get_size())
        lastScreen.blit(self.screen, (0,0))
        while self.show:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if not outOfText and not nextPage:
                            delayTimer = 0
                            continue
                        elif nextPage:
                            nextPage = False
                            textImage = pygame.Surface(self.image.get_size())
                            textImage.fill((0,0,0))
                            textImage.set_colorkey((0,0,0))
                            delayTimer = 30
                            continue
                        self.show = False
            if not outOfText and not nextPage:
                pygame.time.delay(delayTimer)
                text += self.message[line][text_pos]
                text_pos += 1
                if text_pos > len(self.message[line])-1:
                    textImage.blit(textSurf, (34, lineCount * 20 + 4))
                    textImage.set_colorkey((0,0,0))
                    text_pos = 0
                    line += 1
                    lineCount += 1
                    text = ""
                    if lineCount > 6:
                        nextPage = True
                        lineCount = 0
                        text = ""
                        text_pos = 0
                if line > len(self.message)-1:
                    outOfText = True
                if outOfText or nextPage:
                    textImage.blit(self.nextImage, self.nextImageRect)
                textSurf = self.dFont.render(text, 0, (255,255,255,0))
            self.screen.blit(lastScreen, (0,0))
            self.screen.blit(self.image, self.rect )
            self.screen.blit(textSurf, (self.rect.left + 34,lineCount * 20 + 4 + self.rect.top))
            self.screen.blit(textImage, self.rect)
            pygame.draw.rect(self.screen, (255,255,255), (self.rect), 2)
            if self.photo:
                self.screen.blit(self.photo, (150, 170))
            pygame.display.flip()
        self.screen.blit(lastScreen, (0,0))