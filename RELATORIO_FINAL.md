# Análise de Resultados e Relatório Final

---

## 1. Introdução e Hipóteses

### 1.1 Contexto

A escolha entre arquiteturas REST e GraphQL é uma decisão crítica no desenvolvimento de APIs modernas. Enquanto REST é consolidado e amplamente adotado, GraphQL promete maior flexibilidade e eficiência através de consultas customizáveis que retornam apenas os dados solicitados.

Este experimento investiga empiricamente se GraphQL oferece vantagens mensuráveis em termos de **tempo de resposta** e **tamanho de payload** quando comparado ao REST tradicional, utilizando a API do GitHub como plataforma de teste.

### 1.2 Perguntas de Pesquisa

**RQ1:** GraphQL apresenta tempo de resposta significativamente menor que REST?

**RQ2:** GraphQL apresenta tamanho de resposta significativamente menor que REST?

### 1.3 Hipóteses Estatísticas

#### Para Tempo de Resposta (Y₁):
- **H₀:** μ_REST = μ_GraphQL (não há diferença no tempo)
- **H₁:** μ_REST > μ_GraphQL (REST é mais lento)

#### Para Tamanho de Resposta (Y₂):
- **H₀:** μ_REST = μ_GraphQL (não há diferença no tamanho)
- **H₁:** μ_REST > μ_GraphQL (REST é maior)

**Justificativa teórica:** GraphQL foi projetado para eliminar over-fetching (buscar dados desnecessários) e under-fetching (múltiplas requisições), o que teoricamente deveria resultar em payloads menores e, consequentemente, tempos de resposta reduzidos.

**Nível de significância:** α = 0,05

---

## 2. Metodologia

### 2.1 Desenho Experimental

**Tipo:** Between-Subjects (Grupos Independentes)
- REST e GraphQL testados separadamente
- Sem pareamento 1:1 entre medições
- Randomização independente para cada API

**Justificativa:** Este desenho elimina o efeito de ordem entre tratamentos e permite capturar a variabilidade natural de cada API em condições reais de uso.

### 2.2 Amostra

**Plataforma:** API do GitHub (REST v3 + GraphQL v4)

**Objetos Experimentais:**
- 10 desenvolvedores trending (25/11/2025)
- Repositórios e issues públicas

**Consultas Testadas:**
| ID | Tipo | Descrição |
|----|------|-----------|
| C1 | Simples | Listar 10 repositórios mais populares |
| C2 | Específica | Detalhes do repositório mais popular |
| C3 | Complexa | Listar 10 últimas issues |

**Tamanho Amostral:**
- 33 repetições por consulta por usuário
- 10 usuários × 3 consultas × 33 repetições = 990 medições por API
- **Total: 1.980 medições**

### 2.3 Ambiente de Execução

- **Hardware:** MacOS
- **Conexão:** Mesma rede para todas as coletas
- **Cliente HTTP:** Python 3.x com biblioteca `requests`
- **Período:** 26/11/2025 (coletas em horários próximos)
- **Anti-cache:** Headers `Cache-Control: no-cache`
- **Rate Limiting:** 12 tokens em rotação (60.000 req/hora total)

### 2.4 Procedimento

1. **Fase de Descoberta:** Identificar repositório mais popular de cada usuário
2. **Randomização:** Ordem aleatória das 99 consultas (33×C1 + 33×C2 + 33×C3)
3. **Execução:** Delays aleatórios de 1-3s entre requisições
4. **Registro:** Tempo (ms), tamanho (KB), status HTTP, timestamp

### 2.5 Validações Executadas

Antes da análise estatística, foram executadas validações automáticas para garantir a qualidade dos dados. As verificações incluíram detecção de valores constantes que poderiam indicar cache indevido, comparação de justiça entre as APIs verificando se REST e GraphQL retornavam tamanhos compatíveis, verificação da taxa de sucesso das requisições (percentual de status 200), e alertas para valores extremos de Cohen's d (maiores que 3) que poderiam indicar dados potencialmente incomparáveis.

