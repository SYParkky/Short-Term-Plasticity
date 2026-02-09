
# Short-Term Plasticity in Basal Ganglia Pathways

Implementation of Tsodyks-Markram short-term synaptic plasticity dynamics across six key basal ganglia pathways using NEURON simulator.

## Overview

This repository implements computational models of short-term plasticity (STP) to characterize synaptic dynamics in basal ganglia circuits. The models use the Tsodyks-Markram formalism to simulate synaptic depression and facilitation, enabling quantitative analysis of how different pathways respond to repeated stimulation.

### Modeled Pathways

- **FSN → MSN_D1** (Fast-Spiking Interneuron to D1 Medium Spiny Neuron)
- **FSN → MSN_D2** (Fast-Spiking Interneuron to D2 Medium Spiny Neuron)
- **MSN_D1 → SNr** (D1 Medium Spiny Neuron to Substantia Nigra pars reticulata)
- **MSN_D2 → SNr** (D2 Medium Spiny Neuron to Substantia Nigra pars reticulata)
- **GPe → SNr** (Globus Pallidus externa to Substantia Nigra pars reticulata)
- **STN → SNr** (Subthalamic Nucleus to Substantia Nigra pars reticulata)

## Features

- **Paired-Pulse Ratio (PPR) Testing**: Quantifies short-term plasticity by measuring the ratio of synaptic responses to two closely spaced stimuli
- **Frequency Response Analysis**: Tests synaptic dynamics across multiple stimulation frequencies (1-100 Hz)
- **Resource Dynamics Visualization**: Tracks vesicle release probability (u), available resources (x), and their product (u×x) over time
- **Biologically Calibrated Parameters**: Synaptic parameters (U, τ_rec, τ_facil) derived from experimental literature

## Installation

### Requirements

- Python 3.11.0 (or compatible version)
- NEURON 8.0+ with Python interface
- NumPy
- Matplotlib

### Setup

1. Clone the repository:
```bash
git clone https://github.com/SYParkky/Short-Term-Plasticity.git
cd Short-Term-Plasticity
```

2. Compile NEURON mechanisms:
```bash
nrnivmodl
```

## Usage

### Paired-Pulse Ratio Analysis

Run PPR testing with 50 ms inter-stimulus interval:

```bash
python run_PPR.py
```

**Output**: Generates individual plots for each pathway showing:
- Synaptic current responses to paired pulses
- Release probability (u), available resources (x), and their dynamics
- Calculated PPR values with depression/facilitation classification



### Frequency Response Testing

Test synaptic responses across different firing frequencies:

```bash
python run_freq.py
```

**Output**: Produces comprehensive plots showing:
- Synaptic current traces at 1, 3, 10, 30, 50, and 100 Hz
- Resource depletion/recovery dynamics
- Frequency-dependent filtering properties of each pathway

## Example Outputs
### Paired-Pulse Ratio
<p align="center">
  </p>
<img width="800" height="850" alt="image" src="https://github.com/user-attachments/assets/5f7d7ae0-1bab-47ed-b11e-338370fea574" />
</p>

### Frequency Response 
<p align="center">
  </p>
<img width="800" height="850" alt="image" src="https://github.com/user-attachments/assets/8a9c8f26-8f7a-47d3-9335-f01e18f352e6" />
</p>

## Results

### Paired-Pulse Ratios (ISI = 50 ms)

| Pathway | Behavior | PPR | Benchmark | Reference |
|---------|----------|-----|-----------|-----------|
| FSN → MSN_D1 | Depressing | 0.553 | 0.6-0.8 | [Planert et al., J Neurosci ](https://pubmed.ncbi.nlm.nih.gov/20203210/)|
| FSN → MSN_D2 | Depressing | 0.553 | 0.6-0.8 | [Planert et al., J Neurosci](https://pubmed.ncbi.nlm.nih.gov/20203210/) |
| MSN_D1 → SNr | Facilitating | 1.387 | 1.22 ± 0.07 | [Dvorzhak et al.](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0082191&utm_source=chatgpt.com) |
| MSN_D2 → SNr | Facilitating | 1.149 | 1.4 ± 0.1 | [Dvorzhak et al.](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0082191&utm_source=chatgpt.com) |
| GPe → SNr | Depressing | 0.754 | 0.40 ± 0.06 | [Atherton et al., J Neurosci](https://pubmed.ncbi.nlm.nih.gov/23616523/) |
| STN → SNr | Depressing | 0.673 | 0.7-0.9 | [Ding et al. 2013](https://pubmed.ncbi.nlm.nih.gov/23486958/) |

### Key Findings

- **Inhibitory pathways** (FSN → MSN, GPe → SNr, STN → SNr) show synaptic depression, acting as high-pass filters that attenuate sustained input
- **MSN → SNr pathways** exhibit facilitation, enhancing responses during bursts of activity
- Frequency response curves reveal pathway-specific filtering properties that shape basal ganglia circuit dynamics



## Other References
[Lindahl et al., Front Comput Neurosci (2013)](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2013.00076/full)
