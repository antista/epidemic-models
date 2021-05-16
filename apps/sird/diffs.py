from apps.core.models import Coefficients, EpidemicNumbers


def get_dots(form):
    S = form.N - 1
    I = 1
    R = 0
    D = 0
    coefficients = Coefficients(beta=form.beta, gamma=form.gamma, mu=form.mu)
    curr_sird = EpidemicNumbers(S=S, I=I, R=R, D=D)
    y_S = get_y(dS, S, form.days, form.N, curr_sird, coefficients)
    y_I = get_y(dI, I, form.days, form.N, curr_sird, coefficients)
    y_R = get_y(dR, R, form.days, form.N, curr_sird, coefficients)
    y_D = get_y(dD, D, form.days, form.N, curr_sird, coefficients)
    return y_S, y_I, y_R, y_D


def dS(N: int, sird: EpidemicNumbers, coefficients: Coefficients):
    return sird.S - (coefficients.beta * sird.S * sird.I) / N


def dI(N: int, sird: EpidemicNumbers, coefficients: Coefficients) -> float:
    return sird.I + (
            (coefficients.beta * sird.S * sird.I) / N
            - sird.I * (coefficients.gamma + coefficients.mu)
    )


def dR(N: int, sird: EpidemicNumbers, coefficients: Coefficients) -> float:
    return sird.R + coefficients.gamma * sird.I


def dD(N: int, sird: EpidemicNumbers, coefficients: Coefficients) -> float:
    return sird.D + coefficients.mu * sird.I


def get_y(func, start, days, N, curr_sird, coefficients):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_sird, coefficients))
        next_sird = EpidemicNumbers(
            S=dS(N, curr_sird, coefficients),
            I=dI(N, curr_sird, coefficients),
            R=dR(N, curr_sird, coefficients),
            D=dD(N, curr_sird, coefficients),
        )
        curr_sird = next_sird
    return cases
