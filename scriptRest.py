import requests
import time
import csv

TOKEN = ""
API_URL = "https://api.github.com"

HEADERS = {
"Authorization": f"Bearer {TOKEN}",
"Accept": "application/vnd.github+json"
}

def fetch_popular_repos():
url = f"{API_URL}/users/sindresorhus/repos?per_page=10&sort=stars"
return requests.get(url, headers=HEADERS)

def fetch_repo_details():
url = f"{API_URL}/repos/sindresorhus/awesome"
return requests.get(url, headers=HEADERS)

def fetch_repo_issues():
url = f"{API_URL}/repos/sindresorhus/awesome/issues?per_page=10&state=all&sort=created&direction=desc"
return requests.get(url, headers=HEADERS)

consultas = [
("Lista de repositórios populares de sindresorhus", fetch_popular_repos),
("Detalhes do repositório sindresorhus/awesome", fetch_repo_details),
("Últimas 10 issues do repositório sindresorhus/awesome", fetch_repo_issues)
]

repos_data = []
detalhes_data = []
issues_data = []

for nome, fetch_func in consultas:
response = fetch_func()
if response.status_code == 200:
    result = response.json()
    if "Lista de repositórios" in nome:
        for repo in result:
            repos_data.append({
                'nome': repo['name'],
                'stars': repo['stargazers_count'],
                'url': repo['html_url']
            })
    elif "Detalhes do repositório" in nome:
        repo = result
        detalhes_data.append({
            'nome': repo['name'],
            'descricao': repo['description'],
            'stars': repo['stargazers_count'],
            'forks': repo['forks_count'],
            'url': repo['html_url']
        })
    elif "issues" in nome:
        for issue in result:
            if 'pull_request' in issue:
                continue
            issues_data.append({
                'repositorio': 'awesome',
                'numero': issue['number'],
                'titulo': issue['title'],
                'estado': issue['state'],
                'criado_em': issue['created_at'],
                'autor': issue['user']['login'] if issue.get('user') else 'N/A'
            })

with open('repositorios.csv', 'w', newline='', encoding='utf-8') as csvfile:
fieldnames = ['nome', 'stars', 'url']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(repos_data)

with open('detalhes_repositorio.csv', 'w', newline='', encoding='utf-8') as csvfile:
fieldnames = ['nome', 'descricao', 'stars', 'forks', 'url']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(detalhes_data)

with open('issues.csv', 'w', newline='', encoding='utf-8') as csvfile:
fieldnames = ['repositorio', 'numero', 'titulo', 'estado', 'criado_em', 'autor']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(issues_data)