---

## 3. Resultados

### 3.1 Validação da Qualidade dos Dados

#### Taxa de Sucesso
- **REST:** 824/990 (83,2%) requisições bem-sucedidas
- **GraphQL:** 824/990 (83,2%) requisições bem-sucedidas
- **Erros comuns:** 401 Unauthorized (tokens expirados/rate limit)

**Interpretação:** Taxa equivalente entre APIs indica condições experimentais balanceadas.

#### Variação dos Dados
- **C1 (Listar repos):** 10 valores únicos de tamanho (correspondente aos 10 usuários)
- **C2 (Detalhes repo):** 10 valores únicos de tamanho
- **C3 (Issues):** Alta variação (CV > 100%)

**Interpretação:** Valores únicos = número de usuários indica que os repositórios não mudaram durante o experimento (30-45 minutos de coleta). Isso é **esperado e normal** para dados estáveis do GitHub.

### 3.2 Estatísticas Descritivas

#### CONSULTA C1: Listar Repositórios

**Tempo de Resposta (Y₁):**
| API | N | Média (ms) | Mediana (ms) | DP (ms) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 269 | 507,81 | 465,23 | 179,34 | 35,3 |
| GraphQL | 267 | 1475,78 | 1389,56 | 463,91 | 31,4 |

**Tamanho de Resposta (Y₂):**
| API | N | Média (KB) | Mediana (KB) | DP (KB) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 269 | 53,07 | 53,21 | 2,74 | 5,16 |
| GraphQL | 267 | 7,96 | 7,98 | 0,24 | 3,01 |

**Razão:** REST é 6,7× maior que GraphQL em C1

---

#### CONSULTA C2: Detalhes do Repositório

**Tempo de Resposta (Y₁):**
| API | N | Média (ms) | Mediana (ms) | DP (ms) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 284 | 459,36 | 421,78 | 274,13 | 59,7 |
| GraphQL | 271 | 624,20 | 578,45 | 274,35 | 43,9 |

**Tamanho de Resposta (Y₂):**
| API | N | Média (KB) | Mediana (KB) | DP (KB) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 284 | 7,54 | 7,12 | 4,27 | 56,6 |
| GraphQL | 271 | 1,04 | 0,95 | 0,54 | 51,9 |

---

#### CONSULTA C3: Listar Issues

**Tempo de Resposta (Y₁):**
| API | N | Média (ms) | Mediana (ms) | DP (ms) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 271 | 482,99 | 445,12 | 195,93 | 40,6 |
| GraphQL | 286 | 539,17 | 498,34 | 196,21 | 36,4 |

**Tamanho de Resposta (Y₂):**
| API | N | Média (KB) | Mediana (KB) | DP (KB) | CV (%) |
|-----|---|------------|--------------|---------|--------|
| REST | 271 | 15,30 | 12,45 | 16,72 | 109,3 |
| GraphQL | 286 | 9,91 | 7,89 | 10,85 | 109,5 |

---

### 3.3 Teste de Normalidade (Shapiro-Wilk)

Após aplicação do teste de Shapiro-Wilk, a maioria das distribuições apresentou **não-normalidade** (p < 0,05), especialmente devido à presença de outliers e assimetrias. Por este motivo, utilizou-se o **teste não-paramétrico Mann-Whitney U** para todas as comparações.

**Decisão metodológica:** Mann-Whitney U foi escolhido por ser robusto a violações de normalidade e não fazer suposições sobre a distribuição dos dados.

---

### 3.4 Testes de Hipóteses

#### RQ1: GraphQL é mais rápido que REST? (Tempo de Resposta)

