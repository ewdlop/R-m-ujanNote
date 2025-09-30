"""
Examples and demonstrations of Analytical Lambda Calculus

This module provides practical examples of lambda calculus operations
and analytical techniques.
"""

from lambda_calculus import (
    Var, Abs, App,
    beta_reduce, alpha_convert, eta_convert, normalize,
    church_numeral, church_true, church_false,
    church_and, church_or, church_not,
    church_succ, church_add, church_mult,
    Y_combinator,
    count_redexes, term_size, reduction_steps,
    is_normal_form
)


def example_identity():
    """Identity function: λx.x"""
    print("=== Identity Function ===")
    identity = Abs("x", Var("x"))
    print(f"Identity: {identity}")
    
    # Apply to a variable
    applied = App(identity, Var("a"))
    print(f"Applied to 'a': {applied}")
    
    reduced = beta_reduce(applied)
    print(f"After beta reduction: {reduced}")
    print()


def example_const():
    """Constant function: λx.λy.x"""
    print("=== Constant Function ===")
    const = Abs("x", Abs("y", Var("x")))
    print(f"Constant: {const}")
    
    # Apply to two variables
    applied = App(App(const, Var("a")), Var("b"))
    print(f"Applied to 'a' and 'b': {applied}")
    
    # First reduction
    reduced1 = beta_reduce(applied)
    print(f"After first beta reduction: {reduced1}")
    
    # Second reduction
    reduced2 = beta_reduce(reduced1)
    print(f"After second beta reduction: {reduced2}")
    print()


def example_omega():
    """Omega combinator: (λx.x x)(λx.x x) - non-terminating"""
    print("=== Omega Combinator (Non-terminating) ===")
    omega_term = Abs("x", App(Var("x"), Var("x")))
    omega = App(omega_term, omega_term)
    print(f"Omega: {omega}")
    print(f"Is in normal form: {is_normal_form(omega)}")
    print(f"Number of redexes: {count_redexes(omega)}")
    
    # Show first few reductions
    print("First 3 reduction steps:")
    steps = reduction_steps(omega, max_steps=3)
    for i, step in enumerate(steps):
        print(f"  Step {i}: {step}")
    print("  (continues infinitely...)")
    print()


def example_church_numerals():
    """Church numerals and arithmetic"""
    print("=== Church Numerals ===")
    
    zero = church_numeral(0)
    one = church_numeral(1)
    two = church_numeral(2)
    three = church_numeral(3)
    
    print(f"Church 0: {zero}")
    print(f"Church 1: {one}")
    print(f"Church 2: {two}")
    print(f"Church 3: {three}")
    print()
    
    print("=== Church Arithmetic ===")
    succ = church_succ()
    print(f"Successor: {succ}")
    
    # Compute successor of 2
    succ_two = App(succ, two)
    print(f"Successor of 2: {succ_two}")
    print(f"Reduced: {normalize(succ_two)}")
    print()
    
    # Addition
    add = church_add()
    print(f"Addition: {add}")
    add_one_two = App(App(add, one), two)
    print(f"1 + 2: {add_one_two}")
    print(f"Reduced: {normalize(add_one_two)}")
    print()
    
    # Multiplication
    mult = church_mult()
    print(f"Multiplication: {mult}")
    mult_two_three = App(App(mult, two), three)
    print(f"2 * 3: {mult_two_three}")
    print(f"Reduced: {normalize(mult_two_three)}")
    print()


def example_church_booleans():
    """Church booleans and logical operations"""
    print("=== Church Booleans ===")
    
    true = church_true()
    false = church_false()
    
    print(f"True: {true}")
    print(f"False: {false}")
    print()
    
    print("=== Boolean Operations ===")
    
    # NOT
    not_op = church_not()
    print(f"NOT: {not_op}")
    not_true = App(not_op, true)
    print(f"NOT True: {not_true}")
    print(f"Reduced: {normalize(not_true)}")
    print()
    
    # AND
    and_op = church_and()
    print(f"AND: {and_op}")
    true_and_false = App(App(and_op, true), false)
    print(f"True AND False: {true_and_false}")
    print(f"Reduced: {normalize(true_and_false)}")
    print()
    
    # OR
    or_op = church_or()
    print(f"OR: {or_op}")
    true_or_false = App(App(or_op, true), false)
    print(f"True OR False: {true_or_false}")
    print(f"Reduced: {normalize(true_or_false)}")
    print()


