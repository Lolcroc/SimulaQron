#
# Copyright (c) 2017, Stephanie Wehner and Axel Dahlberg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by Stephanie Wehner, QuTech.
# 4. Neither the name of the QuTech organization nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from SimulaQron.cqc.pythonLib.cqc import CQCConnection, qubit

import sys

import numpy.random as random
import numpy as np

#####################################################################################################
#
# main
#
def main(n):

    # Initialize the connection
    with CQCConnection("Alice") as Alice:

        # Create 2 n-sized random bit strings x and theta
        xA, thetaA = random.randint(2, size=(2,n), dtype='int8')

        # Encode every bit x according to base theta, and send to Eve;
        # theta = 0: Standard basis (0 -> |0>, 1 -> |1>)
        # theta = 1: Hadamard badis (0 -> |+>, 1 -> |->)
        for xAj, tAj in zip(xA, thetaA):
            qA = qubit(Alice)
            if xAj == 1:
                qA.X()
            if tAj == 1:
                qA.H()
            Alice.sendQubit(qA, "Eve")

        # -----

        # Retrieve Bob's bases and send Alice's own
        thetaB = np.asarray(list(Alice.recvClassical()))
        Alice.sendClassical("Bob", thetaA)

        # -----

        # Allocate and store all indices which were created/measured in the same basis
        S = []
        for j in range(n):
            if thetaA[j] == thetaB[j]:
                S.append(j)

        # -----

        # Pick a random subset T of size |S|/2 to test measurements; send it to Bob
        T = random.choice(S, size=len(S)//2, replace=False)
        Alice.sendClassical("Bob", list(T))

        # -----

        # Retrieve Bob's measurements for test set T and send Alice's own
        xAT = [xA[t] for t in T]
        xBT = np.asarray(list(Alice.recvClassical()))
        Alice.sendClassical("Bob", xAT)

        # Calculate the number of disagreements in test set T
        W = 0
        for xATj, xBTj in zip(xAT, xBT):
            if xATj != xBTj:
                W += 1

        # Calculate the delta error and abort the protocol if d > 0
        delta = W/len(T)
        print("Alice's delta error: {}".format(delta))

        if delta > 0:
            print("Alice aborted protocol")
            return

        # -----

        # Retrieve the remaining measurements not used for test set T
        remain = [s for s in S if s not in T]
        xAr = [xA[r] for r in remain]

        # -----

        # Create a random seed for the extractor and send it to Bob
        r = random.randint(2, size=len(xAr))
        Alice.sendClassical("Bob", list(r))

        # -----

        # Calculate 1 bit of key by randomly XORing Alice's remaining bit-string x with the seed
        k = np.inner(r, xAr) % 2
        print("Alice made key = {}".format(k))

##################################################################################################

if __name__ == '__main__':
    n = int(sys.argv[1])
    main(n)

    print("Alice done")
