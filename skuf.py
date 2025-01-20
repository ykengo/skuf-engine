"""
Visual Novel Game Engine: 'Скуф Приближается'

A humorous visual novel about a peculiar mechanic named Skuf and his adventures.
Features dialog system, choice-based narrative, and multiple endings.

Game Structure:
- Main menu with game options
- Multiple branching story paths
- Character interactions through dialog system
- Sound effects and background music
- Scene transitions and backgrounds

Dependencies:
    pygame: Game engine and graphics
    logging: Event and error tracking
    dialog: Custom dialog system
    menu: Custom menu system
    game_manager: Game state coordination
"""

import os
import pygame
from pygame.locals import *
from dialog import Dialog
from menu import generate_menu
from datetime import datetime
import logging
from game_manager import GameManager

# === System Configuration ===
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# === Pygame Initialization ===
pygame.mixer.pre_init(44100, -16, 2, 2048)  # Audio setup for better sound quality
pygame.init()

# === Game Constants ===
COLORS = {
    'red': (255, 0, 0),     # Used for warnings and bad endings
    'green': (81, 220, 55),  # Used for help text and good choices
    'blue': (0, 0, 255),    # Used for highlights
    'black': (0, 0, 0),     # Used for backgrounds
    'yellow': (255, 255, 0), # Used for emphasis
    'white': (255, 255, 255) # Used for regular text
}

# === Display Setup ===
SCREEN_SIZE = (800, 600)  # Standard visual novel resolution
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Скуф Приближается')
clock = pygame.time.Clock()

# === Asset Loading ===
# Load and prepare game assets (images, sounds, etc.)
end = pygame.image.load(os.path.join("image/end/end1.jpg"))
pygame.mixer.music.load(os.path.join('audio', 'theme.ogg'))
click = pygame.mixer.Sound(os.path.join('audio','click.wav'))

# === Helper Functions ===
def show_dialogs(dialog_list: list, background=None) -> None:
    """
    Display a sequence of dialog messages with optional background
    
    Args:
        dialog_list: List of strings containing dialog messages
        background: Optional background scene to display
    """
    if background:
        background.back()
    dialog = Dialog(screen)
    for message in dialog_list:
        dialog.message = (message,)
        dialog.show = True
        dialog.sndNext()

# === Scene Management ===
class Fon:
    """
    Background scene manager
    
    Handles loading and displaying background images for different scenes
    """
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        try:
            self.bitmap = pygame.image.load(os.path.join("image", "backgrounds", filename))
        except pygame.error:
            logging.error(f"Could not load background: {filename}")
            self.bitmap = pygame.Surface(SCREEN_SIZE)
            self.bitmap.fill(COLORS['black'])

    def back(self):    
        screen.blit(self.bitmap, (self.x, self.y))

# Background instances
bg1 = Fon(0, 0, "bg1.jpg")
bg2 = Fon(0, 0, "bg2.jpg")
bg3 = Fon(0, 0, "bg3.jpg")
bg4 = Fon(0, 0, "bg4.jpg")

# Initialize game manager
game_manager = GameManager(screen)

# === Game Scenes ===
def mmenu() -> None:
    """
    Main menu scene
    
    Displays:
    - New Game option
    - Help option
    - Exit option
    
    Transitions to:
    - novel() for new game
    - helps() for help screen
    - exit() to quit
    """
    try:
        menu_items = ["НОВАЯ ИГРА", "ПОМОЩЬ", "ВЫХОД"]
        selected = generate_menu(screen, menu_items, end)
        if selected == "НОВАЯ ИГРА":
            click.play()
            novel()
        elif selected == "ПОМОЩЬ":
            click.play()
            helps()
        elif selected == "ВЫХОД":
            logging.info("Game exited from menu")
            exit()
    except Exception as e:
        logging.error(f"Error in menu: {str(e)}")
        exit()

def helps():
    screen.blit(end, (0, 0))
    help_texts = [
        ("Управление Игрой", 300, 10),
        ("Для продвижения вперед, нажмите пробел или клавишу \"Enter\".", 140, 30),
        ("Для выбора, воспользуйтесь мышью.", 140, 60)
    ]
    
    while True:
        for text, x, y in help_texts:
            font = pygame.font.SysFont("DejaVuSans.ttf", 30)
            label = font.render(text, 0, COLORS['green'])
            screen.blit(label, (x, y))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                click.play()
                return mmenu()

