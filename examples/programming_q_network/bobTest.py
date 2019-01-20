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

        thetaB = random.randint(2, size=n, dtype='int8')

        qBs = []
        for i in range(n):
            qBs.append(Bob.recvQubit())

        xB = []
        for qB, tB in zip(qBs, thetaB):
            if tB == 1:
                qB.H()
            xB.append(qB.measure())

        # -----

        Bob.sendClassical("Alice", thetaB)
        thetaA = np.asarray(list(Bob.recvClassical()))

        # -----

        S = []

        for j in range(n):
            if thetaA[j] == thetaB[j]:
                S.append(j)

        # -----

        T = np.asarray(list(Bob.recvClassical()))

        # -----

        xBT = [xB[t] for t in T]
        Bob.sendClassical("Alice", xBT)

        # -----

        remain = [s for s in S if s not in T]
        xBr = [xB[r] for r in remain]

        # -----

        r = np.asarray(list(Bob.recvClassical()))

        # -----

        k = np.inner(r, xBr) % 2

        print("Bob made key={}".format(k))


##################################################################################################
if __name__ == '__main__':
    n = int(sys.argv[1])
    main(n)
