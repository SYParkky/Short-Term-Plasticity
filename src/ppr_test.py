from neuron import h
import matplotlib.pyplot as plt
import numpy as np
import os
from NeuronModels.bg_parameters import SYNAPSE_PARAMS

h.load_file('stdrun.hoc')


def test_PPR(synapse_key, ISI=50, output_dir='outputs'):
    """Test paired-pulse ratio using passive compartment"""
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{'='*50}")
    print(f"PPR Test: {synapse_key}, ISI={ISI}ms")
    print(f"{'='*50}")
    
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
    
    # NetStim for 2 spikes
    stim = h.NetStim()
    stim.number = 2
    stim.start = 100
    stim.interval = ISI
    stim.noise = 0
    
    # Connect
    nc = h.NetCon(stim, syn)
    nc.weight[0] = 1.0
    nc.delay = params['delay']
    
    # Record
    t_vec = h.Vector().record(h._ref_t)
    i_vec = h.Vector().record(syn._ref_i)
    u_vec = h.Vector().record(syn._ref_u)
    x_vec = h.Vector().record(syn._ref_x)
    
    spike_times = h.Vector()
    nc.record(spike_times)
    
    # Run
    tstop = 100 + ISI + 100
    h.finitialize(-65)
    h.continuerun(tstop)
    
    # Convert to numpy
    t_arr = np.array(t_vec)
    i_arr = np.array(i_vec)
    spikes = list(spike_times)
    
    # Find peaks
    delay = params['delay']
    t1, t2 = 100 + delay, 100 + ISI + delay
    
    idx1 = (t_arr >= t1) & (t_arr <= t1 + 30)
    idx2 = (t_arr >= t2) & (t_arr <= t2 + 30)
    
    peak1 = np.max(np.abs(i_arr[idx1])) if np.any(idx1) else 0
    peak2 = np.max(np.abs(i_arr[idx2])) if np.any(idx2) else 0
    PPR = peak2 / peak1 if peak1 > 0 else 0
    
    print(f"  Peak1: {peak1:.6f} nA")
    print(f"  Peak2: {peak2:.6f} nA")
    print(f"  PPR: {PPR:.3f} ({'facilitating' if PPR > 1 else 'depressing'})")
    
    # Plot
    ptype = 'Facilitation' if PPR > 1 else 'Depression'
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    
    # Synaptic current
    axes[0].plot(t_arr, i_arr, 'r-', lw=1.5)
    axes[0].set_ylabel('Synaptic Current (nA)', fontsize=11)
    axes[0].axhline(0, color='k', ls='--', lw=0.5, alpha=0.5)
    axes[0].set_title(f'{synapse_key}: PPR = {PPR:.3f} ({ptype}) at ISI={ISI}ms', fontsize=13, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    # Add text box with peak values
    textstr = f'Peak 1: {peak1:.6f} nA\nPeak 2: {peak2:.6f} nA\nPPR: {PPR:.3f}'
    axes[0].text(0.02, 0.95, textstr, transform=axes[0].transAxes, fontsize=10,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # STP state variables
    axes[1].plot(t_arr, np.array(u_vec), 'g-', lw=1.5, label='u (facilitation)')
    axes[1].plot(t_arr, np.array(x_vec), 'b-', lw=1.5, label='x (resources)')
    axes[1].axhline(params['U'], color='gray', ls='--', lw=1, alpha=0.7, label=f"U={params['U']}")
    axes[1].axhline(1, color='gray', ls=':', lw=1, alpha=0.5, label='x=1')
    axes[1].set_ylabel('STP State', fontsize=11)
    axes[1].set_xlabel('Time (ms)', fontsize=11)
    axes[1].legend(loc='right', fontsize=9)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(0, 1.1)
    
    plt.tight_layout()
    fname = f'{output_dir}/PPR_{synapse_key}_ISI{ISI}.png'
    plt.savefig(fname, dpi=150)
    plt.close()
    print(f"  Saved: {fname}")
    
    return {'synapse': synapse_key, 'ISI': ISI, 'PPR': PPR, 'peak1': peak1, 'peak2': peak2}


def test_all_synapses(ISI=50, output_dir='outputs'):
    """Test all synapses and make summary plot"""
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    for syn_key in SYNAPSE_PARAMS.keys():
        r = test_PPR(syn_key, ISI=ISI, output_dir=output_dir)
        results.append(r)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"SUMMARY (ISI={ISI}ms)")
    print(f"{'='*50}")
    print(f"{'Synapse':<20} {'PPR':>8} {'Type':<12}")
    print("-" * 42)
    for r in results:
        ptype = 'facilitating' if r['PPR'] > 1 else 'depressing'
        print(f"{r['synapse']:<20} {r['PPR']:>8.3f} {ptype:<12}")
    
    # Summary plot
    names = [r['synapse'] for r in results]
    pprs = [r['PPR'] for r in results]
    colors = ['#66c2a5' if p > 1 else '#fc8d62' for p in pprs]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(names, pprs, color=colors, edgecolor='black', linewidth=0.5)
    
    # Add value labels
    for bar, ppr in zip(bars, pprs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{ppr:.2f}', ha='center', va='bottom', fontsize=10)
    
    ax.axhline(1, color='black', ls='--', lw=2, label='PPR = 1 (no change)')
    ax.set_ylabel('Paired Pulse Ratio', fontsize=12)
    ax.set_xlabel('')
    ax.set_title(f'PPR Comparison Across Synapses (ISI = {ISI} ms)', fontsize=14)
    ax.set_ylim(0, max(pprs) + 0.2)
    ax.legend(loc='upper right')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    fname = f'{output_dir}/PPR_summary_ISI{ISI}.png'
    plt.savefig(fname, dpi=150)
    plt.close()
    print(f"\nSummary plot saved: {fname}")
    
    return results


if __name__ == "__main__":
    test_all_synapses(ISI=50)
