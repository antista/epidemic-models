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
            birth=form.birth / 100,
            death=form.death / 100,
        )
    else:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            alpha=form.alpha,
            mu=form.mu,
        )
    curr_seird = EpidemicNumbers(S=S, E=E, I=I, R=R, D=D)
    y_S = get_y(dS, S, form.days, form.N, curr_seird, coefficients, vital)
    y_E = get_y(dE, E, form.days, form.N, curr_seird, coefficients, vital)
    y_I = get_y(dI, I, form.days, form.N, curr_seird, coefficients, vital)
    y_R = get_y(dR, R, form.days, form.N, curr_seird, coefficients, vital)
    y_D = get_y(dD, D, form.days, form.N, curr_seird, coefficients, vital)
    return y_S, y_E, y_I, y_R, y_D


def dS(
        N: int,
        seird: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seird.S - (coefficients.beta * seird.S * seird.I) / N
    if vital:
        result += coefficients.birth * N - coefficients.death * seird.S
    return result


def dE(
        N: int,
        seird: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seird.E + (
            (coefficients.beta * seird.I * seird.S) / N
            - coefficients.alpha * seird.E
    )
    if vital:
        result -= coefficients.death * seird.E
    return result


def dI(
        N: int,
        seird: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seird.I + (
            coefficients.alpha * seird.E
            - seird.I * (coefficients.gamma + coefficients.mu)
    )
    if vital:
        result -= coefficients.death * seird.I
    return result


def dR(
        N: int,
        seird: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seird.R + coefficients.gamma * seird.I
    if vital:
        result -= coefficients.death * seird.R
    return result


def dD(
        N: int,
        seird: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seird.D + coefficients.mu * seird.I
    # if vital:
    #     result += coefficients.death * (seird.S + seird.E + seird.I + seird.R)
    return result


def get_y(func, start, days, N, curr_seird, coefficients, vital=False):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_seird, coefficients, vital))
        next_seird = EpidemicNumbers(
            S=dS(N, curr_seird, coefficients, vital),
            E=dE(N, curr_seird, coefficients, vital),
            I=dI(N, curr_seird, coefficients, vital),
            R=dR(N, curr_seird, coefficients, vital),
            D=dD(N, curr_seird, coefficients, vital),
        )
        curr_seird = next_seird
    return cases