def example_alpha_conversion():
    """Alpha conversion (renaming bound variables)"""
    print("=== Alpha Conversion ===")
    
    term = Abs("x", App(Var("x"), Var("y")))
    print(f"Original: {term}")
    print(f"Free variables: {term.free_vars()}")
    
    converted = alpha_convert(term, "z")
    print(f"After α-conversion (x → z): {converted}")
    print(f"Free variables: {converted.free_vars()}")
    print()


def example_eta_conversion():
    """Eta conversion"""
    print("=== Eta Conversion ===")
    
    # λx.(f x) can be reduced to f if x is not free in f
    term = Abs("x", App(Var("f"), Var("x")))
    print(f"Original: {term}")
    
    converted = eta_convert(term)
    print(f"After η-conversion: {converted}")
    print()
    
    # Counter-example: λx.(x x) cannot be η-converted
    term2 = Abs("x", App(Var("x"), Var("x")))
    print(f"Counter-example: {term2}")
    converted2 = eta_convert(term2)
    print(f"η-conversion result: {converted2} (None means not applicable)")
    print()


def example_substitution():
    """Variable substitution with capture avoidance"""
    print("=== Substitution with Capture Avoidance ===")
    
    # Simple substitution
    term = App(Var("x"), Var("y"))
    print(f"Original: {term}")
    subst = term.substitute("x", Var("z"))
    print(f"After substituting x with z: {subst}")
    print()
    
    # Substitution requiring alpha conversion
    term2 = Abs("y", App(Var("x"), Var("y")))
    print(f"Original: {term2}")
    print(f"Free variables: {term2.free_vars()}")
    
    # Substitute x with y - should trigger alpha conversion
    subst2 = term2.substitute("x", Var("y"))
    print(f"After substituting x with y (avoids capture): {subst2}")
    print(f"Free variables: {subst2.free_vars()}")
    print()


def example_y_combinator():
    """Y combinator for recursion"""
    print("=== Y Combinator ===")
    
    y = Y_combinator()
    print(f"Y combinator: {y}")
    print(f"Term size: {term_size(y)}")
    print()
    
    # The Y combinator satisfies: Y f = f (Y f)
    # This allows us to define recursive functions
    print("The Y combinator enables recursion in lambda calculus")
    print("Property: Y f = f (Y f)")
    print()


def analyze_term(term, name):
    """Perform analytical operations on a term"""
    print(f"=== Analysis of {name} ===")
    print(f"Term: {term}")
    print(f"Size: {term_size(term)}")
    print(f"Free variables: {term.free_vars()}")
    print(f"Number of redexes: {count_redexes(term)}")
    print(f"Is in normal form: {is_normal_form(term)}")
    
    if not is_normal_form(term):
        print("\nReduction sequence:")
        steps = reduction_steps(term, max_steps=10)
        for i, step in enumerate(steps[:5]):  # Show first 5 steps
            print(f"  Step {i}: {step}")
        if len(steps) > 5:
            print(f"  ... ({len(steps)} total steps)")
    print()


def main():
    """Run all examples"""
    print("=" * 60)
    print("ANALYTICAL LAMBDA CALCULUS EXAMPLES")
    print("=" * 60)
    print()
    
    example_identity()
    example_const()
    example_alpha_conversion()
    example_eta_conversion()
    example_substitution()
    example_church_numerals()
    example_church_booleans()
    example_omega()
    example_y_combinator()
    
    # Analytical examples
    print("=" * 60)
    print("ANALYTICAL OPERATIONS")
    print("=" * 60)
    print()
    
    analyze_term(church_numeral(3), "Church numeral 3")
    analyze_term(
        App(church_succ(), church_numeral(2)),
        "Successor of 2"
    )
    analyze_term(
        App(App(church_add(), church_numeral(1)), church_numeral(2)),
        "1 + 2"
    )


if __name__ == "__main__":
    main()
