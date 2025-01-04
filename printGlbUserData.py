#!/usr/bin/env python3
import sys
import json
import argparse
from pygltflib import GLTF2

def print_extras(input_file: str, verbose: bool = False) -> None:
    """
    Prints the extras data from a GLB file
    
    Args:
        input_file: Path to input GLB file
        verbose: If True, prints all scene data, not just extras
    """
    # Load the GLB file
    gltf = GLTF2().load(input_file)
    
    print(f"\nReading GLB file: {input_file}\n")
    
    scene=gltf.scenes[0]
        
    if hasattr(scene, 'extras') and scene.extras:
        print("userData:")
        print(json.dumps(scene.extras["userData"], indent=2))
    else:
        print("No extras data found")
    
    print("-" * 40)
    

def main():
    parser = argparse.ArgumentParser(description='Display extras data from GLB file')
    parser.add_argument('input_file', help='Input GLB file path')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Show all scene data, not just extras')
    
    args = parser.parse_args()
    
    try:
        print_extras(args.input_file, args.verbose)
    except Exception as e:
        print(f"Error reading GLB file: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()