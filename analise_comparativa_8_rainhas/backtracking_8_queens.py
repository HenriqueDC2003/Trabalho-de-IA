"""
Implementação do algoritmo de Backtracking para o problema das 8 Rainhas.
"""

import time
import tracemalloc # Para medição de memória

class EightQueensBacktracking:
    def __init__(self, n=8):
        self.n = n
        self.solutions = []
        self.board = [-1] * n # board[col] = linha da rainha na coluna col
        self.nodes_visited = 0 # Custo computacional

    def is_safe(self, row, col):
        """Verifica se é seguro colocar uma rainha em board[col] = row."""
        for prev_col in range(col):
            prev_row = self.board[prev_col]
            if prev_row == row or \
               abs(prev_row - row) == abs(prev_col - col):
                return False
        return True

    def solve_nq_util(self, col, find_all=False):
        """Função utilitária recursiva para resolver o problema."""
        self.nodes_visited += 1
        if col >= self.n:
            self.solutions.append(list(self.board))
            return True # Retorna True se uma solução foi encontrada

        res = False
        for i in range(self.n):
            if self.is_safe(i, col):
                self.board[col] = i
                # Recorre para colocar o resto das rainhas
                if self.solve_nq_util(col + 1, find_all):
                    if not find_all:
                        return True # Retorna se apenas uma solução é necessária
                    res = True # Marca que uma solução foi encontrada, continua para outras
                self.board[col] = -1 # Backtrack
        return res

    def find_one_solution(self):
        """Encontra a primeira solução válida."""
        self.solutions = []
        self.board = [-1] * self.n
        self.nodes_visited = 0
        tracemalloc.start()
        start_time = time.perf_counter()

        self.solve_nq_util(0, find_all=False)

        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        execution_time = end_time - start_time
        memory_used_peak = peak / 1024  # Convertendo para KB

        if self.solutions:
            return self.solutions[0], execution_time, memory_used_peak, self.nodes_visited
        return None, execution_time, memory_used_peak, self.nodes_visited

    def find_all_solutions(self):
        """Encontra todas as 92 soluções."""
        self.solutions = []
        self.board = [-1] * self.n
        self.nodes_visited = 0
        tracemalloc.start()
        start_time = time.perf_counter()

        self.solve_nq_util(0, find_all=True)

        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        execution_time = end_time - start_time
        memory_used_peak = peak / 1024  # Convertendo para KB

        return self.solutions, execution_time, memory_used_peak, self.nodes_visited

def get_backtracking_metrics(num_runs=5):
    solver_bt = EightQueensBacktracking()
    
    # Metrics for finding one solution
    times_one, mems_one, costs_one = [], [], []
    solution_example_one = None
    for _ in range(num_runs):
        solution, time_val, mem_val, cost_val = solver_bt.find_one_solution()
        if solution:
            if solution_example_one is None: solution_example_one = solution
            times_one.append(time_val)
            mems_one.append(mem_val)
            costs_one.append(cost_val)
    
    avg_time_one = sum(times_one) / len(times_one) if times_one else 0
    avg_mem_one = sum(mems_one) / len(mems_one) if mems_one else 0
    avg_cost_one = sum(costs_one) / len(costs_one) if costs_one else 0

    # Metrics for finding all solutions
    times_all, mems_all, costs_all = [], [], []
    solutions_count_example = 0
    for _ in range(num_runs):
        solutions, time_val, mem_val, cost_val = solver_bt.find_all_solutions()
        if solutions:
            if solutions_count_example == 0: solutions_count_example = len(solutions)
            times_all.append(time_val)
            mems_all.append(mem_val)
            costs_all.append(cost_val)

    avg_time_all = sum(times_all) / len(times_all) if times_all else 0
    avg_mem_all = sum(mems_all) / len(mems_all) if mems_all else 0
    avg_cost_all = sum(costs_all) / len(costs_all) if costs_all else 0
            
    return {
        "find_one": {
            "avg_time_s": avg_time_one,
            "avg_mem_peak_kb": avg_mem_one,
            "avg_cost_nodes": avg_cost_one,
            "solution_example": solution_example_one
        },
        "find_all": {
            "avg_time_s": avg_time_all,
            "avg_mem_peak_kb": avg_mem_all,
            "avg_cost_nodes": avg_cost_all,
            "solutions_count": solutions_count_example
        }
    }

if __name__ == '__main__':
    metrics = get_backtracking_metrics(num_runs=5)
    print("Backtracking Metrics (Find One):")
    print(f"  Avg Time: {metrics['find_one']['avg_time_s']:.6f} s")
    print(f"  Avg Peak Memory: {metrics['find_one']['avg_mem_peak_kb']:.2f} KB")
    print(f"  Avg Cost (Nodes Visited): {metrics['find_one']['avg_cost_nodes']:.2f}")
    print(f"  Solution Example: {metrics['find_one']['solution_example']}")
    print("\nBacktracking Metrics (Find All):")
    print(f"  Avg Time: {metrics['find_all']['avg_time_s']:.6f} s")
    print(f"  Avg Peak Memory: {metrics['find_all']['avg_mem_peak_kb']:.2f} KB")
    print(f"  Avg Cost (Nodes Visited): {metrics['find_all']['avg_cost_nodes']:.2f}")
    print(f"  Solutions Count: {metrics['find_all']['solutions_count']}")

