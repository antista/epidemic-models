from apps.core.models import Coefficients, EpidemicNumbers


def get_dots(form):
    S = form.N - 1
    I = 1
    R = 0
    E = 1
    coefficients = Coefficients(
        beta=form.beta,
        gamma=form.gamma,
        # mu=form.mu,
        alpha=form.alpha,
    )
    curr_seir = EpidemicNumbers(S=S, I=I, R=R, E=E)
    y_S = get_y(dS, S, form.days, form.N, curr_seir, coefficients)
    y_I = get_y(dI, I, form.days, form.N, curr_seir, coefficients)
    y_R = get_y(dR, R, form.days, form.N, curr_seir, coefficients)
    y_E = get_y(dE, E, form.days, form.N, curr_seir, coefficients)
    return y_S, y_I, y_R, y_E


def dS(N: int, seir: EpidemicNumbers, coefficients: Coefficients):
    return seir.S + (
        # (N - seir.S) * coefficients.mu
            - (coefficients.beta * seir.I * seir.S) / N
    )


def dI(N: int, seir: EpidemicNumbers, coefficients: Coefficients) -> float:
    return seir.I + (
            coefficients.alpha * seir.E
            - coefficients.gamma * seir.I
        # - (coefficients.gamma + coefficients.mu) * seir.I
    )


def dR(N: int, seir: EpidemicNumbers, coefficients: Coefficients) -> float:
    return seir.R + (
            coefficients.gamma * seir.I
        # - coefficients.mu * seir.R
    )


def dE(N: int, seir: EpidemicNumbers, coefficients: Coefficients) -> float:
    return seir.E + (
            (coefficients.beta * seir.I * seir.S) / N
            - coefficients.alpha * seir.E
        # - (coefficients.mu + coefficients.alpha) * seir.E
    )


def get_y(func, start, days, N, curr_seir, coefficients):
    cases = [start]
    for _ in range(days - 1):
        cases.append(func(N, curr_seir, coefficients))
        next_seir = EpidemicNumbers(
            S=dS(N, curr_seir, coefficients),
            I=dI(N, curr_seir, coefficients),
            R=dR(N, curr_seir, coefficients),
            E=dE(N, curr_seir, coefficients),
        )
        curr_seir = next_seir
    return cases