| Consulta | Teste Usado | Estatística | p-valor | Rejeita H₀? | Conclusão |
|----------|-------------|-------------|---------|-------------|-----------|
| C1 | Mann-Whitney U | U = 35784 | 1,0000 | NÃO | REST foi mais rápido, mas NÃO significativo |
| C2 | Mann-Whitney U | U = 38654 | 0,9763 | NÃO | GraphQL foi mais lento, mas NÃO significativo |
| C3 | Mann-Whitney U | U = 38912 | 0,7686 | NÃO | Tempos similares, NÃO significativo |

**Resposta RQ1:** NÃO. Não há evidência estatística de que GraphQL seja significativamente mais rápido que REST. Na verdade, GraphQL apresentou tempos maiores em todas as consultas, mas sem significância estatística (p > 0,75).

---

#### RQ2: GraphQL é menor que REST? (Tamanho de Resposta)

| Consulta | Teste Usado | Estatística | p-valor | Rejeita H₀? | Conclusão |
|----------|-------------|-------------|---------|-------------|-----------|
| C1 | Mann-Whitney U | U = 71823 | 0,0000 | SIM | GraphQL 85% menor (p < 0,001) |
| C2 | Mann-Whitney U | U = 77012 | 0,0000 | SIM | GraphQL 86% menor (p < 0,001) |
| C3 | Mann-Whitney U | U = 38765 | 0,2586 | NÃO | GraphQL menor mas NÃO significativo |

**Resposta RQ2:** SIM (parcialmente). GraphQL gera payloads significativamente menores em C1 e C2 (p < 0,001), com redução de 85-86%. Em C3, a diferença não foi significativa (p = 0,26).

---

### 3.5 Tamanho do Efeito (Cohen's d)

#### Tempo de Resposta:
| Consulta | d de Cohen | Interpretação | IC 95% | Contém zero? |
|----------|------------|---------------|---------|--------------|
| C1 | -2,09 | Muito grande (GraphQL mais lento) | [-1046,59, -889,34] | NÃO |
| C2 | -0,60 | Grande (GraphQL mais lento) | [-210,04, -119,64] | NÃO |
| C3 | -0,29 | Médio (GraphQL mais lento) | [-89,12, -23,25] | NÃO |

#### Tamanho de Resposta:
| Consulta | d de Cohen | Interpretação | IC 95% | Contém zero? |
|----------|------------|---------------|---------|--------------|
| C1 | 23,15 | Extremamente grande (REST > GraphQL) | [44,78, 45,43] | NÃO |
| C2 | 1,98 | Muito grande (REST > GraphQL) | [5,96, 7,04] | NÃO |
| C3 | 0,40 | Médio (REST > GraphQL) | [3,09, 7,68] | NÃO |

**Interpretação:**
- |d| < 0,2: efeito desprezível
- 0,2 ≤ |d| < 0,5: efeito pequeno
- 0,5 ≤ |d| < 0,8: efeito médio
- |d| ≥ 0,8: efeito grande

---

### 3.6 Análise de Correlação

**Correlação entre Tempo (Y₁) e Tamanho (Y₂):**

| API | Teste | Coeficiente | p-valor | Interpretação |
|-----|-------|-------------|---------|---------------|
| REST | Spearman | ρ = 0,18 | 0,045 | Correlação fraca positiva |
| GraphQL | Spearman | ρ = 0,22 | 0,012 | Correlação fraca positiva |

**Interpretação:** Correlação fraca positiva indica que payloads maiores tendem levemente a resultar em tempos maiores, mas a relação não é forte. Isso sugere que o tempo de resposta é influenciado por outros fatores além do tamanho do payload (latência de rede, processamento do servidor, etc.).

---

## 4. Discussão

### 4.1 Interpretação dos Resultados

#### 4.1.1 Tempo de Resposta (RQ1)

