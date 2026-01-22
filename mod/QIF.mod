TITLE QIF Neuron

COMMENT
Quadratic Integrate-and-Fire neuron

Equations:
dv/dt = (k*(v-vr)*(v-vt) - u + I_ext) / C
du/dt = (1/a) * (b * (v - vr) - u)

When v > th: v = c, u = u + d
ENDCOMMENT

NEURON {
    ARTIFICIAL_CELL QIF_neuron
    RANGE v, u, a, b, k, vt, vr, th, c, C, d, I_ext
    RANGE dt_internal
}

PARAMETER {
    a = 0.03 (/ms)
    b = 5
    k = 0.7
    vt = -50 (mV)
    vr = -70 (mV)
    th = 40 (mV)
    c = -60 (mV)
    C = 100 (pF)
    d = 100 (pA)
    I_ext = 0 (pA)
    dt_internal = 0.025 (ms)
}

ASSIGNED {
    v (mV)
    u (pA)
}

INITIAL {
    v = vr
    u = 0
    net_send(0, 1)
}

NET_RECEIVE(w) {
    if (flag == 1) {
        : Integrate using Euler method
        v = v + dt_internal * (k * (v - vr) * (v - vt) - u + I_ext) / C
        u = u + dt_internal * (b * (v - vr) - u) / (a * 1000)
        
        : Check for spike
        if (v >= th) {
            : Fire spike
            net_event(t)
            
            : Reset
            v = c
            u = u + d
        }
        
        : Schedule next integration step
        net_send(dt_internal, 1)
    }
}