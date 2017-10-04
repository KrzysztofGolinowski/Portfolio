from asian_options import *


opt = AsianOption(20 / 365, 100, 100, 0.25, 0.1)

print(opt)
print("\n" + "*" * 80 + "\n")


sim1 = opt.simulation(1500, 20)
sim2 = opt.simulation(1500, 20, var_reduction="antithetic")
print("Simulation for {0[trials]:,} paths, {0[path_len]} observations in each.\n"
      "Standard Monte Carlo: Estimated value:\t\t{0[mean]:.3f},\tstandard deviation:\t{0[std]:.3f}\n"
      "Antithetic variate:   Estimated value:\t\t{1[mean]:.3f},\tstandard deviation:\t{1[std]:.3f}".format(sim1, sim2))

eq12 = opt.pseudo_closed_form()
eq25 = opt.approximation_eq25()
print("Pseudo-closed-form solution (12): \t{:3.3f}\nSolution of equation (25): \t{:3.3f}".format(eq12, eq25))
print("\n" + "*" * 80 + "\n")


print("Value of asian option for different volatilities (simulation of 10,000 paths, antithetic variate)")
print("Volatility\t\tEstimated value\t\tStandard deviation\t\tPseudo-closed-form solution")

for sig in [0.1, 0.25, 0.5]:
    opt._volatility = sig
    sim3 = opt.simulation(10000, 20, var_reduction="antithetic")
    eq12 = opt.pseudo_closed_form()
    print(("{:2.3f}\t\t\t\t"*4).format(sig, sim3["mean"], sim3["std"], eq12))
