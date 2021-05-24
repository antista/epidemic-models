from apps.core.models import Coefficients, EpidemicNumbers


def get_dots(form, vital=False):
    S = form.N - 1
    I = 1
    if vital:
        coefficients = Coefficients(
            beta=form.beta,
            birth=form.birth / 100,
            death=form.death / 100,
        )
    else:
        coefficients = Coefficients(beta=form.beta)
    curr_si = EpidemicNumbers(S=S, I=I)
    y_S = get_y(dS, S, form.days, form.N, curr_si, coefficients, vital)
    y_I = get_y(dI, I, form.days, form.N, curr_si, coefficients, vital)
    return y_S, y_I


def dS(
        N: int,
        si: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = si.S - (coefficients.beta * si.S * si.I) / N
    if vital:
        result += coefficients.birth * N - coefficients.death * si.S
    return result


def dI(
        N: int,
        si: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = si.I + (coefficients.beta * si.S * si.I) / N
    if vital:
        result -= coefficients.death * si.I
    return result


def get_y(func, start, days, N, curr_si, coefficients, vital=False):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_si, coefficients, vital))
        next_si = EpidemicNumbers(
            S=dS(N, curr_si, coefficients, vital),
            I=dI(N, curr_si, coefficients, vital),
        )
        curr_si = next_si
    return cases
