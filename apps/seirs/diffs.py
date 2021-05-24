from apps.core.models import Coefficients, EpidemicNumbers


def get_dots(form, vital=False):
    S = form.N - 1
    I = 0
    R = 0
    E = 1
    if vital:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            alpha=form.alpha,
            ksi=form.ksi,
            birth=form.birth / 100,
            death=form.death / 100,
        )
    else:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            alpha=form.alpha,
            ksi=form.ksi,
        )
    curr_seirs = EpidemicNumbers(S=S, I=I, R=R, E=E)
    y_S = get_y(dS, S, form.days, form.N, curr_seirs, coefficients, vital)
    y_I = get_y(dI, I, form.days, form.N, curr_seirs, coefficients, vital)
    y_R = get_y(dR, R, form.days, form.N, curr_seirs, coefficients, vital)
    y_E = get_y(dE, E, form.days, form.N, curr_seirs, coefficients, vital)
    return y_S, y_I, y_R, y_E


def dS(
        N: int,
        seirs: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seirs.S + (
            - (coefficients.beta * seirs.I * seirs.S) / N
            + coefficients.ksi * seirs.R
    )
    if vital:
        result += coefficients.birth * N - seirs.S * coefficients.death
    return result


def dE(
        N: int,
        seirs: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seirs.E + (
            (coefficients.beta * seirs.I * seirs.S) / N
            - coefficients.alpha * seirs.E
    )
    if vital:
        result -= coefficients.death * seirs.E
    return result


def dI(
        N: int,
        seirs: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seirs.I + (
            coefficients.alpha * seirs.E
            - coefficients.gamma * seirs.I
    )
    if vital:
        result -= coefficients.death * seirs.I
    return result


def dR(
        N: int,
        seirs: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seirs.R + (
            coefficients.gamma * seirs.I
            - coefficients.ksi * seirs.R
    )
    if vital:
        result -= coefficients.death * seirs.R
    return result


def get_y(func, start, days, N, curr_seirs, coefficients, vital=False):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_seirs, coefficients, vital))
        next_seirs = EpidemicNumbers(
            S=dS(N, curr_seirs, coefficients, vital),
            I=dI(N, curr_seirs, coefficients, vital),
            R=dR(N, curr_seirs, coefficients, vital),
            E=dE(N, curr_seirs, coefficients, vital),
        )
        curr_seirs = next_seirs
    return cases
