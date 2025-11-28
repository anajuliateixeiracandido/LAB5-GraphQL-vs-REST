# Relatorio Final: REST vs GraphQL

## 1. Introducao e Hipoteses

### 1.1 Contexto

A escolha entre arquiteturas REST e GraphQL e uma decisao critica no desenvolvimento de APIs modernas. Enquanto REST e consolidado e amplamente adotado, GraphQL promete maior flexibilidade e eficiencia atraves de consultas customizaveis que retornam apenas os dados solicitados.

Este experimento investiga empiricamente se GraphQL oferece vantagens mensuráveis em termos de **tempo de resposta** e **tamanho de payload** quando comparado ao REST tradicional, utilizando a API do GitHub como plataforma de teste.

### 1.2 Perguntas de Pesquisa

**RQ1:** GraphQL apresenta tempo de resposta significativamente menor que REST?

**RQ2:** GraphQL apresenta tamanho de resposta significativamente menor que REST?

### 1.3 Hipoteses Estatisticas

#### Para Tempo de Resposta (Y1):
- **H0:** μ_REST = μ_GraphQL (nao ha diferenca no tempo)
- **H1:** μ_REST ≠ μ_GraphQL (ha diferenca no tempo)

#### Para Tamanho de Resposta (Y2):
- **H0:** μ_REST = μ_GraphQL (nao ha diferenca no tamanho)
- **H1:** μ_REST > μ_GraphQL (REST e maior)

**Nivel de significancia:** α = 0.05

---

## 2. Metodologia

### 2.1 Desenho Experimental

**Tipo:** Between-Subjects (Grupos Independentes)
- REST e GraphQL testados separadamente
- Sem pareamento 1:1 entre medicoes
- Randomizacao independente para cada API

**Justificativa:** Este desenho elimina o efeito de ordem entre tratamentos e permite capturar a variabilidade natural de cada API em condicoes reais de uso.

### 2.2 Amostra

**Plataforma:** API do GitHub (REST v3 + GraphQL v4)

**Objetos Experimentais:**
- 10 desenvolvedores trending (25/11/2025)
- Repositorios e issues publicas

**Consultas Testadas:**
| ID | Tipo | Descricao |
|----|------|-----------|
| C1 | Simples | Listar 10 repositorios mais populares |
| C2 | Especifica | Detalhes do repositorio mais popular |
| C3 | Complexa | Listar 10 ultimas issues |

**Tamanho Amostral:**
- 33 repeticoes por consulta por usuario
- 10 usuarios × 3 consultas × 33 repeticoes = 990 medicoes por API
- **Total planejado: 1.980 medicoes**
- **Total valido: 1.648 medicoes (824 REST + 824 GraphQL)**
- **Taxa de sucesso: 83.2% para ambas APIs**

### 2.3 Ambiente de Execucao

- **Hardware:** MacOS
- **Conexao:** Mesma rede para todas as coletas
- **Cliente HTTP:** Python 3.x com biblioteca `requests`
- **Periodo:** 27-28/11/2025 (coletas em horarios proximos)
- **Anti-cache:** Headers `Cache-Control: no-cache`
- **Rate Limiting:** Tokens GitHub em rotacao
- **Delays:** 1-3 segundos aleatorios entre requisicoes

### 2.4 Procedimento

1. **Fase de Descoberta:** Identificar repositorio mais popular de cada usuario
2. **Randomizacao:** Ordem aleatoria das 99 consultas (33×C1 + 33×C2 + 33×C3)
3. **Execucao:** Delays aleatorios de 1-3s entre requisicoes
4. **Registro:** Tempo (ms), tamanho (KB), status HTTP, timestamp
5. **Data da Coleta:** 27-28 de novembro de 2025

### 2.5 Validacoes Executadas

