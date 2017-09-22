from options import *
from scipy.stats import norm


class AsianOption(Option):
    """ Class of asian options

    Attributes:
        maturity (float): maturity of option in years
        strike_price (float): price at which contract can be exercised
        underlying_price (float): underlying security's current market price
        volatility (float): volatility of underlying price
        risk_free_rate (float): risk-free rate
        avg_period (optional, float): the average period of forward-starting options
    """

    def __init__(self, maturity, strike_price, underlying_price, volatility, risk_free_rate, avg_period=None):
        super().__init__(maturity, strike_price, underlying_price, volatility, risk_free_rate)

        if not avg_period or avg_period == 0:
            self._forward_staring_period = maturity
        else:
            self._forward_staring_period = avg_period

    def payoff(self, price_path):
        """ Payoff function for asian option """
        return np.maximum(np.mean(price_path) - self._strike_price, 0)

    def pseudo_closed_form(self):
        """ closed-from solution to the pricing of the asian option, L.Bouaziz, E.Briys, M.Crouhy """
        s = self._underlying_price
        a = self._maturity
        sig = self._volatility
        r = self._r
        rh = r - 0.5*sig**2

        return s * np.exp(-r * a) * (
            (rh*a/2) * norm.cdf(rh*np.sqrt(3*a)/(2*sig))
            + np.sqrt(sig**2*a/(6*np.pi))*np.exp(-3*rh**2*a/(8*sig**2))
        )

    def approximation_eq25(self):
        s = self._underlying_price
        a = self._maturity
        sig = self._volatility
        r = self._r
        rhm = r - 0.5*sig**2
        rhp = r + 0.5*sig**2

        return 0.5 * s * (
            norm.cdf(rhp * np.sqrt(a) / sig)
            - np.exp(-r * a) * norm.cdf(rhm * np.sqrt(a) / sig)
            )

    def __str__(self):
        return ("Asian option\n\tmaturity: {0._maturity:0.3f} year,\tstrike price: {0._strike_price}, \n"
                "\tunderlying price: {0._underlying_price},\tvolatility: {0._volatility}, \n"
                "\trisk-free rate: {0._r},\taverage period: {0._forward_staring_period:0.3f}".format(self))


if __name__ == '__main__':
    print("*** Please run main.py script! ***")
