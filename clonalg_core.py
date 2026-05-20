import numpy as np
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist

class ClonalG:
    """
    Motor do Algoritmo de Seleção Clonal (ClonalG) aplicado ao Agrupamento de Dados.
    """
    def __init__(self, n_antibodies=10, k_range=(2, 10), rho=2.0, beta=10, replace_rate=0.1, selection_rate=1.0, silhouette_sample_size=300):
        """
        :param n_antibodies: N - Quantidade de anticorpos na população.
        :param k_range: (min_k, max_k) - Faixa de busca para o número de clusters.
        :param rho: Parâmetro de decaimento da mutação exponencial.
        :param beta: Fator de controle da clonagem.
        :param replace_rate: Proporção de indivíduos piores substituídos por novos.
        :param selection_rate: Proporção dos melhores anticorpos usados para clonagem.
        :param silhouette_sample_size: Tamanho da amostra usada na afinidade interna; None usa todos os dados.
        """
        self.n_antibodies = n_antibodies
        self.k_min, self.k_max = k_range
        self.rho = rho
        self.beta = beta
        self.replace_rate = replace_rate
        self.selection_rate = selection_rate
        self.silhouette_sample_size = silhouette_sample_size
        self.population = None # Agora será uma lista de arrays, pois k varia
        self.affinities = None

    def _initialize_population(self, data):
        """Inicializa a população com anticorpos tendo k aleatórios dentro da faixa."""
        n_samples, n_features = data.shape
        self.population = []
        for _ in range(self.n_antibodies):
            k = np.random.randint(self.k_min, self.k_max + 1)
            indices = np.random.choice(n_samples, k, replace=False)
            self.population.append(data[indices].copy())

    def _calculate_affinity(self, data, population):
        """
        Calcula a afinidade (af) baseada no Índice Silhouette.
        """
        raw_scores = []
        for antibody in population:
            # Garante que temos pelo menos 2 clusters e no máximo n_samples - 1 para o Silhouette
            k = len(antibody)
            if k < 2:
                raw_scores.append(-1.0)
                continue
                
            distances = cdist(data, antibody, metric='euclidean')
            labels = np.argmin(distances, axis=1)
            
            if len(np.unique(labels)) < 2:
                raw_scores.append(-1.0)
                continue
            
            try:
                sample_size = None
                if self.silhouette_sample_size is not None and len(data) > self.silhouette_sample_size:
                    sample_size = self.silhouette_sample_size
                score = silhouette_score(data, labels, sample_size=sample_size, random_state=42)
                raw_scores.append(score)
            except:
                raw_scores.append(-1.0)
        
        raw_scores = np.array(raw_scores)
        
        min_s, max_s = np.min(raw_scores), np.max(raw_scores)
        if max_s == min_s:
            af_norm = np.zeros_like(raw_scores)
        else:
            af_norm = (raw_scores - min_s) / (max_s - min_s + 1e-8)
            
        return raw_scores, af_norm

    def _clone_and_mutate(self, population, affinities_norm, data):
        """
        Proliferação e Hipermutação Somática.
        Inclui mutação estrutural (adicionar/remover centroides).
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
                
                # 2. Mutação estrutural (mudar o k)
                # Chance de mudar k inversamente proporcional à afinidade
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
            affinities, af_norm = self._calculate_affinity(data, self.population)
            pop_order = np.argsort(affinities)[::-1]
            n_selected = max(1, int(np.ceil(self.n_antibodies * self.selection_rate)))
            n_selected = min(n_selected, self.n_antibodies)
            selected_idx = pop_order[:n_selected]
            selected_pop = [self.population[idx] for idx in selected_idx]
            selected_af_norm = af_norm[selected_idx]

            clones = self._clone_and_mutate(selected_pop, selected_af_norm, data)
            clones_affinities, _ = self._calculate_affinity(data, clones)
            
            # Combina populações (listas de arrays)
            combined_pop = self.population + clones
            combined_aff = np.concatenate((affinities, clones_affinities))
            
            indices_sorted = np.argsort(combined_aff)[::-1]
            
            # Seleciona os melhores para manter a memória populacional
            self.population = [combined_pop[idx] for idx in indices_sorted[:self.n_antibodies]]
            self.affinities = combined_aff[indices_sorted[:self.n_antibodies]]
            
            # Reposição (Diversidade)
            n_replace = int(self.n_antibodies * self.replace_rate)
            if n_replace > 0:
                n_samples = data.shape[0]
                for i in range(1, n_replace + 1):
                    k = np.random.randint(self.k_min, self.k_max + 1)
                    indices = np.random.choice(n_samples, k, replace=False)
                    self.population[-i] = data[indices].copy()
            
            best_score = np.max(self.affinities)
            history.append(best_score)
            
            if verbose and (it % 10 == 0 or it == n_iterations - 1):
                best_k = len(self.population[0])
                print(f"Geração {it}: Melhor Silhouette = {best_score:.4f} (k={best_k})")
                
        return self.population[0], history

    def predict(self, data, best_antibody):
        distances = cdist(data, best_antibody, metric='euclidean')
        return np.argmin(distances, axis=1)
