"""
Implementação do algoritmo Hill Climbing para o problema das 8 Rainhas (versão para benchmark).
"""
import random
import time
import tracemalloc

NUM_RAINHAS = 8

def contar_conflitos(solucao):
    """Calcula o número de conflitos entre rainhas."""
    if not solucao or len(solucao) != NUM_RAINHAS: # Adiciona verificação para evitar erros com soluções incompletas
        return float('inf') # Retorna infinito se a solução for inválida/incompleta
    conflitos = 0
    for i in range(NUM_RAINHAS):
        for j in range(i + 1, NUM_RAINHAS):
            if solucao[i] == solucao[j] or abs(solucao[i] - solucao[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def hill_climbing_single_run():
    """Executa uma única tentativa de Hill Climbing para encontrar uma solução."""
    tracemalloc.start()
    start_time = time.perf_counter()
    
    estado_atual = [random.randint(0, NUM_RAINHAS - 1) for _ in range(NUM_RAINHAS)]
    conflitos_avaliados = 0

    max_iter_sem_melhora = 50 # Para evitar ficar preso em platôs muito longos
    iter_sem_melhora_count = 0

    while True:
        conflitos_atuais = contar_conflitos(estado_atual)
        conflitos_avaliados +=1
        
        if conflitos_atuais == 0:
            break 

        melhor_vizinho = list(estado_atual)
        melhores_conflitos_vizinho = conflitos_atuais

        # Explora vizinhos
        for coluna_idx in range(NUM_RAINHAS):
            posicao_original_na_coluna = estado_atual[coluna_idx]
            for nova_linha in range(NUM_RAINHAS):
                if nova_linha == posicao_original_na_coluna:
                    continue
                
                estado_atual[coluna_idx] = nova_linha
                novos_conflitos = contar_conflitos(estado_atual)
                conflitos_avaliados +=1
                
                if novos_conflitos < melhores_conflitos_vizinho:
                    melhores_conflitos_vizinho = novos_conflitos
                    melhor_vizinho = list(estado_atual)
            
            estado_atual[coluna_idx] = posicao_original_na_coluna # Restaura

        if melhores_conflitos_vizinho >= conflitos_atuais:
            iter_sem_melhora_count += 1
            if iter_sem_melhora_count > max_iter_sem_melhora:
                 # Preso em ótimo local ou platô por muitas iterações
                break
            # Se não houve melhora, mas ainda não atingiu o limite, pode tentar perturbar ou reiniciar
            # Para este benchmark, vamos apenas continuar e ver se sai do platô ou atinge o limite
            # Se for um platô e houver movimentos laterais que não pioram, ele pode continuar explorando.
            # Se for um ótimo local, ele vai parar aqui na próxima checagem de `melhores_conflitos_vizinho >= conflitos_atuais`
            # Para simplificar, se não melhora, consideramos que pode ficar preso.
            if melhores_conflitos_vizinho == conflitos_atuais: # Movimento lateral ou platô
                 # Tenta um movimento aleatório para escapar de platôs simples
                 col_perturbar = random.randint(0, NUM_RAINHAS -1)
                 nova_pos_perturbar = random.randint(0, NUM_RAINHAS -1)
                 estado_atual[col_perturbar] = nova_pos_perturbar
            else: # Ótimo local
                break
        else:
            estado_atual = melhor_vizinho
            iter_sem_melhora_count = 0 # Reset contador se houve melhora
            
    end_time = time.perf_counter()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time
    memory_used_peak = peak_mem / 1024  # KB
    
    is_solution = (contar_conflitos(estado_atual) == 0)
    return estado_atual if is_solution else None, execution_time, memory_used_peak, conflitos_avaliados, is_solution

def get_hill_climbing_metrics(num_runs=100): # Hill climbing pode falhar, então mais runs
    times, mems, costs = [], [], []
    solutions_found = 0
    solution_example = None

    for _ in range(num_runs):
        solution, time_val, mem_val, cost_val, found = hill_climbing_single_run()
        if found:
            if solution_example is None: solution_example = solution
            times.append(time_val)
            mems.append(mem_val)
            costs.append(cost_val)
            solutions_found += 1
    
    avg_time = sum(times) / len(times) if times else 0
    avg_mem = sum(mems) / len(mems) if mems else 0
    avg_cost = sum(costs) / len(costs) if costs else 0
    success_rate = solutions_found / num_runs if num_runs > 0 else 0
            
    return {
        "find_one": {
            "avg_time_s": avg_time,
            "avg_mem_peak_kb": avg_mem,
            "avg_cost_conflict_evals": avg_cost,
            "success_rate": success_rate,
            "solutions_found_count": solutions_found,
            "solution_example": solution_example
        }
    }

if __name__ == '__main__':
    metrics_hc = get_hill_climbing_metrics(num_runs=20)
    print("Hill Climbing Metrics (Find One):")
    print(f"  Avg Time (successful runs): {metrics_hc['find_one']['avg_time_s']:.6f} s")
    print(f"  Avg Peak Memory (successful runs): {metrics_hc['find_one']['avg_mem_peak_kb']:.2f} KB")
    print(f"  Avg Cost (Conflict Evaluations for successful runs): {metrics_hc['find_one']['avg_cost_conflict_evals']:.2f}")
    print(f"  Success Rate: {metrics_hc['find_one']['success_rate']:.2%}")
    print(f"  Solutions Found: {metrics_hc['find_one']['solutions_found_count']}")
    if metrics_hc['find_one']['solution_example']:
        print(f"  Solution Example: {metrics_hc['find_one']['solution_example']}")

