# Desenho do Experimento: Comparação REST vs. GraphQL

## 1. Objetivo

### 1.1 Objetivo Geral
Determinar se a arquitetura GraphQL oferece uma redução significativa no tempo de resposta e no tamanho da resposta em comparação com a arquitetura REST para consultas equivalentes na API do GitHub.

### 1.2 Objetivos Específicos
- Medir o tempo de resposta de consultas simples, específicas e complexas em REST e GraphQL
- Comparar o tamanho das respostas (payload) entre as duas abordagens
- Identificar qual tecnologia apresenta melhor performance em cenários reais de uso

---

## 2. Hipóteses Estatísticas

**Hipótese Nula (H₀):** Não há diferença significativa no tempo de resposta e no tamanho da resposta entre consultas realizadas por APIs REST e GraphQL.

H₀: μ_GraphQL = μ_REST

**Hipótese Alternativa (H₁):** Consultas realizadas por APIs GraphQL apresentam tempo de resposta menor e tamanho de resposta menor do que consultas realizadas por APIs REST.

H₁: μ_GraphQL < μ_REST

---

## 3. Definição das Variáveis

### 3.1 Variável Independente (Fator)
- **Nome:** Tipo de API (X₁)
- **Tipo:** Qualitativo
- **Níveis/Tratamentos:**
  - **T1:** REST (Consulta via REST API)
  - **T2:** GraphQL (Consulta via GraphQL API)

### 3.2 Variáveis Dependentes (Respostas)
- **Y₁:** Tempo de resposta da consulta (medido em milissegundos)
- **Y₂:** Tamanho da resposta (payload medido em kilobytes)

---

## 4. Objetos Experimentais e Amostra de Consultas

### 4.1 Plataforma Escolhida
**API GitHub:** Escolhida por possuir suporte tanto a REST quanto a GraphQL, permitindo comparações diretas sob o mesmo domínio de dados.

### 4.2 Entidades de Teste
**Usuários Selecionados:** 10 desenvolvedores trending do GitHub (25/11/2025):
- bradfitz
- dgtlmoon
- aaronpowell
- gtsteffaniak
- junjiem
- pawurb
- stephenberry
- mrgrain
- me-no-dev
- chitalian

### 4.3 Amostra de Consultas

| ID | Tipo | Descrição | Dados Coletados |
|----|------|-----------|-----------------|
| **C1** | Simples | Listar os 10 repositórios públicos mais populares de cada usuário | Nome do repositório, número de estrelas, URL, descrição, linguagem, licença, datas de criação/atualização |
| **C2** | Específica | Obter detalhes do repositório mais popular do usuário | Nome, descrição completa, estrelas, forks, watchers, linguagens, tópicos, issues/PRs totais, configurações |
| **C3** | Complexa/Aninhada | Listar as 10 últimas issues criadas no repositório mais popular | Número da issue, título, corpo, data de criação, estado, autor, labels, assignees, comentários, reações |

---

## 5. Desenho Experimental e Amostragem

### 5.1 Tipo de Projeto Experimental
- **Desenho:** Between-Subjects (Grupos Independentes)
- **Justificativa:** REST e GraphQL são executados em momentos diferentes, sem pareamento 1:1. Cada API é testada independentemente com randomização própria, o que elimina o efeito de ordem entre tratamentos e permite comparação estatística usando testes para amostras independentes.

### 5.2 Tamanho da Amostra e Randomização
- **Número de Repetições por Consulta:** 33 execuções
- **Número Total de Observações por API:** 10 usuários × 3 consultas × 33 repetições = **990 medições por API**
- **Total Geral:** 990 (REST) + 990 (GraphQL) = **1.980 medições**

### 5.3 Procedimento de Randomização
Para cada usuário:
1. Criar lista com 99 consultas (33×C1 + 33×C2 + 33×C3)
2. Randomizar completamente a ordem de execução
3. Executar sequencialmente com delays aleatórios entre 1-3 segundos

**Objetivo:** Eliminar viés temporal e efeito de ordem dentro de cada API.

---

## 6. Ameaças à Validade e Mitigação

| Ameaça (Tipo) | Descrição do Problema | Estratégia de Mitigação |
|---------------|----------------------|-------------------------|
| **Latência de Internet** (Externa) | Variações na conexão de rede podem afetar o tempo de resposta | Uso do mesmo computador e mesma rede; Realizar testes em horários próximos |
| **Cache de Resposta** (Externa) | Respostas cacheadas podem distorcer os tempos medidos | Headers `Cache-Control: no-cache`; Randomização da ordem; 33 repetições |
| **Carga no Servidor** (Externa) | Servidor da API pode estar sobrecarregado em momentos específicos | Coleta em horários próximos; Monitorar taxa de sucesso; 33 repetições para média |
| **Variação de Código** (Interna) | Diferenças na implementação podem afetar medições | Mesmo cliente HTTP (requests); Mesma linguagem (Python 3); Mesmo ambiente |
| **Efeito de Ordem** (Interna) | Executar sempre REST antes de GraphQL pode criar viés | Randomização completa dentro de cada API; APIs executadas independentemente |
| **Rate Limiting** (Externa) | API pode limitar o número de requisições | Delays de 1-3s entre requisições; 12 tokens em rotação; Monitoramento de headers |
| **Comparação Injusta** (Interna) | GraphQL e REST podem retornar dados diferentes | GraphQL busca TODOS os campos disponíveis equivalentes ao REST |

