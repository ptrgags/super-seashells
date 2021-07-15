#!/usr/bin/env python3
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
    parser.add_argument(
        '-t', '--type',
        choices=['obj', 'glb'],
        default='obj',
        help="type of the output 3D model, either obj or glb")
    args = parser.parse_args()

    json_fname = f'params/{args.shape_id}.json'
    shell = SuperSeashell(fetch_params(json_fname))
    mesh = shell.generate_mesh()


    obj_fname = f'models/{args.shape_id}.{args.type}'
    with open(obj_fname, 'wb') as f:
        if args.type == 'obj':
            mesh.write_obj(f)
        else:
            mesh.write_glb(f)
