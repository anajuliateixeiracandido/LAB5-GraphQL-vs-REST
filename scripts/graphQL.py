import requests
import time
import csv
import random
import sys
from datetime import datetime

API_URL = "https://api.github.com/graphql"

TOKENS = [
    "SEU_TOKEN_AQUI",
]

current_token_index = 0

def get_headers():
    global current_token_index
    if not TOKENS or TOKENS[0] == "SEU_TOKEN_AQUI":
        print("ERRO: Configure seu token GitHub no inicio do script.")
        sys.exit(1)
    
    token = TOKENS[current_token_index]
    current_token_index = (current_token_index + 1) % len(TOKENS)
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
    }

USUARIOS = [
    "bradfitz",
    "dgtlmoon",
    "aaronpowell",
    "gtsteffaniak",
    "junjiem",
    "pawurb",
    "stephenberry",
    "mrgrain",
    "me-no-dev",
    "chitalian"
]

REPETICOES = 33

def validar_tokens():
    if not TOKENS or TOKENS[0] == "SEU_TOKEN_AQUI":
        print("ERRO: Lista de tokens vazia ou nao configurada.")
        return False
    
    tokens_validos = 0
    for i, token in enumerate(TOKENS):
        try:
            test_query = '{ viewer { login } }'
            response = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={"query": test_query},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'viewer' in data['data']:
                    tokens_validos += 1
        except Exception:
            pass
    
    if tokens_validos == 0:
        return False
    
    return True

def fazer_requisicao_com_retry(url, headers, data, max_tentativas=3):
    for tentativa in range(max_tentativas):
        try:
            return requests.post(url, headers=headers, json=data, timeout=30)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if tentativa < max_tentativas - 1:
                time.sleep(5)
            else:
                raise

def query_repos(username):
    return f"""
    {{
      user(login: "{username}") {{
        repositories(first: 10, privacy: PUBLIC, orderBy: {{field: STARGAZERS, direction: DESC}}) {{
          nodes {{
            name
            description
            url
            homepageUrl
            stargazerCount
            forkCount
            watchers {{
              totalCount
            }}
            createdAt
            updatedAt
            pushedAt
            isPrivate
            isFork
            isArchived
            isDisabled
            primaryLanguage {{
              name
              color
            }}
            licenseInfo {{
              name
              spdxId
            }}
            owner {{
              login
              avatarUrl
            }}
            defaultBranchRef {{
              name
            }}
            issues {{
              totalCount
            }}
            pullRequests {{
              totalCount
            }}
            diskUsage
            hasIssuesEnabled
            hasWikiEnabled
          }}
        }}
      }}
    }}
    """

def query_repo_details(username, repo_name):
    return f"""
    {{
      repository(owner: "{username}", name: "{repo_name}") {{
        name
        description
        url
        homepageUrl
        stargazerCount
        forkCount
        watchers {{
          totalCount
        }}
        createdAt
        updatedAt
        pushedAt
        isPrivate
        isFork
        isArchived
        isTemplate
        primaryLanguage {{
          name
          color
        }}
        languages(first: 10) {{
          edges {{
            size
            node {{
              name
              color
            }}
          }}
        }}
        licenseInfo {{
          name
          key
          spdxId
          url
        }}
        owner {{
          login
          avatarUrl
          url
        }}
        defaultBranchRef {{
          name
          target {{
            ... on Commit {{
              oid
              messageHeadline
              committedDate
            }}
          }}
        }}
        repositoryTopics(first: 10) {{
          nodes {{
            topic {{
              name
            }}
          }}
        }}
        issues {{
          totalCount
        }}
        pullRequests {{
          totalCount
        }}
        releases {{
          totalCount
        }}
        diskUsage
        hasIssuesEnabled
        hasProjectsEnabled
        hasWikiEnabled
        openGraphImageUrl
        usesCustomOpenGraphImage
      }}
    }}
    """