---

## 7. Procedimento e Cuidados na Execução

### 7.1 Configuração do Cenário Experimental
- Mesmo computador (macOS)
- Mesma rede e conexão
- Python 3.x com biblioteca `requests`
- Coletas realizadas em intervalo de tempo próximo (mesmo dia)
- Headers anti-cache: `Cache-Control: no-cache`

### 7.2 Controle de Rate Limiting
- **Delay Programado:** 1 a 3 segundos aleatórios entre cada requisição
- **Múltiplos Tokens:** 12 tokens GitHub em rotação (limite: 5.000 req/hora por token = 60.000 req/hora total)
- **Monitoramento:** Scripts verificam headers `X-RateLimit-Remaining`

### 7.3 Execução Randomizada e Registro
Para cada execução:
1. Realizar a requisição (REST ou GraphQL)
2. Registrar tempo de resposta (início até recebimento completo)
3. Registrar tamanho da resposta (bytes do conteúdo)
4. Registrar status HTTP e timestamp
5. Aplicar delay aleatório
6. Verificar rate limit

### 7.4 Formato de Saída (CSV)

Todas as métricas são consolidadas em arquivos CSV:

| Coluna | Descrição |
|--------|-----------|
| `id_execucao` | ID único da medição (1 a 990) |
| `usuario` | Usuário GitHub testado |
| `consulta` | Tipo de Consulta (C1, C2, C3) |
| `tipo_api` | Tipo de API (REST ou GraphQL) |
| `tempo_resposta_ms` | Tempo de resposta em milissegundos (Y₁) |
| `tamanho_resposta_kb` | Tamanho do payload em kilobytes (Y₂) |
| `status_code` | Código HTTP da resposta |
| `timestamp` | Data/hora da execução (ISO 8601) |
| `observacoes` | Registro de anomalias (erros, rate limit, etc.) |

**Arquivos gerados:**
- `dados/metricas_rest.csv` (990 registros + header)
- `dados/metricas_graphql.csv` (990 registros + header)

---

## 8. Análise de Dados e Critérios Estatísticos

Devido ao desenho experimental do tipo "between-subjects" (grupos independentes), a análise utiliza métodos estatísticos para **amostras independentes**, comparando REST e GraphQL como dois grupos distintos.

### 8.1 Estatísticas Descritivas

Para cada uma das 6 combinações (3 Consultas × 2 Tratamentos) e para cada Variável Dependente (Y₁ e Y₂):

**Medidas de Tendência Central:**
- Média (μ)
- Mediana (Q2)
- Moda

**Medidas de Dispersão:**
- Desvio padrão (σ)
- Variância (σ²)
- Amplitude (máx - mín)
- Intervalo interquartil (IQR = Q3 - Q1)
- Coeficiente de variação (CV = σ/μ × 100%)

**Medidas de Posição:**
- Mínimo
- Quartil 1 (Q1)
- Quartil 3 (Q3)
- Máximo

**Identificação de Outliers:**
- Método IQR: valores < Q1 - 1.5×IQR ou > Q3 + 1.5×IQR

### 8.2 Teste de Normalidade (Verificação de Pressupostos)

**Teste:** Shapiro-Wilk

**Aplicação:** O teste é aplicado **separadamente** para cada grupo (REST e GraphQL) em cada combinação (consulta × variável dependente).

**Hipóteses:**
- H₀: A distribuição dos dados segue uma distribuição normal
- H₁: A distribuição dos dados não segue uma distribuição normal

**Nível de significância:** α = 0,05

**Critério de Decisão:**
- Se **ambos os grupos** têm p-valor > 0,05: usar **Teste t Independente** (paramétrico)
- Se **pelo menos um grupo** tem p-valor ≤ 0,05: usar **Teste de Mann-Whitney U** (não-paramétrico)

### 8.3 Teste Principal de Hipóteses (Para Amostras Independentes)

#### 8.3.1 Se os dados forem Normais: Teste t Independente

**Nível de Significância:** α = 0,05

**Teste Unilateral (à direita):**

| Variável | Hipótese Nula (H₀) | Hipótese Alternativa (H₁) |
|----------|-------------------|---------------------------|
| Tempo de Resposta (Y₁) | μ_REST = μ_GraphQL | μ_REST > μ_GraphQL (REST é mais lento) |
| Tamanho de Resposta (Y₂) | μ_REST = μ_GraphQL | μ_REST > μ_GraphQL (REST é maior) |

