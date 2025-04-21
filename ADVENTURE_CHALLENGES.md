# 🏆 THE GRAND PYTHON ADVENTURE CHALLENGES 🚀

*Greetings, brave wizard apprentice! Are you ready to test your magical powers? This scroll contains exciting challenges to prove your mastery of Python gardens!*

![Imagine a map with different challenge locations, treasures, and magical obstacles to overcome]

## 🌟 CHALLENGE LEVELS

Choose your adventure path:

* 🌱 **Seedling Challenges** - For new wizard apprentices
* 🌲 **Sapling Challenges** - For growing magic users
* 🌳 **Ancient Oak Challenges** - For experienced enchanters

## 🌱 SEEDLING CHALLENGES

### 🧩 Challenge 1: The First Garden
**Mission**: Create your very first Python garden and enter it!
1. Run the magic spell (`./init_py310_venv.sh` or `./init_py311_venv.sh`)
2. Enter your garden with the activation spell
3. Verify you're inside by running: `python -c "import sys; print('Magic level:', sys.version)"`
4. Exit your garden with the `deactivate` spell

**Success Spell**: When you see your Python version printing correctly, you've completed the challenge!

### 🧩 Challenge 2: The Magical Creature Collector
**Mission**: Summon three magical creatures (packages) to your garden!
1. Enter your magical garden
2. Summon these creatures:
   - `pip install cowsay` - A fun creature that makes animals talk!
   - `pip install colorama` - A creature that brings colors to your terminal!
   - `pip install emoji` - A creature that knows the secret language of emojis!
3. Check your collection with `pip list`

**Success Spell**: Create a small Python script called `creature_parade.py`:

```python
import cowsay
import colorama
from colorama import Fore, Style
import emoji

# Initialize the color magic
colorama.init()

# Show off your creatures
print(Fore.GREEN + "✨ WELCOME TO MY MAGICAL CREATURE PARADE! ✨" + Style.RESET_ALL)

# Make a cow say something
cowsay.cow("Moooo! I'm a magical cow from your Python garden!")

# Add some colorful messages
print(Fore.BLUE + "This text is as blue as the sky!" + Style.RESET_ALL)
print(Fore.RED + "This text is as red as a dragon's fire!" + Style.RESET_ALL)
print(Fore.YELLOW + "This text is as yellow as magical gold!" + Style.RESET_ALL)

# Add emojis
print(emoji.emojize("I love magic :sparkles: and pythons :snake:!"))

print(Fore.MAGENTA + "✨ THE END OF THE PARADE! ✨" + Style.RESET_ALL)
```

Run with `python creature_parade.py` to see your magical creatures perform!

## 🌲 SAPLING CHALLENGES

### 🧩 Challenge 3: The Garden Keeper
**Mission**: Create a spell (script) that helps manage your gardens!

Create a file called `garden_keeper.py` with this magic:

```python
#!/usr/bin/env python3
import os
import sys
import subprocess

def print_colorful(text, color_code):
    """Print text in color"""
    print(f"\033[{color_code}m{text}\033[0m")

def list_gardens():
    """Find all virtual environment gardens in current directory"""
    print_colorful("🔍 Searching for magical gardens...", "1;34")
    
    gardens = []
    for item in os.listdir('.'):
        if os.path.isdir(item) and os.path.exists(os.path.join(item, 'bin', 'activate')):
            gardens.append(item)
    
    if gardens:
        print_colorful(f"✨ Found {len(gardens)} magical gardens!", "1;32")
        for i, garden in enumerate(gardens, 1):
            print_colorful(f"{i}. {garden}", "1;35")
    else:
        print_colorful("😢 No magical gardens found in this realm!", "1;31")
    
    return gardens

def garden_info(garden_path):
    """Show information about a specific garden"""
    if not os.path.exists(os.path.join(garden_path, 'bin', 'activate')):
        print_colorful(f"❌ {garden_path} is not a magical garden!", "1;31")
        return
    
    print_colorful(f"✨ Garden Information: {garden_path} ✨", "1;33")
    
    # Get Python version
    python_path = os.path.join(garden_path, 'bin', 'python')
    result = subprocess.run([python_path, '--version'], capture_output=True, text=True)
    py_version = result.stdout.strip() or result.stderr.strip()
    print_colorful(f"🐍 Python Version: {py_version}", "1;36")
    
    # Get installed packages
    print_colorful("📦 Magical Creatures (Top 5):", "1;36")
    result = subprocess.run([os.path.join(garden_path, 'bin', 'pip'), 'list'], 
                          capture_output=True, text=True)
    packages = result.stdout.strip().split('\n')[2:7]  # Skip header and show first 5
    for pkg in packages:
        print_colorful(f"  {pkg}", "1;34")
    
    return py_version

def main():
    """Main garden keeper function"""
    print_colorful("🧙‍♂️ Welcome to the Magical Garden Keeper! 🧙‍♀️", "1;32")
    print_colorful("What would you like to do today?", "1;37")
    print_colorful("1. List all magical gardens", "1;33")
    print_colorful("2. Check info about a specific garden", "1;33")
    print_colorful("3. Exit", "1;33")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == '1':
        list_gardens()
    elif choice == '2':
        gardens = list_gardens()
        if gardens:
            garden_num = input("\nWhich garden would you like to inspect? (enter number): ")
            try:
                selected = gardens[int(garden_num) - 1]
                garden_info(selected)
            except (ValueError, IndexError):
                print_colorful("❌ That's not a valid garden number!", "1;31")
    elif choice == '3':
        print_colorful("👋 Farewell, young wizard! Keep your gardens magical!", "1;32")
    else:
        print_colorful("❌ That's not a valid spell! Try again.", "1;31")

if __name__ == "__main__":
    main()
```

