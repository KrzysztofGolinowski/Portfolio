from data_set import *
import matplotlib.pyplot as plt


# creating two data sets
# the first with 1000 samples from know distribution
# and the second with 100 samples coming from "unknown" distribution, i.e. from experiment
set_A = Data_Set(1000)
set_B = Data_Set(100)

# generating points for these sets: A - normal distribution, B - Cauchy distribution
set_A.generate(0, 1)
set_B.generate(0, 1, "Cauchy")


# creating object of data comparator and pass to it two data sets - known, referential A and experimental B
comparator = Data_Comparator(set_A, set_B)

# computing distribution of inner energy in set A with bootstrap method
# by randomly dividing set A to two samples (9:1)
# repeated 1000 times, using exponent function with 0.7 parameter
energies_A = comparator.generate_bootstrap_fi(1000, "exp", 0.7)

# computing energy between sets A and {}
energy_AB = comparator.compare_distributions()

# computing p-value for hypothesis that sets A and B come from the same distribution
p_value = sum(1 for i in energies_A if i > energy_AB) / len(energies_A)
print("p_value = {:0.2f}%".format(p_value*100))
print("Hypothesis that set A and B come from the same distribution can be {}"
      " on significance level = 5%".format("confirmed" if p_value <= 0.05 else "regret"))


# plotting two data sets
plt.figure(1)
plt.grid(linestyle=":")
plt.scatter(set_A.x, set_A.y, s=1, label="Data set A - normal")
plt.scatter(set_B.x, set_B.y, s=4, label="Data set B - Cauchy")
plt.axis('equal')
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show(block=False)

# plotting distribution of inner energy of set A and energy between A and B
plt.figure(2)
plt.grid(linestyle=":")
plt.hist(energies_A, bins=40)
plt.plot((energy_AB, energy_AB), (0, len(energies_A)/15.0), 'r-')
plt.annotate(s="Observed\nenergy", xy=(energy_AB, len(energies_A)/20.0),
             xytext=(0.1, 0.9), textcoords='axes fraction', arrowprops=dict(arrowstyle='->'))
plt.xlabel("Energy")
plt.ylabel("Number of entries")
plt.show()
