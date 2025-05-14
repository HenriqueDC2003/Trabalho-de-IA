"""
Script principal para executar os benchmarks dos algoritmos para o problema das 8 Rainhas
e coletar/consolidar as métricas de desempenho.
"""
import json
import backtracking_8_queens
import hill_climbing_benchmark
import random_restart_benchmark

NUM_RUNS_BT = 5
NUM_RUNS_HC = 100  # Hill Climbing pode falhar, precisa de mais execuções
NUM_RUNS_RR = 100  # Random Restart é estocástico

def run_all_benchmarks():
    """Executa todos os benchmarks e retorna um dicionário com os resultados."""
    all_metrics = {}

    print(f"Executando Backtracking benchmark ({NUM_RUNS_BT} execuções)...")
    metrics_bt = backtracking_8_queens.get_backtracking_metrics(num_runs=NUM_RUNS_BT)
    all_metrics["backtracking"] = metrics_bt
    print("Backtracking benchmark concluído.")

    print(f"\nExecutando Hill Climbing benchmark ({NUM_RUNS_HC} execuções)...")
    metrics_hc = hill_climbing_benchmark.get_hill_climbing_metrics(num_runs=NUM_RUNS_HC)
    all_metrics["hill_climbing"] = metrics_hc
    print("Hill Climbing benchmark concluído.")

    print(f"\nExecutando Random Restart benchmark ({NUM_RUNS_RR} execuções)...")
    metrics_rr = random_restart_benchmark.get_random_restart_metrics(num_runs=NUM_RUNS_RR)
    all_metrics["random_restart"] = metrics_rr
    print("Random Restart benchmark concluído.")

    return all_metrics

if __name__ == "__main__":
    print("Iniciando a coleta de métricas de benchmark para os algoritmos das 8 Rainhas...")
    
    collected_metrics = run_all_benchmarks()
    
    # Salvar as métricas em um arquivo JSON para uso posterior (gráficos, relatório)
    output_file = "/home/ubuntu/benchmark_metrics.json"
    try:
        with open(output_file, "w") as f:
            json.dump(collected_metrics, f, indent=4)
        print(f"\nMétricas de benchmark salvas em: {output_file}")
    except Exception as e:
        print(f"\nErro ao salvar métricas em JSON: {e}")

    # Imprimir um resumo das métricas coletadas
    print("\n--- Resumo das Métricas Coletadas ---")
    for algo_name, metrics in collected_metrics.items():
        print(f"\nAlgoritmo: {algo_name.replace('_', ' ').title()}")
        if "find_one" in metrics:
            print("  Métricas para encontrar UMA solução:")
            for key, value in metrics["find_one"].items():
                if isinstance(value, float):
                    print(f"    {key}: {value:.4f}")
                else:
                    print(f"    {key}: {value}")
        if "find_all" in metrics: # Apenas para Backtracking
            print("  Métricas para encontrar TODAS as soluções:")
            for key, value in metrics["find_all"].items():
                if isinstance(value, float):
                    print(f"    {key}: {value:.4f}")
                else:
                    print(f"    {key}: {value}")
    print("\nColeta de métricas finalizada.")

