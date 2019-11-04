import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class SIR:

    def __init__(self, **kwargs):
        # Total population
        self.population = kwargs.get('population', 1000)

        # Initial number of infected and recovered individuals
        self.patient_zero = kwargs.get('patient_zero', 1)
        self.recovered_patient_zero = kwargs.get('recovered_patient_zero', 0)

        # Everyone else, S0, is susceptible to infection initially.
        self.S0 = self.population - self.patient_zero - self.recovered_patient_zero

        # Contact rate
        self.beta = kwargs.get('contact_rate', 0.2)
        # mean recovery rate (in 1/days).
        self.gamma = kwargs.get('mean_recovery_rate', 1. / 10)

        # A grid of time points (in days)
        days = kwargs.get('days', 160)
        self.time_space = np.linspace(start=0, stop=days, num=days+1)

        self.initial_cond_vect = self.S0, self.patient_zero, self.recovered_patient_zero

        self.result = None

    # The SIR model differential equations.
    @staticmethod
    def __deriv__(y, t, population, beta, gamma):
        S, I, R = y
        dS_dt = -beta * S * I / population
        dI_dt = beta * S * I / population - gamma * I
        dR_dt = gamma * I
        return dS_dt, dI_dt, dR_dt

    def calculate(self):
        # Integrate the SIR equations over the time grid, t.
        ret = odeint(self.__deriv__, y0=self.initial_cond_vect, t=self.time_space,
                     args=(self.population, self.beta, self.gamma))
        self.result = ret.T

    def plot_result(self):
        susceptibles, infected, recovered = self.result

        # Plot the data on three separate curves for S(t), I(t) and R(t)
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111)
        ax.plot(self.time_space, susceptibles/1000, 'b', alpha=0.5, lw=2, label='Susceptible',)
        ax.plot(self.time_space, infected/1000, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(self.time_space, recovered/1000, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        ax.set_xlabel('Time /days')
        ax.set_ylabel('Number (in 1000s)')
        ax.set_ylim(0, max(np.amax(susceptibles/1000), np.amax(infected/1000), np.amax(recovered/1000)) + 100)
        #ax.yaxis.set_tick_params(length=0)
        #ax.xaxis.set_tick_params(length=0)
        #ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        # for spine in ('top', 'right', 'bottom', 'left'):
        #     ax.spines[spine].set_visible(False)
        plt.show()
