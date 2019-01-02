#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# Created Date: Friday, October 19th 2018, 12:21:02 am
# Author: Greagen
# -----
# Last Modified: Tue Jan 01 2019
# Modified By: Greagen
# -----
# Copyright (c) 2018 Greagen
# ------------------------------------
# Life is short. I use python
###
import pydotplus
import os
import subprocess


DOXYGENFILE = '/Users/greagen/Desktop/DotParser/Doxyfile'

def doxygen(dirname):
    work_path = os.getcwd()
    os.chdir(dirname)
    status, output = subprocess.getstatusoutput('cp '+DOXYGENFILE+' .')
    if status != 0:
        print('errors! copy DOXYGENFILE to the dir')
        print('output:\n', output)
    status, output = subprocess.getstatusoutput('doxygen Doxyfile')
    os.chdir(work_path)
    return dirname + '/doxygen_results'


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


def delete_first_two_lines(dirname):
    dot_files = filter_files_by_extension(dirname)
    for dot_file in dot_files:
        with open(dot_file, 'r') as f:
            lines = f.readlines()
            if lines[2].startswith('  node [') or lines[2].startswith('  edge [') or lines[2].startswith('  rankdir='):
                del lines[2]
            if lines[2].startswith('  node [') or lines[2].startswith('  edge [') or lines[2].startswith('  rankdir='):
                del lines[2]
            if lines[2].startswith('  node [') or lines[2].startswith('  edge [') or lines[2].startswith('  rankdir='):
                del lines[2]
        with open(dot_file, 'w') as f:
            f.writelines(lines)


def get_lines_number_list(dirname):
    dot_files = filter_files_by_extension(dirname)
    result = {}
    for dot_file in dot_files:
        with open(dot_file, 'r') as f:
            lines = f.readlines()
            length = len(lines)
            result[dot_file] = length
    result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    return result


def build_graph(dotfile):
    dot_graph = pydotplus.graph_from_dot_file(dotfile)
    graph = {}
    graph['graph_name'] = dot_graph.get_name().strip('"')
    print('graph_name:', dot_graph.get_name().strip('"'))
    graph['nodes'] = {}
    for node in dot_graph.get_nodes():
        label = node.obj_dict['attributes']['label'].strip('"')
        if label in graph['nodes'].keys():
            print('Two same functions exist in one graph.')
            exit()
        graph['nodes'][label] = []
    for edge in dot_graph.get_edges():
        source_node_list = dot_graph.get_node(edge.get_source())
        desti_node_list = dot_graph.get_node(edge.get_destination())
        if len(source_node_list) != 1 or len(desti_node_list) != 1:
            print('node do not exist or there are more than one node with the same name.')
            exit()
        source_label = source_node_list[0].obj_dict['attributes']['label'].strip('"')
        desti_node_label = desti_node_list[0].obj_dict['attributes']['label'].strip('"')
        graph['nodes'][source_label].append(desti_node_label)
    return graph


def compare_two_lists(list1, list2):
    if len(list1) != len(list2):
        return False
    else:
        for item in list1:
            if item not in list2:
                return False
    return True


def judge_new_dotfile(dotfile, graphs):
    dot_graph = pydotplus.graph_from_dot_file(dotfile)
    node1_label = dot_graph.get_node('Node1')[0].obj_dict['attributes']['label'].strip('"')
    desti = []
    for edge in dot_graph.get_edges():
        if edge.get_source() == 'Node1':
            desti.append(dot_graph.get_node(edge.get_destination())[0].obj_dict['attributes']['label'].strip('"'))
    for graph in graphs:
        if node1_label in graph['nodes'].keys():
            desti_list = graph['nodes'][node1_label]
            if compare_two_lists(desti, desti_list) is True:
                return True
    return False


def main(dirname):
    dot_files_list = get_lines_number_list(dirname) 
    graphs = []
    id = 0
    for dot_file_item in dot_files_list:
        dot_file = dot_file_item[0]
        if judge_new_dotfile(dot_file, graphs) is True:
            print(dot_file)
            print('This dot file is included in former graph')
            continue
        graph = build_graph(dot_file)
        print(dot_file)
        print('building...... ok!')
        graphs.append(graph)
    print(graphs)


if __name__ == '__main__':
    # delete_first_two_lines('./dot')
    #main('./dot')
    print(doxygen('/Users/greagen/Desktop/gimp'))
