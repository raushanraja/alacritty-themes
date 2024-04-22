import os
import dotenv
from inquirer import List, prompt

# Load environment variables
dotenv.load_dotenv()

# Path to the alacritty.yaml file
alacritty_config_path = os.getenv("ALACRITTY_CONFIG_PATH")

if not alacritty_config_path:
    raise Exception("ALACRITTY_CONFIG_PATH not set")

alacritty_config_file = os.path.expanduser(alacritty_config_path)

# Path to the themes directory
yml_themes_dir = os.getenv("THEMES_DIR_YAML")
toml_themes_dir = os.getenv("THEMES_DIR_TOML")


if alacritty_config_path.endswith(".yaml") or alacritty_config_path.endswith(".yml"):
    if not yml_themes_dir:
        raise Exception("THEMES_DIR_YAML not set")
    themes_dir = yml_themes_dir
    theme_format = ("yaml", "yml")
    startswith = "import:"
    endswith = "\n"

else:
    if not toml_themes_dir:
        raise Exception("THEMES_DIR_TOML not set")
    themes_dir = toml_themes_dir 
    theme_format = ("toml",)

# Function to read the themes directory and return a list of theme filenames
def list_themes(themes_dir, theme_format=("yaml", "yml")):
    themes = []
    for root, dirs, files in os.walk(os.path.expanduser(themes_dir)):
        for file in files:
            if file.endswith(theme_format):
                themes.append(file)
    return themes


def import_content(theme_file, themes_dir: str, theme_format=("yaml", "yml")):
    if 'yaml' in theme_format:
        return f'import: \n  - "{themes_dir}/{theme_file}"\n'
    else:
        return f'import = ["{themes_dir}/{theme_file}"]'


def insert_theme_import(theme_file: str):
    exists = False
    curr_line = ""

    with open(os.path.expanduser(alacritty_config_file), "r") as f:
        config_content = f.read()

    for line in config_content.splitlines():
        print(line)

        if line.find(themes_dir) > -1:
            exists = True
            curr_line = line
            break

    print(f"Exists: {exists}, Curr Line: {curr_line}")

    import_str = import_content(theme_file, themes_dir, theme_format)
    print(f"New Import Line: {import_str}")

    if exists:
        # Replace the existing theme import
        config_content = config_content.replace(
            curr_line,
            import_str
        )

    else:
        # Insert the theme import at the top
        config_content = import_str + "\n\n" +  config_content

    with open(os.path.expanduser(alacritty_config_file), "w") as f:
        f.write(config_content)


def main():
    # List available themes
    themes = list_themes(toml_themes_dir, theme_format=("toml"))
    current_theme = themes[0]

    # Continue selecting themes until the user quits
    while True:
        try:
            theme_prompt = List("theme", message="Select a theme:", choices=themes, default=current_theme, autocomplete=True)
            current_theme = prompt([theme_prompt])["theme"]
            os.system("clear")
            print(f"Selected theme: {current_theme}, dir: {themes_dir}, format: {theme_format}")
            insert_theme_import(current_theme)
        except Exception as e:
            print("\nExiting...")
            break

    os.system("clear")


if __name__ == "__main__":
    main()
