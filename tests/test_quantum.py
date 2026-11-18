import unittest
from quantum import Circuit,bell,ghz

class QuantumTests(unittest.TestCase):
    def test_bell(self):
        p=bell().probabilities()
        self.assertAlmostEqual(p['00'],.5);self.assertAlmostEqual(p['11'],.5)
        self.assertAlmostEqual(p['01'],0);self.assertAlmostEqual(p['10'],0)
    def test_unitary_norm(self):
        c=Circuit(3).gate('H',0).gate('T',2).cnot(0,1).gate('Y',2)
        self.assertAlmostEqual(c.norm(),1)
    def test_x_and_cnot(self):
        c=Circuit(2).gate('X',1).cnot(1,0)
        self.assertAlmostEqual(c.probabilities()['11'],1)
    def test_ghz(self):
        p=ghz(4).probabilities()
        self.assertAlmostEqual(p['0000'],.5);self.assertAlmostEqual(p['1111'],.5)
    def test_seeded_sample(self):
        self.assertEqual(bell().sample(100,7),bell().sample(100,7))
        self.assertEqual(sum(bell().sample(100).values()),100)
    def test_errors(self):
        with self.assertRaises(ValueError):Circuit(0)
        with self.assertRaises(ValueError):Circuit(2).cnot(0,0)
if __name__=='__main__':unittest.main()
