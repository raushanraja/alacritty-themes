import os
import yaml
import toml
import dotenv

dotenv.load_dotenv()

themes_dir = os.getenv("THEMES_DIR")

if not themes_dir:
    raise Exception("THEMES_DIR not set")

new_themes_dir = themes_dir +"toml/"

try:
    if not os.path.exists(new_themes_dir):
        os.makedirs(os.path.expanduser(new_themes_dir))
except FileExistsError:
    pass

for root, dirs, files in os.walk(os.path.expanduser(themes_dir)):
    for file in files:
        if file.endswith(".yaml") or file.endswith(".yml"):
            with open(os.path.join(root, file), "r") as f:
                data = yaml.safe_load(f)

            toml_file = new_themes_dir + file.split('.')[0] + ".toml"
            with open(os.path.expanduser(toml_file),'w') as f:
                toml.dump(data, f)