def novel():
    logging.info("Starting novel sequence")
    dialogs = [
        "?:Египетская сила!",
        "?:Что стоишь иди помоги мне с моей ласточкой.",
        "Скуф:Я Петрович, для тебя могу быть скуфом, называй как хочешь.",
        "Cкуф:Подай ключ на (что-то невнятное)."
    ]
    game_manager.show_dialogs(dialogs, bg1)
    
    menu_items = ["Подать ключ на 10.", "Подать ключ на 15."]
    selected = game_manager.show_menu(menu_items)
    
    if selected == "Подать ключ на 10.":
        logging.info("Player chose: Подать ключ на 10")
        click.play()
        whot()
    elif selected == "Подать ключ на 15.":
        logging.info("Player chose: Подать ключ на 15")
        click.play()
        fix()

def whot():
    screen.fill((0, 0, 0))
    while True:
        font = pygame.font.SysFont("DejaVuSans.ttf", 35)
        texts = [
            ("Вы погубили своего героя, попробуйте пройти снова,", 100, 280),
            ("возможно вам понравиться.", 100, 310),
            ("Вы были залиты пивом", 100, 340)
        ]
        for text, x, y in texts:
            label = font.render(text, 0, COLORS['red'])
            screen.blit(label, (x, y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                click.play()
                mmenu()

def fix():
    logging.info("Starting fix sequence")
    dialogs = [
        "А ты молодец, красавчик я бы сказал *злобно рыгнул*.",
        "С-с-с-спасибо.",
        "Сейчас дочиню и поедем ко мне, бахнем по пивку.",
        "На протяжении всего времени было много ругательств, таких как.",
        "жеваный рот.",
        "Египетская сила.",
        "Поехали?"
    ]
    show_dialogs(dialogs, bg1)
    
    menu_items = ["Поехали.", "Не я обойдусь."]
    selected = generate_menu(screen, menu_items)
    
    if selected == "Поехали.":
        logging.info("Player chose: Поехали")
        click.play()
        ments()
    elif selected == "Не я обойдусь.":
        logging.info("Player chose: Не я обойдусь")
        click.play()
        whot()

def ments():
    logging.info("Starting ments sequence")
    dialogs = [
        "Бл*ть гайцы.",
        "музыка на фоне *Эй мусорок не шей мне срок*.",
        "Щас порешаем.",
        "Добрый день, показываем документики, огнетушитель, аптечку.",
        "Может договоримся?.",
        "*Показал на кулькуляторе 1000Р*.",
        "У тебя есть косарик?."
    ]
    show_dialogs(dialogs, bg3)
    
    menu_items = ["НЕ ТЫ ЖИРНЫЙ", "Да держи"]
    selected = generate_menu(screen, menu_items)
    
    if selected == "НЕ ТЫ ЖИРНЫЙ":
        click.play()
        whot()
    elif selected == "Да держи":
        click.play()
        evening()

def evening():
    logging.info("Starting evening sequence")
    dialogs = [
        "O  у меня ведь в холодильнике холодный пивас.",
        "Чиназес.",
        "Что? *громко рыгнул после пива*.",
        "Спасибо, наверное.",
        "Включили телевизор а там футбол.",
        "Гоооооооооол.",
        "Гоооооооооол.",
        "Гоооооооооол.",
        "Гоооооооооол, рыгнул.",
        "Гоооооооооол.",
        "Гоооооооооол."
    ]
    show_dialogs(dialogs, bg2)
    
    screen.fill((0, 0, 0))
    while True:
        font = pygame.font.SysFont("DejaVuSans.ttf", 33)
        texts = [
            ("Обезьянья возня", 80, 280),
            ("Пердеж и отрыжка", 80, 310)
        ]
        for text, x, y in texts:
            label = font.render(text, 0, COLORS['red'])
            screen.blit(label, (x, y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                outside()

def outside():
    logging.info("Starting outside sequence")
    dialogs = [
        "Всего всегда по немногу скуф попал в реанимацию  с инсультом.",
        "Гайца посадили.",
        "А наш главный герой остался жив.",
        "Может когда-то они соберутся вновь."
    ]
    show_dialogs(dialogs, bg4)
    
    screen.blit(end, (0, 0))
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                mmenu()

# === Game Flow Functions ===
def main() -> None:
    """
    Main game loop
    
    Handles:
    - Music playback (continuous loop)
    - Event processing
    - Frame rate control (30 FPS)
    - Scene management
    - Display updates
    
    Exit Conditions:
    - User closes window
    - System error occurs
    """
    logging.info("Game started")
    while True:
        pygame.mixer.music.play(-1)  # -1 for infinite loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Game closed by user")
                exit()
        mmenu()
        clock.tick(30)  # Maintain 30 FPS
        pygame.display.flip()  # Update display

# === Entry Point ===
if __name__ == "__main__":
    main()  # Launch game