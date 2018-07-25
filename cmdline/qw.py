#!/usr/local/bin/python

import argparse
import os
import sys
import numpy as np
from pwscf.pw_input import PWin

# installpath = '/Users/Woosun/Dropbox/Dev/QEhandler'
# sys.path.extend([installpath])


def executepwintags(args):
    p = PWin()
    p.read_file(args.input)

    if args.write is not None:
        p.write_tags_from_tagvaluepairlist(args.write)

    if args.remove is not None:
        p.remove_tags(args.remove)

    p.write_pwin(args.output)
    return


def executepwincell(args):
    p = PWin()
    p.read_file(args.input)
    p.unitcell_transform(args.unit, args.cell, args.rotation)
    p.write_pwin(args.output)
    return


def executepwinatom(args):
    p = PWin()
    p.read_file(args.input)

    if args.elements is not None:
        p.write_atoms(args.elements, args.coordinates, args.unit)

    else:
        if args.unit is not None:
            if args.translation is not None:
                p.position_translation(args.translation, args.unit)
            else:
                p.position_unittransform(args.unit)

    p.write_pwin(args.output)
    return


def executepwinpseudo(args):
    p = PWin()
    p.read_file(args.input)

    if args.pseudomass is None:
        mass = np.full(len(args.pseudoelem), None)
    else:
        mass = args.pseudomass

    if args.pseudofile is not None:
        for i in range(len(args.pseudoelem)):
            p.write_pseudo(args.pseudoelem[i], mass[i], args.pseudofile[i])
    else:
        for i in range(len(args.pseudoelem)):
            p.write_pseudo(args.pseudoelem[i], mass[i], None, args.pseudolabel[i])

    p.write_pwin(args.output)
    return


def executepwinkpoints(args):
    p = PWin()
    p.read_file(args.input)
    p.change_kpoints(args.ktype, args.kspacing, args.kgrid, args.kshift, args.knum, args.kpts, args.kreduce)
    p.write_pwin(args.output)
    return


# def executepwingen(args):
#     p = PWin()
#     p.read_file(args.input)
#
#     p.write_pwin(args.output)
#     return


def main():
    description = """qw.py
    Type qw.py [function] --help for more detailed informations.
    """

    desc_in = """
    """

    # Main parser
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)

    # Subparsers
    subparsers = parser.add_subparsers(title="Functions")

    parser_pwin = subparsers.add_parser("pwin", formatter_class=argparse.RawTextHelpFormatter, description=desc_in)

    pwinsubparsers = parser_pwin.add_subparsers()

    parser_tags = pwinsubparsers.add_parser("tags")
    parser_tags.add_argument("-i", dest="input", type=str, default="pw.in")
    parser_tags.add_argument("-o", dest="output", type=str, default="pw.in")
    parser_tags.add_argument("-w", dest="write", type=str, default=None, nargs='*')
    parser_tags.add_argument("-r", dest="remove", type=str, default=None, nargs='*')
    parser_tags.set_defaults(func=executepwintags)

    parser_cell = pwinsubparsers.add_parser("cell")
    parser_cell.add_argument("-i", dest="input", type=str, default="pw.in")
    parser_cell.add_argument("-o", dest="output", type=str, default="pw.in")
    parser_cell.add_argument("-u", dest="unit", type=str, default=None)
    parser_cell.add_argument("-v", dest="cell", type=str, default=None, nargs='*')
    parser_cell.add_argument("-r", dest="rotation", type=str, default=None, nargs='*')
    parser_cell.set_defaults(func=executepwincell)

    parser_atom = pwinsubparsers.add_parser("atom")
    parser_atom.add_argument("-i", dest="input", type=str, default="pw.in")
    parser_atom.add_argument("-o", dest="output", type=str, default="pw.in")
    parser_atom.add_argument("-e", dest="elements", type=str, default=None, nargs='*')
    parser_atom.add_argument("-c", dest="coordinates", type=str, default=None, nargs='*')
    parser_atom.add_argument("-u", dest="unit", type=str, default=None)
    parser_atom.add_argument("-t", dest="translation", type=str, default=None, nargs='*')
    parser_atom.set_defaults(func=executepwinatom)

    parser_pseudo = pwinsubparsers.add_parser("pseudo")
    parser_pseudo.add_argument("-i", dest="input", type=str, default="pw.in")
    parser_pseudo.add_argument("-o", dest="output", type=str, default="pw.in")
    parser_pseudo.add_argument("-pe", dest="pseudoelem", type=str, default=None, nargs='*')
    parser_pseudo.add_argument("-pm", dest="pseudomass", type=str, default=None, nargs='*')
    parser_pseudo.add_argument("-pl", dest="pseudolabel", type=str, default=None, nargs='*')
    parser_pseudo.add_argument("-pf", dest="pseudofile", type=str, default=None, nargs='*')
    parser_pseudo.set_defaults(func=executepwinpseudo)

    parser_kpoints = pwinsubparsers.add_parser("kpoints")
    parser_kpoints.add_argument("-ktype", dest="ktype", type=str, default=None)
    parser_kpoints.add_argument("-kgrid", dest="kgrid", type=str, default=None, nargs='*')
    parser_kpoints.add_argument("-kshift", dest="kshift", type=str, default=None, nargs='*')
    parser_kpoints.add_argument("-kspacing", dest="kspacing", type=str, default=None)
    parser_kpoints.add_argument("-knum", dest="knum", type=str, default=None)
    parser_kpoints.add_argument("-klist", dest="klist", type=str, default=None, nargs='*')
    parser_kpoints.add_argument("-kred", dest="kreduce", type=str, default=None)
    parser_kpoints.set_defaults(func=executepwinkpoints)

    # parser_gen = pwinsubparsers.add_parser("generate")
    # parser_gen.set_defaults(func=executepwingen)

    args = parser.parse_args()

    try:
        getattr(args, "func")
    except AttributeError:
        parser.print_help()
        sys.exit(0)
    args.func(args)


if __name__ == "__main__":
    main()