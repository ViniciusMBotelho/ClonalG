import numpy as np
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist

class ClonalG:
    """
    Motor do Algoritmo de Seleção Clonal (ClonalG) aplicado ao Agrupamento de Dados.
    """
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
    ):
        """
        :param n_antibodies: N - Quantidade de anticorpos na população.
        :param k: Número inicial de clusters usado nesta execução.
        :param k_min: Menor número de clusters permitido pela mutação estrutural.
        :param k_max: Maior número de clusters permitido pela mutação estrutural.
        :param rho: Parâmetro de decaimento da mutação exponencial.
        :param beta: Fator de controle da clonagem.
        :param replace_rate: Proporção de anticorpos Abr substituídos por novos.
        :param selection_rate: Proporção da memória Abm usada para clonagem.
        :param memory_rate: Proporção da população total preservada explicitamente como memória Abm.
        :param silhouette_sample_size: Tamanho da amostra usada apenas no histórico de Silhouette; None usa todos os dados.
        """
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
        """Inicializa Abm e Abr com anticorpos de k inicial."""
        n_samples = data.shape[0]
        antibodies = []
        for _ in range(self.n_antibodies):
            indices = np.random.choice(n_samples, self.k, replace=False)
            antibodies.append(data[indices].copy())
        affinities, _ = self._calculate_affinity(data, antibodies)
        self._select_memory_and_population(antibodies, affinities)

    def _calculate_affinity(self, data, population):
        """
        Calcula a afinidade interna por distância Euclidiana.

        Cada anticorpo representa k centroides. A afinidade é o negativo da
        distância média das amostras ao centroide mais próximo, mantendo a
        convenção de que valores maiores são melhores.
        """
        raw_scores = []
        for antibody in population:
            distances = cdist(data, antibody, metric='euclidean')
            nearest_distances = np.min(distances, axis=1)
            raw_scores.append(-float(np.mean(nearest_distances)))
        
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

    def _select_memory_and_population(self, candidates, affinities):
        order = np.argsort(affinities)[::-1]
        ordered_candidates = [candidates[idx] for idx in order]
        ordered_affinities = affinities[order]
        n_memory = self._memory_size()

        self.memory = ordered_candidates[:n_memory]
        self.memory_affinities = ordered_affinities[:n_memory]
        self.population = ordered_candidates[n_memory:self.n_antibodies]
        self.population_affinities = ordered_affinities[n_memory:self.n_antibodies]
        self.affinities = ordered_affinities[:self.n_antibodies]

    def _clone_and_mutate(self, population, affinities_norm, data):
        """
        Proliferação e Hipermutação Somática.

        A mutação altera as posições dos centroides e pode adicionar/remover
        centroides dentro dos limites k_min e k_max.
        """
        new_clones = []
        n_samples = data.shape[0]
        
        for i, antibody in enumerate(population):
            num_clones = int(self.beta * affinities_norm[i]) + 1
            alpha = np.exp(-self.rho * affinities_norm[i])
            
            for _ in range(num_clones):
                clone = antibody.copy()
                
                # 1. Mutação nos valores (posição dos centroides)
                noise = np.random.normal(0, alpha, size=clone.shape)
                clone += noise

                if np.random.rand() < alpha:
                    op = np.random.choice(['add', 'remove', 'keep'])
                    if op == 'add' and len(clone) < self.k_max:
                        new_idx = np.random.choice(n_samples)
                        clone = np.vstack([clone, data[new_idx]])
                    elif op == 'remove' and len(clone) > self.k_min:
                        remove_idx = np.random.choice(len(clone))
                        clone = np.delete(clone, remove_idx, axis=0)

                new_clones.append(clone)
        return new_clones

    def fit(self, data, n_iterations=50, verbose=True):
        """Executa o ciclo de treinamento do SIA."""
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
            
            # Reposição de Abr (diversidade), sem sobrescrever Abm diretamente.
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
            best_silhouette = self._calculate_silhouette(data, self.memory[0])
            history.append(best_silhouette)
            
            if verbose and (it % 10 == 0 or it == n_iterations - 1):
                print(
                    f"Geração {it}: Silhouette = {best_silhouette:.4f} "
                    f"| afinidade euclidiana = {best_affinity:.4f} (k={len(self.memory[0])})"
                )
                
        return self.memory[0], history

    def predict(self, data, best_antibody):
        distances = cdist(data, best_antibody, metric='euclidean')
        return np.argmin(distances, axis=1)