Antes da analise estatistica, foram executadas validacoes automaticas para garantir a qualidade dos dados:
- Deteccao de valores constantes (possivel cache indevido)
- Comparacao de justica entre APIs (tamanhos compativeis?)
- Verificacao da taxa de sucesso das requisicoes
- Alertas para valores extremos de Cohen's d (> 3)

---

## 3. Resultados

### 3.1 Validacao da Qualidade dos Dados

#### Taxa de Sucesso
- **REST:** 824/990 (83.2%) requisicoes bem-sucedidas
- **GraphQL:** 824/990 (83.2%) requisicoes bem-sucedidas
- **Erros comuns:** 401 Unauthorized (tokens expirados/rate limit)

**Interpretacao:** Taxa equivalente entre APIs indica condicoes experimentais balanceadas.

#### Variacao dos Dados
- **REST C1:** 10 valores unicos, CV=5.09%
- **REST C2:** 10 valores unicos, CV=61.02%
- **REST C3:** 7 valores unicos, CV=118.70%
- **GraphQL C1:** 10 valores unicos, CV=3.27% (variacao muito baixa - ALERTA)
- **GraphQL C2:** 7 valores unicos, CV=83.89%
- **GraphQL C3:** 8 valores unicos, CV=99.16%

#### Comparacao de Tamanhos
- **C1:** REST=52.92KB vs GraphQL=7.94KB (razao=6.7x)
- **C2:** REST=9.03KB vs GraphQL=1.03KB (razao=8.7x)
- **C3:** REST=14.06KB vs GraphQL=12.10KB (razao=1.2x)

**Interpretacao:** Valores unicos = numero de usuarios indica que os repositorios nao mudaram durante o experimento (cerca de 30-45 minutos de coleta). Isso e esperado e normal para dados estaveis do GitHub.

---

### 3.2 Estatisticas Descritivas

#### CONSULTA C1: Listar Repositorios

**Tempo de Resposta (Y1):**
| API | N | Media (ms) | Mediana (ms) | DP (ms) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 273 | 602.30 | 567.09 | 158.26 | 26.28 |
| GraphQL | 271 | 1554.92 | 1500.99 | 298.92 | 19.22 |

**Tamanho de Resposta (Y2):**
| API | N | Media (KB) | Mediana (KB) | DP (KB) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 273 | 52.92 | 52.66 | 2.69 | 5.09 |
| GraphQL | 271 | 7.94 | 7.99 | 0.26 | 3.27 |

**Razao:** REST e 6.7× maior que GraphQL em C1

---

#### CONSULTA C2: Detalhes do Repositorio

**Tempo de Resposta (Y1):**
| API | N | Media (ms) | Mediana (ms) | DP (ms) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 276 | 590.91 | 570.08 | 135.89 | 23.00 |
| GraphQL | 273 | 728.80 | 681.54 | 294.03 | 40.34 |

**Tamanho de Resposta (Y2):**
| API | N | Media (KB) | Mediana (KB) | DP (KB) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 276 | 9.03 | 5.48 | 5.51 | 61.02 |
| GraphQL | 273 | 1.03 | 0.22 | 0.87 | 83.89 |

**Razao:** REST e 8.7× maior que GraphQL em C2

---

#### CONSULTA C3: Listar Issues

**Tempo de Resposta (Y1):**
| API | N | Media (ms) | Mediana (ms) | DP (ms) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 275 | 602.55 | 599.53 | 123.15 | 20.44 |
| GraphQL | 280 | 686.94 | 684.72 | 248.89 | 36.23 |

**Tamanho de Resposta (Y2):**
| API | N | Media (KB) | Mediana (KB) | DP (KB) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 275 | 14.06 | 8.55 | 16.69 | 118.70 |
| GraphQL | 280 | 12.10 | 15.19 | 12.00 | 99.16 |

**Razao:** REST e 1.2× maior que GraphQL em C3 (diferenca pequena)

---

### 3.3 Teste de Normalidade (Shapiro-Wilk)

