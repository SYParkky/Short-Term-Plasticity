TITLE Tsodyks-Markram Short-Term Plasticity Synapse

COMMENT
Tsodyks-Markram model for short-term synaptic plasticity (STP)


Three-state kinetic model:
  x: fraction of recovered (available) vesicles
  yrel: fraction of active (releasing) vesicles  
  z: fraction of inactive (refractory) vesicles

Conservation: x + yrel + z = 1

Dynamics:
  dx/dt = z/tau_rec - u*x*delta(t-t_spike)
  dy/dt = -yrel/tau_inact + u*x*delta(t-t_spike)
  dz/dt = yrel/tau_inact - z/tau_rec

Where:
  u = facilitation variable (use-dependent)
  U = baseline release probability
  tau_rec = recovery time constant
  tau_inact = inactivation time constant
  tau_facil = facilitation time constant

For depression-dominated synapses (TC->cortex):
  U = 0.5-0.8, tau_rec = 500-800 ms, tau_facil = 0 ms

Author: DBS Simulation Package
ENDCOMMENT

NEURON {
    POINT_PROCESS TsodyksMarkramSTP
    RANGE U, tau_rec, tau_inact, tau_facil
    RANGE x, yrel, z, u, R, A
    RANGE g, i, e
    RANGE gmax
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

PARAMETER {
    : STP parameters - depression-dominated (TC synapse)
    U = 0.5              : baseline release probability
    tau_rec = 800 (ms)   : recovery time constant
    tau_inact = 3 (ms)   : inactivation time constant  
    tau_facil = 0 (ms)   : facilitation time constant (0 = no facilitation)
    
    : Synaptic parameters
    gmax = 0.001 (uS)    : maximum conductance
    e = 0 (mV)           : reversal potential (excitatory)
}

ASSIGNED {
    v (mV)
    i (nA)
    g (uS)
    R          : effective release (x * u at spike time)
    A          : amplitude scaling factor
}

STATE {
    x          : recovered fraction
    yrel       : active fraction (releasing)
    z          : inactive fraction
    u          : facilitation variable
}

INITIAL {
    x = 1
    yrel = 0
    z = 0
    u = U
    R = 1
    A = 1
    g = 0
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    g = gmax * yrel
    i = g * (v - e)
}

DERIVATIVE states {
    : Recovery: z -> x
    x' = z / tau_rec
    
    : Inactivation: yrel -> z
    yrel' = -yrel / tau_inact
    z' = yrel / tau_inact - z / tau_rec
    
    : Facilitation decay (if tau_facil > 0)
    if (tau_facil > 0) {
        u' = -(u - U) / tau_facil  
    }
}

NET_RECEIVE(weight) {
    : Called on each presynaptic spike
    
    : Update facilitation (if enabled)
    if (tau_facil > 0) {
        u = u + U * (1 - u)
    } else {
        u = U
    }
    
    : Calculate effective release
    R = weight * u * x
    
    : State transitions at spike time
    yrel = yrel + R
    x = x - R
    
    : Store for analysis
    A = R
}