def query_repo_issues(username, repo_name):
    return f"""
    {{
      repository(owner: "{username}", name: "{repo_name}") {{
        issues(first: 10, orderBy: {{field: CREATED_AT, direction: DESC}}) {{
          nodes {{
            number
            title
            body
            createdAt
            updatedAt
            closedAt
            state
            url
            author {{
              login
              avatarUrl
              url
            }}
            authorAssociation
            labels(first: 10) {{
              nodes {{
                name
                color
                description
              }}
            }}
            assignees(first: 5) {{
              nodes {{
                login
                avatarUrl
              }}
            }}
            comments {{
              totalCount
            }}
            reactions {{
              totalCount
            }}
            milestone {{
              title
              number
              state
            }}
            locked
            activeLockReason
          }}
        }}
      }}
    }}
    """

metricas_data = []
id_execucao = 1

def main():
    global id_execucao
    
    print("\nScript GraphQL - Coleta de Dados")
    print("="*80)
    
    if not validar_tokens():
        print("ERRO: Tokens invalidos.")
        sys.exit(1)
    
    print(f"\nUsuarios: {len(USUARIOS)} | Repeticoes: {REPETICOES} | Total: {len(USUARIOS) * REPETICOES * 3}")
    
    for usuario in USUARIOS:
        print(f"\nProcessando usuario: {usuario}")
        
        data = {"query": query_repos(usuario)}
        response = fazer_requisicao_com_retry(API_URL, get_headers(), data)
        time.sleep(random.uniform(1, 3))
        
        if response.status_code != 200:
            continue
        
        result = response.json()
        if 'data' not in result or not result['data'] or not result['data']['user']:
            continue
        
        repos = result['data']['user']['repositories']['nodes']
        if not repos:
            continue
        
        repo_mais_popular = max(repos, key=lambda x: x['stargazerCount'])
        repo_name = repo_mais_popular['name']
        
        consultas = []
        for i in range(REPETICOES):
            consultas.extend([
                ('C1', 'query_repos', usuario, None),
                ('C2', 'query_repo_details', usuario, repo_name),
                ('C3', 'query_repo_issues', usuario, repo_name)
            ])
        
        random.shuffle(consultas)
        
        total = len(consultas)
        
        for consulta_tipo, func_name, user, repo in consultas:
            start_time = time.time()
            
            if func_name == 'query_repos':
                query = query_repos(user)
            elif func_name == 'query_repo_details':
                query = query_repo_details(user, repo)
            elif func_name == 'query_repo_issues':
                query = query_repo_issues(user, repo)
            
            data = {"query": query}
            response = fazer_requisicao_com_retry(API_URL, get_headers(), data)
            
            tempo_resposta_ms = (time.time() - start_time) * 1000
            tamanho_resposta_kb = len(response.content) / 1024
            
            metricas_data.append({
                'id_execucao': id_execucao,
                'usuario': user,
                'consulta': consulta_tipo,
                'tipo_api': 'GraphQL',
                'tempo_resposta_ms': round(tempo_resposta_ms, 2),
                'tamanho_resposta_kb': round(tamanho_resposta_kb, 2),
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat(),
                'observacoes': 'OK' if response.status_code == 200 else f'Erro {response.status_code}'
            })
            
            id_execucao += 1
            
            time.sleep(random.uniform(1, 3))
    
    print("\nSalvando metricas em CSV...")
    
    with open('../dados/metricas_graphql.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id_execucao', 'usuario', 'consulta', 'tipo_api', 'tempo_resposta_ms', 
                      'tamanho_resposta_kb', 'status_code', 'timestamp', 'observacoes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metricas_data)
    
    sucesso = len([m for m in metricas_data if m['status_code'] == 200])
    print(f"\nTotal: {len(metricas_data)} | Sucesso: {sucesso} ({sucesso/len(metricas_data)*100:.1f}%)")
    print("Experimento concluido.")

if __name__ == "__main__":
    main()