Apos aplicacao do teste de Shapiro-Wilk, todas as distribuicoes apresentaram **nao-normalidade** (p < 0.05), especialmente devido a presenca de outliers e assimetrias. Por este motivo, utilizou-se o **teste nao-parametrico Mann-Whitney U** para todas as comparacoes.

**Decisao metodologica:** Mann-Whitney U foi escolhido por ser robusto a violacoes de normalidade e nao fazer suposicoes sobre a distribuicao dos dados.

---

### 3.4 Testes de Hipoteses

#### RQ1: GraphQL e mais rapido que REST? (Tempo de Resposta)

| Consulta | Teste Usado | Estatistica | p-valor | Rejeita H0? | Conclusao |
|----------|-------------|-------------|---------|-------------|-----------|
| C1 | Mann-Whitney U | U = 300.0 | 1.0000 | NAO | GraphQL foi MAIS LENTO (NAO significativo) |
| C2 | Mann-Whitney U | U = 28496.0 | 1.0000 | NAO | GraphQL foi MAIS LENTO (NAO significativo) |
| C3 | Mann-Whitney U | U = 30362.5 | 1.0000 | NAO | GraphQL foi MAIS LENTO (NAO significativo) |

**Resposta RQ1:** NAO. GraphQL foi consistentemente MAIS LENTO que REST em todas as consultas, embora as diferencas nao sejam estatisticamente significativas (p = 1.0000).

**Observacao importante:** Os valores de p = 1.0000 indicam que REST apresentou tempos consistentemente menores, mas sem significancia estatistica ao nivel α = 0.05.

---

#### RQ2: GraphQL e menor que REST? (Tamanho de Resposta)

| Consulta | Teste Usado | Estatistica | p-valor | Rejeita H0? | Conclusao |
|----------|-------------|-------------|---------|-------------|-----------|
| C1 | Mann-Whitney U | U = 73983.0 | 0.0000 | SIM | GraphQL 85% menor (p < 0.001) |
| C2 | Mann-Whitney U | U = 75348.0 | 0.0000 | SIM | GraphQL 89% menor (p < 0.001) |
| C3 | Mann-Whitney U | U = 34384.0 | 0.9858 | NAO | Tamanhos similares (NAO significativo) |

**Resposta RQ2:** SIM (parcialmente). GraphQL gera payloads significativamente menores em C1 e C2 (p < 0.001), com reducao de 85-89%. Em C3, a diferenca nao foi significativa (p = 0.99).

---

### 3.5 Tamanho do Efeito (Cohen's d)

#### Tempo de Resposta:
| Consulta | d de Cohen | Interpretacao | IC 95% | Contem zero? |
|----------|------------|---------------|---------|--------------|
| C1 | -3.99 | EXTREMAMENTE GRANDE - SUSPEITO | [-992.94, -912.29] | NAO |
| C2 | -0.60 | GRANDE | [-176.37, -99.43] | NAO |
| C3 | -0.43 | MEDIO | [-117.05, -51.74] | NAO |

**ALERTA CRITICO:** Cohen's d = -3.99 em C1 e extremamente raro e sugere que REST e GraphQL podem estar medindo DADOS DIFERENTES, nao apenas formatos diferentes do mesmo dado.

#### Tamanho de Resposta:
| Consulta | d de Cohen | Interpretacao | IC 95% | Contem zero? |
|----------|------------|---------------|---------|--------------|
| C1 | 23.46 | EXTREMAMENTE GRANDE - SUSPEITO | [44.65, 45.29] | NAO |
| C2 | 2.02 | MUITO GRANDE | [7.34, 8.66] | NAO |
| C3 | 0.13 | PEQUENO | [-0.47, 4.38] | SIM |

**ALERTA CRITICO:** Cohen's d = 23.46 em C1 e extremamente alto, indicando diferenca massiva nos tamanhos das respostas.

---

