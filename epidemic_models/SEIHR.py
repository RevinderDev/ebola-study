import numpy as np
from scipy.integrate import odeint


class SEIHR:
    def __init__(self, **kwargs):
        self.alpha = kwargs.get('birth_rate', 0)
        self.mu = kwargs.get('natural_death', 0)
        self.beta_I = kwargs.get('contact_rate_S_to_I', 0)  # Suspected to Infected
        self.beta_H = kwargs.get('contact_rate_S_to_H', 0)  # Suspected to Hospitalized
        self.sigma = 1. / kwargs.get('incubation_period', 0)
        self.mu_h = 1. / kwargs.get('hospitalization_time', 0)
        self.mu_r = kwargs.get('recovery_rate_infected', 0)
        self.mu_h_r = kwargs.get('recovery_rate_hospitalized', 0)
        self.mu_q = kwargs.get('death_rate_by_infection', 0)
        self.mu_q_h = kwargs.get('death_rate_by_infection_in_hospital')
        self.N = kwargs.get('population', 1)
        days = kwargs.get('days', 500)
        self.time_space = np.linspace(start=0, stop=days, num=days + 1)

        # Initial number of infected and recovered individuals
        self.infected = kwargs.get('patient_zero', 0.2)
        self.recovered = kwargs.get('recovered_patient_zero', 0.2)
        self.hospitalized = kwargs.get('hospitalized', 0.2)
        self.susceptible = kwargs.get('susceptible', 0.2)
        self.exposed = kwargs.get('exposed', 0.2)
        self.y0 = self.susceptible, self.exposed, self.infected, self.hospitalized, self.recovered

        if self.beta_I <= self.mu_q:
            raise Exception('Contact rate between susceptible and infected '
                            'must be superior to death rate due to infection.')

        # if self.beta_H <= self.mu_q_h:
        #     raise Exception(
        #         'Contact rate between susceptible and hospitalized '
        #         'individuals must be superior to death rate due to infection in hospital.')

        self.result = None

        # The SIR model differential equations.

    @staticmethod
    def _main_model_(y, t, n, alpha, mu, beta_i, beta_h, sigma, mu_q, mu_h, mu_r, mu_h_r, mu_h_q):
        s, e, i, h, r = y

        ds_dt = alpha * n - mu * s - (beta_i * s * i) / n - (beta_h * s * h) / n
        de_dt = (beta_i * s * i) / n + (beta_h * s * h) / n - (mu + sigma) * e
        di_dt = sigma * e - (mu_h * mu_q * mu * mu_r) * i
        dh_dt = mu_h * i - (mu_h_q + mu + mu_h_r) * h
        dr_dt = mu_r * i - mu * r + mu_h_r * h

        return ds_dt, de_dt, di_dt, dh_dt, dr_dt

    def calculate_model(self):
        return odeint(self._main_model_, y0=self.y0, t=self.time_space,
                      args=(self.N, self.alpha, self.mu,
                            self.beta_I, self.beta_H, self.sigma,
                            self.mu_q, self.mu_h, self.mu_r,
                            self.mu_h_r, self.mu_q_h))
