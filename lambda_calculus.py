"""
Analytical Lambda Calculus Implementation

This module implements the core concepts of lambda calculus including:
- Lambda terms (variables, abstractions, applications)
- Beta reduction
- Alpha conversion
- Eta conversion
- Normal form evaluation
"""

from typing import Set, Dict, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


class LambdaTerm(ABC):
    """Abstract base class for lambda calculus terms"""
    
    @abstractmethod
    def free_vars(self) -> Set[str]:
        """Return the set of free variables in the term"""
        pass
    
    @abstractmethod
    def substitute(self, var: str, term: 'LambdaTerm') -> 'LambdaTerm':
        """Substitute all free occurrences of var with term"""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        pass


@dataclass
class Var(LambdaTerm):
    """Variable term"""
    name: str
    
    def free_vars(self) -> Set[str]:
        return {self.name}
    
    def substitute(self, var: str, term: LambdaTerm) -> LambdaTerm:
        if self.name == var:
            return term
        return self
    
    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Var) and self.name == other.name


@dataclass
class Abs(LambdaTerm):
    """Lambda abstraction (λx.M)"""
    var: str
    body: LambdaTerm
    
    def free_vars(self) -> Set[str]:
        return self.body.free_vars() - {self.var}
    
    def substitute(self, var: str, term: LambdaTerm) -> LambdaTerm:
        if self.var == var:
            # Bound variable shadows the substitution
            return self
        elif self.var not in term.free_vars():
            # Safe to substitute in body
            return Abs(self.var, self.body.substitute(var, term))
        else:
            # Need alpha conversion to avoid capture
            fresh_var = self._fresh_var(term.free_vars() | self.body.free_vars() | {var})
            renamed_body = self.body.substitute(self.var, Var(fresh_var))
            return Abs(fresh_var, renamed_body.substitute(var, term))
    
    def _fresh_var(self, avoid: Set[str]) -> str:
        """Generate a fresh variable name not in avoid"""
        base = self.var
        counter = 1
        while f"{base}_{counter}" in avoid:
            counter += 1
        return f"{base}_{counter}"
    
    def __str__(self) -> str:
        return f"(λ{self.var}.{self.body})"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Abs) and self.var == other.var and self.body == other.body


@dataclass
class App(LambdaTerm):
    """Application (M N)"""
    func: LambdaTerm
    arg: LambdaTerm
    
    def free_vars(self) -> Set[str]:
        return self.func.free_vars() | self.arg.free_vars()
    
    def substitute(self, var: str, term: LambdaTerm) -> LambdaTerm:
        return App(self.func.substitute(var, term), self.arg.substitute(var, term))
    
    def __str__(self) -> str:
        func_str = str(self.func)
        arg_str = str(self.arg)
        
        # Add parentheses for clarity
        if isinstance(self.arg, App) or isinstance(self.arg, Abs):
            arg_str = f"({arg_str})"
        
        return f"{func_str} {arg_str}"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, App) and self.func == other.func and self.arg == other.arg


# Analytical Operations

def beta_reduce(term: LambdaTerm) -> Optional[LambdaTerm]:
    """
    Perform one step of beta reduction.
    Returns None if no reduction is possible.
    """
    if isinstance(term, Var):
        return None
    
    elif isinstance(term, Abs):
        # Try to reduce the body
        reduced_body = beta_reduce(term.body)
        if reduced_body is not None:
            return Abs(term.var, reduced_body)
        return None
    
    elif isinstance(term, App):
        # Beta reduction: (λx.M) N → M[x := N]
        if isinstance(term.func, Abs):
            return term.func.body.substitute(term.func.var, term.arg)
        
        # Try to reduce the function
        reduced_func = beta_reduce(term.func)
        if reduced_func is not None:
            return App(reduced_func, term.arg)
        
        # Try to reduce the argument
        reduced_arg = beta_reduce(term.arg)
        if reduced_arg is not None:
            return App(term.func, reduced_arg)
        
        return None


def alpha_convert(term: Abs, new_var: str) -> Abs:
    """
    Perform alpha conversion: rename the bound variable.
    λx.M → λy.M[x := y]
    """
    return Abs(new_var, term.body.substitute(term.var, Var(new_var)))