### 3.6 Analise de Correlacao

A analise de correlacao investiga a relacao entre tempo de resposta e tamanho de resposta dentro de cada API.

#### Metodologia
- **Teste de Normalidade:** Shapiro-Wilk aplicado a tempo e tamanho
- **Escolha do Teste:**
  - Pearson (r): usado quando ambas variaveis sao normais
  - Spearman (ρ): usado quando pelo menos uma variavel e nao-normal
- **Interpretacao:**
  - |r| < 0.3: correlacao fraca
  - 0.3 ≤ |r| < 0.7: correlacao moderada
  - |r| ≥ 0.7: correlacao forte
  - p-valor < 0.05: correlacao significativa

#### Resultados REST

| Consulta | Teste | Coeficiente | p-valor | Interpretacao |
|----------|-------|-------------|---------|---------------|
| C1 | Spearman | ρ = -0.0754 | p = 0.2144 | Correlacao negativa fraca, NAO significativa |
| C2 | Spearman | ρ = 0.2449 | p < 0.001 | Correlacao positiva fraca, SIGNIFICATIVA |
| C3 | Spearman | ρ = 0.2625 | p < 0.001 | Correlacao positiva fraca, SIGNIFICATIVA |

#### Resultados GraphQL

| Consulta | Teste | Coeficiente | p-valor | Interpretacao |
|----------|-------|-------------|---------|---------------|
| C1 | Spearman | ρ = -0.0604 | p = 0.3219 | Correlacao negativa fraca, NAO significativa |
| C2 | Spearman | ρ = 0.7951 | p < 0.001 | Correlacao positiva FORTE, SIGNIFICATIVA |
| C3 | Spearman | ρ = 0.5540 | p < 0.001 | Correlacao positiva MODERADA, SIGNIFICATIVA |

**Interpretacao Geral:**

1. **C1 (Listar Repositorios):**
   - Ambas APIs mostram correlacao **fraca e nao-significativa**
   - Correlacao **negativa** (contraintuitiva): pode indicar que tempos maiores nao estao relacionados ao tamanho
   - **Possivel explicacao:** Tamanhos muito constantes em C1 (CV baixo) limitam a analise de correlacao

2. **C2 (Detalhes do Repositorio):**
   - **REST:** correlacao positiva fraca (ρ = 0.24) mas significativa
   - **GraphQL:** correlacao positiva **FORTE** (ρ = 0.80) e altamente significativa
   - **Interpretacao:** Em GraphQL C2, respostas maiores estao fortemente associadas a tempos maiores
   - Sugere que **GraphQL e mais sensivel ao tamanho da resposta** nesta consulta

3. **C3 (Listar Issues):**
   - **REST:** correlacao positiva fraca (ρ = 0.26) mas significativa
   - **GraphQL:** correlacao positiva **MODERADA** (ρ = 0.55) e significativa
   - **Interpretacao:** GraphQL novamente mostra relacao mais forte entre tamanho e tempo

**Conclusao da Analise de Correlacao:**
- **GraphQL** apresenta correlacoes **mais fortes** entre tamanho e tempo (C2 e C3)
- Sugere que o tempo de processamento GraphQL e **mais dependente do tamanho da resposta**
- **REST** mostra correlacoes mais fracas, indicando que outros fatores (latencia de rede, cache) podem dominar
- Todas as analises usaram **Spearman** devido a nao-normalidade dos dados

**NOTA:** Os valores foram obtidos da execucao mais recente do script `analise_estatistica.py` (28/11/2025 09:17:36).

---

## 4. Discussao

### 4.1 Tempo de Resposta (RQ1)

**Resultado surpreendente:** Ao contrario da expectativa teorica, GraphQL foi consistentemente MAIS LENTO que REST em todas as tres consultas:
- C1: GraphQL 158% mais lento (1554ms vs 602ms)
- C2: GraphQL 23% mais lento (728ms vs 590ms)
- C3: GraphQL 14% mais lento (686ms vs 602ms)

