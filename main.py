#!/usr/bin/env python
import json
from argparse import ArgumentParser

from superseashells import SuperSeashell

def fetch_params(json_fname):
    with open(json_fname, 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        'shape_id', 
        help=(
            'Name of the shape. This will be used to read'
            'params/<shape_id>.json and write models/<shape_id>.obj'))
    args = parser.parse_args()

    json_fname = f'params/{args.shape_id}.json'
    shell = SuperSeashell(fetch_params(json_fname))
    mesh = shell.generate_mesh()


    obj_fname = f'models/{args.shape_id}.obj'
    with open(obj_fname, 'w') as f:
        mesh.write_obj(f)
