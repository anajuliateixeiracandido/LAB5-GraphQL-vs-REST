# **Desenho do Experimento: Comparação REST vs. GraphQL**

## **1. Objetivo**

### **1.1 Objetivo Geral**

Determinar se a arquitetura **GraphQL** oferece uma redução significativa no **tempo de resposta** e no **tamanho da resposta** em comparação com a arquitetura **REST** para consultas de dados complexas e simples na API do GitHub.

### **1.2 Objetivos Específicos**

* Medir o tempo de resposta de consultas simples, específicas e complexas em REST e GraphQL.
* Comparar o tamanho das respostas (payload) entre as duas abordagens.
* Identificar qual tecnologia apresenta melhor performance em cenários reais de uso.

---

## **2. Hipóteses Estatísticas**

* **Hipótese Nula (H0):** Não há diferença significativa no tempo e tamanho da resposta entre REST e GraphQL.
  **H₀: μ_GraphQL = μ_REST**

* **Hipótese Alternativa (H1):** GraphQL apresenta menor tempo e menor tamanho de resposta.
  **H₁: μ_GraphQL < μ_REST**

---

## **3. Definição das Variáveis**

### **3.1 Variável Independente (Fator)**

* **Nome:** Tipo de API (X₁)
* **Tipo:** Qualitativo
* **Níveis/Tratamentos:**

  * **T1:** REST
  * **T2:** GraphQL

### **3.2 Variáveis Dependentes (Respostas)**

* **Y1:** Tempo de resposta (ms)
* **Y2:** Tamanho da resposta (bytes ou KB)

---

## **4. Objetos Experimentais e Amostra de Consultas**

### **4.1 Plataforma Escolhida**

* **API GitHub**, devido ao suporte a REST e GraphQL sobre o mesmo domínio de dados.

### **4.2 Entidades de Teste**

* **Usuários:** 10 usuários mais populares (critério: seguidores ou estrelas).
* **Repositórios:** Para cada usuário, os 10 repositórios públicos mais populares.

### **4.3 Amostra de Consultas**

* **Consulta Simples (C1):** Listar os 10 repositórios mais populares de cada usuário.

  * Coleta: nome, estrelas, URL.

* **Consulta de Item Específico (C2):** Obter detalhes do repositório mais popular.

  * Coleta: nome, descrição, estrelas, forks, URL.

* **Consulta Complexa/Aninhada (C3):** Listar as 10 últimas issues do repositório mais popular.

  * Coleta: número da issue, título, criação, estado, autor.

---

## **5. Desenho Experimental e Amostragem**

### **5.1 Tipo de Projeto Experimental**

* **Desenho:** *Within-Subjects* (Medidas Repetidas).
* **Justificativa:** Cada consulta é executada em REST e GraphQL, reduzindo variabilidade externa.

### **5.2 Tamanho da Amostra e Randomização**

* **Repetições por Tratamento:** 33
* **Total de Medições:** 3 consultas × 2 tratamentos × 33 repetições = **198**
* **Randomização:** Ordem aleatória das 6 combinações (C1-T1, C1-T2, ..., C3-T2).

---

## **6. Ameaças à Validade e Mitigação**

| Ameaça               | Tipo    | Descrição                                   | Mitigação                                       |
| -------------------- | ------- | ------------------------------------------- | ----------------------------------------------- |
| Latência de Internet | Externa | Variação de rede altera tempo               | Mesmo computador/rede; horários próximos        |
| Cache de Resposta    | Externa | Pode distorcer tempos                       | Headers anti-cache; aumentar réplicas           |
| Carga no Servidor    | Externa | GitHub pode estar sobrecarregado            | Realizar em horários próximos; monitorar status |
| Variação de Código   | Interna | Implementações distintas influenciam tempos | Usar o mesmo script e ambiente                  |
| Efeito de Ordem      | Interna | Execuções em ordem fixa causam viés         | Randomização completa                           |
| Rate limiting        | Externa | API limita número de requisições            | Delays e monitoramento de cabeçalhos            |

---

## **7. Procedimento e Cuidados na Execução**

### **7.1 Configuração do Cenário**

* Usar o mesmo equipamento e rede.
* Realizar o experimento em intervalo contínuo.
* Manter constantes os parâmetros das queries.

### **7.2 Controle de Rate Limiting**

* Inserir delay de **1 a 3 segundos** entre requisições.
* Monitorar headers de limite da API.

### **7.3 Execução Randomizada e Registro**

Para cada execução:

* Registrar:

  * `id_execucao`
  * `consulta (C1, C2, C3)`
  * `tipo_api (REST/GraphQL)`
  * `tempo_resposta_ms`
  * `tamanho_resposta_kb`
  * `observacoes`

Todos os dados serão gravados em **CSV**.

---

## **8. Análise de Dados e Critérios Estatísticos**

### **8.1 Estatísticas Descritivas**

Para cada combinação:

* Média, mediana, moda
* Desvio padrão, variância, amplitude, IQR, coeficiente de variação
* Quartis e identificação de outliers (IQR)

### **8.2 Teste de Normalidade**

* **Método:** Shapiro-Wilk
* **Aplicado sobre a diferença:** *D = YREST − YGraphQL*
* **Decisão (α = 0,05):**

  * p > 0,05 → usar **Teste t pareado**
  * p ≤ 0,05 → usar **Wilcoxon**

### **8.3 Teste Principal se Normalidade for atendida**

* **Teste:** t pareado
* **Hipóteses (Y1 e Y2):**

  * H₀: μREST = μGraphQL
  * H₁: μREST > μGraphQL

### **8.4 Teste Alternativo se Normalidade não for atendida**

* **Teste:** Wilcoxon
* **Hipóteses:**

  * H₀: mediana(diferença) = 0
  * H₁: mediana(diferença) > 0

### **8.5 Tamanho do Efeito e Intervalo de Confiança**

* **d de Cohen:**

  * <0,2: pequeno
  * 0,2–0,5: médio
  * 0,5–0,8: grande
  * ≥0,8: muito grande

* **IC 95% para a diferença:**

  * Se não contém 0 → diferença significativa.

### **8.6 Análise Complementar**

* **Correlação entre Y1 e Y2:**

  * Pearson (normal)
  * Spearman (não-normal)