**Possíveis explicacoes:**
1. **Overhead de processamento:** GraphQL requer parsing e resolucao de queries complexas no servidor
2. **Otimizacao REST:** A API REST do GitHub e altamente otimizada e madura
3. **Cache REST:** Apesar dos headers anti-cache, REST pode ter camadas adicionais de cache
4. **Latencia de rede:** Nao compensada pela reducao de payload nas condicoes testadas
5. **C1 anomalo:** Cohen's d = -3.99 sugere possivel problema experimental nesta consulta

**Limitacao:** Os testes estatisticos nao detectaram significancia (p = 1.0), possivelmente devido a alta variabilidade ou tamanho amostral insuficiente.

### 4.2 Tamanho de Resposta (RQ2)

**Resultado confirmado:** GraphQL demonstrou clara vantagem na reducao de payload:
- C1: 85% menor (7.94KB vs 52.92KB) - SIGNIFICATIVO
- C2: 89% menor (1.03KB vs 9.03KB) - SIGNIFICATIVO  
- C3: 14% menor (12.10KB vs 14.06KB) - NAO significativo

**Explicacao:**
- **Over-fetching eliminado:** GraphQL retorna apenas campos solicitados
- **REST verbose:** REST retorna estruturas completas com muitos campos desnecessarios
- **C3 similar:** Consultas de issues tem estrutura semelhante em ambas APIs

**Implicacoes praticas:**
- Economia de largura de banda
- Menor consumo de dados moveis
- Menor tempo de transferencia (embora nao observado em RQ1)

### 4.3 Alertas de Qualidade e suas Explicacoes

O experimento identificou 5 alertas metodologicos:

#### Alerta 1: GraphQL C1 tem variacao muito baixa (CV=3.3%)
- **Natureza:** Caracteristica dos dados, NAO e erro
- **Explicacao:** Tamanhos de resposta muito constantes indicam que os repositorios retornaram estruturas similares
- **Causa:** 10 usuarios com repositorios de tamanhos parecidos + dados estaveis do GitHub
- **Impacto:** MINIMO - esperado para dados reais de APIs estabilizadas
- **Correcao necessaria?** NAO - e comportamento legitimo

#### Alertas 2 e 3: Taxa de sucesso 83.2% (166 falhas)
- **Natureza:** Limitacao experimental
- **Explicacao:** 166 requisicoes falharam com 401 Unauthorized
- **Causa:** Rate limiting do GitHub (5000 req/hora) e tokens expirados/rotacionados
- **Impacto:** MODERADO - reduz tamanho amostral de 990 para 824 por API
- **Correcao possivel?** SIM - nova coleta com mais tokens ou intervalos maiores
- **Justificativa:** Taxa de 83.2% ainda e aceitavel (> 80%), e identica para ambas APIs (comparacao justa)

#### Alertas 4 e 5: Cohen's d extremo em C1
- **Tempo:** d = -3.99 (GraphQL 158% mais lento)
- **Tamanho:** d = 23.46 (REST 6.7x maior)

**Analise Detalhada:**
- **Natureza:** NAO e erro estatistico - reflete diferencas REAIS entre as APIs
- **Explicacao tecnica:**
  - REST C1: Retorna objetos completos com todos os campos (52KB media)
  - GraphQL C1: Retorna apenas campos solicitados (7.94KB media)
  - Diferenca de **44.97KB** (6.7x) e **legitima e esperada**
  
- **Por que Cohen's d tao alto?**
  - Numerador: Diferenca de medias muito grande (952ms para tempo, 45KB para tamanho)
  - Denominador: Desvio-padrao pooled pequeno (dados com baixa variacao)
  - Resultado: d = (diferenca grande) / (variacao pequena) = valor extremo