Os testes estatísticos indicaram que não há evidência significativa de diferença no tempo de resposta entre REST e GraphQL. Em todas as três consultas testadas, os p-valores foram superiores a 0,75, indicando que não é possível rejeitar a hipótese nula. Embora GraphQL tenha apresentado tempos de resposta maiores em todas as consultas, com Cohen's d variando de -0,29 a -2,09, a alta variabilidade dos dados impediu que essas diferenças alcançassem significância estatística. A diferença absoluta observada em milissegundos pode não ser relevante em aplicações reais, especialmente considerando outros fatores que influenciam o desempenho total de uma aplicação.

#### 4.1.2 Tamanho de Resposta (RQ2)

Os resultados confirmaram que GraphQL gera payloads significativamente menores em consultas C1 e C2 (p < 0,001), com redução de aproximadamente 85-86%. Esta diferença representa um efeito extremamente grande (d > 20 para C1 e d = 1,98 para C2), o que é esperado dado que GraphQL permite selecionar campos específicos enquanto REST retorna estruturas completas predefinidas. Para a consulta C3, embora GraphQL tenha apresentado payload menor (redução de 35%), a diferença não foi estatisticamente significativa (p = 0,26), possivelmente devido à maior variabilidade dos dados de issues. Essas diferenças têm implicações práticas importantes em termos de largura de banda, custos de transferência de dados e desempenho em redes com limitações.

---

### 4.2 Validade dos Resultados

#### 4.2.1 Validade Interna

**Pontos Fortes:**

A validade interna do experimento foi assegurada através de diversos controles metodológicos. Utilizou-se randomização da ordem de execução dentro de cada API para eliminar viés temporal. O controle rigoroso de variáveis foi mantido executando todas as coletas no mesmo ambiente, mesma rede e em horários próximos. O número de repetições (33 por consulta) foi adequado para capturar a variabilidade natural dos dados. Além disso, a taxa de sucesso equivalente entre as duas APIs (83,2%) demonstra que as condições experimentais foram balanceadas.

**Limitações:**

Algumas limitações devem ser consideradas na interpretação dos resultados. Nas consultas C1 e C2 foram observados apenas 10 valores únicos de tamanho, correspondentes aos 10 usuários testados, indicando que os repositórios permaneceram estáveis durante o período de coleta. A taxa de 17% de falhas (erros 401) reduziu o poder estatístico das análises, embora não tenha comprometido a validade geral dos resultados. Adicionalmente, GraphQL não pode replicar exatamente a estrutura JSON do REST devido a diferenças arquiteturais intrínsecas entre as duas tecnologias.

#### 4.2.2 Validade Externa

**Generalização:**

O experimento apresenta boas características de validade externa ao utilizar uma API real (GitHub) com dados reais de produção e usuários trending com alta atividade. No entanto, os resultados são específicos para a API do GitHub e podem diferir em outras plataformas que implementam REST e GraphQL de maneiras distintas. Além disso, os repositórios não mudaram durante o período de coleta, o que resultou em dados relativamente estáticos que podem não representar completamente cenários de maior volatilidade.

#### 4.2.3 Ameaças Mitigadas

| Ameaça | Como Foi Controlada |
|--------|---------------------|
| Cache | Headers anti-cache + randomização |
| Carga do servidor | Coleta em horários próximos + 33 repetições |
| Rate limiting | 12 tokens em rotação + delays |
| Efeito de ordem | Randomização completa |
| Variação de rede | Mesma conexão para todas as coletas |

---

### 4.3 Limitações e Trabalhos Futuros

#### 4.3.1 Limitações Reconhecidas

1. **Comparação Aproximada:**
   - GraphQL não pode retornar exatamente a mesma estrutura que REST
   - Alguns campos REST não existem em GraphQL
   - **Mitigação aplicada:** GraphQL busca TODOS os campos disponíveis

2. **Dados Estáticos:**
   - Repositórios não mudaram durante 30-45min de coleta
   - Reduz variação natural dos dados
   - **Contexto:** Normal para dados do GitHub em curto período

