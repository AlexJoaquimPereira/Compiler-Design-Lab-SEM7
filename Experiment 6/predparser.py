# File: predictive_parser.py
# This version uses the robust iterative FOLLOW set algorithm
# and a custom table-printing function that formats for a terminal.

import sys
# import pandas as pd # <-- Removed pandas dependency

# --- Global Constants ---
EPSILON = '#'
END_MARKER = '$'
PRODUCTION_ARROW = '->'
PRODUCTION_SEPARATOR = '|'

# --- Global Data Structures ---
grammar = {}
first_sets = {}
follow_sets = {}
terminals = set()
non_terminals = set()
parsing_table = {}

# -----------------------------------------------------------------------------
# FIRST computation
# -----------------------------------------------------------------------------
def compute_first(symbol):
    if symbol in first_sets:
        return first_sets[symbol]

    first = set()

    # Terminal or epsilon
    if symbol in terminals:
        first.add(symbol)
    elif symbol == EPSILON:
        first.add(EPSILON)
    # Non-terminal
    elif symbol in grammar:
        for production in grammar.get(symbol, []):
            if production == [EPSILON]:
                first.add(EPSILON)
            else:
                for sym in production:
                    sym_first = compute_first(sym)
                    first.update(sym_first - {EPSILON})
                    if EPSILON not in sym_first:
                        break
                else:
                    first.add(EPSILON)

    first_sets[symbol] = first
    return first

def compute_first_of_sequence(sequence):
    if not sequence:
        return {EPSILON}
    result = set()
    for sym in sequence:
        sym_first = compute_first(sym)
        result.update(sym_first - {EPSILON})
        if EPSILON not in sym_first:
            return result
    result.add(EPSILON)
    return result

# -----------------------------------------------------------------------------
# FOLLOW computation (Iterative algorithm)
# -----------------------------------------------------------------------------
def compute_all_follow_sets(start_symbol):
    # initialize
    for nt in non_terminals:
        follow_sets[nt] = set()
    follow_sets[start_symbol].add(END_MARKER)

    updated = True
    while updated:
        updated = False
        # For each production A -> alpha
        for A, productions in grammar.items():
            for prod in productions:
                prod_len = len(prod)
                for i, B in enumerate(prod):
                    if B not in non_terminals:
                        continue
                    # beta is the sequence after B
                    beta = prod[i+1:] if i+1 < prod_len else []
                    first_beta = compute_first_of_sequence(beta)
                    # Add FIRST(beta) - {EPSILON} to FOLLOW(B)
                    to_add = (first_beta - {EPSILON})
                    if not to_add.issubset(follow_sets[B]):
                        follow_sets[B].update(to_add)
                        updated = True
                    # If beta is empty OR FIRST(beta) contains EPSILON, add FOLLOW(A) to FOLLOW(B)
                    if (not beta) or (EPSILON in first_beta):
                        if not follow_sets[A].issubset(follow_sets[B]):
                            follow_sets[B].update(follow_sets[A])
                            updated = True

# -----------------------------------------------------------------------------
# Parsing table construction
# -----------------------------------------------------------------------------
def construct_parsing_table(start_symbol):
    all_terminals = sorted(list(terminals)) + [END_MARKER]
    for nt in non_terminals:
        parsing_table[nt] = {}
        for t in all_terminals:
            parsing_table[nt][t] = None  # None signifies an error

    for nt, productions in grammar.items():
        for prod in productions:
            first_of_prod = compute_first_of_sequence(prod)
            for terminal in (first_of_prod - {EPSILON}):
                if parsing_table[nt][terminal] is not None:
                    print(f"Error: LL(1) conflict at M[{nt}, {terminal}]!")
                    print(f"  Existing: {nt} -> {' '.join(parsing_table[nt][terminal])}")
                    print(f"  New:      {nt} -> {' '.join(prod)}")
                    return False
                parsing_table[nt][terminal] = prod

            if EPSILON in first_of_prod:
                for terminal in follow_sets[nt]:
                    if parsing_table[nt][terminal] is not None:
                        print(f"Error: LL(1) conflict at M[{nt}, {terminal}]!")
                        print(f"  Existing: {nt} -> {' '.join(parsing_table[nt][terminal])}")
                        print(f"  New:      {nt} -> {' '.join(prod)}")
                        return False
                    parsing_table[nt][terminal] = prod
    return True

# --- MODIFIED FUNCTION (No Pandas) ---
def print_parsing_table():
    """Prints the parsing table formatted for a standard terminal."""
    print("\n--- Predictive Parsing Table ---")
    
    all_terminals = sorted(list(terminals)) + [END_MARKER]
    
    # Find max width for the first column (Non-Terminal names)
    max_nt_len = max(len(nt) for nt in non_terminals)
    
    # Calculate widths for each terminal column
    col_widths = {}
    for t in all_terminals:
        # Start with the width of the terminal name itself
        max_width = len(t)
        for nt in non_terminals:
            prod = parsing_table[nt].get(t)
            if prod:
                # Use a shorter "-> rule" format to save space
                prod_str = f"-> {' '.join(prod)}"
                max_width = max(max_width, len(prod_str))
        # Add 2 for padding
        col_widths[t] = max(max_width, len("Error")) + 2

    # --- Print Header ---
    print(f"{'':<{max_nt_len}} |", end="")
    for t in all_terminals:
        print(f" {t:^{col_widths[t]-2}} |", end="")
    
    # --- Print Separator ---
    total_width = max_nt_len + 1 + sum(col_widths.values()) + len(all_terminals) * 2
    print("\n" + "-" * total_width)

    # --- Print Rows ---
    for nt in sorted(list(non_terminals)):
        print(f"{nt:<{max_nt_len}} |", end="")
        for t in all_terminals:
            prod = parsing_table[nt].get(t)
            if prod:
                prod_str = f"-> {' '.join(prod)}"
            else:
                prod_str = "Error"
            print(f" {prod_str:^{col_widths[t]-2}} |", end="")
        print() # Newline for next row

