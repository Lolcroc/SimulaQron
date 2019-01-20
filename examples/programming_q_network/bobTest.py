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
    with CQCConnection("Bob") as Bob:

        # Create an n-sized random bit string theta
        thetaB = random.randint(2, size=n, dtype='int8')

        # Allocate and fill qubits from Eve
        qBs = []
        for i in range(n):
            qBs.append(Bob.recvQubit())

        # Measure each qubit along the base theta.
        # theta = 0: Standard basis
        # theta = 1: Hadamard basis
        xB = []
        for qB, tB in zip(qBs, thetaB):
            if tB == 1:
                qB.H()
            xB.append(qB.measure())

        # -----

        # Retrieve Alice's bases and send Bob's own
        Bob.sendClassical("Alice", thetaB)
        thetaA = np.asarray(list(Bob.recvClassical()))

        # -----

        # Allocate and store all indices which were created/measured in the same basis
        S = []
        for j in range(n):
            if thetaA[j] == thetaB[j]:
                S.append(j)

        # -----

        # Retrieve Alice's test set T for testing measurements
        T = np.asarray(list(Bob.recvClassical()))

        # -----

        # Retrieve Alice's measurements for test set T and send Bob's own
        xBT = [xB[t] for t in T]
        Bob.sendClassical("Alice", xBT)
        xAT = np.asarray(list(Bob.recvClassical()))

        # Calculate the number of disagreements in test set T
        W = 0
        for xATj, xBTj in zip(xAT, xBT):
            if xATj != xBTj:
                W += 1

        # Calculate the delta error and abort the protocol if d > 0
        delta = W/len(T)
        print("Bob's delta error: {}".format(delta))

        if delta > 0:
            print("Bob aborted protocol")
            return

        # -----

        # Retrieve the remaining measurements not used for test set T
        remain = [s for s in S if s not in T]
        xBr = [xB[r] for r in remain]

        # -----

        # Retrieve Alice's random seed for the extractor
        r = np.asarray(list(Bob.recvClassical()))

        # -----

        # Calculate 1 bit of key by randomly XORing Bob's remaining bit-string x with the seed
        k = np.inner(r, xBr) % 2
        print("Bob made key = {}".format(k))


##################################################################################################
if __name__ == '__main__':
    n = int(sys.argv[1])
    main(n)

    print("Bob done")
