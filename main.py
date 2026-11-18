import argparse
from quantum import Circuit,bell,ghz,histogram

def main():
    p=argparse.ArgumentParser(description='Quantum state-vector circuit simulator')
    p.add_argument('--demo',choices=['bell','ghz','plus'],default='bell')
    p.add_argument('--qubits',type=int,default=3)
    p.add_argument('--shots',type=int,default=1024)
    p.add_argument('--seed',type=int,default=7)
    a=p.parse_args()
    c=bell() if a.demo=='bell' else ghz(a.qubits) if a.demo=='ghz' else Circuit(1).gate('H',0)
    print('Operations:',c.operations)
    print('Theoretical probabilities:', {k:round(v,5) for k,v in c.probabilities().items() if v>1e-10})
    print(histogram(c.sample(a.shots,a.seed)))
if __name__=='__main__':main()
