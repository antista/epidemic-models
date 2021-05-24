from apps.core.models import Coefficients, EpidemicNumbers


def get_dots(form, vital=False):
    S = form.N - 1
    I = 1
    if vital:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            birth=form.birth / 100,
            death=form.death / 100,
        )
    else:
        coefficients = Coefficients(beta=form.beta, gamma=form.gamma)
    curr_sis = EpidemicNumbers(S=S, I=I)
    y_S = get_y(dS, S, form.days, form.N, curr_sis, coefficients, vital)
    y_I = get_y(dI, I, form.days, form.N, curr_sis, coefficients, vital)
    return y_S, y_I


def dS(
        N: int,
        sis: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sis.S + (
            -(coefficients.beta * sis.S * sis.I) / N
            + coefficients.gamma * sis.I
    )
    if vital:
        result += coefficients.birth * N - coefficients.death * sis.S
    return result


def dI(
        N: int,
        sis: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sis.I + (
            (coefficients.beta * sis.S * sis.I) / N
            - coefficients.gamma * sis.I
    )
    if vital:
        result -= coefficients.death * sis.I
    return result


def get_y(func, start, days, N, curr_sis, coefficients, vital=False):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_sis, coefficients, vital))
        next_sis = EpidemicNumbers(
            S=dS(N, curr_sis, coefficients, vital),
            I=dI(N, curr_sis, coefficients, vital),
        )
        curr_sis = next_sis
    return cases
