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

        # Birth rate (taken from https://www.indexmundi.com/guinea/demographics_profile.html)
        self.mu = kwargs.get('birth_rate', 0)

        # Death rate
        self.nu = kwargs.get('death_rate', 0)

        self.result = None

    # The SIR model differential equations.
    @staticmethod
    def _deriv_non_vital_SIR_(y, t, population, beta, gamma):
        S, I, R = y
        dS_dt = -beta * S * I / population
        dI_dt = beta * S * I / population - gamma * I
        dR_dt = gamma * I 
        return dS_dt, dI_dt, dR_dt

    def calculate_non_vital_SIR(self):
        # Integrate the SIR equations over the time grid, t.
        ret = odeint(self._deriv_non_vital_SIR_, y0=self.initial_cond_vect, t=self.time_space,
                     args=(self.population, self.beta, self.gamma))
        self.result = ret.T

    @staticmethod
    def _deriv_vital_SIR_(y, t, population, beta, gamma, mu, nu):
        S, I, R = y
        dS_dt = mu * population - (beta * S * I) / population - nu * S
        dI_dt = (beta * S * I) / population - gamma * I - mu * I
        dR_dt = gamma * I - nu * R
        return dS_dt, dI_dt, dR_dt


    def calculate_vital_SIR(self):
        if self.mu == self.nu:
            print("Stable popultion {0} (mu) == {1} (nu)".format(self.mu, self.nu))    
            if self.mu == 0:
                print("Mu and Nu are 0. Non vital variant will be calculated.")
        ret = odeint(self._deriv_vital_SIR_, y0=self.initial_cond_vect, t=self.time_space,
                     args=(self.population, self.beta, self.gamma, self.mu, self.nu))
        self.result = ret.T


    def plot_result(self, **kwargs):
        susceptibles, infected, recovered = self.result

        magnitude = kwargs.get('magnitude', 1000)
        # Plot the data on three separate curves for S(t), I(t) and R(t)
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111)
        ax.plot(self.time_space, susceptibles/magnitude, 'b', alpha=0.5, lw=2, label='Susceptible',)
        ax.plot(self.time_space, infected/magnitude, 'r', alpha=0.5, lw=2, label='Infected')
        ax.plot(self.time_space, recovered/magnitude, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
        ax.set_xlabel('Time /days')
        ax.set_ylabel('Number (in {0}s)'.format(magnitude))
        ax.set_ylim(0, max(np.amax(susceptibles/magnitude), np.amax(infected/magnitude), np.amax(recovered/magnitude)) + 100)
        #ax.yaxis.set_tick_params(length=0)
        #ax.xaxis.set_tick_params(length=0)
        #ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        # for spine in ('top', 'right', 'bottom', 'left'):
        #     ax.spines[spine].set_visible(False)
        plt.show()
