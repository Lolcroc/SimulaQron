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

import numpy.random as random
import numpy as np

#####################################################################################################
#
# main
#
def main():

    # Initialize the connection
    with CQCConnection("Alice") as Alice:

        n = 16;
        xA, thetaA = random.randint(2, size=(2,n), dtype='int8')

        Alice.sendClassical("Bob", n)
        Alice.set_pending(True)

        for xAj, tAj in zip(xA, thetaA):
            qA = qubit(Alice)
            if xAj == 1:
                qA.X()
            if tAj == 1:
                qA.H()
            Alice.sendQubit(qA, "Eve")

        Alice.flush()
        Alice.set_pending(False)

        # -----

        thetaB = np.asarray(list(Alice.recvClassical()), dtype=np.int8)
        Alice.sendClassical("Bob", thetaA)

        # -----

        S = []

        for j in range(n):
            if thetaA[j] == thetaB[j]:
                S.append(j)

        # -----

        T = random.choice(S, size=len(S)//2, replace=False)
        Alice.sendClassical("Bob", list(T))

        # -----

        xAT = [xA[t] for t in T]
        xBT = np.asarray(list(Alice.recvClassical()), dtype=np.int8)

        W = 0
        for xATj, xBTj in zip(xAT, xBT):
            if xATj != xBTj:
                W += 1

        delta = W/len(T)

        print("Error delta: {}".format(delta))

        # -----

        remain = [s for s in S if s not in T]
        xAr = [xA[r] for r in remain]

        # -----

        r = random.randint(2, size=len(xAr))
        Alice.sendClassical("Bob", list(r))

        # -----

        k = np.inner(r, xAr) % 2

        print("Alice made key={}".format(k))

##################################################################################################
main()
