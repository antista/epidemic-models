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
            birth=form.birth / 100,
            death=form.death / 100,
        )
    else:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            mu=form.mu,
        )
    curr_sird = EpidemicNumbers(S=S, I=I, R=R, D=D)
    y_S = get_y(dS, S, form.days, form.N, curr_sird, coefficients, vital)
    y_I = get_y(dI, I, form.days, form.N, curr_sird, coefficients, vital)
    y_R = get_y(dR, R, form.days, form.N, curr_sird, coefficients, vital)
    y_D = get_y(dD, D, form.days, form.N, curr_sird, coefficients, vital)
    return y_S, y_I, y_R, y_D


def dS(
        N: int,
        sird: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sird.S - (coefficients.beta * sird.S * sird.I) / N
    if vital:
        result += coefficients.birth * N - coefficients.death * sird.S
    return result


def dI(
        N: int,
        sird: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sird.I + (
            (coefficients.beta * sird.S * sird.I) / N
            - sird.I * (coefficients.gamma + coefficients.mu)
    )
    if vital:
        result -= coefficients.death * sird.I
    return result


def dR(
        N: int,
        sird: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sird.R + coefficients.gamma * sird.I
    if vital:
        result -= coefficients.death * sird.R
    return result


def dD(
        N: int,
        sird: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sird.D + coefficients.mu * sird.I
    if vital:
        result += coefficients.death * (sird.S + sird.I + sird.R)
    return result


def get_y(func, start, days, N, curr_sird, coefficients, vital=False):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_sird, coefficients, vital))
        next_sird = EpidemicNumbers(
            S=dS(N, curr_sird, coefficients, vital),
            I=dI(N, curr_sird, coefficients, vital),
            R=dR(N, curr_sird, coefficients, vital),
            D=dD(N, curr_sird, coefficients, vital),
        )
        curr_sird = next_sird
    return cases