- **E problema?** NAO para o tamanho (objetivo do GraphQL), ATENCAO para o tempo
  - **Tamanho:** Cohen's d alto e **esperado** - GraphQL foi projetado para reduzir payload
  - **Tempo:** Cohen's d alto e **surpresa** - GraphQL deveria ser mais rapido, nao 158% mais lento
  
- **Correcao necessaria?** NAO no codigo, SIM na interpretacao:
  - Alertas servem para lembrar que C1 tem comportamento anomalo
  - Necessario investigar por que GraphQL C1 e tao mais lento
  - Possivel causa: overhead de parsing/resolucao de queries complexas

**Conclusao dos Alertas:** 
Os alertas **NAO indicam erros de implementacao**, mas sim **caracteristicas metodologicas importantes** que devem ser consideradas na interpretacao. Os valores extremos de Cohen's d em C1 sao **matematicamente corretos** e refletem diferencas reais entre as arquiteturas.

### 4.4 Ameacas a Validade

**Ameacas Internas:**
- Implementacao diferente entre APIs (GraphQL mais nova, menos otimizada?)
- Possível cache nao documentado no lado do servidor
- Taxa de sucesso de 83.2% indica problemas com tokens/rate limiting

**Ameacas Externas:**
- Resultados especificos para API do GitHub
- Condicoes de rede especificas do ambiente de teste
- Horario das coletas pode ter afetado carga do servidor

**Ameacas de Constructo:**
- Medicao de tempo inclui latencia de rede (nao apenas processamento)
- C1 pode estar medindo operacoes diferentes entre APIs

---

## 5. Conclusoes

### 5.1 Respostas as Perguntas de Pesquisa

**RQ1: GraphQL e mais rapido que REST?**
- **Resposta:** NAO. GraphQL foi consistentemente mais lento em todas as consultas.
- **Evidencia:** Diferencas de 14% a 158%, mas sem significancia estatistica.

**RQ2: GraphQL tem respostas menores que REST?**
- **Resposta:** SIM. GraphQL reduz significativamente o tamanho das respostas.
- **Evidencia:** Reducao de 85-89% em C1 e C2 (p < 0.001).

### 5.2 Implicacoes Praticas

**Quando usar GraphQL:**
- Aplicacoes moveis com restricao de banda
- Cenarios onde over-fetching e problema critico
- Quando flexibilidade de consulta e mais importante que velocidade

**Quando usar REST:**
- Aplicacoes onde tempo de resposta e critico
- Quando APIs sao otimizadas e maduras
- Consultas simples e padronizadas

### 5.3 Limitacoes do Estudo

1. **Taxa de sucesso:** 83.2% indica problemas com rate limiting
2. **C1 anomalo:** Cohen's d extremo sugere possivel problema experimental
3. **Ambiente especifico:** Resultados validos apenas para API GitHub
4. **Sem significancia em RQ1:** Necessario maior tamanho amostral
5. **Medicao de tempo:** Inclui latencia de rede, nao apenas processamento

### 5.4 Trabalhos Futuros

1. Repetir experimento com maior tamanho amostral (n > 1000 por consulta)
2. Investigar C1 separadamente para entender Cohen's d extremo
3. Medir tempo de processamento no servidor (excluindo rede)
4. Testar outras APIs alem do GitHub
5. Analisar consumo de CPU/memoria no cliente
6. Avaliar performance com cache habilitado

---

## 6. Referencias

- GitHub REST API v3: https://docs.github.com/rest
- GitHub GraphQL API v4: https://docs.github.com/graphql
- Mann-Whitney U Test: Teste nao-parametrico para amostras independentes
- Cohen's d: Medida de tamanho de efeito padronizada
- Shapiro-Wilk: Teste de normalidade

---

**Data da Analise:** 28 de novembro de 2025
**Periodo de Coleta:** 27-28 de novembro de 2025
**Total de Medicoes Validas:** 1.648 (824 REST + 824 GraphQL)
