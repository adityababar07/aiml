class Holder:
    def __init__(self, attributes):
        self.factors = {}  # Initialize an empty dictionary
        for attr in attributes:
            self.factors[attr] = []

class CandidateElimination:

    def __init__(self, dataset, factors):

        self.num_factors = len(dataset[0][0])
        self.factors = factors
        self.attributes = list(factors.keys())
        self.dataset = dataset

    def run_algorithm(self):
        S = self.initializeS()
        G = self.initializeG()
        for trial_set in self.dataset:
            if self.is_positive(trial_set):
                G = self.remove_inconsistent_G(G, trial_set[0])
                S_new = []
                for s in S:
                    if self.consistent(s, trial_set[0]):
                        S_new.append(s)
                    else:
                        generalization = self.generalize_inconsistent_S(s, trial_set[0])
                        generalization = self.get_general(generalization, G)
                        if generalization:
                            S_new.append(generalization)
                S = self.remove_more_general(S_new)
            else:
                G_new = []
                for g in G:
                    if self.consistent(g, trial_set[0]):  # If g is consistent with the trial set
                        G_new.append(g)
                    else:
                        specializations = self.specialize_inconsistent_G(g, trial_set[0])  # Get specializations for inconsistent G
                        specializations = self.get_specific(specializations, 5)  # Get specific versions of the specializations
                        G_new.extend(specializations)  # Add the specializations to G_new
                G = self.remove_more_specific(G_new)  # Remove more specific hypotheses from G

        print("S:", S)
        print("G:", G)

    def initializeS(self):
        return [tuple(['-' for _ in range(self.num_factors)])]  # Initialize S with '-' for each factor

    def initializeG(self):
        return [tuple(["?" for _ in range(self.num_factors)])]  # Initialize G with '?' for each factor

    def is_positive(self, trial_set):
        return trial_set[1] == 'Y'  # Check if the trial set is positive ('Y')

    def remove_inconsistent_G(self, hypotheses, instance):
        G_new = hypotheses[:]  # Create a copy of the hypotheses

        for old in hypotheses:
            for new in G_new:
                if old != new and self.more_specific(new, old):  # Check if new is more specific than old
                    G_new.remove(old)  # Remove old from G_new
                    break  # Exit the loop after modification

        return G_new  # Return the modified G_new

    def generalize_inconsistent_S(self, hypothesis, instance):
        hypo = list(hypothesis)

        for i, factor in enumerate(hypo):
            if factor == '-':  # If the factor is unspecified ('-')
                hypo[i] = instance[i]  # Set it to the instance value
            elif not self.match_factor(factor, instance[i]):  # If it does not match the instance
                hypo[i] = '?'  # Generalize it to '?'

        return tuple(hypo)  # Return the generalized hypothesis

    def specialize_inconsistent_G(self, hypothesis, instance):
        specializations = []
        hypo = list(hypothesis)

        for i, factor in enumerate(hypo):
            if factor == '?':  # If the factor is '?'
                values = self.factors[self.attributes[i]]  # Get the possible values for that factor
                for j in values:
                    if instance[i] != j:  # If the value in the instance is not the same as the value
                        hyp = hypo[:]  # Copy the current hypothesis
                        hyp[i] = j  # Set the factor to the new value
                        specializations.append(tuple(hyp))  # Add the new hypothesis to the list

        return specializations  # Return all the specialized hypotheses

    def get_general(self, generalization, G):
        for g in G:
            if self.more_general(g, generalization):  # If g is more general than the generalization
                return generalization  # Return the generalization

        return None  # Return None if no more general hypotheses were found

    def get_specific(self, specializations, S):
        valid_specializations = []

        for hypo in specializations:
            for s in S:
                if self.more_specific(s, hypo) or s == self.initializeS()[0]:  # Check if the hypothesis is more specific than s
                    valid_specializations.append(hypo)  # Add it to valid specializations
                    break  # No need to check against other S hypotheses

        return valid_specializations  # Return the valid specializations
    
    def remove_more_general(self, S_new):
        for new in S_new:
            for old in S_new:
                if old != new and self.more_general(new, old):  # If old is more general than new
                    S_new.remove(new)  # Remove new
                    break  # Exit the loop after modification

        return S_new  # Return the modified S_new

    def remove_more_specific(self, G_new):
        for new in G_new[:]:
            for old in G_new:
                if old != new and self.more_specific(new, old):  # If new is more specific than old
                    G_new.remove(new)  # Remove new
                    break  # Exit the loop after modification

        return G_new  # Return the modified G_new
    def consistent(self, hypothesis, instance):
        for h, i in zip(hypothesis, instance):
            if h != '?' and h != i:  # If the hypothesis is not '?' and doesn't match the instance, return False
                return False
        return True  # Otherwise, it's consistent

    def match_factor(self, factor, value):
        return factor == value or factor == '?'  # A factor matches a value if they are equal or if the factor is '?'


    def more_general(self, hyp1, hyp2):
        for h1, h2 in zip(hyp1, hyp2):
            if h1 != '?' and (h1 != h2 and h2 != '-'):
                return False
        return True
    
    def more_specific(self, hyp1, hyp2):
        return self.more_general(hyp2, hyp1)

if __name__ == "__main__":
    attributes = ['Sky', 'Temp', 'Humidity', 'Wind', 'Water', 'Forecast']
    factors = {
        'Sky': ['sunny', 'rainy', 'cloudy'],
        'Temp': ['cold', 'warm'],
        'Humidity': ['normal', 'high'],
        'Wind': ['weak', 'strong'],
        'Water': ['warm', 'cold'],
        'Forecast': ['same', 'change']
    }
    dataset = [
        (['sunny', 'warm', 'normal', 'strong', 'warm', 'same'], 'Y'),
        (['sunny', 'warm', 'high', 'strong', 'warm', 'same'], 'Y'),
        (['rainy', 'cold', 'high', 'strong', 'warm', 'change'], 'N'),
        (['sunny', 'warm', 'high', 'strong', 'cool', 'change'], 'Y')
    ]
    holder = Holder(attributes)
    for attr, values in factors.items():
        holder.factors[attr] = values
    algorithm = CandidateElimination(dataset, holder.factors)
    algorithm.run_algorithm()