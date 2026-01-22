TITLE AdEx NEURON

COMMENT
Adaptive Exponential Integrate-and-Fire neuron


Equations:
dv/dt = (-g_L*(v-E_L) + g_L*Delta_T*exp((v-vt)/Delta_T) - z + I_ext) / C
dz/dt = (a*(v-E_L) - z) / tau_w

When v > th: v = vr, z = z + d
ENDCOMMENT

NEURON {
    ARTIFICIAL_CELL AdEx_neuron
    RANGE v, z, g_L, E_L, Delta_T, vt, vr, tau_w, th, a, d, C, I_ext
    RANGE dt_internal
}

PARAMETER {
    g_L = 10 (nS)
    E_L = -70 (mV)
    Delta_T = 2 (mV)
    vt = -50 (mV)
    vr = -70 (mV)
    tau_w = 30 (ms)
    th = 20 (mV)
    a = 2 (nS)
    d = 0 (pA)
    C = 200 (pF)
    I_ext = 0 (pA)
    dt_internal = 0.025 (ms)
}

ASSIGNED {
    v (mV)
    z (pA)
}

INITIAL {
    v = vr
    z = 0
    net_send(0, 1)
}

NET_RECEIVE(w) {
    LOCAL exp_term
    
    if (flag == 1) {
        : Safe exponential term
        if ((v - vt) / Delta_T > 10) {
            exp_term = g_L * Delta_T * exp(10)
        } else if ((v - vt) / Delta_T < -10) {
            exp_term = 0
        } else {
            exp_term = g_L * Delta_T * exp((v - vt) / Delta_T)
        }
        
        : Integrate using Euler method
        v = v + dt_internal * (-g_L * (v - E_L) + exp_term - z + I_ext) / C
        z = z + dt_internal * (a * (v - E_L) - z) / tau_w
        
        : Check for spike
        if (v >= th) {
            : Fire spike
            net_event(t)
            
            : Reset
            v = vr
            z = z + d
        }
        
        : Schedule next integration step
        net_send(dt_internal, 1)
    }
}
