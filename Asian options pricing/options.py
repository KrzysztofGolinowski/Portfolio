import numpy as np


class Option:
    """ Class of options

    Attributes:
        maturity (float): maturity of option in years
        strike_price (float): price at which contract can be exercised
        underlying_price (float): underlying security's current market price
        volatility (float): volatility of underlying price
        risk_free_rate (float): risk-free rate

    """
    def __init__(self, maturity, strike_price, underlying_price, volatility, risk_free_rate):
        self._maturity = maturity
        self._strike_price = strike_price
        self._underlying_price = underlying_price
        self._volatility = volatility
        self._r = risk_free_rate

    def payoff(self, current_u_price):
        """ Payoff function """
        return max(current_u_price[-1] - self._strike_price, 0)

    def simulate_path(self, n_observations, drift_factor, volatility_factor):
        """ Function to simulate price path
        Attributes:
            n_observations: number of price observations
            drift_factor: exp((r-0.5*sig**2)*dt)
            volatility_factor: sig*sqrt(dt) """
        path = [self._underlying_price]
        for i in range(1, n_observations):
            # path.append(path[i-1] * np.exp(drift*dt) * exp(self._volatility * np.sqrt(dt) * np.random.normal()))
            path.append(path[i-1] * drift_factor * np.exp(volatility_factor * np.random.normal()))
        return path

    def simulate_2_paths(self, n_observations, drift_factor, volatility_factor):
        """ Function to simulate two price paths for antithetic variate
        Second path uses random numbers from first: Z_2(i) = - Z_1(i)
        Attributes:
            n_observations: number of price observations
            drift_factor: exp((r-0.5*sig**2)*dt)
            volatility_factor: sig*sqrt(dt) """
        path1 = [self._underlying_price]
        path2 = [self._underlying_price]
        for i in range(1, n_observations):
            z = np.random.normal()
            path1.append(path1[i-1] * drift_factor * np.exp(volatility_factor * z))
            path2.append(path2[i-1] * drift_factor * np.exp(volatility_factor * -z))
        return path1, path2

    def simulation(self, n_paths, n_observations, **var_reduction):
        """ Function which run simulation
        Attributes:
            n_paths: number of simulated paths
            n_observations: number of price observations in each path
            **var_reduction: method of variance reduction,
                var_reduction="antithetic" for antithetic variate or blank for standard monte carlo
        """
        results = []

        drift = self._r - 0.5*self._volatility**2
        dt = self._maturity / n_observations
        drift_factor = np.exp(drift*dt)
        volatility_factor = self._volatility * np.sqrt(dt)
        discount_factor = np.exp(-self._r * self._maturity)

        for i in range(0, n_paths):
            if var_reduction == "antithetic":
                path1, path2 = self.simulate_2_paths(n_observations, drift_factor, volatility_factor)
                c = 0.5*(self.payoff(path1) + self.payoff(path2))
            else:
                path = self.simulate_path(n_observations, drift_factor, volatility_factor)
                c = self.payoff(path)

            results.append(discount_factor * c)

        return {"mean": np.mean(results),
                "std": np.std(results)/np.sqrt(n_paths),
                "trials": n_paths,
                "path_len": n_observations}

    def pseudo_closed_form(self):
        pass

    def __str__(self):
        return ("Main class option\n\tmaturity: {0._maturity:0.3f} year,\tstrike price: {0._strike_price}, \n"
                "\tunderlying price: {0._underlying_price},\tvolatility: {0._volatility}, \n"
                "\trisk-free rate: {0._r},\t}".format(self))


if __name__ == '__main__':
    print("*** Please run main.py script! ***")