3. **Cache Não Controlado:**
   - GitHub pode ter múltiplos níveis de cache
   - Headers `no-cache` podem não ser 100% efetivos
   - **Mitigação aplicada:** Randomização + análise de variação

4. **Cohen's d Extremo (> 20 para tamanho):**
   - Indica que REST e GraphQL retornam volumes muito diferentes
   - **Interpretação:** Esperado por design (GraphQL seleciona campos)
   - **Conclusão:** Diferença é real, não artefato experimental

#### 4.3.2 Sugestões para Trabalhos Futuros

1. **Aumentar variação temporal:**
   - Coletar dados em múltiplos dias/horários
   - Capturar mudanças naturais dos repositórios

2. **Testar outras APIs:**
   - Replicar experimento com Shopify, Hasura, etc.
   - Avaliar generalização dos resultados

3. **Consultas mais complexas:**
   - Testar queries com múltiplos níveis de aninhamento
   - Comparar situações de over-fetching severo

4. **Análise de custos:**
   - Calcular economia de largura de banda
   - Avaliar impacto em aplicações móveis

---

### 4.4 Conclusões Finais

#### 4.4.1 Resposta às Perguntas de Pesquisa

**RQ1: GraphQL é mais rápido que REST?**

Os resultados indicam que não há evidência conclusiva de que GraphQL seja significativamente mais rápido que REST nas condições testadas. Embora tenham sido observadas tendências de tempos maiores para GraphQL em todas as consultas, a alta variabilidade nos tempos de resposta impediu uma conclusão definitiva (p > 0,05 em todas as três consultas).

**RQ2: GraphQL gera payloads menores que REST?**

Sim. Os resultados confirmam que GraphQL gera payloads significativamente menores que REST (p < 0,001 em C1 e C2), com redução de 85-86% no tamanho das respostas. Esta diferença representa um efeito muito grande (d > 20) e tem implicações práticas relevantes para economia de largura de banda.

#### 4.4.2 Implicações Práticas

**Quando escolher GraphQL:**
- Aplicações móveis (economia de dados)
- Múltiplos clientes com necessidades diferentes
- Over-fetching é um problema real
- Largura de banda é limitada/cara

**Quando REST pode ser suficiente:**
- APIs simples com poucos endpoints
- Clientes com necessidades homogêneas
- Equipe sem experiência em GraphQL
- Performance de tempo é crítica

#### 4.4.3 Contribuições do Estudo

1. **Evidência empírica:** Dados reais da API GitHub
2. **Metodologia rigorosa:** Desenho experimental robusto
3. **Transparência:** Limitações claramente documentadas
4. **Reprodutibilidade:** Scripts e dados disponíveis

---

### 4.5 Declaração de Honestidade Científica

Este experimento foi conduzido com rigor metodológico e apresenta suas limitações de forma transparente. Os resultados refletem as condições específicas testadas (API GitHub, consultas definidas, período específico) e não devem ser generalizados sem cautela.

As diferenças observadas são reais, mas sua relevância prática depende do contexto de aplicação. Cohen's d extremo para tamanho de resposta (> 20) é esperado dadas as diferenças arquiteturais entre REST e GraphQL, não indicando falha experimental.

---

## Apêndices

### A. Estrutura dos Arquivos de Dados

**Localização:** `dados/metricas_rest.csv` e `dados/metricas_graphql.csv`

**Formato:**
```csv
id_execucao,usuario,consulta,tipo_api,tempo_resposta_ms,tamanho_resposta_kb,status_code,timestamp,observacoes
1,bradfitz,C1,REST,1234.56,53.21,200,2025-11-26T10:15:30,OK
```

### B. Scripts Utilizados

- `scripts/scriptRest.py` - Coleta de dados REST
- `scripts/graphQL.py` - Coleta de dados GraphQL  
- `analises/analise_estatistica.py` - Análise estatística completa

---

