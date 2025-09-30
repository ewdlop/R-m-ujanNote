# Quick Reference Guide: Analytical Lambda Calculus

## Basic Syntax

```python
from lambda_calculus import Var, Abs, App

# Variables
x = Var("x")

# Abstraction (function definition): λx.x
identity = Abs("x", Var("x"))

# Application (function call): f x
app = App(Var("f"), Var("x"))
```

## Common Operations

### Beta Reduction

```python
from lambda_calculus import beta_reduce, normalize

# Single step reduction
term = App(Abs("x", Var("x")), Var("a"))  # (λx.x) a
reduced = beta_reduce(term)  # a

# Reduce to normal form
result = normalize(term)  # a
```

### Alpha Conversion

```python
from lambda_calculus import alpha_convert

# Rename bound variable
term = Abs("x", Var("x"))  # λx.x
converted = alpha_convert(term, "y")  # λy.y
```

### Eta Conversion

```python
from lambda_calculus import eta_convert

# λx.(f x) → f
term = Abs("x", App(Var("f"), Var("x")))
converted = eta_convert(term)  # Var("f")
```

## Church Numerals

```python
from lambda_calculus import church_numeral, church_succ, church_add, church_mult

# Create numerals
zero = church_numeral(0)   # λf.λx.x
one = church_numeral(1)    # λf.λx.f x
two = church_numeral(2)    # λf.λx.f(f x)

# Successor
succ = church_succ()       # λn.λf.λx.f(n f x)
three = normalize(App(succ, two))

# Addition
add = church_add()         # λm.λn.λf.λx.m f (n f x)
result = normalize(App(App(add, one), two))  # 3

# Multiplication
mult = church_mult()       # λm.λn.λf.m(n f)
result = normalize(App(App(mult, two), two))  # 4
```

## Church Booleans

```python
from lambda_calculus import church_true, church_false, church_and, church_or, church_not

# Boolean values
true = church_true()       # λt.λf.t
false = church_false()     # λt.λf.f

# Logic operations
and_op = church_and()      # λp.λq.p q p
or_op = church_or()        # λp.λq.p p q
not_op = church_not()      # λp.λt.λf.p f t

# Examples
result = normalize(App(App(and_op, true), false))  # false
result = normalize(App(App(or_op, true), false))   # true
result = normalize(App(not_op, true))              # false
```

## Analysis Functions

```python
from lambda_calculus import count_redexes, term_size, is_normal_form, reduction_steps

term = App(Abs("x", Var("x")), Var("a"))

# Count beta-redexes
num_redexes = count_redexes(term)  # 1

# Calculate term size
size = term_size(term)  # 4

# Check if in normal form
is_normal = is_normal_form(term)  # False

# Get reduction sequence
steps = reduction_steps(term, max_steps=10)
for i, step in enumerate(steps):
    print(f"Step {i}: {step}")
```

## Working with Free Variables

```python
term = Abs("x", App(Var("x"), Var("y")))

# Get free variables
free = term.free_vars()  # {'y'}

# Substitute variables
substituted = term.substitute("y", Var("z"))
# Result: λx.x z (with capture avoidance)
```

## Advanced: Y Combinator

```python
from lambda_calculus import Y_combinator

# Fixed-point combinator for recursion
Y = Y_combinator()  # λf.(λx.f(x x))(λx.f(x x))

# Use Y to define recursive functions
# Example: factorial = Y (λf.λn.if (n=0) 1 (n * f(n-1)))
```

## Common Patterns

### Compose two functions

```python
# compose = λf.λg.λx.f(g x)
compose = Abs("f", Abs("g", Abs("x", 
    App(Var("f"), App(Var("g"), Var("x"))))))
```

### Apply function twice

```python
# twice = λf.λx.f(f x)
twice = Abs("f", Abs("x", 
    App(Var("f"), App(Var("f"), Var("x")))))
```

### Church pair

```python
# pair = λx.λy.λf.f x y
pair = Abs("x", Abs("y", Abs("f", 
    App(App(Var("f"), Var("x")), Var("y")))))

# fst = λp.p (λx.λy.x)
fst = Abs("p", App(Var("p"), church_true()))

# snd = λp.p (λx.λy.y)  
snd = Abs("p", App(Var("p"), church_false()))
```

## Tips

1. **Always normalize** after operations to get the final result
2. **Use max_steps** in normalize() to prevent infinite loops
3. **Check is_normal_form()** to verify if reduction is complete
4. **Count redexes** to estimate computation complexity
5. **Use alpha_convert** when you need to avoid name conflicts manually

## Common Issues

### Non-terminating Reduction

```python
# Omega combinator: (λx.x x)(λx.x x)
omega_term = Abs("x", App(Var("x"), Var("x")))
omega = App(omega_term, omega_term)

# This never terminates!
# result = normalize(omega)  # Will stop after max_steps

# Use with caution and appropriate max_steps
steps = reduction_steps(omega, max_steps=5)
```

### Variable Capture

The implementation handles capture-avoiding substitution automatically:

```python
# Substituting x with y in λy.x y
term = Abs("y", App(Var("x"), Var("y")))
result = term.substitute("x", Var("y"))
# Automatically renames bound y to avoid capture
# Result: λy_1.y y_1
```

## Performance Notes

- **Term size grows** during reduction (especially with Church numerals)
- **Reduction complexity** can be exponential in worst case
- **Use smaller max_steps** for exploration, larger for computation
- **Normal order** reduction (implemented) guarantees finding normal form if it exists

## Running Tests

```bash
# Run all tests
python3 test_lambda_calculus.py

# Run examples
python3 examples.py
```

## Further Reading

- See `README.md` for detailed overview
- See `THEORY.md` for mathematical foundations
- See `examples.py` for comprehensive examples
- See `lambda_calculus.py` for implementation details
