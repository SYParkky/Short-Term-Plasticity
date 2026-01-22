from neuron import h
import matplotlib.pyplot as plt
import numpy as np
import os
from NeuronModels.bg_parameters import SYNAPSE_PARAMS

h.load_file('stdrun.hoc')

# All 6 pathways
PATHWAYS = ['FSN_MSN_D1', 'FSN_MSN_D2', 'MSN_D1_SNr', 'MSN_D2_SNr', 'GPe_SNr', 'STN_SNr']


def run_frequency(synapse_key, freq, duration=500):
    """
    Run simulation at a given frequency
    """
    # Passive compartment
    soma = h.Section(name='soma')
    soma.L = 20
    soma.diam = 20
    soma.insert('pas')
    soma.e_pas = -65
    soma.g_pas = 0.0001
    
    # Create synapse
    params = SYNAPSE_PARAMS[synapse_key]
    syn = h.TsodyksMarkramSTP(0.5, sec=soma)
    syn.U = params['U']
    syn.tau_rec = params['tau_rec']
    syn.tau_facil = params['tau_facil']
    syn.tau_inact = params['tau_inact']
    syn.e = params['e']
    syn.gmax = params['gmax']
    
    # Create spike times
    interval = 1000 / freq
    spike_times = np.arange(50, duration, interval)
    
    # Create NetStims
    netstims = []
    netcons = []
    for t in spike_times:
        ns = h.NetStim()
        ns.number = 1
        ns.start = t
        ns.noise = 0
        netstims.append(ns)
        
        nc = h.NetCon(ns, syn)
        nc.weight[0] = 1.0
        nc.delay = params['delay']
        netcons.append(nc)
    
    # Record
    t_rec = h.Vector().record(h._ref_t)
    i_rec = h.Vector().record(syn._ref_i)
    x_rec = h.Vector().record(syn._ref_x)
    
    # Run
    h.finitialize(-65)
    h.continuerun(duration)
    
    return {
        't': np.array(t_rec.to_python()),
        'i_syn': np.array(i_rec.to_python()),
        'x': np.array(x_rec.to_python()),
    }


def test_pathway(synapse_key, frequencies=None, duration=500, output_dir='outputs'):
    """
    Test a single pathway across multiple frequencies
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if frequencies is None:
        frequencies = [10, 20, 50, 100, 130, 200]
    
    params = SYNAPSE_PARAMS[synapse_key]
    tau_rec = params['tau_rec']
    tau_facil = params['tau_facil']
    U = params['U']
    
    print(f"\n{synapse_key} (τ_rec={tau_rec}ms, τ_facil={tau_facil}ms, U={U})")
    
    # Run simulations
    results = {}
    for freq in frequencies:
        results[freq] = run_frequency(synapse_key, freq, duration)
        print(f"  {freq} Hz done")
    
    # Plot
    n_freqs = len(frequencies)
    fig, axes = plt.subplots(n_freqs, 2, figsize=(14, 2.5 * n_freqs), sharex='col')
    
    fig.suptitle(f'{synapse_key}\n(τ_rec = {tau_rec} ms, τ_facil = {tau_facil} ms, U = {U})', 
                 fontsize=14, fontweight='bold')
    
    axes[0, 0].set_title('Synaptic Current', fontsize=12)
    axes[0, 1].set_title('Resources (x)', fontsize=12)
    
    for i, freq in enumerate(frequencies):
        result = results[freq]
        
        # Synaptic current
        axes[i, 0].plot(result['t'], result['i_syn'], 'r-', lw=1)
        axes[i, 0].set_ylabel(f'{freq} Hz\n\nI_syn (nA)', fontsize=10)
        axes[i, 0].axhline(0, color='k', ls='--', lw=0.5, alpha=0.5)
        axes[i, 0].grid(True, alpha=0.3)
        
        # Resources
        axes[i, 1].plot(result['t'], result['x'], 'b-', lw=1)
        axes[i, 1].set_ylabel('x', fontsize=10)
        axes[i, 1].set_ylim(0, 1.1)
        axes[i, 1].axhline(1, color='gray', ls='--', lw=0.5)
        axes[i, 1].grid(True, alpha=0.3)
    
    axes[-1, 0].set_xlabel('Time (ms)', fontsize=11)
    axes[-1, 1].set_xlabel('Time (ms)', fontsize=11)
    
    plt.tight_layout()
    fname = f'{output_dir}/freq_response_{synapse_key}.png'
    plt.savefig(fname, dpi=150)
    plt.close()
    
    print(f"  Saved: {fname}")
    return results


def test_all_pathways(frequencies=None, duration=500, output_dir='outputs'):
    """
    Test all pathways
    """
    if frequencies is None:
        frequencies = [10, 20, 50, 100, 130, 200]
    
    print("\n" + "=" * 60)
    print("Frequency Response Test")
    print("=" * 60)
    
    for syn_key in PATHWAYS:
        test_pathway(syn_key, frequencies, duration, output_dir)


if __name__ == "__main__":
    test_all_pathways()