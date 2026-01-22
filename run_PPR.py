from neuron import h
h.nrn_load_dll('mod/arm64/libnrnmech.dylib')
from src.ppr_test import test_all_synapses

test_all_synapses(ISI=50)