from neuron import h
h.nrn_load_dll('mod/arm64/libnrnmech.dylib')
from src.frequency import test_all_pathways

# Test all 6 synapses across frequencies
test_all_pathways()
