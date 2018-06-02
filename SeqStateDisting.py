# -*- coding: utf-8 -*-

# Copyright 2017 IBM RESEARCH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

"""
SeqDist state example illustrating mapping onto the backend.
"""

import sys
import os
import numpy
import math

# We don't know from where the user is running the example,
# so we need a relative position from this file path.
# TODO: Relative imports for intra-package imports are highly discouraged.
# http://stackoverflow.com/a/7506006
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from qiskit import QuantumProgram

import Qconfig

###############################################################
# Set the backend name and coupling map.
###############################################################
backend = "ibmqx4"
coupling_map = {0: [],
                1: [0],
                2: [0, 1, 4],
                3: [2, 4],
                4: []}

###############################################################
# Make a quantum program for the SeqDist state.
###############################################################
QPS_SPECS = {
    "circuits": [{
        "name": "SeqDist",
        "quantum_registers": [{
            "name": "q",
            "size": 5
        }],
        "classical_registers": [
            {"name": "c",
             "size": 5}
        ]}]
}

qp = QuantumProgram(specs=QPS_SPECS)
qc = qp.get_circuit("SeqDist")
q = qp.get_quantum_register("q")
c = qp.get_classical_register("c")

#Creat rand number
RndNum=numpy.random.randint(0,2);

#Mix state produced
#if RndNum==1:
#qc.x(q[0])

#Init state
qc.u3(1.1503,6.4850,2.2555,q[0])   #ignore the global phase
qc.barrier()

if RndNum==0:
    qc.u1(2/3*math.pi,q[0])      #This is U
qc.barrier()

qc.u3(1.231,0,0,q[0])  #This is X


if RndNum==0:
    qc.u1(2/3*math.pi,q[0])      #This is U

#Meausre Unitary
qc.u3(0.7854,6.0214,6.1913,q[0])

print("RndNum is",RndNum)



# Insert a barrier before measurement
qc.barrier()
# Measure all of the qubits in the standard basis
for i in range(5):
    qc.measure(q[i], c[i])

###############################################################
# Set up the API and execute the program.
###############################################################
qp.set_api(Qconfig.APItoken, Qconfig.config["url"])

# First version: no mapping
# print("no mapping, simulator")
# result = qp.execute(["SeqDist"], backend='ibmqx_qasm_simulator',
#                     coupling_map=None, shots=3072)
# print(result)
# print(result.get_counts("SeqDist"))
#
# # Second version: map to qx2 coupling graph and simulate
# print("map to %s, simulator" % backend)
# result = qp.execute(["SeqDist"], backend='ibmqx_qasm_simulator',
#                     coupling_map=coupling_map, shots=3072)
# print(result)
# answer=result.get_counts("SeqDist")
# print(answer)
#
# for key in answer.keys():
#     aa=[int(key[-1]),int(key[-2]),int(key[-3]),int(key[-4]),int(key[-5])]
#
# print(aa)

# Third version: map to qx4 coupling graph and simulate locally
#print("map to %s, local qasm simulator" % backend)
#result = qp.execute(["SeqDist"], backend='local_qasm_simulator',
#                    coupling_map=coupling_map, shots=1024)
#print(result)
#print(result.get_counts("SeqDist"))

# Fourth version: map to qx2 coupling graph and run on qx2
print("map to %s, backend" % backend)
result = qp.execute(["SeqDist"], backend=backend,
                    coupling_map=coupling_map, shots=1024, timeout=180)
print(result)
print(result.get_counts("SeqDist"))
print(result.get_ran_qasm("SeqDist"))