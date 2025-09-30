"""
Test suite for Analytical Lambda Calculus implementation

This module contains tests for verifying the correctness of lambda calculus
operations and analytical properties.
"""

import unittest
from lambda_calculus import (
    Var, Abs, App,
    beta_reduce, alpha_convert, eta_convert, normalize,
    church_numeral, church_true, church_false,
    church_and, church_or, church_not,
    church_succ, church_add, church_mult,
    count_redexes, term_size, is_normal_form
)


class TestLambdaTerms(unittest.TestCase):
    """Test basic lambda term operations"""
    
    def test_var_creation(self):
        """Test variable creation"""
        var = Var("x")
        self.assertEqual(str(var), "x")
        self.assertEqual(var.free_vars(), {"x"})
    
    def test_abs_creation(self):
        """Test abstraction creation"""
        abs_term = Abs("x", Var("x"))
        self.assertEqual(str(abs_term), "(λx.x)")
        self.assertEqual(abs_term.free_vars(), set())
    
    def test_app_creation(self):
        """Test application creation"""
        app = App(Var("f"), Var("x"))
        self.assertEqual(str(app), "f x")
        self.assertEqual(app.free_vars(), {"f", "x"})
    
    def test_free_vars_nested(self):
        """Test free variables in nested terms"""
        term = Abs("x", App(Var("x"), Var("y")))
        self.assertEqual(term.free_vars(), {"y"})


class TestBetaReduction(unittest.TestCase):
    """Test beta reduction operations"""
    
    def test_identity_reduction(self):
        """Test (λx.x) a → a"""
        identity = Abs("x", Var("x"))
        applied = App(identity, Var("a"))
        reduced = beta_reduce(applied)
        self.assertEqual(reduced, Var("a"))
    
    def test_const_reduction(self):
        """Test (λx.λy.x) a b → a"""
        const = Abs("x", Abs("y", Var("x")))
        applied = App(App(const, Var("a")), Var("b"))
        
        # First reduction
        reduced1 = beta_reduce(applied)
        self.assertIsNotNone(reduced1)
        
        # Second reduction
        reduced2 = beta_reduce(reduced1)
        self.assertEqual(reduced2, Var("a"))
    
    def test_normalize_identity(self):
        """Test normalizing identity application"""
        identity = Abs("x", Var("x"))
        applied = App(identity, Var("a"))
        normalized = normalize(applied)
        self.assertEqual(normalized, Var("a"))
    
    def test_no_reduction_on_normal_form(self):
        """Test that normal forms cannot be reduced"""
        var = Var("x")
        self.assertIsNone(beta_reduce(var))
        
        abs_term = Abs("x", Var("x"))
        self.assertIsNone(beta_reduce(abs_term))


class TestSubstitution(unittest.TestCase):
    """Test variable substitution"""
    
    def test_simple_substitution(self):
        """Test simple variable substitution"""
        term = Var("x")
        result = term.substitute("x", Var("y"))
        self.assertEqual(result, Var("y"))
    
    def test_no_substitution(self):
        """Test substitution of non-occurring variable"""
        term = Var("x")
        result = term.substitute("y", Var("z"))
        self.assertEqual(result, Var("x"))
    
    def test_substitution_in_abstraction(self):
        """Test substitution in abstraction"""
        term = Abs("x", App(Var("y"), Var("x")))
        result = term.substitute("y", Var("z"))
        expected = Abs("x", App(Var("z"), Var("x")))
        self.assertEqual(result, expected)
    
    def test_capture_avoidance(self):
        """Test that substitution avoids variable capture"""
        term = Abs("y", App(Var("x"), Var("y")))
        result = term.substitute("x", Var("y"))
        
        # Should perform alpha conversion to avoid capture
        # The bound y should be renamed
        self.assertNotEqual(result.var, "y")
        self.assertEqual(result.free_vars(), {"y"})


class TestAlphaConversion(unittest.TestCase):
    """Test alpha conversion"""
    
    def test_alpha_rename(self):
        """Test renaming bound variable"""
        term = Abs("x", Var("x"))
        converted = alpha_convert(term, "y")
        self.assertEqual(converted, Abs("y", Var("y")))
    
    def test_alpha_preserves_free_vars(self):
        """Test that alpha conversion preserves free variables"""
        term = Abs("x", App(Var("x"), Var("y")))
        converted = alpha_convert(term, "z")
        self.assertEqual(term.free_vars(), converted.free_vars())


class TestEtaConversion(unittest.TestCase):
    """Test eta conversion"""
    
    def test_eta_reduction(self):
        """Test λx.(f x) → f"""
        term = Abs("x", App(Var("f"), Var("x")))
        result = eta_convert(term)
        self.assertEqual(result, Var("f"))
    
    def test_no_eta_when_var_free(self):
        """Test that eta doesn't apply when variable is free"""
        term = Abs("x", App(Var("x"), Var("x")))
        result = eta_convert(term)
        self.assertIsNone(result)
    
    def test_no_eta_on_non_matching_pattern(self):
        """Test that eta doesn't apply to non-matching patterns"""
        term = Abs("x", Var("x"))
        result = eta_convert(term)
        self.assertIsNone(result)


