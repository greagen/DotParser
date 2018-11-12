#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Created Date: Friday, October 19th 2018, 12:21:02 am
# Author: Greagen
# -----
# Last Modified: Mon Nov 12 2018
# Modified By: Greagen
# -----
# Copyright (c) 2018 Greagen
# ------------------------------------
# Life is short. I use python
###
import pydotplus
import os


def filter_files_by_extension(dirname):
    filter = [".dot"]
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            ext = os.path.splitext(apath)[1]
            if ext in filter:
                result.append(apath)
    return result


def main(dirname):
    dot_files = filter_files_by_extension(dirname)
    graphs = []
    for dot_file in dot_files:
        dot_graph = pydotplus.graph_from_dot_file(dot_file)
        graph = {}
        print('graph_name:', dot_graph.get_name())
        i = 0
        for node in graph.get_nodes():
            i = i+1
            if (i == 1 and node.get_name() == 'edge') or (i == 2 and node.get_name() == 'node'):
                continue
            print('get_port:',node.get_port())
            print('to_strings:', node.to_string())
            print('obj_dict:', node.obj_dict)


        for edge in dot_graph.get_edges():
            print(i)
            i += 1
            print(edge.get_source())
            print(edge.get_destination())
            print(edge.to_string())
            print(edge.obj_dict)
        print(dot_graph.get_edges())


if __name__ == '__main__':
    main('./dotfiles')
