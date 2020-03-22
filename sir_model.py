#!/usr/bin/env python

"""
SIR model: very simple infectious dieseases model. It assumes once healed you
have immunity.

https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model

That's all folks.
"""

__author__ = "Martin De Kauwe"
__version__ = "1.0 (23.03.2020)"
__email__ = "mdekauwe@gmail.com"

def SIR(t, y, beta, gamma):
    """
    Susceptible: people vulnerable to exposure with infectious people
    Infectious: infected people
    Recovered: people get immunity

    where Beta controls how much of the disease is transmitted via exposure and
    gamma sets the recovery rate
    """
    S = y[0]
    I = y[1]
    R = y[2]

    dS_dt = -beta * S * I
    dI_dt = beta * S * I - gamma * I
    dR_dt = gamma * I

    return (dS_dt, dI_dt, dR_dt)
