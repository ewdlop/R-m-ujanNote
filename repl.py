#!/usr/bin/env python3
"""
Interactive REPL for Analytical Lambda Calculus

This provides an interactive environment for experimenting with lambda calculus.
"""

import sys
from lambda_calculus import (
    Var, Abs, App,
    beta_reduce, alpha_convert, eta_convert, normalize,
    church_numeral, church_true, church_false,
    church_and, church_or, church_not,
    church_succ, church_add, church_mult,
    Y_combinator,
    count_redexes, term_size, is_normal_form, reduction_steps
)


class LambdaREPL:
    """Interactive REPL for lambda calculus"""
    
    def __init__(self):
        self.env = {}
        self._setup_builtins()
    
    def _setup_builtins(self):
        """Setup built-in definitions"""
        # Basic combinators
        self.env['id'] = Abs("x", Var("x"))
        self.env['const'] = Abs("x", Abs("y", Var("x")))
        self.env['omega'] = App(Abs("x", App(Var("x"), Var("x"))), 
                                Abs("x", App(Var("x"), Var("x"))))
        
        # Church numerals
        for i in range(10):
            self.env[f'c{i}'] = church_numeral(i)
        
        # Church booleans
        self.env['true'] = church_true()
        self.env['false'] = church_false()
        
        # Church operations
        self.env['succ'] = church_succ()
        self.env['add'] = church_add()
        self.env['mult'] = church_mult()
        self.env['and'] = church_and()
        self.env['or'] = church_or()
        self.env['not'] = church_not()
        
        # Advanced
        self.env['Y'] = Y_combinator()
    
    def print_help(self):
        """Print help message"""
        print("\n=== Lambda Calculus REPL ===")
        print("\nCommands:")
        print("  :help           - Show this help")
        print("  :list           - List all definitions")
        print("  :show <name>    - Show definition")
        print("  :reduce <name>  - Beta reduce term")
        print("  :norm <name>    - Normalize term")
        print("  :analyze <name> - Analyze term")
        print("  :steps <name>   - Show reduction steps")
        print("  :quit           - Exit REPL")
        print("\nBuilt-in definitions:")
        print("  id, const, omega")
        print("  c0, c1, c2, ..., c9  (Church numerals)")
        print("  true, false")
        print("  succ, add, mult")
        print("  and, or, not")
        print("  Y")
        print("\nExamples:")
        print("  :show id")
        print("  :norm (app id c1)")
        print("  :steps (app (app add c1) c2)")
        print()
    
    def show_definition(self, name):
        """Show a definition"""
        if name in self.env:
            term = self.env[name]
            print(f"{name} = {term}")
        else:
            print(f"Error: '{name}' not defined")
    
    def reduce_term(self, name):
        """Perform one beta reduction"""
        if name in self.env:
            term = self.env[name]
            reduced = beta_reduce(term)
            if reduced is not None:
                print(f"Original: {term}")
                print(f"Reduced:  {reduced}")
            else:
                print(f"Term is already in normal form: {term}")
        else:
            print(f"Error: '{name}' not defined")
    
    def normalize_term(self, name):
        """Normalize a term"""
        if name in self.env:
            term = self.env[name]
            print(f"Original: {term}")
            normalized = normalize(term, max_steps=100)
            print(f"Normal:   {normalized}")
        else:
            print(f"Error: '{name}' not defined")
    
    def analyze_term(self, name):
        """Analyze a term"""
        if name in self.env:
            term = self.env[name]
            print(f"\nAnalysis of '{name}':")
            print(f"  Term:         {term}")
            print(f"  Size:         {term_size(term)}")
            print(f"  Free vars:    {term.free_vars() or 'none'}")
            print(f"  Redexes:      {count_redexes(term)}")
            print(f"  Normal form:  {is_normal_form(term)}")
        else:
            print(f"Error: '{name}' not defined")
    
    def show_reduction_steps(self, name):
        """Show reduction steps"""
        if name in self.env:
            term = self.env[name]
            print(f"\nReduction steps for '{name}':")
            steps = reduction_steps(term, max_steps=10)
            for i, step in enumerate(steps):
                print(f"  Step {i}: {step}")
            if len(steps) == 11:
                print("  ... (limited to 10 steps)")
        else:
            print(f"Error: '{name}' not defined")
    
    def list_definitions(self):
        """List all definitions"""
        print("\nDefined terms:")
        for name in sorted(self.env.keys()):
            print(f"  {name:10s} = {str(self.env[name])[:60]}")
    
    def run(self):
        """Run the REPL"""
        print("=" * 60)
        print("LAMBDA CALCULUS REPL")
        print("=" * 60)
        print("Type :help for help, :quit to exit")
        
        while True:
            try:
                line = input("\nλ> ").strip()
                
                if not line:
                    continue
                
                if line == ':help':
                    self.print_help()
                elif line == ':quit':
                    print("Goodbye!")
                    break
                elif line == ':list':
                    self.list_definitions()
                elif line.startswith(':show '):
                    name = line[6:].strip()
                    self.show_definition(name)
                elif line.startswith(':reduce '):
                    name = line[8:].strip()
                    self.reduce_term(name)
                elif line.startswith(':norm '):
                    name = line[6:].strip()
                    self.normalize_term(name)
                elif line.startswith(':analyze '):
                    name = line[9:].strip()
                    self.analyze_term(name)
                elif line.startswith(':steps '):
                    name = line[7:].strip()
                    self.show_reduction_steps(name)
                else:
                    print("Unknown command. Type :help for help.")
            
            except KeyboardInterrupt:
                print("\nInterrupted. Type :quit to exit.")
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main entry point"""
    repl = LambdaREPL()
    repl.run()


if __name__ == "__main__":
    main()
