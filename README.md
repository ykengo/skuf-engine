# Skuf Novel Engine

A lightweight Python visual novel engine built with Pygame. Create interactive stories with branching narratives, character dialogs, and rich backgrounds.

## ✨ Features

- Dialog system with character support
- Choice-based branching narratives  
- Scene management and transitions
- Background image handling
- Sound effects and music
- Event logging
- Simple API for game creation

## 🚀 Quick Start

1. Clone and install:
```bash
git clone https://github.com/ykengo/skuf-engine.git
cd visual-novel-engine
pip install -r requirements.txt
```


## 💡 Usage Examples

1. Dialog system
   ```
    game.show_dialogs([
      "Alice: What brings you here?",
      "Bob: I'm looking for adventure!",
      "Alice: Well, you came to the right place..."
    ])
   ```
2. Choice menu
    ```
      choices = ["Investigate the cave", "Return to town"]
      result = game.show_menu(choices)
      
      if result == "Investigate the cave":
          # Cave exploration scene
          game.show_dialogs(["You enter the dark cave..."])
      else:
          # Town scene
          game.show_dialogs(["You head back to safety..."])
    ```
3. Scene managment
   ```
    background = Fon(0, 0, "town.jpg")
    game.show_dialogs(["A peaceful village..."], background)
    
    
    def town_scene():
        background = Fon(0, 0, "town.jpg")
        game.show_dialogs([
            "You arrive in the town square.",
            "People bustle about their daily lives."
        ], background)
        
        choices = ["Visit shop", "Talk to villagers"]
        return game.show_menu(choices)
   ```
   
## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a pull request
