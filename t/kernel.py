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


