from apps.core.models import Coefficients, EpidemicNumbers


def get_dots(form, vital=False):
    S = form.N - 1
    E = 1
    I = 0
    R = 0
    D = 0
    if vital:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            alpha=form.alpha,
            mu=form.mu,
            ksi=form.ksi,
            birth=form.birth / 100,
            death=form.death / 100,
        )
    else:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            alpha=form.alpha,
            mu=form.mu,
            ksi=form.ksi,
        )
    curr_seirds = EpidemicNumbers(S=S, E=E, I=I, R=R, D=D)
    y_S = get_y(dS, S, form.days, form.N, curr_seirds, coefficients, vital)
    y_E = get_y(dE, E, form.days, form.N, curr_seirds, coefficients, vital)
    y_I = get_y(dI, I, form.days, form.N, curr_seirds, coefficients, vital)
    y_R = get_y(dR, R, form.days, form.N, curr_seirds, coefficients, vital)
    y_D = get_y(dD, D, form.days, form.N, curr_seirds, coefficients, vital)
    return y_S, y_E, y_I, y_R, y_D


def dS(
        N: int,
        seirds: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seirds.S + (
            - (coefficients.beta * seirds.S * seirds.I) / N
            + coefficients.ksi * seirds.R
    )
    if vital:
        result += coefficients.birth * N - coefficients.death * seirds.S
    return result


def dE(
        N: int,
        seirds: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seirds.E + (
            (coefficients.beta * seirds.I * seirds.S) / N
            - coefficients.alpha * seirds.E
    )
    if vital:
        result -= coefficients.death * seirds.E
    return result


def dI(
        N: int,
        seirds: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seirds.I + (
            coefficients.alpha * seirds.E
            - seirds.I * (coefficients.gamma + coefficients.mu)
    )
    if vital:
        result -= coefficients.death * seirds.I
    return result


def dR(
        N: int,
        seirds: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seirds.R + (
            coefficients.gamma * seirds.I
            - coefficients.ksi * seirds.R
    )
    if vital:
        result -= coefficients.death * seirds.R
    return result


def dD(
        N: int,
        seirds: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seirds.D + coefficients.mu * seirds.I
    # if vital:
    #     result += coefficients.death * (seirds.S + seirds.E + seirds.I + seirds.R)
    return result


def get_y(func, start, days, N, curr_seirds, coefficients, vital=False):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_seirds, coefficients, vital))
        next_seirds = EpidemicNumbers(
            S=dS(N, curr_seirds, coefficients, vital),
            E=dE(N, curr_seirds, coefficients, vital),
            I=dI(N, curr_seirds, coefficients, vital),
            R=dR(N, curr_seirds, coefficients, vital),
            D=dD(N, curr_seirds, coefficients, vital),
        )
        curr_seirds = next_seirds
    return cases
