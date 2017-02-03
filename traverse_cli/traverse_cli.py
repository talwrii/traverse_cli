#!/usr/bin/python

# make code as python 3 compatible as possible
from __future__ import absolute_import, division, print_function, unicode_literals

"""
traverse_cli   ' if [ -d "{node}" ]; then ls {node} | sed "s!^!{node}/!" ; fi ' . # A little more wordy that I wanted
"""

import argparse
import logging
import pipes
import subprocess

LOGGER = logging.getLogger()


PARSER = argparse.ArgumentParser(description='Traverse using command line commands to find children')
PARSER.add_argument('child_command', type=str, help='Shell command to find children. {node} is expanded to the current node')
PARSER.add_argument('--depth', type=int, help='Depth of the tree to explore')
PARSER.add_argument('root', type=str, help='Shell command to find children')
PARSER.add_argument('--separator', '-s', type=str, help='Separate levels with this separator')
PARSER.add_argument('--tree', action='store_true', help='Output a tree structure instead of breadth waves. (does not stream)')
PARSER.add_argument('--progress', action='store_true', help='Show progress')
PARSER.add_argument('--debug', action='store_true', help='Print debug output')

def find_children(command, root):
    LOGGER.debug('Find children of %r', root)
    raw_command = command.format(node=pipes.quote(root))
    LOGGER.debug('Running %r', raw_command)
    proc = subprocess.Popen(raw_command, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
    output, _ = proc.communicate(raw_command)
    output = output.decode('utf8')
    if proc.returncode != 0:
        raise Exception('{!r} failed with return code {!r}'.format(raw_command, proc))
    return output.splitlines()

def breadth_first(start):
    frontier = set(start)
    all_nodes = set()

    yield frontier, all_nodes, dict()

    while True:
        new_frontier = set()
        node_children = dict()

        all_nodes |= frontier

        for node in frontier:
            node_children[node] = find_children(args.child_command, node)
            new_frontier |= set(node_children[node])

        yield new_frontier, all_nodes, node_children

        LOGGER.debug('New frontier: %r', new_frontier)
        new_frontier -= all_nodes

        frontier = set(new_frontier)

        if not new_frontier:
            return

def main():
    args = PARSER.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # This is mostly topological
    topological_nodes = []

    tree_graph = dict()

    for depth, (frontier, _all_nodes, children) in enumerate(breadth_first([args.root])):

        tree_graph.update(children)

        if not args.tree:
            for x in sorted(frontier):
                print(x)
            if args.separator is not None:
                print(args.separator)

        if args.depth is not None and depth >= args.depth:
            break


    if args.tree:
        print(format_tree(tree_graph, args.root))


def format_tree(tree_graph, root):
    return '{}\n{}'.format(
        root,
        '\n'.join(map(indent, [format_tree(tree_graph, x) for x in  tree_graph.get(root, [])])))

def indent(s):
    return '\n'.join(['    ' + l for l in s.splitlines()])