def eta_convert(term: LambdaTerm) -> Optional[LambdaTerm]:
    """
    Perform eta conversion: λx.(M x) → M (if x not free in M)
    Returns None if eta conversion is not applicable.
    """
    if isinstance(term, Abs):
        if isinstance(term.body, App):
            if isinstance(term.body.arg, Var) and term.body.arg.name == term.var:
                if term.var not in term.body.func.free_vars():
                    return term.body.func
    return None


def normalize(term: LambdaTerm, max_steps: int = 1000) -> LambdaTerm:
    """
    Reduce term to normal form using beta reduction.
    Stops after max_steps to prevent infinite loops.
    """
    steps = 0
    current = term
    
    while steps < max_steps:
        reduced = beta_reduce(current)
        if reduced is None:
            break
        current = reduced
        steps += 1
    
    return current


def is_normal_form(term: LambdaTerm) -> bool:
    """Check if term is in normal form (cannot be reduced further)"""
    return beta_reduce(term) is None


# Church Encodings (examples of analytical lambda calculus)

def church_numeral(n: int) -> LambdaTerm:
    """Create Church numeral for natural number n"""
    # λf.λx.f(f(...(f x)...)) with n applications of f
    body = Var("x")
    for _ in range(n):
        body = App(Var("f"), body)
    return Abs("f", Abs("x", body))


def church_true() -> LambdaTerm:
    """Church encoding of true: λt.λf.t"""
    return Abs("t", Abs("f", Var("t")))


def church_false() -> LambdaTerm:
    """Church encoding of false: λt.λf.f"""
    return Abs("t", Abs("f", Var("f")))


def church_and() -> LambdaTerm:
    """Church encoding of AND: λp.λq.p q p"""
    return Abs("p", Abs("q", App(App(Var("p"), Var("q")), Var("p"))))


def church_or() -> LambdaTerm:
    """Church encoding of OR: λp.λq.p p q"""
    return Abs("p", Abs("q", App(App(Var("p"), Var("p")), Var("q"))))


def church_not() -> LambdaTerm:
    """Church encoding of NOT: λp.λt.λf.p f t"""
    return Abs("p", Abs("t", Abs("f", App(App(Var("p"), Var("f")), Var("t")))))


def church_succ() -> LambdaTerm:
    """Church encoding of successor: λn.λf.λx.f(n f x)"""
    return Abs("n", Abs("f", Abs("x", 
        App(Var("f"), App(App(Var("n"), Var("f")), Var("x"))))))


def church_add() -> LambdaTerm:
    """Church encoding of addition: λm.λn.λf.λx.m f (n f x)"""
    return Abs("m", Abs("n", Abs("f", Abs("x",
        App(App(Var("m"), Var("f")), 
            App(App(Var("n"), Var("f")), Var("x")))))))


def church_mult() -> LambdaTerm:
    """Church encoding of multiplication: λm.λn.λf.m(n f)"""
    return Abs("m", Abs("n", Abs("f", 
        App(Var("m"), App(Var("n"), Var("f"))))))


def Y_combinator() -> LambdaTerm:
    """Y combinator for recursion: λf.(λx.f(x x))(λx.f(x x))"""
    inner = Abs("x", App(Var("f"), App(Var("x"), Var("x"))))
    return Abs("f", App(inner, inner))


# Helper functions for analysis

def count_redexes(term: LambdaTerm) -> int:
    """Count the number of beta-redexes in a term"""
    if isinstance(term, Var):
        return 0
    elif isinstance(term, Abs):
        return count_redexes(term.body)
    elif isinstance(term, App):
        count = count_redexes(term.func) + count_redexes(term.arg)
        if isinstance(term.func, Abs):
            count += 1  # This application is a redex
        return count
    return 0


def term_size(term: LambdaTerm) -> int:
    """Calculate the size of a term (number of nodes)"""
    if isinstance(term, Var):
        return 1
    elif isinstance(term, Abs):
        return 1 + term_size(term.body)
    elif isinstance(term, App):
        return 1 + term_size(term.func) + term_size(term.arg)
    return 0


def reduction_steps(term: LambdaTerm, max_steps: int = 1000) -> list:
    """
    Return the sequence of reduction steps.
    Useful for analytical purposes.
    """
    steps = [term]
    current = term
    
    for _ in range(max_steps):
        reduced = beta_reduce(current)
        if reduced is None:
            break
        steps.append(reduced)
        current = reduced
    
    return steps
