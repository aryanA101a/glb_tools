#!/usr/bin/env python3
import sys
import json
import curses
import argparse
from pygltflib import GLTF2



def modify_glb(input_file: str,output_file: str, data:dict) -> None:
        gltf = GLTF2().load(input_file)

        if not hasattr(gltf.scenes[0], 'extras'):
            gltf.scenes[0].extras = {}
        if 'userData' not in gltf.scenes[0].extras:
            gltf.scenes[0].extras['userData'] = {}

        gltf.scenes[0].extras['userData'] = data

        output_path = output_file if output_file else input_file
        gltf.save(output_path)





def fill_user_data(config:any,input_file: str,output_file: str):

    def draw_menu(stdscr, question, options):
        curses.curs_set(0)
        current_option = 0

        while True:
            stdscr.clear()
            stdscr.addstr(f"{question}\n\n")

            for idx, option in enumerate(options):
                if idx == current_option:
                    stdscr.addstr(f"> {option}\n", curses.A_REVERSE)
                else:
                    stdscr.addstr(f"  {option}\n")

            key = stdscr.getch()

            if key == curses.KEY_UP and current_option > 0:
                current_option -= 1
            elif key == curses.KEY_DOWN and current_option < len(options) - 1:
                current_option += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                return options[current_option]

    def handle_free_text(stdscr, question):
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(f"{question}\n\n")
        stdscr.addstr("Your answer: ")
        stdscr.refresh()
        curses.echo()
        answer = stdscr.getstr().decode("utf-8")
        curses.noecho()
        return answer

    def execute(stdscr):
        try:
            data={}
            for entry in config:
                question = entry["question"]
                options = entry["options"]

                if options:
                    answer = draw_menu(stdscr, question, options)
                else:
                    answer = handle_free_text(stdscr, question)

                data[entry["key"]]=answer
                stdscr.refresh()

            stdscr.clear()
            modify_glb(input_file,output_file,data)
            stdscr.refresh()
        except Exception as e:
            curses.endwin()
            print(f"Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
    curses.wrapper(execute)
    


def main():
    parser = argparse.ArgumentParser(description='Add model_type and is_light to GLB file userData')
    parser.add_argument('input_file', help='Input GLB file path')
    parser.add_argument('-o', '--output', help='Output file path (optional)')
    args = parser.parse_args()

    with open('./config.json', 'r') as f:
        config = json.load(f)

    fill_user_data(config,args.input_file,args.output)

if __name__ == "__main__":
    main()
    