Make it executable with `chmod +x garden_keeper.py` and run it with `./garden_keeper.py`!

### 🧩 Challenge 4: The Garden Explorer
**Mission**: Compare two different garden types!

1. Create both a Python 3.10 garden AND a Python 3.11 garden
2. Enter each garden one at a time
3. In each garden, run this spell to see what's different:
   ```python
   import sys
   import platform
   
   print(f"Python version: {sys.version}")
   print(f"Platform info: {platform.platform()}")
   
   # Check for new Python 3.11 features in a fun way
   if sys.version_info.major == 3 and sys.version_info.minor >= 11:
       print("✨ SPECIAL MAGIC DETECTED! ✨")
       print("This garden has the power of Python 3.11 or higher!")
       print("It contains magical treasures like:")
       print("  - Faster spells (improved interpreter)")
       print("  - Better error detection magic")
       print("  - Enhanced exception notes")
   else:
       print("This garden has the classic Python magic!")
   ```

**Success Spell**: Write down three differences you noticed between the gardens!

## 🌳 ANCIENT OAK CHALLENGES

### 🧩 Challenge 5: The Magical Library
**Mission**: Create a library of useful Python spells in your garden!

1. Enter your garden
2. Create a folder called `spellbook`
3. Inside that folder, create these magical files:

**spellbook/weather_magic.py**:
```python
import random

def forecast():
    """Predict the magical weather"""
    weathers = [
        "Sunny with floating magical sparkles",
        "Cloudy with a chance of falling chocolate frogs",
        "Rainbow dragons flying overhead",
        "Gentle shower of glowing pixie dust",
        "Stormy with magic lightning bolts",
        "Foggy with mysterious whispers"
    ]
    return random.choice(weathers)

def temperature():
    """Get the magical temperature"""
    return random.randint(60, 85)
```

**spellbook/wizard_tools.py**:
```python
def spell_checker(spell_name):
    """Check if a spell is correct"""
    real_spells = ["alohomora", "wingardium leviosa", "expecto patronum", 
                  "lumos", "accio", "expelliarmus"]
    
    if spell_name.lower() in real_spells:
        return f"✓ {spell_name} is a correct spell!"
    else:
        return f"✗ Beware! {spell_name} is not in the standard spellbook!"

def magic_calculator(a, b, operation):
    """Perform magical calculations"""
    if operation == "add":
        return f"{a} + {b} = {a + b}"
    elif operation == "subtract":
        return f"{a} - {b} = {a - b}"
    elif operation == "multiply":
        return f"{a} × {b} = {a * b}"
    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero! Even magic has limits!"
        return f"{a} ÷ {b} = {a / b}"
    else:
        return "Unknown magical operation!"
```

**test_spellbook.py** (in the main folder):
```python
from spellbook import weather_magic, wizard_tools

print("🧙‍♂️ TESTING THE MAGICAL SPELLBOOK 🧙‍♀️")

# Test the weather magic
print("\n🌦️  WEATHER DIVINATION 🌦️")
print(f"Today's forecast: {weather_magic.forecast()}")
print(f"Temperature: {weather_magic.temperature()}°F")

# Test the wizard tools
print("\n🪄 SPELL CHECKER 🪄")
print(wizard_tools.spell_checker("wingardium leviosa"))
print(wizard_tools.spell_checker("abracadabra"))

print("\n🔮 MAGICAL CALCULATIONS 🔮")
print(wizard_tools.magic_calculator(7, 3, "add"))
print(wizard_tools.magic_calculator(10, 2, "multiply"))

print("\n✨ SPELLBOOK TEST COMPLETE! ✨")
```

