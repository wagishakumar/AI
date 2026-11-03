def is_variable(x):
    """Returns True if x is a variable (represented as a lowercase string)."""
    return isinstance(x, str) and x.islower()

def is_constant(x):
    """Returns True if x is a constant (represented as an uppercase string)."""
    return isinstance(x, str) and x.isupper()

def occurs_check(var, expr):
    """Returns True if the variable occurs inside the given expression."""
    if var == expr:
        return True
    if isinstance(expr, list):
        return any(occurs_check(var, sub_expr) for sub_expr in expr)
    return False

def apply_substitution(subst, expr):
    """Applies a substitution set (dictionary) to an expression recursively."""
    if not subst:
        return expr
    if isinstance(expr, str):
        return subst.get(expr, expr)
    if isinstance(expr, list):
        return [apply_substitution(subst, item) for item in expr]
    return expr

def unify(psi1, psi2):
    # Step 1: If psi1 or psi2 is a variable or constant
    if isinstance(psi1, str) or isinstance(psi2, str):
        # a) If they are identical, return NIL (empty dict representing success with no new subst)
        if psi1 == psi2:
            return {}
        
        # b) Else if psi1 is a variable
        elif is_variable(psi1):
            # a. Occurs check
            if occurs_check(psi1, psi2):
                return "FAILURE"
            # b. Return substitution {variable: replacement}
            else:
                return {psi1: psi2}
        
        # c) Else if psi2 is a variable
        elif is_variable(psi2):
            # a. Occurs check
            if occurs_check(psi2, psi1):
                return "FAILURE"
            # b. Return substitution {variable: replacement}
            else:
                return {psi2: psi1}
        
        # d) Else (both constants but not identical)
        else:
            return "FAILURE"

    # Step 2: If the initial Predicate symbol in psi1 and psi2 are not the same
    if psi1[0] != psi2[0]:
        return "FAILURE"

    # Step 3: If different number of arguments
    if len(psi1) != len(psi2):
        return "FAILURE"

    # Step 4: Set Substitution set (SUBST) to NIL (empty dictionary)
    subst = {}

    # Step 5: For i=1 to number of elements (arguments)
    for i in range(1, len(psi1)):
        # a) Call unify function with the ith element
        s = unify(psi1[i], psi2[i])
        
        # b) If S = failure then return Failure
        if s == "FAILURE":
            return "FAILURE"
        
        # c) If S != NIL (not empty)
        if s:
            # a. Apply S to the remainder of both lists
            psi1 = apply_substitution(s, psi1)
            psi2 = apply_substitution(s, psi2)
            
            # b. SUBST = APPEND(S, SUBST)
            # Update existing substitutions with the new one, and merge them
            new_subst = {k: apply_substitution(s, v) for k, v in subst.items()}
            new_subst.update(s)
            subst = new_subst

    # Step 6: Return SUBST
    return subst

# --- Example Usage ---
if __name__ == "__main__":
    # Example 1: Unifying P(x, A) and P(B, y)
    # Expected output: {'x': 'B', 'y': 'A'}
    expr1 = ["P", "x", "A"]
    expr2 = ["P", "B", "y"]
    print("Unifying P(x, A) and P(B, y):", unify(expr1, expr2))

    # Example 2: Unifying P(x, x) and P(A, B) -> Should fail because x cannot be both A and B
    expr3 = ["P", "x", "x"]
    expr4 = ["P", "A", "B"]
    print("Unifying P(x, x) and P(A, B):", unify(expr3, expr4))

    # Example 3: Occurs Check failure: Unifying P(x) and P(f(x))
    expr5 = ["P", "x"]
    expr6 = ["P", ["f", "x"]]
    print("Unifying P(x) and P(f(x)):", unify(expr5, expr6))

    expr7=["loves",["john","x"]]
    expr8=["hates",["john","x"]]
    print("Unifying P(x) and P(f(x)):", unify(expr7, expr8))