**Critério de Decisão:**
- Se p-valor ≤ 0,05: **Rejeitar H₀**. Concluir que REST é significativamente maior/mais lento que GraphQL.
- Se p-valor > 0,05: **Não rejeitar H₀**. Concluir que não há diferença significativa.

#### 8.3.2 Se os dados forem Não-Normais: Teste de Mann-Whitney U

**Nível de Significância:** α = 0,05

**Teste Unilateral:**

| Variável | Hipótese Nula (H₀) | Hipótese Alternativa (H₁) |
|----------|-------------------|---------------------------|
| Tempo de Resposta (Y₁) | Mediana_REST = Mediana_GraphQL | Mediana_REST > Mediana_GraphQL |
| Tamanho de Resposta (Y₂) | Mediana_REST = Mediana_GraphQL | Mediana_REST > Mediana_GraphQL |

**Critério de Decisão:** Idêntico ao teste t independente.

### 8.4 Tamanho do Efeito e Intervalo de Confiança

#### 8.4.1 Tamanho do Efeito (Magnitude)

**Medida:** d de Cohen (para amostras independentes)

**Fórmula:**
```
d = (μ_REST - μ_GraphQL) / σ_pooled

onde σ_pooled = √[(σ²_REST × (n_REST - 1) + σ²_GraphQL × (n_GraphQL - 1)) / (n_REST + n_GraphQL - 2)]
```

**Interpretação:**
- |d| < 0,2: efeito pequeno
- 0,2 ≤ |d| < 0,5: efeito médio
- 0,5 ≤ |d| < 0,8: efeito grande
- |d| ≥ 0,8: efeito muito grande

#### 8.4.2 Intervalo de Confiança (Precisão)

**Cálculo:** IC de 95% para a diferença das médias (μ_REST - μ_GraphQL)

**Interpretação:**
- Se o IC **não contiver zero**: a diferença é estatisticamente significativa ao nível de 5%
- Se o IC **contiver zero**: não há diferença significativa

### 8.5 Análise Complementar

**Correlação entre Tempo (Y₁) e Tamanho (Y₂):**

- **Teste de Pearson (r):** Se os dados forem normais
  - H₀: ρ = 0 (não há correlação linear)
  - H₁: ρ ≠ 0 (há correlação linear)
  
- **Teste de Spearman (ρ):** Se os dados forem não-normais
  - H₀: ρ_s = 0 (não há correlação monotônica)
  - H₁: ρ_s ≠ 0 (há correlação monotônica)

**Interpretação da Correlação:**
- |r| < 0,3: correlação fraca
- 0,3 ≤ |r| < 0,7: correlação moderada
- |r| ≥ 0,7: correlação forte

---

## 9. Estrutura do Projeto

```
LAB5-GraphQL-vs-REST/
├── README.md
├── scripts/
│   ├── scriptRest.py
│   └── graphQL.py
├── dados/
│   ├── metricas_rest.csv
│   └── metricas_graphql.csv
└── analises/
    └── analise_estatistica.py
```

---

## 10. Como Executar o Experimento

### 10.1 Pré-requisitos

```bash
pip install requests pandas numpy scipy matplotlib seaborn
```

### 10.2 Configurar Tokens do GitHub

**OBRIGATÓRIO:** Edite os arquivos `scripts/scriptRest.py` e `scripts/graphQL.py` e adicione seus tokens:

```python
TOKENS = [
    "github_pat_SEU_TOKEN_1",
    "github_pat_SEU_TOKEN_2",
    # ... adicione até 12 tokens
]
```

**Como obter tokens:**
1. Acesse https://github.com/settings/tokens
2. Clique em "Generate new token (classic)"
3. Selecione permissões: `repo`, `read:user`
4. Copie e adicione aos scripts

### 10.3 Executar Coleta de Dados

```bash
# Coleta REST (30-45 minutos)
cd scripts
python scriptRest.py

# Coleta GraphQL (30-45 minutos)
python graphQL.py
```

**Saídas:**
- `dados/metricas_rest.csv` (990 registros + header)
- `dados/metricas_graphql.csv` (990 registros + header)

### 10.4 Executar Análise Estatística

```bash
cd analises
python analise_estatistica.py
```

**Saídas:**
- Relatório estatístico completo em formato texto

---

## 11. Validação dos Dados

Antes da análise estatística, o script `analise_estatistica.py` executa validações automáticas:

1. **Verificação de valores fixos/constantes** (possível cache)
2. **Verificação de comparação justa** (tamanhos similares entre REST e GraphQL?)
3. **Verificação de taxa de sucesso** (% de requisições com status 200)
4. **Alertas para Cohen's d extremo** (> 3 indica possível problema)

---



