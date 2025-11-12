# GraphQL vs REST - Um experimento controlado
# 1. Desenho do Experimento

## A. Hipóteses Nula e Alternativa

**Hipótese Nula (H₀):**
Não há diferença significativa no tempo de resposta e no tamanho da resposta entre consultas realizadas por APIs REST e GraphQL.

**Hipótese Alternativa (H₁):**
Consultas realizadas por APIs GraphQL apresentam tempo de resposta menor e tamanho de resposta menor do que consultas realizadas por APIs REST.

## B. Variáveis Dependentes

* **Tempo de resposta da consulta** (medido em milissegundos)
* **Tamanho da resposta** (medido em bytes)

## C. Variáveis Independentes

* **Tipo de API utilizada:** REST vs GraphQL

## D. Tratamentos

* **Consulta via REST:** Executar consultas usando a API no formato REST.
* **Consulta via GraphQL:** Executar as mesmas consultas, com os mesmos dados alvos, usando a API em formato GraphQL.

## E. Objetos Experimentais

* **API testada:** GitHub (API pública, disponível em versões REST e GraphQL)
* **Usuário analisado:** Sindre Sorhus (`sindresorhus`)
* **Repositório analisado:** `awesome` (`sindresorhus/awesome`)

## F. Tipo de Projeto Experimental

**Experimento controlado do tipo “within-subjects”**
Cada consulta será realizada nas duas APIs separadamente, medindo as mesmas variáveis, para comparação direta sob mesmas condições.

## G. Quantidade de Medições

Para cada operação (consultar lista, consultar item, consultar issues), registrar:

* Tempo de resposta
* Tamanho da resposta

Executadas tanto em REST quanto em GraphQL.

## H. Ameaças à Validade

* Ambiente de execução não controlado (latência de Internet variável, servidores distintos)
* Cache (resultados podem ser “cacheados”, afetando tempos medidos)
* Carga no servidor (API pode estar sobrecarregada em algum momento do teste)

## Justificativa de Escolha dos Objetos Experimentais

Para garantir **relevância, atualidade e representatividade**, selecionou-se o usuário **Sindre Sorhus** (`sindresorhus`), que possui o maior número de estrelas agregadas em seus repositórios dentre todos os desenvolvedores do GitHub, sendo amplamente reconhecido pela comunidade *open-source*.

O repositório **“awesome”** (`sindresorhus/awesome`) foi escolhido para as consultas específicas e complexas. É um dos repositórios mais populares do mundo, famoso por listar diversos projetos e recursos considerados excelentes por área de tecnologia, com uma das maiores quantidades de estrelas da plataforma.

Essas entidades foram definidas para aproximar o experimento de **cenários reais de alta demanda**, promovendo resultados mais representativos pela quantidade de dados envolvidos.

## Consultas Realizadas

### **Consulta 1: Lista de Repositórios Populares**

**Objetivo:**
Listar os dez repositórios públicos mais populares do usuário Sindre Sorhus, ordenados pelo número de estrelas.

**Métricas coletadas:**

* Nome do repositório (string)
* Número de estrelas (inteiro)
* URL do repositório (string)

### **Consulta 2: Detalhes do Repositório**

**Objetivo:**
Obter detalhes gerais do repositório “awesome”, incluindo nome, descrição, quantidade de estrelas, forks e URL.

**Métricas coletadas:**

* Nome do repositório (string)
* Descrição (texto)
* Número de estrelas (inteiro)
* Número de forks (inteiro)
* URL do repositório (string)

### **Consulta 3: Issues Recentes**

**Objetivo:**
Listar as dez últimas issues criadas no repositório “awesome”, obtendo informações como número, título, data de criação, estado e autor de cada issue.

**Métricas coletadas:**

* Nome do repositório (string)
* Número da issue (inteiro)
* Título da issue (string)
* Estado (aberta/fechada)
* Data de criação (timestamp ISO)
* Nome de usuário do autor (string)

## Cuidados Tomados para Execução Posterior

* Configurar ambiente local: rodar sempre do mesmo computador, preferencialmente na mesma rede, para reduzir variáveis.
* Definir horário dos testes: realizar os testes em horários próximos para minimizar variações de carga.
* Manter constantes os parâmetros das queries (número de itens, campos requisitados, etc).
* Salvar todas as respostas e métricas em arquivo `.csv`.
