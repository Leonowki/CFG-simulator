import re
from node import Node

class CFGParser:
    def __init__(self):
        # Define the grammar
        self.grammar = {
            'S': [['M', '/', 'D', '/', 'Y'], ['M', '-', 'D', '-', 'Y'], ['M', '.', 'D', '.', 'Y']],
            'M': [['0', 'X'], ['1', 'V']],
            'D': [['0', 'X'], ['1', 'N'], ['2', 'N'], ['3', 'Z']],
            'Y': [['N', 'N', 'N', 'N']],
            'N': [['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
            'X': [['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']],
            'V': [['0'], ['1'], ['2']],
            'Z': [['0'], ['1']]
        }
        
        # Define terminals and non-terminals
        self.terminals = set()
        self.non_terminals = set(self.grammar.keys())
        
        for productions in self.grammar.values():
            for production in productions:
                for symbol in production:
                    if symbol not in self.grammar:
                        self.terminals.add(symbol)
    
    def is_terminal(self, symbol):
        return symbol in self.terminals
    
    def is_non_terminal(self, symbol):
        return symbol in self.non_terminals
    
    def get_productions(self, symbol):
        return self.grammar.get(symbol, [])
    
    def validate_input(self, input_string):
        # Check if input matches the pattern defined by the grammar
        pattern = r'^[0-9][1-9][-/.][0-3][0-9][-/.][0-9]{4}$'
        if not re.match(pattern, input_string):
            return False
        
        # Ensure both separators are the same
        separators = re.findall(r'[-/.]', input_string)
        if len(separators) != 2 or separators[0] != separators[1]:
            return False
        
        # Extract parts of the date string
        parts = re.split(r'[-/.]', input_string)
        if len(parts) != 3:
            return False
        
        month, day, year = parts
        
        # Check M (first part)
        if not (month[0] == '0' and month[1] in '123456789') and not (month[0] == '1' and month[1] in '012'):
            return False
        
        # Check D (second part)
        if day[0] == '0' and day[1] not in '123456789':
            return False
        if day[0] == '1' and not day[1].isdigit():
            return False
        if day[0] == '2' and not day[1].isdigit():
            return False
        if day[0] == '3' and day[1] not in '01':
            return False
        
        # If all checks pass, the input is valid
        return True
    
    def leftmost_derivation(self, input_string):
        if not self.validate_input(input_string):
            return "Invalid input", None
        
        # Create the root node and start with S
        root = Node("S")
        steps = ["S"]
        current = "S"
        
        # Extract parts of the date string
        parts = re.split(r'[-/.]', input_string)
        month, day, year = parts
        
        # Determine the separator
        separator = '/'
        if '-' in input_string:
            separator = '-'
        elif '.' in input_string:
            separator = '.'
        
        # Step 1: S -> M/D/Y or M-D-Y or M.D.Y based on the separator
        if separator == '/':
            replacement = "M/D/Y"
        elif separator == '-':
            replacement = "M-D-Y"
        else:  # separator == '.'
            replacement = "M.D.Y"
        
        current = replacement
        steps.append(current)
        
        # Add children to root node based on the production used
        m_node = Node("M")
        sep1_node = Node(separator)
        d_node = Node("D")
        sep2_node = Node(separator)
        y_node = Node("Y")
        
        root.add_child(m_node)
        root.add_child(sep1_node)
        root.add_child(d_node)
        root.add_child(sep2_node)
        root.add_child(y_node)
        
        # Step 2: Replace leftmost non-terminal M
        if month[0] == '0':
            m_replacement = "0X"
            m_node.add_child(Node("0"))
            m_node.add_child(Node("X"))
        else:  # month[0] == '1'
            m_replacement = "1V"
            m_node.add_child(Node("1"))
            m_node.add_child(Node("V"))
        
        current = current.replace("M", m_replacement, 1)
        steps.append(current)
        
        # Step 3: Replace leftmost non-terminal (X or V)
        if month[0] == '0':
            x_replacement = month[1]
            m_node.children[1].add_child(Node(month[1]))  # X -> digit
            current = current.replace("X", x_replacement, 1)
        else:  # month[0] == '1'
            v_replacement = month[1]
            m_node.children[1].add_child(Node(month[1]))  # V -> digit
            current = current.replace("V", v_replacement, 1)
        
        steps.append(current)
        
        # Step 4: Replace leftmost non-terminal D
        if day[0] == '0':
            d_replacement = "0X"
            d_node.add_child(Node("0"))
            d_node.add_child(Node("X"))
        elif day[0] in '12':
            d_replacement = day[0] + "N"
            d_node.add_child(Node(day[0]))
            d_node.add_child(Node("N"))
        else:  # day[0] == '3'
            d_replacement = "3Z"
            d_node.add_child(Node("3"))
            d_node.add_child(Node("Z"))
        
        current = current.replace("D", d_replacement, 1)
        steps.append(current)
        
        # Step 5: Replace leftmost non-terminal (X, N, or Z)
        if day[0] == '0':
            replacement = day[1]
            d_node.children[1].add_child(Node(day[1]))  # X -> digit
            current = current.replace("X", replacement, 1)
        elif day[0] in '12':
            replacement = day[1]
            d_node.children[1].add_child(Node(day[1]))  # N -> digit
            current = current.replace("N", replacement, 1)
        else:  # day[0] == '3'
            replacement = day[1]
            d_node.children[1].add_child(Node(day[1]))  # Z -> digit
            current = current.replace("Z", replacement, 1)
        
        steps.append(current)
        
        # Step 6: Replace Y -> NNNN
        replacement = "NNNN"
        for i in range(4):
            y_node.add_child(Node("N"))
        
        current = current.replace("Y", replacement, 1)
        steps.append(current)
        
        # Steps 7-10: Replace each N with a digit from year
        for i in range(4):
            digit = year[i]
            y_node.children[i].add_child(Node(digit))
            current = current.replace("N", digit, 1)
            steps.append(current)
        
        return steps, root
    
    def rightmost_derivation(self, input_string):
        if not self.validate_input(input_string):
            return "Invalid input", None
        
        # Create the root node and start with S
        root = Node("S")
        steps = ["S"]
        current = "S"
        
        # Extract parts of the date string
        parts = re.split(r'[-/.]', input_string)
        month, day, year = parts
        
        # Determine the separator
        separator = '/'
        if '-' in input_string:
            separator = '-'
        elif '.' in input_string:
            separator = '.'
        
        # Add children to root node
        m_node = Node("M")
        sep1_node = Node(separator)
        d_node = Node("D")
        sep2_node = Node(separator)
        y_node = Node("Y")
        
        root.add_child(m_node)
        root.add_child(sep1_node)
        root.add_child(d_node)
        root.add_child(sep2_node)
        root.add_child(y_node)
        
        # Step 1: S -> M/D/Y or M-D-Y or M.D.Y based on the separator
        if separator == '/':
            replacement = "M/D/Y"
        elif separator == '-':
            replacement = "M-D-Y"
        else:  # separator == '.'
            replacement = "M.D.Y"
        
        current = replacement
        steps.append(current)
        
        # In rightmost derivation, we start with the rightmost non-terminal Y
        # Step 2: Expand Y -> NNNN
        current_y_index = current.rfind("Y")
        if current_y_index != -1:
            for i in range(4):
                y_node.add_child(Node("N"))
            current = current[:current_y_index] + "NNNN" + current[current_y_index+1:]
            steps.append(current)
            
            # Step 3-6: Expand each N in NNNN from right to left
            for i in range(3, -1, -1):  # Process 3, 2, 1, 0
                n_index = current.rfind("N")
                if n_index != -1:
                    digit = year[i]
                    y_node.children[i].add_child(Node(digit))
                    current = current[:n_index] + digit + current[n_index+1:]
                    steps.append(current)
        
        # Step 7: Expand D
        d_index = current.rfind("D")
        if d_index != -1:
            if day[0] == '0':
                d_replacement = "0X"
                d_node.add_child(Node("0"))
                d_node.add_child(Node("X"))
            elif day[0] in '12':
                d_replacement = day[0] + "N"
                d_node.add_child(Node(day[0]))
                d_node.add_child(Node("N"))
            else:  # day[0] == '3'
                d_replacement = "3Z"
                d_node.add_child(Node("3"))
                d_node.add_child(Node("Z"))
            
            current = current[:d_index] + d_replacement + current[d_index+1:]
            steps.append(current)
            
            # Step 8: Expand X, N, or Z in D
            if day[0] == '0':
                x_index = current.rfind("X")
                if x_index != -1:
                    d_node.children[1].add_child(Node(day[1]))
                    current = current[:x_index] + day[1] + current[x_index+1:]
                    steps.append(current)
            elif day[0] in '12':
                n_index = current.rfind("N")
                if n_index != -1:
                    d_node.children[1].add_child(Node(day[1]))
                    current = current[:n_index] + day[1] + current[n_index+1:]
                    steps.append(current)
            else:  # day[0] == '3'
                z_index = current.rfind("Z")
                if z_index != -1:
                    d_node.children[1].add_child(Node(day[1]))
                    current = current[:z_index] + day[1] + current[z_index+1:]
                    steps.append(current)
        
        # Step 9: Expand M
        m_index = current.rfind("M")
        if m_index != -1:
            if month[0] == '0':
                m_replacement = "0X"
                m_node.add_child(Node("0"))
                m_node.add_child(Node("X"))
            else:  # month[0] == '1'
                m_replacement = "1V"
                m_node.add_child(Node("1"))
                m_node.add_child(Node("V"))
            
            current = current[:m_index] + m_replacement + current[m_index+1:]
            steps.append(current)
            
            # Step 10: Expand X or V in M
            if month[0] == '0':
                x_index = current.rfind("X")
                if x_index != -1:
                    m_node.children[1].add_child(Node(month[1]))
                    current = current[:x_index] + month[1] + current[x_index+1:]
                    steps.append(current)
            else:  # month[0] == '1'
                v_index = current.rfind("V")
                if v_index != -1:
                    m_node.children[1].add_child(Node(month[1]))
                    current = current[:v_index] + month[1] + current[v_index+1:]
                    steps.append(current)
        
        return steps, root
    
    # def build_tree_from_derivation(self, steps):
    #     # A simplified tree builder for demonstration purposes
    #     root = Node("S")
        
    #     # For our specific grammar, we can build a tree directly
    #     m_node = Node("M")
    #     p1_node = Node("P")
    #     d_node = Node("D")
    #     p2_node = Node("P")
    #     y_node = Node("Y")
        
    #     root.add_child(m_node)
    #     root.add_child(p1_node)
    #     root.add_child(d_node)
    #     root.add_child(p2_node)
    #     root.add_child(y_node)
        
    #     # Y always expands to NNNN
    #     n1 = Node("N")
    #     n2 = Node("N")
    #     n3 = Node("N")
    #     n4 = Node("N")
    #     y_node.add_child(n1)
    #     y_node.add_child(n2)
    #     y_node.add_child(n3)
    #     y_node.add_child(n4)
        
    #     return root
    
    # def print_tree(self, node, prefix="", is_last=True, result=None):
    #     if result is None:
    #         result = []
        
    #     branch = "└── " if is_last else "├── "
    #     result.append(prefix + branch + node.value)
        
    #     prefix += "    " if is_last else "│   "
        
    #     for i, child in enumerate(node.children):
    #         is_last_child = i == len(node.children) - 1
    #         self.print_tree(child, prefix, is_last_child, result)
        
    #     return result