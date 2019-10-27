#!/usr/bin/env python3
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class FilterModule(object):
    def filters(self):
        return {
            'ldap_tree2list': self.ldap_tree2list,
        }

    def ldap_tree2list(self, root_node):
        """Traverses a LDAP tree from the configuration and returns a list
        of all nodes in the tree. This allows iterating over the tree
        using a simple loop. Parent nodes preceed their children in the
        list.

        :root_node: The LDAP tree's root node as a dictionary.
        :returns: A list of nodes in the tree. Children are removed from
                  the nodes and an attribute called full_dn is added.
        """
        # Expand and store the DN of the root node.
        root_node['full_dn'] = ','.join([a + '=' + root_node['attributes'][a]
                                         for a in root_node['dn']])
        # Initialise the list with the root node.
        tree_nodes = [root_node]
        i = 0
        # Iterate over the list, extending it. This is a BFS algorithm.
        while i < len(tree_nodes):
            if 'children' in tree_nodes[i]:
                # Expand and store the full DN of the child nodes.
                for node in tree_nodes[i]['children']:
                    node['full_dn'] = ','.join([a + '=' + node['attributes'][a]
                                                for a in node['dn']] +
                                               [tree_nodes[i]['full_dn']])
                # Append the current node's children to the list.
                tree_nodes.extend(tree_nodes[i]['children'])
                # Remove children from the already processed node to avoid
                # duplicating every subtree.
                del tree_nodes[i]['children']
            # Next in list.
            i += 1
        return tree_nodes
