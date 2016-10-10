import unittest
from jupyter_gauche.kernel import parse_commands

class KernelTest(unittest.TestCase):
    def test_parse_code(self):
        s = """
        (define (linear-combination a b x y)
          (+ (* a x) (* b y)))

        (define (linear-combination a b x y)
          (add (mul a x) (mul b y)))

        (define (add +))
        (define (mul +))
        """
        actual = parse_commands(s)
        expected = [
        "(define (linear-combination a b x y) (+ (* a x) (* b y)))",
        "(define (linear-combination a b x y) (add (mul a x) (mul b y)))",
        "(define (add +))",
        "(define (mul +))"
                ]
        self.assertEqual(actual, expected)

    def test_parse_code_with_comment_out(self):
        s = """
        (define (linear-combination a b x y)
          (+ (* a x) (* b y)))
        ; hogehoge fugafuga

        (define (linear-combination a b x y)
          (add (mul a x) (mul b y)))

        (define (add +))
        (define (mul +))
        """
        actual = parse_commands(s)
        expected = [
        "(define (linear-combination a b x y) (+ (* a x) (* b y)))",
        "(define (linear-combination a b x y) (add (mul a x) (mul b y)))",
        "(define (add +))",
        "(define (mul +))"
                ]
        self.assertEqual(actual, expected)

    def test_parse_code_with_comment_out_in_some_scheme_code(self):
        s = """
        (define (linear-combination a b x y)
          (+ (* a x) (* b y)))
        (print "aaa") ; hogehoge fugafuga

        (define (linear-combination a b x y)
          (add (mul a x) (mul b y)))

        (define (add +))
        (define (mul +))
        """
        actual = parse_commands(s)
        expected = [
        "(define (linear-combination a b x y) (+ (* a x) (* b y)))",
        "(print \"aaa\")",
        "(define (linear-combination a b x y) (add (mul a x) (mul b y)))",
        "(define (add +))",
        "(define (mul +))"
                ]
        self.assertEqual(actual, expected)


