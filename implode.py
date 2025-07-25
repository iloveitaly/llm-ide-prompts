#!/usr/bin/env python3
"""
Bundle Cursor or Copilot instruction component files into a single instruction file.
Usage: python3 implode.py [cursor|github] [output_file]
"""
import os
import sys
import argparse
from pathlib import Path

# Add current directory to path for constants import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constants import SECTION_GLOBS, header_to_filename, filename_to_header

def get_ordered_files(file_list, section_globs_keys):
    """Order files based on SECTION_GLOBS key order, with unmapped files at the end."""
    file_dict = {f.stem: f for f in file_list}
    ordered_files = []
    
    # Add files in SECTION_GLOBS order
    for section_name in section_globs_keys:
        filename = header_to_filename(section_name)
        if filename in file_dict:
            ordered_files.append(file_dict[filename])
            del file_dict[filename]
    
    # Add any remaining files (not in SECTION_GLOBS) sorted alphabetically
    remaining_files = sorted(file_dict.values(), key=lambda p: p.name)
    ordered_files.extend(remaining_files)
    
    return ordered_files

def bundle_cursor_rules(rules_dir, output_file):
    rule_files = list(Path(rules_dir).glob("*.mdc"))
    general = [f for f in rule_files if f.stem == "general"]
    others = [f for f in rule_files if f.stem != "general"]
    
    # Order the non-general files based on SECTION_GLOBS
    ordered_others = get_ordered_files(others, SECTION_GLOBS.keys())
    ordered = general + ordered_others
    
    with open(output_file, "w") as out:
        for rule_file in ordered:
            with open(rule_file, "r") as f:
                content = f.read().strip()
                if not content:
                    continue
                content = strip_yaml_frontmatter(content)
                content = strip_header(content)
                # Convert dash-separated names to title case with spaces
                header = filename_to_header(rule_file.stem)
                if rule_file.stem != "general":
                    out.write(f"## {header}\n\n")
                out.write(content)
                out.write("\n\n")

def strip_yaml_frontmatter(text):
    lines = text.splitlines()
    if lines and lines[0].strip() == '---':
        # Find the next '---' after the first
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                return '\n'.join(lines[i+1:]).lstrip('\n')
    return text

def strip_header(text):
    """Remove the first markdown header (## Header) from text if present."""
    lines = text.splitlines()
    if lines and lines[0].startswith('## '):
        # Remove the header line and any immediately following empty lines
        remaining_lines = lines[1:]
        while remaining_lines and not remaining_lines[0].strip():
            remaining_lines = remaining_lines[1:]
        return '\n'.join(remaining_lines)
    return text

def bundle_github_instructions(instructions_dir, output_file):
    copilot_general = Path(".github/copilot-instructions.md")
    instr_files = list(Path(instructions_dir).glob("*.instructions.md"))
    
    # Order the instruction files based on SECTION_GLOBS
    ordered_files = get_ordered_files(instr_files, SECTION_GLOBS.keys())
    
    with open(output_file, "w") as out:
        # Write general copilot instructions if present
        if copilot_general.exists():
            content = copilot_general.read_text().strip()
            if content:
                out.write(content)
                out.write("\n\n")
        for instr_file in ordered_files:
            with open(instr_file, "r") as f:
                content = f.read().strip()
                if not content:
                    continue
                content = strip_yaml_frontmatter(content)
                content = strip_header(content)
                # Convert dash-separated names to title case with spaces
                header = filename_to_header(instr_file.stem.replace('.instructions',''))
                out.write(f"## {header}\n\n")
                out.write(content)
                out.write("\n\n")

def main():
    parser = argparse.ArgumentParser(description="Bundle Cursor or Copilot rules into a single file.")
    parser.add_argument("mode", choices=["cursor", "github"], help="Which rules to bundle")
    parser.add_argument("output", nargs="?", default="instructions.md", help="Output file")
    args = parser.parse_args()

    if args.mode == "cursor":
        bundle_cursor_rules(".cursor/rules", args.output)
    else:
        bundle_github_instructions(".github/instructions", args.output)
    print(f"Bundled {args.mode} rules into {args.output}")

if __name__ == "__main__":
    main()
