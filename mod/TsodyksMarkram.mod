TITLE Tsodyks-Markram Short-Term Plasticity Synapse

COMMENT
Three-state kinetic model for short-term synaptic plasticity:
  x: fraction of recovered (available) vesicles
  yrel: fraction of active (releasing) vesicles  
  z: fraction of inactive (refractory) vesicles

Conservation: x + yrel + z = 1

  dx/dt = z/tau_rec - u*x*delta(t-t_spike)
  dy/dt = -yrel/tau_inact + u*x*delta(t-t_spike)
  dz/dt = yrel/tau_inact - z/tau_rec
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
    U = 0.5
    tau_rec = 800 (ms)
    tau_inact = 3 (ms)
    tau_facil = 0 (ms)
    gmax = 0.001 (uS)
    e = 0 (mV)
}

ASSIGNED {
    v (mV)
    i (nA)
    g (uS)
    R
    A
}

STATE {
    x
    yrel
    z
    u
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
    x' = z / tau_rec
    yrel' = -yrel / tau_inact
    z' = yrel / tau_inact - z / tau_rec
    if (tau_facil > 0) {
        u' = -(u - U) / tau_facil  
    }
}

NET_RECEIVE(weight) {
    if (tau_facil > 0) {
        u = u + U * (1 - u)
    } else {
        u = U
    }
    R = weight * u * x
    yrel = yrel + R
    x = x - R
    A = R
}
