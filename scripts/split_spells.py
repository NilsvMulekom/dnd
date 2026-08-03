import logging
from pathlib import Path
import shutil
import re

# TODO: Fill automatic linking list
# TODO: Automatic table forming
# TODO: add metadata as obsidian metadata
# TODO: Add scripts for classes and potentially other things

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

def print_spell_book(spell_book: dict[str, dict[str, list[str]]]):
    for file_name, spell_dict in spell_book.items():
        print(f"filename: {file_name}")
        for index, line in enumerate(spell_dict["content"]):
            print(f"{index}: {line}")
            
def write_files(spell_book: dict[str, dict[str, list[str]]], output_directory: str):
    for file_name, spell_dict in spell_book.items():
        write_file(file_name, spell_dict["content"], output_directory)
            
def write_file(spell_title: str, file_body: list[str], output_path: str):
    file_name: str = f"{spell_title}.md"
    output_file = Path(output_path) / file_name
    
    with open(output_file, "w", encoding="utf-8") as file:
        for index, line in enumerate(file_body):
            file.write(f"{line}\n")
            
def create_output_dir(output_directory: str):
    output_path = Path(output_directory)
    # Create output dir, if it already exists delete the old version first
    if output_path.exists():
        shutil.rmtree(output_path)

    output_path.mkdir(exist_ok=True)
    
def split_files(input_file) -> dict[str, dict[str, list[str]]]:
    input_path  = Path(input_file)
    
    with open(input_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    spell_book: dict[str, dict[str, list[str]]] = {}
    first_file: bool = True
    
    for line in file_content.splitlines():
        if line.startswith("#### "):
            # After the first cycle, copy the last one into spell_book
            if (first_file == False):
                spell_with_metadata : dict[str, list] = {}
                spell_with_metadata["content"] = spell_body
                spell_book[spell_name] = spell_with_metadata
            spell_body: list[str] = []
            first_file = False

            # Slice from the 5th character onwards
            spell_name: str = line[5:]

        else:
            spell_body.append(line)
    # Copy the last item into spell_book
    spell_with_metadata : dict[str, list]
    spell_with_metadata["content"] = spell_body
    spell_book[spell_name] = spell_with_metadata

    return spell_book

def add_linking(spell_book: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, list[str]]]:
    # TODO: Fix

    linked_book: dict[str, dict[str, list[str]]] = {}
    linked_book = spell_book
    for file_name, spell_dict in spell_book.items():
        spell_body: list[str]
        spell_body = spell_dict["content"]
        for line in spell_dict:
            new_line = line
            for pattern in PATTERN_LIST:
                new_line=re.sub(pattern, f"[[{pattern}]]",new_line)
            spell_body.append(new_line)
        linked_book[file_name]["content"] = spell_body
    
    
    # for file_name, file_contents in spell_book.items():
    #     spell_body = []
    #     for index, line in enumerate(file_contents):
    #         new_line = line
    #         for pattern in PATTERN_LIST:
    #             new_line=re.sub(pattern, f"[[{pattern}]]",new_line)
    #         spell_body.append(new_line)
    #     linked_book[file_name] = spell_body
            
    return linked_book
    
def main(input_file, output_directory):
    spell_book: dict[str, dict[str, list[str]]] = {}
    create_output_dir(output_directory)
    spell_book = split_files(input_file)
    # print_spell_book(spell_book)
    write_files(spell_book, output_directory)
    # spell_book = add_linking(spell_book)
    # print_spell_book(spell_book)
    # write_files(spell_book, output_directory)



main("reduced_spells.md", "spells_folder")
