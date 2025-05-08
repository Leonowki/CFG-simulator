import customtkinter as ctk
import tkinter as tk
from node import Node

class TreeVisualizer(ctk.CTkCanvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.node_radius = 20
        self.level_height = 60
        self.horizontal_spacing = 30
        self.nodes = {}  # Store node objects and their coordinates
        self.node_colors = {
            # Non-terminals in blue 
            'S': '#3498db',
            'M': '#2980b9',
            'D': '#2980b9',
            'Y': '#2980b9',
            'P': '#2980b9',
            'N': '#2980b9',
            'X': '#2980b9',
            'V': '#2980b9',
            'Z': '#2980b9',
            # Terminals in green 
            '0': '#2ecc71',
            '1': '#2ecc71',
            '2': '#2ecc71',
            '3': '#2ecc71',
            '4': '#2ecc71',
            '5': '#2ecc71',
            '6': '#2ecc71',
            '7': '#2ecc71',
            '8': '#2ecc71',
            '9': '#2ecc71',
            '/': '#2ecc71',
            '-': '#2ecc71',
            '.': '#2ecc71'
        }
        
    def draw_tree(self, root):
        """Draw the parse tree on the canvas"""
        self.delete("all")  # Clear canvas
        self.nodes = {}
        
        # Calculate the width needed
        self._calculate_node_positions(root, 0, 0)
        
        # Adjust canvas size based on node positions
        max_x = max([pos[0] for pos in self.nodes.values()]) + self.node_radius + 20
        max_y = max([pos[1] for pos in self.nodes.values()]) + self.node_radius + 20
        
        self.configure(width=max_x, height=max_y, scrollregion=(0, 0, max_x, max_y))
        
        # Draw connections first (so they appear behind nodes)
        self._draw_connections(root)
        
        # Draw nodes
        self._draw_nodes()
    
    def _calculate_node_positions(self, node, level, x_offset):
        """Calculate positions for all nodes in the tree"""
        if not node.children:
            # This is a leaf node
            node_width = self.node_radius * 2 + self.horizontal_spacing
            self.nodes[node] = (x_offset + self.node_radius, level * self.level_height + self.node_radius)
            return node_width
        
        # Calculate width for this subtree
        total_width = 0
        for child in node.children:
            child_width = self._calculate_node_positions(child, level + 1, x_offset + total_width)
            total_width += child_width
        
        # Position this node at the center of its children
        first_child_x = self.nodes[node.children[0]][0]
        last_child_x = self.nodes[node.children[-1]][0]
        center_x = (first_child_x + last_child_x) / 2
        
        self.nodes[node] = (center_x, level * self.level_height + self.node_radius)
        
        return total_width
    
    def _draw_nodes(self):
        """Draw all nodes on the canvas"""
        for node, (x, y) in self.nodes.items():
            # Get color based on node type
            color = self.node_colors.get(node.value, '#95a5a6')  # Default gray
            
            # Draw node circle
            self.create_oval(
                x - self.node_radius, y - self.node_radius, 
                x + self.node_radius, y + self.node_radius, 
                fill=color, outline='black'
            )
            
            # Draw node text
            self.create_text(x, y, text=node.value, fill='white', font=('Arial', 12, 'bold'))
    
    def _draw_connections(self, node):
        """Draw connections between nodes"""
        if not node.children:
            return
            
        parent_x, parent_y = self.nodes[node]
        
        for child in node.children:
            child_x, child_y = self.nodes[child]
            
            # Draw line from parent to child
            self.create_line(parent_x, parent_y + self.node_radius, 
                        child_x, child_y - self.node_radius,
                        fill='black', width=2)
            
            # Recursive call for child's connections
            self._draw_connections(child)