# -----------------------------------------------------------------------------
# Parser driver
# -----------------------------------------------------------------------------
def parse_input_string(input_str, start_symbol):
    print("\n--- Parsing Input String ---")
    print(f"Input: '{input_str}'\n")

    tokens = input_str.split() + [END_MARKER]
    stack = [END_MARKER, start_symbol]
    input_pointer = 0

    # Calculate max stack width for formatting
    max_stack_width = len(' '.join(stack)) + 20
    
    print(f"{'Stack':<{max_stack_width}} | {'Input':<30} | {'Action':<40}")
    print("-" * (max_stack_width + 30 + 40 + 6))

    while stack:
        stack_str = ' '.join(stack)
        input_str_remaining = ' '.join(tokens[input_pointer:])

        top_of_stack = stack[-1]
        current_input = tokens[input_pointer]

        # Terminal or end marker on top
        if top_of_stack in terminals or top_of_stack == END_MARKER:
            if top_of_stack == current_input:
                action = f"Match and pop '{current_input}'"
                stack.pop()
                input_pointer += 1
            else:
                action = f"Error: Mismatch (Stack: {top_of_stack}, Input: {current_input})"
                print(f"{stack_str:<{max_stack_width}} | {input_str_remaining:<30} | {action:<40}")
                print("\nParsing failed: Mismatch error.")
                return False

        # Non-terminal on top
        elif top_of_stack in non_terminals:
            production = parsing_table[top_of_stack].get(current_input)
            if production is None:
                action = f"Error: No table entry for M[{top_of_stack}, {current_input}]"
                print(f"{stack_str:<{max_stack_width}} | {input_str_remaining:<30} | {action:<40}")
                print("\nParsing failed: Syntax error.")
                return False

            action = f"Apply: {top_of_stack} -> {' '.join(production)}"
            stack.pop()
            if production != [EPSILON]:
                for symbol in reversed(production):
                    stack.append(symbol)
                
                # Update max stack width if it grew
                stack_str_len = len(' '.join(stack))
                if stack_str_len > max_stack_width - 5:
                    max_stack_width = stack_str_len + 10
        else:
            action = f"Error: Unknown symbol on stack: {top_of_stack}"
            print(f"{stack_str:<{max_stack_width}} | {input_str_remaining:<30} | {action:<40}")
            return False

        print(f"{stack_str:<{max_stack_width}} | {input_str_remaining:<30} | {action:<40}")

        if top_of_stack == END_MARKER and current_input == END_MARKER:
            print("\nParsing successful!")
            return True

    return False

# -----------------------------------------------------------------------------
# Main execution
# -----------------------------------------------------------------------------
def main():
    if len(sys.argv) != 3:
        print("Usage: python predictive_parser.py <grammar_file> <input_string_file>")
        sys.exit(1)

    grammar_file = sys.argv[1]
    input_file = sys.argv[2]

    # --- 1. Parse Grammar ---
    try:
        with open(grammar_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Grammar file '{grammar_file}' not found.")
        sys.exit(1)

    start_symbol = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if PRODUCTION_ARROW not in line:
            print(f"Ignoring malformed line (no '{PRODUCTION_ARROW}'): {line}")
            continue

        head, body = line.split(PRODUCTION_ARROW, 1)
        head = head.strip()
        non_terminals.add(head)

        if start_symbol is None:
            start_symbol = head
        if head not in grammar:
            grammar[head] = []

        productions = [p.strip() for p in body.split(PRODUCTION_SEPARATOR)]
        for prod in productions:
            symbols = prod.split() if prod != '' else []
            if not symbols:
                symbols = [EPSILON]
            grammar[head].append(symbols)
            for symbol in symbols:
                if symbol != EPSILON and not ('A' <= symbol[0] <= 'Z'):
                    terminals.add(symbol)

    # Add any symbol that looks like non-terminal but wasn't seen as head
    all_symbols = set(terminals) | non_terminals | {EPSILON}
    for nt in list(grammar):
        for prod in grammar[nt]:
            for symbol in prod:
                # Basic check: if it starts with a capital, it's a non-terminal
                if ('A' <= symbol[0] <= 'Z') and symbol not in all_symbols:
                    non_terminals.add(symbol)
                    all_symbols.add(symbol)

    print("--- Grammar Details ---")
    print(f"Non-Terminals: {sorted(list(non_terminals))}")
    print(f"Terminals:     {sorted(list(terminals))}")
    print(f"Start Symbol:  {start_symbol}\n")

    # --- 2. Compute FIRST Sets ---
    for nt in non_terminals:
        compute_first(nt)

    # --- 3. Compute FOLLOW Sets (fixed) ---
    compute_all_follow_sets(start_symbol)

    # --- 4. Construct Parsing Table ---
    if not construct_parsing_table(start_symbol):
        print("\nGrammar is not LL(1). Halting.")
        sys.exit(1)

    print_parsing_table()

    # --- 5. Parse Input String ---
    try:
        with open(input_file, 'r') as f:
            input_str = f.read().strip()
    except FileNotFoundError:
        print(f"\nError: Input file '{input_file}' not found.")
        sys.exit(1)

    parse_input_string(input_str, start_symbol)


if __name__ == '__main__':
    main()

