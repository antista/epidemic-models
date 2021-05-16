from apps.core.models import Coefficients, EpidemicNumbers


def get_dots(form):
    S = form.N - 1
    I = 1
    coefficients = Coefficients(beta=form.beta, gamma=form.gamma)
    curr_sis = EpidemicNumbers(S=S, I=I)
    y_S = get_y(dS, S, form.days, form.N, curr_sis, coefficients)
    y_I = get_y(dI, I, form.days, form.N, curr_sis, coefficients)
    return y_S, y_I


def dS(N: int, sis: EpidemicNumbers, coefficients: Coefficients):
    return sis.S + (
            -(coefficients.beta * sis.S * sis.I) / N
            + coefficients.gamma * sis.I
    )


def dI(N: int, sis: EpidemicNumbers, coefficients: Coefficients) -> float:
    return sis.I + (
            (coefficients.beta * sis.S * sis.I) / N
            - coefficients.gamma * sis.I
    )


def get_y(func, start, days, N, curr_sis, coefficients):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_sis, coefficients))
        next_sis = EpidemicNumbers(
            S=dS(N, curr_sis, coefficients),
            I=dI(N, curr_sis, coefficients),
        )
        curr_sis = next_sis
    return cases
