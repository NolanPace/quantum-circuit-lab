"""Small dependency-free quantum state-vector simulator. Qubit 0 is least-significant bit."""
from __future__ import annotations
import cmath
import math
import random
from dataclasses import dataclass

SQRT2=math.sqrt(2)
GATES={
 'I':((1,0),(0,1)),
 'X':((0,1),(1,0)),
 'Y':((0,-1j),(1j,0)),
 'Z':((1,0),(0,-1)),
 'H':((1/SQRT2,1/SQRT2),(1/SQRT2,-1/SQRT2)),
 'S':((1,0),(0,1j)),
 'T':((1,0),(0,cmath.exp(1j*math.pi/4))),
}

@dataclass
class Circuit:
    qubits: int
    def __post_init__(self):
        if not 1 <= self.qubits <= 14: raise ValueError('qubits must be between 1 and 14')
        self.state=[0j]*(1<<self.qubits);self.state[0]=1+0j
        self.operations=[]
    def gate(self, name:str, target:int):
        if name not in GATES: raise ValueError('Unknown gate')
        self._check(target)
        a,b=GATES[name]
        for i in range(len(self.state)):
            if i&(1<<target):continue
            j=i|(1<<target);v,w=self.state[i],self.state[j]
            self.state[i]=a[0]*v+a[1]*w
            self.state[j]=b[0]*v+b[1]*w
        self.operations.append((name,target));return self
    def cnot(self,control:int,target:int):
        self._check(control);self._check(target)
        if control==target: raise ValueError('Control and target must differ')
        for i in range(len(self.state)):
            if i&(1<<control) and not i&(1<<target):
                j=i|(1<<target);self.state[i],self.state[j]=self.state[j],self.state[i]
        self.operations.append(('CX',control,target));return self
    def _check(self,index):
        if not 0 <= index < self.qubits: raise IndexError('Qubit out of range')
    def probabilities(self)->dict[str,float]:
        return {format(i,f'0{self.qubits}b'):abs(v)**2 for i,v in enumerate(self.state)}
    def sample(self,shots:int=1024,seed:int|None=None)->dict[str,int]:
        if shots<1:raise ValueError('shots must be positive')
        rng=random.Random(seed);p=list(self.probabilities().items());counts={bits:0 for bits,_ in p}
        keys,weights=zip(*p)
        for state in rng.choices(keys,weights=weights,k=shots):counts[state]+=1
        return {k:v for k,v in counts.items() if v}
    def norm(self)->float:return sum(abs(v)**2 for v in self.state)

def bell()->Circuit:return Circuit(2).gate('H',0).cnot(0,1)
def ghz(n:int)->Circuit:
    if n<2:raise ValueError('GHZ requires at least two qubits')
    c=Circuit(n).gate('H',0)
    for target in range(1,n):c.cnot(0,target)
    return c

def histogram(counts:dict[str,int],width:int=42)->str:
    max_count=max(counts.values(),default=1)
    return '\n'.join(f'{k} | {"█"*round(width*v/max_count)} {v}' for k,v in sorted(counts.items()))
