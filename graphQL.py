import requests
import time
import csv

API_URL = "https://api.github.com/graphql"
TOKEN = ""

HEADERS = {
  "Authorization": f"Bearer {TOKEN}",
  "Content-Type": "application/json"
}

query_repos = """
{
user(login: "sindresorhus") {
  repositories(first: 10, privacy: PUBLIC, orderBy: {field: STARGAZERS, direction: DESC}) {
    nodes {
      name
      stargazerCount
      url
    }
  }
}
}
"""

query_repo_details = """
{
repository(owner: "sindresorhus", name: "awesome") {
  name
  description
  stargazerCount
  forkCount
  url
}
}
"""

query_repo_issues = """
{
repository(owner: "sindresorhus", name: "awesome") {
  issues(first: 10, orderBy: {field: CREATED_AT, direction: DESC}) {
    nodes {
      number
      title
      createdAt
      state
      author {
        login
      }
    }
  }
}
}
"""

consultas = [
  ("Lista de repositórios populares de sindresorhus", query_repos),
  ("Detalhes do repositório sindresorhus/awesome", query_repo_details),
  ("Últimas 10 issues do repositório sindresorhus/awesome", query_repo_issues)
]

repos_data = []
detalhes_data = []
issues_data = []

for nome, query in consultas:
  print(f"\n--- {nome} ---")
  data = {"query": query}
  start = time.time()
  response = requests.post(API_URL, headers=HEADERS, json=data)
  elapsed = (time.time() - start) * 1000
  resp_size = len(response.content)
  print(f"Tempo de resposta: {elapsed:.2f} ms")
  print(f"Tamanho da resposta: {resp_size} bytes")
  if response.status_code == 200:
      print("Consulta realizada com sucesso.")
      result = response.json()
      
      if "Lista de repositórios" in nome:
          repos = result['data']['user']['repositories']['nodes']
          for repo in repos:
              repos_data.append({
                  'nome': repo['name'],
                  'stars': repo['stargazerCount'],
                  'url': repo['url']
              })
      
      elif "Detalhes do repositório" in nome:
          repo = result['data']['repository']
          detalhes_data.append({
              'nome': repo['name'],
              'descricao': repo['description'],
              'stars': repo['stargazerCount'],
              'forks': repo['forkCount'],
              'url': repo['url']
          })
      
      elif "issues" in nome:
          issues = result['data']['repository']['issues']['nodes']
          for issue in issues:
              issues_data.append({
                  'repositorio': 'awesome',
                  'numero': issue['number'],
                  'titulo': issue['title'],
                  'estado': issue['state'],
                  'criado_em': issue['createdAt'],
                  'autor': issue['author']['login'] if issue['author'] else 'N/A'
              })
  else:
      print(f"Erro na consulta! Status: {response.status_code}")

print("\n📊 Salvando arquivos CSV...")

with open('repositorios.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['nome', 'stars', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(repos_data)
print(f" repositorios.csv criado com {len(repos_data)} repositórios")

with open('detalhes_repositorio.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['nome', 'descricao', 'stars', 'forks', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(detalhes_data)
print(f" detalhes_repositorio.csv criado com {len(detalhes_data)} registro")

with open('issues.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['repositorio', 'numero', 'titulo', 'estado', 'criado_em', 'autor']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(issues_data)
print(f" issues.csv criado com {len(issues_data)} issues")

print(f"\n🎉 Total: {len(repos_data) + len(detalhes_data) + len(issues_data)} registros salvos em 3 arquivos CSV!")