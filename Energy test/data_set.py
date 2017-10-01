import numpy as np
import scipy.spatial.distance as dist


class Data_Set(object):
    """ Class of data set
    Attribute - n (int): number of points
    """

    def __init__(self, n):
        self._n = n
        self._values = np.zeros((n, 2))

        self._x0 = None
        self._p = None
        self._distribution = None

    def generate(self, x0, p, distribution=""):
        """ Function to generate data set
            Quantile function is used to generate data from Cauchy distribution
            (uniform distribution limits are 0.11 and 0.89 to cutoff huge values)
        """

        self._x0 = x0
        self._p = p
        self._distribution = distribution

        if self._distribution == "Cauchy":
            self._values = self._x0 + self._p * np.tan(np.pi * (np.random.uniform(0.11, 0.89, (self._n, 2)) - 0.5))
        else:
            self._values = np.random.normal(self._x0, self._p, (self._n, 2))

    def load_values(self, values):
        """ Function to load external values to data set """
        self._values = values

    def __len__(self):
        return self._n

    def __getattr__(self, item):
        if item == "x":
            return self._values[:, 0]
        elif item == "y":
            return self._values[:, 1]
        else:
            return None

    def __call__(self, *args, **kwargs):
        return self._values


class Data_Comparator(object):
    """ Class of two data sets comparator
    Attributes:
         set_reference(Data_Set): data set of points from known distribution
         set_experimental(Data_Set): data set of points from unknown distribution - i.e. from experiment
    """

    def __init__(self, set_reference, set_experimental):
        self._set_ref = set_reference
        self._set_exp = set_experimental

        """ two auxiliary data sets to store divided reference set in proportions 9:1 """
        temp_len = int(0.9*len(set_reference))
        self._temp_set_f = Data_Set(temp_len)
        self._temp_set_g = Data_Set(len(set_reference)-temp_len)

        """ variables to store distance function and parameter """
        self._dist_function = "energy"
        self._dist_parameter = 1.0

        """ variable to store inner energies in reference set with bootstrap method """
        self._fi_bootstrap_ref = []

    def _set_distance_function(self, dist_function, dist_parameter):
        """ function to set distance function and parameter of comparator
         Attributes:
             dist_function (str): 'energy', 'log', 'exp' distance function
             dist_parameter (float): parameter
         """
        self._dist_function = dist_function
        self._dist_parameter = dist_parameter

    def compute_fi(self, set_f, set_g):
        """ function to compute energy between two data sets """
        function_R = {"energy": lambda arr, par: np.divide(par, arr),
                      "log": lambda arr, par: -np.log([x+par for x in arr]),
                      "exp": lambda arr, par: np.exp(-np.divide(np.square(arr), 2*par**2))}

        N = len(set_f)
        M = len(set_g)

        """ Dimensions of samples can be different physical quantities or there may be correlations between them.
        In case of euclidean metric these correlations can influence on test results. 
        For these reasons I have used Mahalanobis metric. """
        dist_inner_f = dist.pdist(set_f(), 'mahalanobis')
        dist_between_f_g = dist.cdist(set_f(), set_g(), 'mahalanobis')
        dist_inner_g = dist.pdist(set_g(), 'mahalanobis')

        p1 = 1/(N*(N-1)) * np.sum(function_R[self._dist_function](dist_inner_f, self._dist_parameter))
        p2 = 1/(N*M) * np.sum(function_R[self._dist_function](dist_between_f_g, self._dist_parameter))
        p3 = 1/(M*(M-1)) * np.sum(function_R[self._dist_function](dist_inner_g, self._dist_parameter))

        return p1 - p2 + p3

    def generate_bootstrap_fi(self, n=1000, dist_function=None, dist_parameter=None):
        """ Function to computing distribution of inner energy in reference set with bootstrap method
        Attributes:
            n (int): number of permutations
            dist_function[optional] (str): change of distance function if needed
            dist_parameter[optional] (float): change of distance function parameter if needed
        """
        if dist_function and dist_parameter:
            self._set_distance_function(dist_function, dist_parameter)

        # print("Calculating: ", end="")

        for i in range(n):
            permutation = np.array(self._set_ref())
            np.random.shuffle(permutation)

            self._temp_set_f.load_values(permutation[:len(self._temp_set_f), :])
            self._temp_set_g.load_values(permutation[len(self._temp_set_f):, :])

            self._fi_bootstrap_ref.append(
                self.compute_fi(self._temp_set_f, self._temp_set_g)
            )

            # if 100*i/n % 5 == 0:
            #     print("{:02.1f}%".format(100*i/n))
        return self._fi_bootstrap_ref

    def compare_distributions(self, n=1000, dist_function=None, dist_parameter=None):
        """ Function comparing data sets
        Attributes:
            n[optional] (int): number of permutations, needed if distribution of inner energy
                               in reference set is not computed yet
            dist_function[optional] (str): change of distance function if needed
            dist_parameter[optional] (float): change of distance function parameter if needed
        """
        if dist_function and dist_parameter:
            self._set_distance_function(dist_function, dist_parameter)

        if len(self._fi_bootstrap_ref) == 0:
            self.generate_bootstrap_fi(n)

        fi_AB = self.compute_fi(self._set_ref, self._set_exp)
        return fi_AB
