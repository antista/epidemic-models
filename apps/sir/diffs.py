from apps.core.models import Coefficients, EpidemicNumbers


def get_dots(form, vital=False):
    S = form.N - 1
    I = 1
    R = 0
    if vital:
        coefficients = Coefficients(
            beta=form.beta,
            gamma=form.gamma,
            birth=form.birth / 100,
            death=form.death / 100,
        )
    else:
        coefficients = Coefficients(beta=form.beta, gamma=form.gamma)
    curr_sir = EpidemicNumbers(S=S, I=I, R=R)
    y_S = get_y(dS, S, form.days, form.N, curr_sir, coefficients, vital)
    y_I = get_y(dI, I, form.days, form.N, curr_sir, coefficients, vital)
    y_R = get_y(dR, R, form.days, form.N, curr_sir, coefficients, vital)
    return y_S, y_I, y_R


def dS(
        N: int,
        sir: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sir.S - (coefficients.beta * sir.S * sir.I) / N
    if vital:
        result += coefficients.birth * N - coefficients.death * sir.S
    return result


def dI(
        N: int,
        sir: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sir.I + (
            (coefficients.beta * sir.S * sir.I) / N
            - coefficients.gamma * sir.I
    )
    if vital:
        result -= coefficients.death * sir.I
    return result


def dR(
        N: int,
        sir: EpidemicNumbers,
        coefficients: Coefficients,
        vital: bool = False,
) -> float:
    result = sir.R + coefficients.gamma * sir.I
    if vital:
        result -= coefficients.death * sir.R
    return result


def get_y(func, start, days, N, curr_sir, coefficients, vital=False):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_sir, coefficients, vital))
        next_sir = EpidemicNumbers(
            S=dS(N, curr_sir, coefficients, vital),
            I=dI(N, curr_sir, coefficients, vital),
            R=dR(N, curr_sir, coefficients, vital),
        )
        curr_sir = next_sir
    return cases
