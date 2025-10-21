# This program eliminates immediate left recursion from a given Context-Free Grammar
#
# Rules for the grammar file:
# - Use '->' for productions (e.g., E -> E + T).
# - Symbols on the RHS must be separated by spaces.
# - Use '|' to separate multiple productions for the same non-terminal.
# - Use '#' for epsilon.

import sys
from collections import OrderedDict

def eliminate_left_recursion(grammar):
    """
    Eliminates immediate left recursion from a grammar.
    The algorithm works for rules of the form: A -> Aα | β
    It transforms them into:
        A -> βA'
        A' -> αA' | #
    """
    # Use an ordered dictionary to process non-terminals in a fixed order
    new_grammar = OrderedDict()
    
    # Iterate over each non-terminal in the original grammar order
    for nt in grammar:
        productions = grammar[nt]
        
        recursive_prods = []
        non_recursive_prods = []
        
        # Separate recursive and non-recursive productions
        for prod in productions:
            if prod[0] == nt:
                recursive_prods.append(prod[1:]) # Store the 'α' part
            else:
                non_recursive_prods.append(prod) # Store the 'β' part

        # If there is no left recursion for this non-terminal, copy it as is
        if not recursive_prods:
            new_grammar[nt] = productions
            continue

        # If there is left recursion, create new rules
        new_nt = nt + "'"
        
        # 1. Create the A -> βA' rules
        new_grammar[nt] = []
        for beta in non_recursive_prods:
            # If beta is epsilon, A -> A', otherwise A -> βA'
            if beta == ['#']:
                new_grammar[nt].append([new_nt])
            else:
                new_grammar[nt].append(beta + [new_nt])

        # 2. Create the A' -> αA' | # rules
        new_grammar[new_nt] = []
        for alpha in recursive_prods:
            new_grammar[new_nt].append(alpha + [new_nt])
        
        # Add the epsilon production to the new non-terminal
        new_grammar[new_nt].append(['#'])
        
    return new_grammar

def print_grammar(grammar):
    """Prints the grammar in a readable format."""
    for nt, productions in grammar.items():
        prods_str = " | ".join([" ".join(p) for p in productions])
        print(f"{nt} -> {prods_str}")

def main():
    """Main function to drive the program."""
    if len(sys.argv) != 2:
        print("Usage: python eliminate_left_recursion.py <grammar_file>")
        sys.exit(1)

    grammar_file = sys.argv[1]
    grammar = OrderedDict()

    try:
        with open(grammar_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                head, body = line.split('->')
                head = head.strip()
                
                productions = [p.strip().split() for p in body.split('|')]
                grammar[head] = productions
    except FileNotFoundError:
        print(f"Error: File '{grammar_file}' not found.")
        sys.exit(1)

    print("--- Original Grammar ---")
    print_grammar(grammar)
    
    transformed_grammar = eliminate_left_recursion(grammar)
    
    print("\n--- Grammar After Eliminating Left Recursion ---")
    print_grammar(transformed_grammar)

if __name__ == '__main__':
    main()