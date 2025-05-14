"""
Implementação do algoritmo Random Restart para o problema das 8 Rainhas (versão para benchmark).
"""
import random
import time
import tracemalloc

NUM_RAINHAS = 8

def eh_valida(solucao):
    """Verifica se uma solução é válida (nenhuma rainha se ataca)."""
    if not solucao or len(solucao) != NUM_RAINHAS:
        return False
    for i in range(NUM_RAINHAS):
        for j in range(i + 1, NUM_RAINHAS):
            if solucao[i] == solucao[j] or abs(solucao[i] - solucao[j]) == abs(i - j):
                return False
    return True

def gerar_solucao_aleatoria():
    """Gera uma permutação aleatória das posições das rainhas."""
    solucao = list(range(NUM_RAINHAS))
    random.shuffle(solucao)
    return solucao

def random_restart_single_run():
    """Executa uma única tentativa de Random Restart para encontrar uma solução."""
    tracemalloc.start()
    start_time = time.perf_counter()
    
    tentativas = 0 
    solucao_encontrada = None
    max_tentativas = 200000 # Limite de segurança para 8-rainhas, geralmente encontra bem antes

    while tentativas < max_tentativas:
        tentativas += 1
        solucao_atual = gerar_solucao_aleatoria()
        if eh_valida(solucao_atual):
            solucao_encontrada = solucao_atual
            break
            
    end_time = time.perf_counter()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time
    memory_used_peak = peak_mem / 1024  # KB
    
    return solucao_encontrada, execution_time, memory_used_peak, tentativas, (solucao_encontrada is not None)

def get_random_restart_metrics(num_runs=100): # Random Restart pode ter variabilidade
    times, mems, costs = [], [], []
    solutions_found_count = 0
    solution_example = None

    for i in range(num_runs):
        solucao, tempo, memoria, custo, found = random_restart_single_run()
        # print(f"Run {i+1}: Found: {found}, Time: {tempo:.4f}s, Mem: {memoria:.2f}KB, Attempts: {custo}")
        if found:
            if solution_example is None: solution_example = solucao
            times.append(tempo)
            mems.append(memoria)
            costs.append(custo)
            solutions_found_count += 1
    
    avg_time = sum(times) / len(times) if times else 0
    avg_mem = sum(mems) / len(mems) if mems else 0
    avg_cost = sum(costs) / len(costs) if costs else 0
    success_rate = solutions_found_count / num_runs if num_runs > 0 else 0
            
    return {
        "find_one": {
            "avg_time_s": avg_time,
            "avg_mem_peak_kb": avg_mem,
            "avg_cost_attempts": avg_cost,
            "success_rate": success_rate,
            "solutions_found_count": solutions_found_count,
            "solution_example": solution_example
        }
    }

if __name__ == '__main__':
    metrics_rr = get_random_restart_metrics(num_runs=20) # Menos runs para teste rápido no main
    print("Random Restart Metrics (Find One):")
    # Correção: Usar aspas simples para o f-string ou variáveis intermediárias
    avg_time_s = metrics_rr['find_one']['avg_time_s']
    avg_mem_peak_kb = metrics_rr['find_one']['avg_mem_peak_kb']
    avg_cost_attempts = metrics_rr['find_one']['avg_cost_attempts']
    success_rate = metrics_rr['find_one']['success_rate']
    solutions_found_count = metrics_rr['find_one']['solutions_found_count']
    solution_example = metrics_rr['find_one']['solution_example']

    print(f'  Avg Time (successful runs): {avg_time_s:.6f} s')
    print(f'  Avg Peak Memory (successful runs): {avg_mem_peak_kb:.2f} KB')
    print(f'  Avg Cost (Attempts for successful runs): {avg_cost_attempts:.2f}')
    print(f'  Success Rate: {success_rate:.2%}')
    print(f'  Solutions Found: {solutions_found_count}')
    if solution_example:
        print(f'  Solution Example: {solution_example}')

