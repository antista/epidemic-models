from dataclasses import dataclass


@dataclass
class Coefficients:
    beta: float = None
    gamma: float = None
    mu: float = None
    alpha: float = None
    ksi: float = None
    birth: float = None
    death: float = None


@dataclass
class EpidemicNumbers:
    S: float = None
    I: float = None
    R: float = None
    D: float = None
    E: float = None