Run `python test_spellbook.py` to test your magical library!

### 🧩 Challenge 6: The Master Gardener
**Mission**: Create a completely custom garden with its own powers!

1. Create a new magical garden with: `./init_py311_venv.sh --name master_garden`
2. Enter your garden
3. Install these powerful creatures: `pip install requests questionary rich`
4. Create a powerful spell called `garden_master.py`:

```python
#!/usr/bin/env python3
import os
import sys
import subprocess
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import requests
import json
from datetime import datetime

console = Console()

def show_banner():
    """Show a fancy banner"""
    console.print(Panel.fit(
        "[bold magenta]🧙‍♂️ MASTER GARDENER WIZARD TOOLKIT 🧙‍♀️[/bold magenta]",
        border_style="green"
    ))

def check_garden():
    """Check if we're in a virtual environment"""
    if os.environ.get('VIRTUAL_ENV'):
        venv_name = os.path.basename(os.environ['VIRTUAL_ENV'])
        console.print(f"[green]✅ Currently in the [bold]{venv_name}[/bold] magical garden![/green]")
        return True
    else:
        console.print("[red]❌ Not currently in any magical garden![/red]")
        console.print("[yellow]Hint: Use 'source your_garden_name/bin/activate' to enter a garden[/yellow]")
        return False

def get_installed_creatures():
    """Get installed packages in the current environment"""
    result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=json'], 
                         capture_output=True, text=True)
    packages = json.loads(result.stdout)
    
    table = Table(title="🦄 Magical Creatures In Your Garden")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="green")
    
    for pkg in packages:
        table.add_row(pkg['name'], pkg['version'])
    
    console.print(table)

def get_python_news():
    """Get latest Python news from PyPI"""
    try:
        console.print("[yellow]Contacting the wizard news network...[/yellow]")
        response = requests.get('https://pypi.org/rss/packages.xml', timeout=5)
        
        if response.status_code == 200:
            # Very simple RSS parsing (not using a parser for simplicity)
            content = response.text
            titles = [line.split('<title>')[1].split('</title>')[0] 
                     for line in content.split('\n') if '<title>' in line][1:6]
            
            console.print(Panel("[bold blue]📰 Latest News from the Python Realm 📰[/bold blue]", 
                               border_style="blue"))
            
            for i, title in enumerate(titles, 1):
                console.print(f"[cyan]{i}.[/cyan] [green]{title}[/green]")
        else:
            console.print("[red]Could not connect to the wizard news network![/red]")
    except Exception as e:
        console.print(f"[red]Error getting news: {e}[/red]")

def create_new_spell():
    """Create a new Python script template"""
    spell_name = questionary.text("What shall we name your new spell?").ask()
    
    if not spell_name.endswith('.py'):
        spell_name += '.py'
    
    if os.path.exists(spell_name):
        overwrite = questionary.confirm(f"{spell_name} already exists. Overwrite it?").ask()
        if not overwrite:
            console.print("[yellow]Spell creation cancelled![/yellow]")
            return

    spell_type = questionary.select(
        "What type of spell would you like to create?",
        choices=[
            "Simple script",
            "Command-line tool",
            "Interactive game",
            "Data processing spell"
        ]
    ).ask()
    
    templates = {
        "Simple script": f'''#!/usr/bin/env python3
# {spell_name} - Created by Master Gardener on {datetime.now().strftime("%Y-%m-%d")}

def main():
    """Main function"""
    print("✨ Welcome to your new magical spell! ✨")
    # Your code goes here
    
if __name__ == "__main__":
    main()
''',
        "Command-line tool": f'''#!/usr/bin/env python3
# {spell_name} - Created by Master Gardener on {datetime.now().strftime("%Y-%m-%d")}
import argparse

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="A magical command-line spell")
    parser.add_argument("--power", type=int, default=10, help="Power level of the spell")
    parser.add_argument("--element", choices=["fire", "water", "earth", "air"], 
                      default="fire", help="Elemental power to use")
    
    args = parser.parse_args()
    
    print(f"✨ Casting a level {args.power} {args.element} spell! ✨")
    # Your code goes here
    
if __name__ == "__main__":
    main()
''',
        "Interactive game": f'''#!/usr/bin/env python3
# {spell_name} - Created by Master Gardener on {datetime.now().strftime("%Y-%m-%d")}

def display_intro():
    """Display game introduction"""
    print("*" * 60)
    print("✨✨✨ WELCOME TO YOUR MAGICAL ADVENTURE! ✨✨✨")
    print("*" * 60)
    print("You are a wizard in training, exploring the ancient forest...")
    print("Your choices will determine your destiny!")
    
def game_loop():
    """Main game loop"""
    display_intro()
    
    playing = True
    while playing:
        choice = input("\\nWhat would you like to do? [explore/rest/quit]: ")
        
        if choice.lower() == "explore":
            print("You venture deeper into the magical forest...")
            # Add your game logic here
        elif choice.lower() == "rest":
            print("You take a rest under a glowing mushroom...")
            # Add your game logic here
        elif choice.lower() == "quit":
            print("Thank you for playing! Come back soon, young wizard!")
            playing = False
        else:
            print("I don't understand that spell. Try again!")
    
if __name__ == "__main__":
    game_loop()
''',
        "Data processing spell": f'''#!/usr/bin/env python3
# {spell_name} - Created by Master Gardener on {datetime.now().strftime("%Y-%m-%d")}
import csv
import json

def read_magic_data(filename):
    """Read data from CSV or JSON file"""
    if filename.endswith('.csv'):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            return list(reader)
    elif filename.endswith('.json'):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        raise ValueError("Unsupported file format! Only CSV or JSON spells work here.")

def process_magic(data):
    """Process the magical data"""
    print(f"Processing {len(data)} magical items...")
    # Your data processing code goes here
    return data

def save_results(data, output_file):
    """Save the processed magical results"""
    if output_file.endswith('.csv'):
        with open(output_file, 'w', newline='') as file:
            if data and len(data) > 0:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
    elif output_file.endswith('.json'):
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=2)
    print(f"✨ Magic results saved to {output_file}! ✨")

def main():
    """Main function"""
    print("✨ Magical Data Processing Spell ✨")
    
    # Example usage:
    # data = read_magic_data('input_file.csv')
    # processed = process_magic(data)
    # save_results(processed, 'output_file.json')
    
    print("To use this spell, edit the code to process your magical data!")
    
if __name__ == "__main__":
    main()
'''
    }
    
    with open(spell_name, 'w') as f:
        f.write(templates[spell_type])
    
    os.chmod(spell_name, 0o755)  # Make executable
    
    console.print(f"[green]✨ Your new spell [bold]{spell_name}[/bold] has been created! ✨[/green]")

def main():
    """Main function"""
    show_banner()
    
    if not check_garden():
        return
    
    while True:
        choice = questionary.select(
            "What would you like to do, Master Gardener?",
            choices=[
                "Check my magical creatures (installed packages)",
                "Get news from the Python realm",
                "Create a new magical spell (Python script)",
                "Exit the toolkit"
            ]
        ).ask()
        
        if "Check my magical creatures" in choice:
            get_installed_creatures()
        elif "Get news" in choice:
            get_python_news()
        elif "Create a new magical spell" in choice:
            create_new_spell()
        else:
            console.print("[magenta]Farewell, Master Gardener! May your gardens always flourish! 🌱✨[/magenta]")
            break
        
        print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[yellow]\nSpell interrupted! Farewell, wizard![/yellow]")
```

