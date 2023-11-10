import argparse

dpll_calls = 1

def read_cnf_file(cnf_filename):
    clauses = []
    with open(cnf_filename, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                clause = line.strip().split()
                clauses.append(clause)
    return clauses

def DPLL_SATISFIABLE(clauses, symbols, model):
    global dpll_calls
    dpll_calls += 1

    def all_clauses_true(clauses, model):
        all_true = True

        for clause in clauses:
            # Check if at least one literal in the clause is true
            clause_satisfied = False
            for literal in clause:
                if literal[0] == '-':
                    # Handle negative literal
                    symbol = literal[1:]  # Remove the '-' sign
                    if symbol in model and model[symbol] == -1:
                        clause_satisfied = True
                        break
                else:
                    # Handle positive literal
                    symbol = literal
                    if symbol in model and model[symbol] == 1:
                        clause_satisfied = True
                        break

            if not clause_satisfied:
                print("All clauses NOT TRUE")
                all_true = False
                break

        return all_true

    def contains_unassigned(clause, model):
        for literal in clause:
            # Check if the literal or its negation is unassigned
            if literal in model:
                if model[literal] == 0:
                    return True
            elif literal[0] == '-':
                    symbol = literal[1:]
                    if model[symbol] == 0:
                        return True
        # print("all literals assigned, clause:", clause)
        return False

    def some_clause_false(clauses, model):
        for clause in clauses:
            # Check if the clause contains any unassigned (0) literals at the beginning
            if contains_unassigned(clause, model):
                continue

            clause_satisfied = False  # Assume the clause is satisfied until proven otherwise
            for literal in clause:
                if literal[0] == '-':
                    # Handle negative literal
                    symbol = literal[1:]  # Remove the '-' sign
                    if model[symbol] == -1:
                        # print(f"False literal: -{symbol}")
                        clause_satisfied = True
                        break
                else:
                    # Handle positive literal
                    symbol = literal
                    if model[symbol] == 1:
                        # print("False literal:", symbol)
                        clause_satisfied = True
                        break

            if not clause_satisfied:
                print("SOME CLAUSES FALSE")
                return True

        print("NO CLAUSES FALSE")
        return False

    def find_unit_clause(clauses, model):
        for clause in clauses:
            negated = False  # Reset the negated flag for each clause
            unassigned_literals = []

            for literal in clause:
                if literal[0] == '-':
                    literal = literal[1:]
                    negated = True

                if literal in model and model[literal] == 1:
                    break
                elif literal in model and model[literal] == 0:
                    unassigned_literals.append(literal)

            if len(unassigned_literals) == 1:
                return unassigned_literals[0] if not negated else '-' + unassigned_literals[0]

        return None


    if all_clauses_true(clauses, model):
        print("backtracking")
        return model
    
    if some_clause_false(clauses, model):
        print("backtracking")
        return None

    if args.UCH:
        unit_clause = find_unit_clause(clauses, model)
        
        if unit_clause:
            new_model = model.copy()
            if unit_clause[0] == '-':
                unit_clause = unit_clause[1:]
                new_model[unit_clause] = 1  # Negate the value for unit_clause
            else:
                new_model[unit_clause] = -1

            new_symbols = [sym for sym in symbols if sym != unit_clause]  # Remove unit_clause from new_symbols
            print(f"forcing {unit_clause}=1 by uch")
            result = DPLL_SATISFIABLE(clauses, new_symbols, new_model)
            if result:
                return result

    if not symbols:
        return model
    
    print_model(model)

    print("choice point")
    first_symbol = symbols[0]
    rest_symbols = symbols[1:]
    new_model_true = model.copy()
    new_model_true[first_symbol] = 1
    print(f"trying {first_symbol}=T")
    result = DPLL_SATISFIABLE(clauses, rest_symbols, new_model_true)
    if result:
        return result
    
    model[first_symbol] = 0  # Restore the original state

    new_model_false = model.copy()
    new_model_false[first_symbol] = -1
    print(f"trying {first_symbol}=F")
    return DPLL_SATISFIABLE(clauses, rest_symbols, new_model_false)

def extract_symbol(literal):
    if literal.startswith('-'):
        return literal[1:]  # Remove the '-' sign for negation
    return literal

def print_model(model):
    sorted_model = dict(sorted(model.items()))
    print("model: {", end=" ")
    for symbol, value in sorted_model.items():
        print(f"{symbol}: {value}", end=" ")
    print("}")

def print_solution(model):
    if model is not None:
        sorted_model = dict(sorted(model.items()))
        print("solution:")
        for literal, value in sorted_model.items():
            print(f"{literal}: {value}")
    else:
        print("No solution found (UNSATISFIABLE)")

# -----------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("literals", nargs="*")
parser.add_argument("--UCH", action="store_true")

args = parser.parse_args()

cnf_filename = args.filename
cnf_clauses = read_cnf_file(cnf_filename)

symbols = list(extract_symbol(literal) for clause in cnf_clauses for literal in clause)

model = {extract_symbol(literal): 0 for literal in symbols}

for literal in args.literals:
    symbol = literal
    model[symbol] = 1

result = DPLL_SATISFIABLE(cnf_clauses, symbols, model)

# ----------------------------------------------------------------------------------------------

print("-------------")
print_solution(result)

true_literals = []
if result is not None:
    true_literals = [literal for literal, value in result.items() if value == 1]
    print("just the satisfied (true) propositions:")
    print(" ".join(true_literals))

    print("DPLL calls =", dpll_calls)

    if args.UCH:
        print("UCH=True")
    else:
        print("UCH=False")
