#!/usr/bin/env python
import json
from argparse import ArgumentParser

from superseashells import SuperSeashell

def fetch_params(args):
    with open(args.json_fname, 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        'json_fname', 
        help='JSON file with parameters for the superseashell')
    parser.add_argument(
        'obj_fname',
        help='output OBJ file name to store the result')
    args = parser.parse_args()

    shell = SuperSeashell(fetch_params(args))
    mesh = shell.generate_mesh()

    with open(args.obj_fname, 'w') as f:
        mesh.write_obj(f)
