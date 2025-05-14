"""
Script para gerar gráficos comparativos do desempenho dos algoritmos para o problema das 8 Rainhas,
utilizando Matplotlib e os dados do arquivo benchmark_metrics.json.
"""
import json
import matplotlib.pyplot as plt
import numpy as np

def load_metrics(filepath="/home/ubuntu/benchmark_metrics.json"):
    """Carrega as métricas do arquivo JSON."""
    try:
        with open(filepath, "r") as f:
            metrics = json.load(f)
        return metrics
    except FileNotFoundError:
        print(f"Erro: Arquivo de métricas não encontrado em {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar o JSON do arquivo {filepath}")
        return None

def plot_comparison_charts(metrics, output_dir="/home/ubuntu/"):
    """Gera e salva os gráficos comparativos."""
    if not metrics:
        print("Nenhuma métrica para plotar.")
        return

    labels = []
    times_one_solution = []
    mems_one_solution = []
    costs_one_solution = [] # Custo normalizado ou interpretado
    cost_labels = []

    # Coletar dados para "encontrar uma solução"
    if "backtracking" in metrics and "find_one" in metrics["backtracking"]:
        labels.append("Backtracking")
        times_one_solution.append(metrics["backtracking"]["find_one"]["avg_time_s"])
        mems_one_solution.append(metrics["backtracking"]["find_one"]["avg_mem_peak_kb"])
        costs_one_solution.append(metrics["backtracking"]["find_one"]["avg_cost_nodes"])
        cost_labels.append("Nós Visitados (Backtracking)")
        
    if "hill_climbing" in metrics and "find_one" in metrics["hill_climbing"]:
        # Apenas se successful_rate > 0
        if metrics["hill_climbing"]["find_one"].get("success_rate", 0) > 0:
            labels.append("Hill Climbing")
            times_one_solution.append(metrics["hill_climbing"]["find_one"]["avg_time_s"])
            mems_one_solution.append(metrics["hill_climbing"]["find_one"]["avg_mem_peak_kb"])
            costs_one_solution.append(metrics["hill_climbing"]["find_one"]["avg_cost_conflict_evals"])
            cost_labels.append("Avaliações de Conflito (Hill Climbing)")
        else:
            print("Hill Climbing não encontrou soluções, não será incluído nos gráficos de 'uma solução'.")

    if "random_restart" in metrics and "find_one" in metrics["random_restart"]:
        if metrics["random_restart"]["find_one"].get("success_rate", 0) > 0:
            labels.append("Random Restart")
            times_one_solution.append(metrics["random_restart"]["find_one"]["avg_time_s"])
            mems_one_solution.append(metrics["random_restart"]["find_one"]["avg_mem_peak_kb"])
            costs_one_solution.append(metrics["random_restart"]["find_one"]["avg_cost_attempts"])
            cost_labels.append("Tentativas (Random Restart)")
        else:
            print("Random Restart não encontrou soluções, não será incluído nos gráficos de 'uma solução'.")

    # Gráfico 1: Tempo para encontrar UMA solução
    if times_one_solution:
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, times_one_solution, color=["skyblue", "lightcoral", "lightgreen"])
        plt.ylabel("Tempo Médio (segundos) - Escala Logarítmica")
        plt.title("Comparativo: Tempo Médio para Encontrar UMA Solução Válida")
        plt.yscale("log") # Usar escala logarítmica devido a grandes variações
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, f"{yval:.6f}s", va="bottom", ha="center")
        plt.savefig(f"{output_dir}comparativo_tempo_uma_solucao.png")
        plt.close()
        print(f"Gráfico 'comparativo_tempo_uma_solucao.png' salvo em {output_dir}")

    # Gráfico 2: Custo de Memória para UMA solução
    if mems_one_solution:
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, mems_one_solution, color=["skyblue", "lightcoral", "lightgreen"])
        plt.ylabel("Pico Médio de Memória (KB)")
        plt.title("Comparativo: Pico Médio de Memória para Encontrar UMA Solução")
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, f"{yval:.2f} KB", va="bottom", ha="center")
        plt.savefig(f"{output_dir}comparativo_memoria_uma_solucao.png")
        plt.close()
        print(f"Gráfico 'comparativo_memoria_uma_solucao.png' salvo em {output_dir}")

    # Gráfico 3: Custo Computacional para UMA solução
    # Como as métricas de custo são diferentes, plotaremos separadamente ou em subplots se necessário.
    # Por simplicidade, vamos criar gráficos individuais para cada tipo de custo se as unidades forem muito diferentes.
    # Ou um gráfico de barras agrupadas se forem comparáveis de alguma forma (aqui são diferentes)
    # Vamos fazer um gráfico com barras para cada um, mas o eixo Y terá descrições diferentes.
    # Para este caso, é melhor apresentar os dados em uma tabela no relatório e talvez um gráfico para cada.
    # Vamos criar um gráfico de barras para cada um dos custos, pois são unidades diferentes.
    
    for i in range(len(labels)):
        if i < len(costs_one_solution):
            plt.figure(figsize=(6, 4))
            plt.bar([labels[i]], [costs_one_solution[i]], color=["skyblue", "lightcoral", "lightgreen"][i])
            plt.ylabel(cost_labels[i].split(" (")[0]) # Pega só a unidade principal
            plt.title(f"Custo Computacional: {labels[i]}")
            plt.text(0, costs_one_solution[i], f"{costs_one_solution[i]:.0f}", va="bottom", ha="center")
            plt.savefig(f"{output_dir}comparativo_custo_{labels[i].lower().replace(' ', '_')}.png")
            plt.close()
            print(f"Gráfico 'comparativo_custo_{labels[i].lower().replace(' ', '_')}.png' salvo em {output_dir}")

    # Gráfico 4: Tempo para encontrar TODAS as 92 soluções (apenas Backtracking)
    if "backtracking" in metrics and "find_all" in metrics["backtracking"]:
        bt_time_all = metrics["backtracking"]["find_all"]["avg_time_s"]
        bt_mem_all = metrics["backtracking"]["find_all"]["avg_mem_peak_kb"]
        bt_cost_all = metrics["backtracking"]["find_all"]["avg_cost_nodes"]
        bt_solutions_count = metrics["backtracking"]["find_all"]["solutions_count"]

        plt.figure(figsize=(8, 5))
        plt.bar(["Backtracking"], [bt_time_all], color="gold")
        plt.ylabel("Tempo Médio (segundos)")
        plt.title(f"Backtracking: Tempo para Encontrar TODAS as {bt_solutions_count} Soluções")
        plt.text(0, bt_time_all, f"{bt_time_all:.4f}s", va="bottom", ha="center")
        plt.savefig(f"{output_dir}backtracking_tempo_todas_solucoes.png")
        plt.close()
        print(f"Gráfico 'backtracking_tempo_todas_solucoes.png' salvo em {output_dir}")

        # Poderia adicionar gráficos para memória e custo de todas as soluções do BT também
        plt.figure(figsize=(8, 5))
        plt.bar(["Backtracking"], [bt_mem_all], color="gold")
        plt.ylabel("Pico Médio de Memória (KB)")
        plt.title(f"Backtracking: Memória para Encontrar TODAS as {bt_solutions_count} Soluções")
        plt.text(0, bt_mem_all, f"{bt_mem_all:.2f} KB", va="bottom", ha="center")
        plt.savefig(f"{output_dir}backtracking_memoria_todas_solucoes.png")
        plt.close()
        print(f"Gráfico 'backtracking_memoria_todas_solucoes.png' salvo em {output_dir}")

        plt.figure(figsize=(8, 5))
        plt.bar(["Backtracking"], [bt_cost_all], color="gold")
        plt.ylabel("Nós Visitados")
        plt.title(f"Backtracking: Custo para Encontrar TODAS as {bt_solutions_count} Soluções")
        plt.text(0, bt_cost_all, f"{bt_cost_all:.0f}", va="bottom", ha="center")
        plt.savefig(f"{output_dir}backtracking_custo_todas_solucoes.png")
        plt.close()
        print(f"Gráfico 'backtracking_custo_todas_solucoes.png' salvo em {output_dir}")

    print("Geração de gráficos concluída.")

if __name__ == "__main__":
    metrics_data = load_metrics()
    if metrics_data:
        plot_comparison_charts(metrics_data)

