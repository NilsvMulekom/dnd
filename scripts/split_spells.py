from dataclasses import dataclass
from pathlib import Path
import shutil
import re

# TODO: Fill automatic linking PATTERN_LIST
# TODO: Automatic table forming
# TODO: add metadata as obsidian metadata
# TODO: Add scripts for dnd classes and potentially other things

@dataclass
class Spell:
    name:    str
    content: list[str]

@dataclass
class SpellBook:
    spells: dict[str, Spell]

PATTERN_LIST = [
    "Blinded",
    "Charmed",
    "Deafened",
    "Exhaustion",
    "Frightened",
    "Grappled",
    "Incapacitated",
    "Invisible",
    "Paralyzed",
    "Petrified",
    "Poisoned",
    "Prone",
    "Restrained",
    "Stunned",
    "Unconscious",
]

def print_spell_book(spell_book: SpellBook):
    for spell_name, spell_obj in spell_book.items():
        print(f"Spell name: {spell_name}")
        for index, line in enumerate(spell_obj.content):
            print(f"{index}: {line}")

def write_spell_files(spell_book: SpellBook, output_directory: str):
    for spell_name, spell_obj in spell_book.items():
        write_file(spell_name, spell_obj.content, output_directory)
        
def write_file(file_title: str, file_body: list[str], output_path: str):
    file_name: str = f"{file_title}.md"
    output_file = Path(output_path) / file_name
    
    with open(output_file, "w", encoding="utf-8") as file:
        for line in file_body:
            file.write(f"{line}\n")

def create_output_dir(output_directory: str):
    output_path = Path(output_directory)
    # Create output dir, if it already exists delete the old version first
    if output_path.exists():
        shutil.rmtree(output_path)

    output_path.mkdir(exist_ok=True)
    
def add_spell_to_book(spell_book:SpellBook, spell:Spell) -> SpellBook:
    spell_book[spell.name] = spell
    return spell_book

def split_files(input_file) -> SpellBook:
    input_path  = Path(input_file)
    
    with open(input_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    spell_book: SpellBook = {}
    file_open: bool = False
    open_spell : Spell = Spell(name="", content=[])
    
    for line in file_content.splitlines():
        if line.startswith("#### "):
            if file_open:
                # Save any open file to spell_book before opening a new one
                spell_book[open_spell.name] = open_spell
                open_spell : Spell = Spell(name="", content=[])
                file_open = False
            # Cut off the first 5 characters to get the spell name
            spell_name: str = line[5:]
            open_spell.name = spell_name
            file_open = True
        open_spell.content.append(line)

    # Add the last spell to the spell_book if there is one open
    if file_open:
        spell_book[open_spell.name] = open_spell

    return spell_book

def add_linking(spell_book: SpellBook) -> SpellBook:
    linked_book: SpellBook = {}

    for spell_name, spell_obj in spell_book.items():
        spell_body: list[str] = []
        for line in spell_obj.content:
            new_line = line
            for pattern in PATTERN_LIST:
                new_line=re.sub(pattern, f"[[{pattern}]]",new_line)
            spell_body.append(new_line)
        linked_book[spell_name] = Spell(name=spell_name, content=spell_body)

    return linked_book
    
def main(input_file, output_directory):
    spell_book: SpellBook = {}
    create_output_dir(output_directory)
    spell_book = split_files(input_file)
    spell_book = add_linking(spell_book)
    print_spell_book(spell_book)
    write_spell_files(spell_book, output_directory)

main("input_folder/reduced_spells.md", "spells_folder")
