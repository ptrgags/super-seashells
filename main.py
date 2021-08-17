#!/usr/bin/env python3
import json
from argparse import ArgumentParser

from superseashells import SuperSeashell
from diffyshell.DifferentialSeashell import DifferentialSeashell

def fetch_params(json_fname):
    with open(json_fname, 'r') as f:
        return json.load(f)

def superseashell_main(args):
    json_fname = f'params/{args.shape_id}.json'
    shell = SuperSeashell(fetch_params(json_fname))
    mesh = shell.generate_mesh()


    obj_fname = f'models/{args.shape_id}.{args.type}'
    with open(obj_fname, 'wb') as f:
        if args.type == 'obj':
            mesh.write_obj(f)
        else:
            mesh.write_glb(f)

def diffyshell_main(args):
    shell = DifferentialSeashell()
    shell.compute()

if __name__ == '__main__':
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    super_parser = subparsers.add_parser("super", help="The original super seashells formula")
    super_parser.add_argument(
        'shape_id', 
        help=(
            'Name of the shape. This will be used to read'
            'params/<shape_id>.json and write models/<shape_id>.obj'))
    super_parser.add_argument(
        '-t', '--type',
        choices=['obj', 'glb'],
        default='glb',
        help="type of the output 3D model, either obj or glb")
    super_parser.set_defaults(func=superseashell_main)

    diffy_parser = subparsers.add_parser("diffy", help="differential seashells formula")
    diffy_parser.set_defaults(func=diffyshell_main)
    args = parser.parse_args()

    args.func(args)