Make it executable with `chmod +x garden_master.py` and run it with `./garden_master.py`!

## 🎭 MAGICAL ENVIRONMENT MYSTERY QUESTS

### 🧩 Mystery Quest 1: The Secret Garden
**Mission**: Find out what happens when you try to use a package that was installed in a different garden!

1. Create a garden called `garden_a` and install the `cowsay` package there
2. Create another garden called `garden_b` but DON'T install cowsay there
3. Write a script called `test_cowsay.py`:
   ```python
   try:
       import cowsay
       cowsay.cow("Mooo! I'm a magical cow!")
   except ImportError:
       print("Oh no! The cow creature is not in this garden!")
   ```
4. Run this script in both gardens and note what happens

What did you learn about magical creatures and their garden homes?

### 🧩 Mystery Quest 2: The Garden Inspector
**Mission**: Discover the hidden structure of your magical garden!

1. Enter one of your gardens
2. Run this spell to see the secret structure:
   ```bash
   find . -type d | sort
   ```
3. Look inside the `bin` directory to find the magical tools:
   ```bash
   ls -la bin
   ```

Can you find the activation script? What other magical tools live there?

## 🌈 YOUR GRAND ADVENTURE AWAITS!

Ready to return to the main quest? Check these magical scrolls:

* 📜 [PYTHON_ADVENTURE_GUIDE.md](PYTHON_ADVENTURE_GUIDE.md) - Return to the main adventure guide!
* 📜 [MAGICAL_CREATURES_GUIDE.md](MAGICAL_CREATURES_GUIDE.md) - Learn about the magical creatures!
* 📜 [MAGICAL_SPELLS_EXPLAINED.md](MAGICAL_SPELLS_EXPLAINED.md) - Understand how the magic works!

Remember: Every great wizard starts small, but with practice and exploration, your powers will grow! Happy adventuring! 🧙‍♂️✨