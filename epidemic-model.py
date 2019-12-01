from epidemic_models import SIR
from epidemic_models import SEIHR
import matplotlib.pyplot as plt
import networkx as nx

def sir_models():
    sir_non_vital = SIR(population=12720000, days=861,
                        contact_rate=0.2, mean_recovery_rate=1. / 10)
    sir_non_vital.calculate_non_vital_SIR()
    sir_non_vital.plot_result(magnitude=1000)

    sir_vital = SIR(population=12720000, days=861,
                    contact_rate=0.2, mean_recovery_rate=1. / 10,
                    death_rate=8.7, birth_rate=37.2)
    sir_vital.calculate_vital_SIR()
    sir_vital.plot_result(magnitude=1000)


def create_seihr():
    # Liberia
    seihr_model = SEIHR(birth_rate=0.01,
                        natural_death=0.007,
                        contact_rate_S_to_I=0.16,
                        contact_rate_S_to_H=0.062,
                        incubation_period=12,
                        death_rate_by_infection= 1./13,
                        death_rate_by_infection_in_hospital=1./10.07,
                        hospitalization_time=3.24,
                        recovery_rate_infected= 1./150,
                        recovery_rate_hospitalized= 1./150.88)

    result = seihr_model.calculate_model()

    s, e, i, h, r = result.T

    plt.plot(seihr_model.time_space, s, 'b', label='susceptible(t)')
    plt.plot(seihr_model.time_space, e, 'g', label='exposed(t)')
    plt.plot(seihr_model.time_space, i, 'r', label='infected(t)')
    plt.plot(seihr_model.time_space, h, 'y', label='hospitalized(t)')
    plt.plot(seihr_model.time_space, r, 'c', label='recovered(t)')
    plt.legend(loc='best')
    plt.xlabel('t')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    # sir_models()
    create_seihr()
