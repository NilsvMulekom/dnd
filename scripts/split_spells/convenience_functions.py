from pathlib import Path
import shutil

from data_classes import SpellBook

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