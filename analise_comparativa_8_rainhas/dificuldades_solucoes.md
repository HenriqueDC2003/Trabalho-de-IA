# Documentação de Dificuldades e Soluções

Durante o desenvolvimento e a análise comparativa dos algoritmos para o problema das 8 Rainhas, algumas dificuldades foram encontradas. Abaixo, descrevo as principais e as soluções adotadas.

## 1. Padronização das Métricas de Custo Computacional

*   **Dificuldade:** Os três algoritmos (Backtracking, Hill Climbing e Random Restart) possuem naturezas distintas, o que torna a definição de uma métrica única de "custo computacional" diretamente comparável um desafio. Por exemplo, Backtracking explora uma árvore de busca, Hill Climbing avalia vizinhanças e Random Restart gera múltiplas soluções aleatórias.
*   **Solução:** Decidiu-se por utilizar métricas de custo que fossem representativas da operação principal de cada algoritmo:
    *   **Backtracking:** Número de nós visitados na árvore de busca.
    *   **Hill Climbing:** Número de vezes que a função de avaliação de conflitos foi chamada (representando o esforço para encontrar melhores vizinhos).
    *   **Random Restart:** Número de tentativas (soluções geradas e testadas) até encontrar uma solução válida.
    No relatório, a natureza distinta dessas métricas será explicitada, e a comparação será feita com essa ressalva, focando mais na ordem de grandeza e no comportamento geral do que em uma comparação numérica direta como se fossem a mesma unidade.

## 2. Benchmark de Algoritmos Estocásticos (Hill Climbing e Random Restart)

*   **Dificuldade:** Hill Climbing pode ficar preso em ótimos locais e não encontrar uma solução, e tanto ele quanto Random Restart têm desempenho que pode variar significativamente entre execuções devido à sua natureza estocástica.
*   **Solução:** Para mitigar a variabilidade e obter resultados mais representativos:
    *   Foram realizadas múltiplas execuções para cada algoritmo (100 execuções para Hill Climbing e Random Restart, 5 para o Backtracking, que é determinístico em sua busca pela primeira solução e por todas as soluções).
    *   As médias de tempo de execução, uso de memória e custo computacional foram calculadas sobre as execuções bem-sucedidas.
    *   Para Hill Climbing e Random Restart, a taxa de sucesso (percentual de execuções que encontraram uma solução) também foi registrada e será reportada, o que é crucial para entender a confiabilidade desses métodos.
    *   No Hill Climbing, foi adicionada uma heurística simples para tentar escapar de platôs (movimento aleatório após um número de iterações sem melhora) e um limite de iterações sem melhora para evitar loops excessivamente longos em ótimos locais.

## 3. Medição Consistente de Uso de Memória

*   **Dificuldade:** Obter uma medição precisa e comparável do pico de uso de memória para cada algoritmo.
*   **Solução:** A biblioteca `tracemalloc` do Python foi utilizada. `tracemalloc.start()` foi chamado no início da seção de código cujo consumo de memória se desejava medir, e `tracemalloc.get_traced_memory()` (retornando `current` e `peak`) foi chamado ao final, com `tracemalloc.stop()` em seguida. O valor de `peak` foi usado como a métrica de pico de uso de memória, convertido para Kilobytes (KB) para facilitar a leitura.

## 4. Visualização de Métricas de Custo Computacional com Unidades Diferentes

*   **Dificuldade:** Como as métricas de custo computacional (nós visitados, avaliações de conflito, tentativas) têm unidades e escalas diferentes, apresentá-las em um único gráfico comparativo direto seria enganoso.
*   **Solução:** Optou-se por gerar gráficos de barras individuais para o custo computacional de cada algoritmo ao encontrar uma solução. Isso permite visualizar o valor para cada um, e o relatório explicará a natureza de cada métrica. Para as outras métricas (tempo e memória para uma solução, e todas as métricas para encontrar todas as soluções com backtracking), gráficos comparativos diretos foram possíveis e gerados.

## 5. Erro de Sintaxe em f-string durante a Execução dos Benchmarks

*   **Dificuldade:** Durante a execução do script `run_benchmarks.py`, ocorreu um `SyntaxError: f-string: unmatched '['` no arquivo `random_restart_benchmark.py`. Isso aconteceu porque aspas duplas foram usadas para acessar chaves de dicionário dentro de uma f-string que também era delimitada por aspas duplas.
*   **Solução:** O erro foi corrigido modificando as f-strings problemáticas. A solução adotada foi atribuir os valores do dicionário a variáveis intermediárias e, em seguida, usar essas variáveis na f-string, que foi então delimitada por aspas simples para evitar o conflito. Uma alternativa seria ter usado aspas simples para delimitar a f-string e aspas duplas para as chaves do dicionário, ou vice-versa, consistentemente.

## 6. Avisos de Glifo Ausente em Matplotlib (Sinal de Menos)

*   **Dificuldade:** Ao gerar os gráficos com Matplotlib, foram exibidos avisos como: `Font 'default' does not have a glyph for '\u2212' [U+2212], substituting with a dummy symbol.` O caractere `U+2212` é o sinal de menos.
*   **Solução:** Este é um aviso comum e, na maioria dos casos, Matplotlib substitui o caractere por um hífen padrão (`-`), que é visualmente aceitável para representar o sinal de menos em gráficos. Os gráficos gerados foram inspecionados e considerados legíveis. Conforme o conhecimento fornecido, as fontes padrão do sistema geralmente são suficientes. Nenhuma ação adicional foi considerada necessária, pois não comprometeu a visualização dos dados.

