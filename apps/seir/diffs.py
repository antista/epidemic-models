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
            birth=form.birth / 100,
            death=form.death / 100,
        )
    else:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            alpha=form.alpha,
        )
    curr_seir = EpidemicNumbers(S=S, I=I, R=R, E=E)
    y_S = get_y(dS, S, form.days, form.N, curr_seir, coefficients, vital)
    y_I = get_y(dI, I, form.days, form.N, curr_seir, coefficients, vital)
    y_R = get_y(dR, R, form.days, form.N, curr_seir, coefficients, vital)
    y_E = get_y(dE, E, form.days, form.N, curr_seir, coefficients, vital)
    return y_S, y_I, y_R, y_E


def dS(
        N: int,
        seir: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seir.S - (coefficients.beta * seir.I * seir.S) / N
    if vital:
        result += coefficients.birth * N - coefficients.death * seir.S
    return result


def dE(
        N: int,
        seir: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seir.E + (
            (coefficients.beta * seir.I * seir.S) / N
            - coefficients.alpha * seir.E
    )
    if vital:
        result -= coefficients.death * seir.E
    return result


def dI(
        N: int,
        seir: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seir.I + (
            coefficients.alpha * seir.E
            - coefficients.gamma * seir.I
    )
    if vital:
        result -= coefficients.death * seir.I
    return result


def dR(
        N: int,
        seir: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = seir.R + coefficients.gamma * seir.I
    if vital:
        result -= coefficients.death * seir.R
    return result


def get_y(func, start, days, N, curr_seir, coefficients, vital=False):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_seir, coefficients, vital))
        next_seir = EpidemicNumbers(
            S=dS(N, curr_seir, coefficients, vital),
            I=dI(N, curr_seir, coefficients, vital),
            R=dR(N, curr_seir, coefficients, vital),
            E=dE(N, curr_seir, coefficients, vital),
        )
        curr_seir = next_seir
    return cases
