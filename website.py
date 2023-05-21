from parsers import json_to_dict
from jinja2 import Environment, FileSystemLoader

def get_home_page():
    site_info = json_to_dict(f"site_info.json")
    environment = Environment(loader=FileSystemLoader("data/templates/"))
    template = environment.get_template("homePage.html")
    #if no content header has been provided, the content header becomes the name of the file
    with open(f"_site/home.html", mode="w", encoding="utf-8") as message:
        message.write(template.render(
            #reverse the list order so newest entries are displayed first
            riders = reversed(site_info.values())
            ))

get_home_page()