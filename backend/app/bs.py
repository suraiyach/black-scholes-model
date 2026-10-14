import math
from math import log, sqrt, exp
from typing import Literal
from statistics import NormalDist

# Use Python 3.11 NormalDist for CDF to avoid SciPy dependency
N = NormalDist()

def d1(S: float, K: float, T: float, r: float, sigma: float) -> float:
    return (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))

def d2(S: float, K: float, T: float, r: float, sigma: float) -> float:
    return d1(S, K, T, r, sigma) - sigma * sqrt(T)

def price(S: float, K: float, T: float, r: float, sigma: float, kind: Literal["C", "P"]) -> float:
    D1 = d1(S, K, T, r, sigma)
    D2 = D1 - sigma * sqrt(T)
    if kind == "C":
        return S * N.cdf(D1) - K * exp(-r * T) * N.cdf(D2)
    else:
        return K * exp(-r * T) * N.cdf(-D2) - S * N.cdf(-D1)

def greeks(S: float, K: float, T: float, r: float, sigma: float):
    D1 = d1(S, K, T, r, sigma)
    D2 = D1 - sigma * math.sqrt(T)
    pdf = math.exp(-0.5 * D1 * D1) / math.sqrt(2 * math.pi)

    delta_call = N.cdf(D1)
    delta_put = delta_call - 1
    gamma = pdf / (S * sigma * math.sqrt(T))
    vega = S * pdf * math.sqrt(T) / 100.0

    theta_call = (-(S * pdf * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * N.cdf(D2)) / 365.0
    theta_put = (-(S * pdf * sigma) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * N.cdf(-D2)) / 365.0

    rho_call = K * T * math.exp(-r * T) * N.cdf(D2) / 100.0
    rho_put = -K * T * math.exp(-r * T) * N.cdf(-D2) / 100.0

    return {
        "delta_call": delta_call,
        "delta_put": delta_put,
        "gamma": gamma,
        "vega": vega,
        "theta_call": theta_call,
        "theta_put": theta_put,
        "rho_call": rho_call,
        "rho_put": rho_put,
    }
