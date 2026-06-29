import numpy as np
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist

class ClonalG:
    def __init__(
        self,
        n_antibodies=10,
        k=3,
        k_min=2,
        k_max=6,
        rho=2.0,
        beta=10,
        replace_rate=0.1,
        selection_rate=1.0,
        memory_rate=0.25,
        silhouette_sample_size=None,
        parametric_mutation_scale=0.05,
        diversity_weight=0.15,
    ):
        self.n_antibodies = n_antibodies
        self.k = int(k)
        self.k_min = int(k_min)
        self.k_max = int(k_max)
        if self.k_min < 2:
            raise ValueError('k_min deve ser pelo menos 2 para permitir avaliacao por Silhouette.')
        if self.k_max < self.k_min:
            raise ValueError('k_max deve ser maior ou igual a k_min.')
        if not self.k_min <= self.k <= self.k_max:
            raise ValueError('k inicial deve estar entre k_min e k_max.')
        self.rho = rho
        self.beta = beta
        self.replace_rate = replace_rate
        self.selection_rate = selection_rate
        self.memory_rate = memory_rate
        self.silhouette_sample_size = silhouette_sample_size
        self.parametric_mutation_scale = parametric_mutation_scale
        self.diversity_weight = diversity_weight
        self.memory = None
        self.population = None
        self.affinities = None
        self.memory_affinities = None
        self.population_affinities = None

    def _memory_size(self):
        if self.n_antibodies <= 1:
            return 1
        size = int(np.ceil(self.n_antibodies * self.memory_rate))
        return min(self.n_antibodies - 1, max(1, size))

    def _initialize_population(self, data):
        n_samples = data.shape[0]
        antibodies = []
        for _ in range(self.n_antibodies):
            indices = np.random.choice(n_samples, self.k, replace=False)
            antibodies.append(data[indices].copy())
        affinities, _ = self._calculate_affinity(data, antibodies)
        self._select_memory_and_population(antibodies, affinities)

    def _calculate_affinity(self, data, population):
        raw_scores = [self._calculate_silhouette(data, antibody) for antibody in population]
        raw_scores = np.array(raw_scores)
        af_norm = self._normalize_affinities(raw_scores)
        return raw_scores, af_norm

    def _calculate_silhouette(self, data, antibody):
        labels = self.predict(data, antibody)
        if len(np.unique(labels)) < 2:
            return -1.0
        sample_size = None
        if self.silhouette_sample_size is not None and len(data) > self.silhouette_sample_size:
            sample_size = self.silhouette_sample_size
        try:
            return float(silhouette_score(data, labels, sample_size=sample_size, random_state=42))
        except ValueError:
            return -1.0

    @staticmethod
    def _normalize_affinities(raw_scores):
        min_s, max_s = np.min(raw_scores), np.max(raw_scores)
        if max_s == min_s:
            return np.zeros_like(raw_scores)
        return (raw_scores - min_s) / (max_s - min_s + 1e-8)

    @staticmethod
    def _antibody_distance(a, b):
        distances = cdist(a, b, metric='euclidean')
        return 0.5 * (np.mean(np.min(distances, axis=1)) + np.mean(np.min(distances, axis=0)))

    def _diversity_scores(self, candidates, selected_indices, remaining_indices):
        if not selected_indices:
            return np.zeros(len(remaining_indices))

        scores = []
        selected = [candidates[idx] for idx in selected_indices]
        for idx in remaining_indices:
            distances = [self._antibody_distance(candidates[idx], selected_item) for selected_item in selected]
            scores.append(min(distances))
        return self._normalize_affinities(np.array(scores))

    def _rank_with_diversity(self, candidates, affinities, limit):
        n_candidates = len(candidates)
        if n_candidates == 0:
            return []

        affinity_norm = self._normalize_affinities(affinities)
        selected = [int(np.argmax(affinities))]
        remaining = [idx for idx in range(n_candidates) if idx != selected[0]]

        while remaining and len(selected) < limit:
            diversity_norm = self._diversity_scores(candidates, selected, remaining)
            scores = affinity_norm[remaining] + self.diversity_weight * diversity_norm
            best_remaining_pos = int(np.argmax(scores))
            selected.append(remaining.pop(best_remaining_pos))

        remaining = sorted(remaining, key=lambda idx: affinities[idx], reverse=True)
        return selected + remaining

    def _select_memory_and_population(self, candidates, affinities):
        n_memory = self._memory_size()
        if self.diversity_weight > 0:
            order = np.array(self._rank_with_diversity(candidates, affinities, n_memory))
        else:
            order = np.argsort(affinities)[::-1]
        ordered_candidates = [candidates[idx] for idx in order]
        ordered_affinities = affinities[order]

        self.memory = ordered_candidates[:n_memory]
        self.memory_affinities = ordered_affinities[:n_memory]
        self.population = ordered_candidates[n_memory:self.n_antibodies]
        self.population_affinities = ordered_affinities[n_memory:self.n_antibodies]
        self.affinities = ordered_affinities[:self.n_antibodies]

    def _apply_parametric_mutation(self, clone, affinity_norm):
        if self.parametric_mutation_scale <= 0:
            return clone
        sigma = self.parametric_mutation_scale * np.exp(-self.rho * affinity_norm)
        noise = np.random.normal(loc=0.0, scale=sigma, size=clone.shape)
        return clone + noise

    def _clone_and_mutate(self, population, affinities_norm, data):
        new_clones = []
        n_samples = data.shape[0]
        
        for i, antibody in enumerate(population):
            num_clones = int(self.beta * affinities_norm[i]) + 1
            alpha = np.exp(-self.rho * affinities_norm[i])
            
            for _ in range(num_clones):
                clone = antibody.copy()

                if np.random.rand() < alpha:
                    op = np.random.choice(['add', 'remove', 'keep'])
                    if op == 'add' and len(clone) < self.k_max:
                        new_idx = np.random.choice(n_samples)
                        clone = np.vstack([clone, data[new_idx]])
                    elif op == 'remove' and len(clone) > self.k_min:
                        remove_idx = np.random.choice(len(clone))
                        clone = np.delete(clone, remove_idx, axis=0)

                clone = self._apply_parametric_mutation(clone, affinities_norm[i])
                new_clones.append(clone)
        return new_clones

    def fit(self, data, n_iterations=50, verbose=True):
        data = np.array(data)
        self._initialize_population(data)
        history = []
        
        for it in range(n_iterations):
            n_selected = max(1, int(np.ceil(len(self.memory) * self.selection_rate)))
            n_selected = min(n_selected, len(self.memory))
            selected_pop = self.memory[:n_selected]
            selected_af_norm = self._normalize_affinities(self.memory_affinities[:n_selected])

            clones = self._clone_and_mutate(selected_pop, selected_af_norm, data)
            clones_affinities, _ = self._calculate_affinity(data, clones)
            
            combined_pop = self.memory + self.population + clones
            combined_aff = np.concatenate((self.memory_affinities, self.population_affinities, clones_affinities))
            self._select_memory_and_population(combined_pop, combined_aff)
            
            n_replace = int(len(self.population) * self.replace_rate)
            if n_replace > 0:
                n_samples = data.shape[0]
                for i in range(1, n_replace + 1):
                    k = np.random.randint(self.k_min, self.k_max + 1)
                    indices = np.random.choice(n_samples, k, replace=False)
                    self.population[-i] = data[indices].copy()
                self.population_affinities, _ = self._calculate_affinity(data, self.population)
                self._select_memory_and_population(
                    self.memory + self.population,
                    np.concatenate((self.memory_affinities, self.population_affinities)),
                )
            
            best_affinity = np.max(self.affinities)
            history.append(best_affinity)

            if verbose and (it % 10 == 0 or it == n_iterations - 1):
                print(f"Geração {it}: Afinidade Silhouette = {best_affinity:.4f} (k={len(self.memory[0])})")

        return self.memory[0], history

    def predict(self, data, best_antibody):
        distances = cdist(data, best_antibody, metric='euclidean')
        return np.argmin(distances, axis=1)
