from apps.core.models import Coefficients, EpidemicNumbers


def get_dots(form):
    S = form.N - 1
    I = 1
    R = 0
    coefficients = Coefficients(beta=form.beta, gamma=form.gamma)
    curr_sir = EpidemicNumbers(S=S, I=I, R=R)
    y_S = get_y(dS, S, form.days, form.N, curr_sir, coefficients)
    y_I = get_y(dI, I, form.days, form.N, curr_sir, coefficients)
    y_R = get_y(dR, R, form.days, form.N, curr_sir, coefficients)
    return y_S, y_I, y_R


def dS(N: int, sir: EpidemicNumbers, coefficients: Coefficients):
    return sir.S + (
            -(coefficients.beta * sir.S * sir.I) / N
    )


def dI(N: int, sir: EpidemicNumbers, coefficients: Coefficients) -> float:
    return sir.I + (
            (coefficients.beta * sir.S * sir.I) / N
            - coefficients.gamma * sir.I
    )


def dR(N: int, sir: EpidemicNumbers, coefficients: Coefficients) -> float:
    return sir.R + coefficients.gamma * sir.I


def get_y(func, start, days, N, curr_sir, coefficients):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_sir, coefficients))
        next_sir = EpidemicNumbers(
            S=dS(N, curr_sir, coefficients),
            I=dI(N, curr_sir, coefficients),
            R=dR(N, curr_sir, coefficients),
        )
        curr_sir = next_sir
    return cases
