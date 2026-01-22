from neuron import h

# ============================================
# CELL MODELS -> Not currently used(Neuron Models)
# ============================================

class CellModel:
    """Base class for all cell types"""
    def __init__(self, name):
        self.name = name
        self.soma = h.Section(name=f'{name}_soma')
        self.soma.L = 20
        self.soma.diam = 20
        self.soma.cm = 1  # µF/cm²
        self.soma.Ra = 100


class MSN_D1(CellModel):
    """MSN D1 neuron - QIF model"""
    def __init__(self):
        super().__init__('MSN_D1')
        # Insert QIF mechanism
        self.cell = h.QIF_neuron(self.soma(0.5))
        self.cell.a = 0.01
        self.cell.b = -20
        self.cell.k = 1.0
        self.cell.C = 15.2
        self.cell.vr = -78.2
        self.cell.vt = -29.7
        self.cell.th = 40
        self.cell.c = -60  
        self.cell.d = 66.9
        self.cell.I_ext = 0


class MSN_D2(CellModel):
    """MSN D2 neuron - QIF model"""
    def __init__(self):
        super().__init__('MSN_D2')
        self.cell = h.QIF_neuron(self.soma(0.5))
        self.cell.a = 0.01
        self.cell.b = -20
        self.cell.k = 1.0
        self.cell.C = 15.2
        self.cell.vr = -80
        self.cell.vt = -29.7
        self.cell.th = 40
        self.cell.c = -60
        self.cell.d = 91
        self.cell.I_ext = 0


class FSN(CellModel):
    """Fast Spiking Neuron - QIF model"""
    def __init__(self):
        super().__init__('FSN')
        self.cell = h.QIF_neuron(self.soma(0.5))
        self.cell.a = 0.2
        self.cell.b = 0.025
        self.cell.k = 1.0
        self.cell.C = 80
        self.cell.vr = -64.4
        self.cell.vt = -50
        self.cell.th = 25
        self.cell.c = -60
        self.cell.d = 0
        self.cell.I_ext = 0


class SNr(CellModel):
    """SNr neuron - AdEx model"""
    def __init__(self):
        super().__init__('SNr')
        self.cell = h.AdEx_neuron(self.soma(0.5))
        self.cell.g_L = 3
        self.cell.E_L = -55.8
        self.cell.Delta_T = 1.8
        self.cell.vt = -55.2
        self.cell.vr = -65
        self.cell.tau_w = 20
        self.cell.th = 20
        self.cell.a = 3
        self.cell.d = 200
        self.cell.C = 80
        self.cell.I_ext = 5


class GPe_TI(CellModel):
    """GPe Type I - AdEx model"""
    def __init__(self):
        super().__init__('GPe_TI')
        self.cell = h.AdEx_neuron(self.soma(0.5))
        self.cell.g_L = 1
        self.cell.E_L = -55.1
        self.cell.Delta_T = 1.7
        self.cell.vt = -54.7
        self.cell.vr = -60
        self.cell.tau_w = 20
        self.cell.th = 15
        self.cell.a = 2.5
        self.cell.d = 70
        self.cell.C = 40
        self.cell.I_ext = 12


class GPe_TA(CellModel):
    """GPe Type A - AdEx model"""
    def __init__(self):
        super().__init__('GPe_TA')
        self.cell = h.AdEx_neuron(self.soma(0.5))
        self.cell.g_L = 1
        self.cell.E_L = -55.1
        self.cell.Delta_T = 2.55
        self.cell.vt = -54.7
        self.cell.vr = -60
        self.cell.tau_w = 20
        self.cell.th = 15
        self.cell.a = 2.5
        self.cell.d = 105
        self.cell.C = 60
        self.cell.I_ext = 1


class STN(CellModel):
    """STN neuron - AdEx model"""
    def __init__(self):
        super().__init__('STN')
        self.cell = h.AdEx_neuron(self.soma(0.5))
        self.cell.g_L = 10
        self.cell.E_L = -80.2
        self.cell.Delta_T = 16.2
        self.cell.vt = -64.0
        self.cell.vr = -70
        self.cell.tau_w = 333
        self.cell.th = 15
        self.cell.a = 0.3
        self.cell.d = 0.05
        self.cell.C = 60
        self.cell.I_ext = 5


# ============================================
# SYNAPSE PARAMETERS
# ============================================

SYNAPSE_PARAMS = {
    'FSN_MSN_D1': {'U': 0.29, 'tau_rec': 902, 'tau_facil': 53, 'tau_inact': 11, 'e': -74, 'gmax': 0.006, 'delay': 1.7},
    'FSN_MSN_D2': {'U': 0.29, 'tau_rec': 902, 'tau_facil': 53, 'tau_inact': 11, 'e': -74, 'gmax': 0.006, 'delay': 1.7},
    'MSN_D1_SNr': {'U': 0.0192, 'tau_rec': 623, 'tau_facil': 559, 'tau_inact': 5.2, 'e': -80, 'gmax': 0.02, 'delay': 7.0},
    'MSN_D2_SNr': {'U': 0.24, 'tau_rec': 11, 'tau_facil': 73, 'tau_inact': 5.2, 'e': -80, 'gmax': 0.002, 'delay': 7.0},
    'GPe_SNr': {'U': 0.250, 'tau_rec': 969, 'tau_facil': 0, 'tau_inact': 2.1, 'e': -72, 'gmax': 0.076, 'delay': 3.0},
    'STN_SNr': {'U': 0.35, 'tau_rec': 800, 'tau_facil': 0, 'tau_inact': 12, 'e': 0, 'gmax': 0.00091, 'delay': 4.5},
}


def get_cell_class(cell_type):
    """Get cell class by name"""
    return {
        'MSN_D1': MSN_D1, 'MSN_D2': MSN_D2, 'FSN': FSN, 'SNr': SNr,
        'GPe_TI': GPe_TI, 'GPe_TA': GPe_TA, 'STN': STN,
    }.get(cell_type)


def list_available_synapses():
    """Print all available synapse types"""
    print("\nAvailable Synapses:")
    print("-" * 60)
    for syn_name in sorted(SYNAPSE_PARAMS.keys()):
        params = SYNAPSE_PARAMS[syn_name]
        syn_type = "Facilitating" if params['tau_facil'] > 0 else "Depressing"
        print(f"  {syn_name:20s} U={params['U']:.4f}  {syn_type}")
    print()


if __name__ == "__main__":
    list_available_synapses
