# This program computes the FIRST and FOLLOW sets for a given Context-Free Grammar.
# The grammar should be provided in a file named 'grammar.txt'.
# Rules for the grammar:
# - Use '->' to represent productions (e.g., S -> A B).
# - Symbols on the right-hand side MUST be separated by spaces.
# - Non-terminals are typically uppercase (e.g., E, T, F_PRIME).
# - Terminals are typically lowercase or symbols (e.g., id, +, *).
# - Use '#' for epsilon (the empty string).
# - Separate multiple productions for the same non-terminal with '|' (e.g., A -> a | #).

import sys

# --- Global Constants ---
EPSILON = '#'
END_MARKER = '$'
PRODUCTION_ARROW = '->'
PRODUCTION_SEPARATOR = '|'
GRAMMAR_FILE = 'grammar.txt'

# --- Global Variables ---
# Using dictionaries to store the grammar, FIRST sets, and FOLLOW sets
grammar = {}
first_sets = {}
follow_sets = {}
terminals = set()
non_terminals = set()

# --- Functions to Compute FIRST Sets ---

def compute_first(symbol):
    """Recursively computes the FIRST set for a given symbol."""
    if symbol in first_sets:
        return first_sets[symbol]

    first = set()
    if symbol in terminals:
        first.add(symbol)
        return first

    for production in grammar.get(symbol, []):
        # Case 1: Epsilon production (A -> #)
        if production == [EPSILON]:
            first.add(EPSILON)
        else:
            # Case 2 & 3: Iterate through symbols in the production
            for symbol_in_prod in production:
                # Compute FIRST of the current symbol
                char_first = compute_first(symbol_in_prod)
                # Add everything from FIRST(symbol) except epsilon
                first.update(char_first - {EPSILON})
                # If epsilon is not in FIRST(symbol), we can stop
                if EPSILON not in char_first:
                    break
            else:
                # If the loop completed, all symbols had epsilon in their FIRST sets
                first.add(EPSILON)

    first_sets[symbol] = first
    return first

# --- Functions to Compute FOLLOW Sets (Iterative Approach) ---

def compute_all_follow_sets(start_symbol):
    """Computes FOLLOW sets for all non-terminals until they stabilize."""
    # Initialize FOLLOW sets for all non-terminals to empty sets
    for nt in non_terminals:
        follow_sets[nt] = set()
    
    # Rule 1: Place $ in FOLLOW(S)
    follow_sets[start_symbol].add(END_MARKER)

    while True:
        updated = False
        for nt_head, productions in grammar.items():
            for prod in productions:
                # Rule 3: For A -> αB, everything in FOLLOW(A) is in FOLLOW(B)
                trailer = follow_sets[nt_head].copy()
                for i in range(len(prod) - 1, -1, -1):
                    symbol = prod[i]
                    if symbol in non_terminals:
                        if not trailer.issubset(follow_sets[symbol]):
                            follow_sets[symbol].update(trailer)
                            updated = True
                        
                        # Rule 2: For A -> αBβ, FIRST(β) is in FOLLOW(B)
                        first_of_beta = compute_first_of_sequence(prod[i+1:])
                        if '#' in first_of_beta:
                            trailer.update(first_of_beta - {'#'})
                        else:
                            trailer = first_of_beta
                    else: # Terminal
                        trailer = {symbol}
        
        if not updated:
            break


def compute_first_of_sequence(sequence):
    """Computes the FIRST set for a sequence of symbols."""
    first = set()
    if not sequence:
        return {EPSILON}

    for symbol in sequence:
        symbol_first = compute_first(symbol)
        first.update(symbol_first - {EPSILON})
        if EPSILON not in symbol_first:
            return first
    
    first.add(EPSILON)
    return first

# --- Main Logic ---

def main():
    """Main function to drive the program."""
    
    if len(sys.argv) != 2:
        print("Usage: python first_follow.py <grammar_file_name>")
        sys.exit(1)
    
    GRAMMAR_FILE = sys.argv[1]
    
    try:
        with open(GRAMMAR_FILE, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: '{GRAMMAR_FILE}' not found. Please create this file.")
        sys.exit(1)

    # 1. Parse the grammar from the file
    start_symbol = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        head, body = line.split(PRODUCTION_ARROW)
        head = head.strip()
        non_terminals.add(head)
        
        if start_symbol is None:
            start_symbol = head

        if head not in grammar:
            grammar[head] = []
            
        productions = [p.strip() for p in body.split(PRODUCTION_SEPARATOR)]
        for prod in productions:
            # Split by space to handle multi-character symbols
            symbols = prod.split()
            grammar[head].append(symbols)
            for symbol in symbols:
                if symbol != EPSILON and not symbol.isupper() and symbol not in non_terminals:
                     # A simple heuristic: if it's not epsilon and not obviously a non-terminal, it's a terminal
                    if 'A' <= symbol[0] <= 'Z' and len(symbol) > 1 and "'" in symbol:
                        non_terminals.add(symbol)
                    elif not ('A' <= symbol[0] <= 'Z'):
                        terminals.add(symbol)


    # Infer non-terminals that might only appear on RHS
    all_symbols = set(terminals) | non_terminals
    for nt in grammar:
        for prod in grammar[nt]:
            for symbol in prod:
                if symbol not in all_symbols and symbol != EPSILON:
                    if 'A' <= symbol[0] <= 'Z':
                        non_terminals.add(symbol)
                    else:
                        terminals.add(symbol)


    print("--- Grammar Details ---")
    print(f"Non-Terminals: {sorted(list(non_terminals))}")
    print(f"Terminals:     {sorted(list(terminals))}")
    print(f"Start Symbol:  {start_symbol}\n")

    # 2. Compute FIRST sets for all non-terminals
    for nt in non_terminals:
        compute_first(nt)
        
    print("--- FIRST Sets ---")
    for nt in sorted(list(non_terminals)):
        print(f"FIRST({nt}) = {sorted(list(first_sets.get(nt, set())))}")
    print()

    # 3. Compute FOLLOW sets for all non-terminals
    compute_all_follow_sets(start_symbol)

    print("--- FOLLOW Sets ---")
    for nt in sorted(list(non_terminals)):
        print(f"FOLLOW({nt}) = {sorted(list(follow_sets.get(nt, set())))}")


if __name__ == '__main__':
    main()