class TestChurchNumerals(unittest.TestCase):
    """Test Church numeral encodings"""
    
    def test_church_zero(self):
        """Test Church numeral 0"""
        zero = church_numeral(0)
        self.assertEqual(str(zero), "(λf.(λx.x))")
    
    def test_church_numerals(self):
        """Test Church numerals 1-3"""
        one = church_numeral(1)
        two = church_numeral(2)
        three = church_numeral(3)
        
        self.assertEqual(str(one), "(λf.(λx.f x))")
        self.assertEqual(str(two), "(λf.(λx.f (f x)))")
        self.assertEqual(str(three), "(λf.(λx.f (f (f x))))")
    
    def test_church_successor(self):
        """Test successor function"""
        succ = church_succ()
        two = church_numeral(2)
        three = church_numeral(3)
        
        succ_two = normalize(App(succ, two))
        self.assertEqual(str(succ_two), str(three))
    
    def test_church_addition(self):
        """Test addition of Church numerals"""
        add = church_add()
        one = church_numeral(1)
        two = church_numeral(2)
        three = church_numeral(3)
        
        one_plus_two = normalize(App(App(add, one), two))
        self.assertEqual(str(one_plus_two), str(three))
    
    def test_church_multiplication(self):
        """Test multiplication of Church numerals"""
        mult = church_mult()
        two = church_numeral(2)
        three = church_numeral(3)
        six = church_numeral(6)
        
        two_times_three = normalize(App(App(mult, two), three))
        self.assertEqual(str(two_times_three), str(six))


class TestChurchBooleans(unittest.TestCase):
    """Test Church boolean encodings"""
    
    def test_church_booleans(self):
        """Test Church boolean values"""
        true = church_true()
        false = church_false()
        
        self.assertEqual(str(true), "(λt.(λf.t))")
        self.assertEqual(str(false), "(λt.(λf.f))")
    
    def test_church_not(self):
        """Test NOT operation"""
        not_op = church_not()
        true = church_true()
        false = church_false()
        
        not_true = normalize(App(not_op, true))
        not_false = normalize(App(not_op, false))
        
        self.assertEqual(str(not_true), str(false))
        self.assertEqual(str(not_false), str(true))
    
    def test_church_and(self):
        """Test AND operation"""
        and_op = church_and()
        true = church_true()
        false = church_false()
        
        true_and_true = normalize(App(App(and_op, true), true))
        true_and_false = normalize(App(App(and_op, true), false))
        false_and_true = normalize(App(App(and_op, false), true))
        false_and_false = normalize(App(App(and_op, false), false))
        
        self.assertEqual(str(true_and_true), str(true))
        self.assertEqual(str(true_and_false), str(false))
        self.assertEqual(str(false_and_true), str(false))
        self.assertEqual(str(false_and_false), str(false))
    
    def test_church_or(self):
        """Test OR operation"""
        or_op = church_or()
        true = church_true()
        false = church_false()
        
        true_or_true = normalize(App(App(or_op, true), true))
        true_or_false = normalize(App(App(or_op, true), false))
        false_or_true = normalize(App(App(or_op, false), true))
        false_or_false = normalize(App(App(or_op, false), false))
        
        self.assertEqual(str(true_or_true), str(true))
        self.assertEqual(str(true_or_false), str(true))
        self.assertEqual(str(false_or_true), str(true))
        self.assertEqual(str(false_or_false), str(false))


class TestAnalyticalOperations(unittest.TestCase):
    """Test analytical operations"""
    
    def test_count_redexes(self):
        """Test counting beta-redexes"""
        identity = Abs("x", Var("x"))
        app = App(identity, Var("a"))
        
        self.assertEqual(count_redexes(identity), 0)
        self.assertEqual(count_redexes(app), 1)
    
    def test_term_size(self):
        """Test calculating term size"""
        var = Var("x")
        self.assertEqual(term_size(var), 1)
        
        identity = Abs("x", Var("x"))
        self.assertEqual(term_size(identity), 2)
        
        app = App(Var("f"), Var("x"))
        self.assertEqual(term_size(app), 3)
    
    def test_is_normal_form(self):
        """Test checking for normal form"""
        var = Var("x")
        self.assertTrue(is_normal_form(var))
        
        identity = Abs("x", Var("x"))
        self.assertTrue(is_normal_form(identity))
        
        app = App(identity, Var("a"))
        self.assertFalse(is_normal_form(app))
        
        # After reduction should be in normal form
        reduced = normalize(app)
        self.assertTrue(is_normal_form(reduced))


class TestComplexReductions(unittest.TestCase):
    """Test complex reduction scenarios"""
    
    def test_nested_applications(self):
        """Test nested function applications"""
        # (λx.λy.x y) a b → a b
        term = App(App(Abs("x", Abs("y", App(Var("x"), Var("y")))), Var("a")), Var("b"))
        result = normalize(term)
        self.assertEqual(result, App(Var("a"), Var("b")))
    
    def test_self_application(self):
        """Test self-application"""
        # (λx.x x) a → a a
        term = App(Abs("x", App(Var("x"), Var("x"))), Var("a"))
        result = normalize(term)
        self.assertEqual(result, App(Var("a"), Var("a")))


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()
