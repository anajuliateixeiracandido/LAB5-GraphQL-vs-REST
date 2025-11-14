# GraphQL vs REST - Um experimento controladoC

# **Desenho do Experimento: Comparação REST vs. GraphQL**

## **1. Objetivo**

### **1.1 Objetivo Geral**

Determinar se a arquitetura **GraphQL** oferece uma redução significativa no **tempo de resposta** e no **tamanho da resposta** em comparação com a arquitetura **REST** para consultas simples e complexas na API do GitHub.

### **1.2 Objetivos Específicos**

* Medir o tempo de resposta de consultas simples, específicas e complexas em REST e GraphQL.
* Comparar o tamanho das respostas (payload) entre as duas abordagens.
* Identificar qual tecnologia apresenta melhor performance em cenários reais de uso.

---

## **2. Hipóteses Estatísticas**

* **Hipótese Nula (H0):**
  Não há diferença significativa no tempo de resposta e no tamanho da resposta entre consultas realizadas por APIs REST e GraphQL.
  **(H₀: μ_GraphQL = μ_REST)**

* **Hipótese Alternativa (H1):**
  Consultas realizadas por APIs GraphQL apresentam tempo de resposta menor e tamanho de resposta menor do que consultas realizadas por APIs REST.
  **(H₁: μ_GraphQL < μ_REST)**

---

## **3. Definição das Variáveis**

### **3.1 Variável Independente (Fator)**

* **Nome:** Tipo de API (X₁)
* **Tipo:** Qualitativo
* **Níveis/Tratamentos:**

  * T1: REST
  * T2: GraphQL

### **3.2 Variáveis Dependentes**

* **Y₁:** Tempo de resposta da consulta (ms)
* **Y₂:** Tamanho da resposta (bytes ou KB)

---

## **4. Objetos Experimentais e Amostra de Consultas**

### **4.1 Plataforma Escolhida**

**API GitHub**: possui suporte a REST e GraphQL, permitindo comparações diretas.

### **4.2 Entidades de Teste**

* **Usuário:** *sindresorhus*
* **Repositório:** *sindresorhus/awesome*

### **4.3 Amostra de Consultas**

#### **Consulta Simples (C1)**

Listar os 10 repositórios mais populares dos 10 usuários mais populares (mais estrelas).
**Dados coletados:** nome, estrelas, URL.

#### **Consulta Específica (C2)**

Obter detalhes dos repositórios.
**Dados coletados:** nome, descrição, estrelas, forks, URL.

#### **Consulta Complexa (C3)**

Listar as 10 últimas issues dos repositórios.
**Dados coletados:** número, título, criação, status, autor.

---

## **5. Desenho Experimental e Amostragem**

### **5.1 Tipo de Projeto Experimental**

**Within-Subjects (Medidas Repetidas)**
Cada consulta é feita com ambos os tratamentos.

### **5.2 Tamanho da Amostra e Randomização**

* **Repetições por tratamento (n):** 33
* **Total de medições:**
  `3 consultas × 2 tratamentos × 33 repetições = 198 medições`
* **Randomização:**
  Ordem das 6 combinações (C1-T1, C1-T2, ..., C3-T2) será aleatória em cada bloco.

---

## **6. Ameaças à Validade e Mitigação**

| Ameaça               | Descrição                 | Estratégia de Mitigação               |
| -------------------- | ------------------------- | ------------------------------------- |
| Latência de Internet | Variações de rede         | Mesma máquina e rede; testes próximos |
| Cache                | Cache distorce tempos     | Headers anti-cache; mais réplicas     |
| Carga no Servidor    | Sobrecarga momentânea     | Horários próximos; monitorar erros    |
| Variação de Código   | Implementações diferentes | Mesmos scripts e ambiente             |
| Efeito de Ordem      | Ordem fixa gera viés      | Randomização completa                 |
| Rate Limit           | Limite da API             | Delays e monitoramento dos headers    |

---

## **7. Procedimento e Cuidados**

### **7.1 Configuração do Cenário**

* Mesmo computador e rede
* Execução contínua
* Mesmos parâmetros entre REST e GraphQL

### **7.2 Controle de Rate Limiting**

* Delay entre 1 e 3 segundos
* Monitorar headers de limite

### **7.3 Execução Randomizada e Registro**

* Gerar sequência aleatória das 198 execuções
* Para cada execução:

  * Registrar **id_execucao**, **consulta**, **tipo_api**
  * Registrar variáveis dependentes (**Y1** e **Y2**)
  * Registrar **observacoes**

**Formato CSV esperado:**

| Coluna              | Descrição       |
| ------------------- | --------------- |
| id_execucao         | ID único        |
| consulta            | C1, C2 ou C3    |
| tipo_api            | REST ou GraphQL |
| tempo_resposta_ms   | Y1              |
| tamanho_resposta_kb | Y2              |
| observacoes         | anomalias       |

---

## **8. Análise de Dados e Critérios Estatísticos**

### **8.1 Estatísticas Descritivas**

Para cada uma das 6 combinações e cada variável dependente:

* Média, mediana, moda
* Desvio padrão, variância, amplitude
* Quartis, mínimo, máximo
* Outliers (IQR)

---

### **8.2 Teste de Normalidade (Shapiro-Wilk)**

Aplicado sobre a diferença **D = YREST − YGraphQL**.

* **H₀:** D é normal
* **H₁:** D não é normal
* **α = 0,05**

**Decisão:**

* p > 0,05 → usar **t pareado**
* p ≤ 0,05 → usar **Wilcoxon**

---

### **8.3 Teste Principal (se normal): Teste t Pareado**

* **α = 0,05**

| Variável     | H₀               | H₁               |
| ------------ | ---------------- | ---------------- |
| Y₁ (tempo)   | μREST = μGraphQL | μREST > μGraphQL |
| Y₂ (tamanho) | μREST = μGraphQL | μREST > μGraphQL |

**Critério:**

* p ≤ 0,05 → rejeita H₀ (GraphQL superior)
* p > 0,05 → não rejeita H₀

---

### **8.4 Teste Alternativo (se não-normal): Wilcoxon**

| Variável | H₀             | H₁             |
| -------- | -------------- | -------------- |
| Y₁       | mediana(D) = 0 | mediana(D) > 0 |
| Y₂       | mediana(D) = 0 | mediana(D) > 0 |

---

### **8.5 Tamanho de Efeito e IC**

* **d de Cohen:**
  `d = (μREST - μGraphQL) / σ_diferença`

Classificação:

* < 0,2 → pequeno
* 0,2–0,5 → médio
* 0,5–0,8 → grande
* ≥ 0,8 → muito grande

**Intervalo de Confiança (95%)** para (μREST – μGraphQL).
Se não contiver zero → diferença significativa.

---

### **8.6 Análise Complementar**

Correlação entre Y1 e Y2:

* Pearson (normal)
* Spearman (não-normal)

<img width="333" height="568" alt="Captura de Tela 2025-11-13 às 23 42 53" src="https://github.com/user-attachments/assets/cf95f78f-f607-48de-b3dd-284ea1044941" />
