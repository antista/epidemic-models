from apps.core.models import Coefficients, EpidemicNumbers


def get_dots(form, vital=False):
    S = form.N - 1
    I = 1
    R = 0
    if vital:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            ksi=form.ksi,
            birth=form.birth / 100,
            death=form.death / 100,
        )
    else:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            ksi=form.ksi,
        )
    curr_sirs = EpidemicNumbers(S=S, I=I, R=R)
    y_S = get_y(dS, S, form.days, form.N, curr_sirs, coefficients, vital)
    y_I = get_y(dI, I, form.days, form.N, curr_sirs, coefficients, vital)
    y_R = get_y(dR, R, form.days, form.N, curr_sirs, coefficients, vital)
    return y_S, y_I, y_R


def dS(
        N: int,
        sirs: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sirs.S + (
            -(coefficients.beta * sirs.S * sirs.I) / N
            + coefficients.ksi * sirs.R
    )
    if vital:
        result += coefficients.birth * N - coefficients.death * sirs.S
    return result


def dI(
        N: int,
        sirs: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sirs.I + (
            (coefficients.beta * sirs.S * sirs.I) / N
            - coefficients.gamma * sirs.I
    )
    if vital:
        result -= coefficients.death * sirs.I
    return result


def dR(
        N: int,
        sirs: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sirs.R + coefficients.gamma * sirs.I - coefficients.ksi * sirs.R
    if vital:
        result -= coefficients.death * sirs.R
    return result


def get_y(func, start, days, N, curr_sirs, coefficients, vital=False):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_sirs, coefficients, vital))
        next_sirs = EpidemicNumbers(
            S=dS(N, curr_sirs, coefficients, vital),
            I=dI(N, curr_sirs, coefficients, vital),
            R=dR(N, curr_sirs, coefficients, vital),
        )
        curr_sirs = next_sirs
    return cases
