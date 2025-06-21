"""CLI to display small documentation snippets for LLM agents using jgtml."""
import argparse
import importlib.resources as pkg_resources
from pathlib import Path

PACKAGE = 'jgtml'
DOC_PATH = 'guide_for_llm_agents'

def _doc_dir() -> Path:
    return pkg_resources.files(PACKAGE) / DOC_PATH

def list_sections():
    return [p.stem for p in _doc_dir().iterdir() if p.suffix == '.md']

def read_section(name: str) -> str:
    path = _doc_dir() / f"{name}.md"
    if path.is_file():
        return path.read_text()
    raise FileNotFoundError(f'Section {name} not found')

def main():
    parser = argparse.ArgumentParser(description='JGTML documentation for LLM agents')
    parser.add_argument('--list', action='store_true', help='List available sections')
    parser.add_argument('--section', help='Display a specific section')
    parser.add_argument('--all', action='store_true', help='Display all sections')
    args = parser.parse_args()

    if args.list:
        for sec in list_sections():
            print(sec)
        return

    if args.all:
        for sec in list_sections():
            print(f"# {sec}\n")
            print(read_section(sec))
            print()
        return

    if args.section:
        print(read_section(args.section))
        return

    parser.print_help()

if __name__ == '__main__':
    main()
