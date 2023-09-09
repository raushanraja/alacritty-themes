import os
import dotenv
from inquirer import List, prompt

# Load environment variables
dotenv.load_dotenv()

# Path to the alacritty.yaml file
alacritty_config_path = os.getenv("ALACRITTY_CONFIG_PATH") 

# Path to the themes directory
themes_dir = os.getenv("THEMES_DIR") 

# Function to read the themes directory and return a list of theme filenames
def list_themes(themes_dir):
    themes = []
    for root, dirs, files in os.walk(os.path.expanduser(themes_dir)):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                themes.append(file)
    return themes

# Function to insert a theme import at the top of alacritty.yaml
def insert_theme_import(theme_file, alacritty_config_file):
    exists =  False
    old_theme_file = ""
    with open(os.path.expanduser(alacritty_config_file), "r") as f:
        config_content = f.read()
    
    for line in config_content.splitlines():
        if line.startswith("import:"):
            exists = True
            old_theme_file = config_content.splitlines()[1].split('"')[1].split('/')[-1]

    if exists:
        # Replace the existing theme import
        config_content = config_content.replace(
            f'import: \n  - "{themes_dir}{old_theme_file}"',
            f'import: \n  - "{themes_dir}{theme_file}"'
        )
        with open(os.path.expanduser(alacritty_config_file), "w") as f:
            f.write(config_content)

    else:
        # Insert the theme import at the top
        config_content = f'import: \n  - "{themes_dir}{theme_file}"\n' + config_content

    with open(os.path.expanduser(alacritty_config_file), "w") as f:
        f.write(config_content)

def main():
    # List available themes
    themes = list_themes(themes_dir)
    current_theme = themes[0]


    # Continue selecting themes until the user quits
    while True:
        try:
            theme_prompt = List("theme", message="Select a theme:", choices=themes, default=current_theme, autocomplete=True)
            current_theme = prompt([theme_prompt])["theme"]
            os.system("clear")
            insert_theme_import(current_theme, alacritty_config_path)
        except Exception as e:
            print("\nExiting...")
            break

    os.system("clear")


if __name__ == "__main__":
    main()
