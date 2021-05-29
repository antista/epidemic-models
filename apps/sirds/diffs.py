from apps.core.models import Coefficients, EpidemicNumbers


def get_dots(form, vital=False):
    S = form.N - 1
    I = 1
    R = 0
    D = 0
    if vital:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            mu=form.mu,
            ksi=form.ksi,
            birth=form.birth / 100,
            death=form.death / 100,
        )
    else:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            mu=form.mu,
            ksi=form.ksi,
        )
    curr_sirds = EpidemicNumbers(S=S, I=I, R=R, D=D)
    y_S = get_y(dS, S, form.days, form.N, curr_sirds, coefficients, vital)
    y_I = get_y(dI, I, form.days, form.N, curr_sirds, coefficients, vital)
    y_R = get_y(dR, R, form.days, form.N, curr_sirds, coefficients, vital)
    y_D = get_y(dD, D, form.days, form.N, curr_sirds, coefficients, vital)
    return y_S, y_I, y_R, y_D


def dS(
        N: int,
        sirds: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sirds.S + (
            - (coefficients.beta * sirds.S * sirds.I) / N
            + coefficients.ksi * sirds.R
    )
    if vital:
        result += coefficients.birth * N - coefficients.death * sirds.S
    return result


def dI(
        N: int,
        sirds: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sirds.I + (
            (coefficients.beta * sirds.S * sirds.I) / N
            - sirds.I * (coefficients.gamma + coefficients.mu)
    )
    if vital:
        result -= coefficients.death * sirds.I
    return result


def dR(
        N: int,
        sirds: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sirds.R + coefficients.gamma * sirds.I - coefficients.ksi * sirds.R
    if vital:
        result -= coefficients.death * sirds.R
    return result


def dD(
        N: int,
        sirds: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sirds.D + coefficients.mu * sirds.I
    return result


def get_y(func, start, days, N, curr_sirds, coefficients, vital=False):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_sirds, coefficients, vital))
        next_sirds = EpidemicNumbers(
            S=dS(N, curr_sirds, coefficients, vital),
            I=dI(N, curr_sirds, coefficients, vital),
            R=dR(N, curr_sirds, coefficients, vital),
            D=dD(N, curr_sirds, coefficients, vital),
        )
        curr_sirds = next_sirds
    return cases
