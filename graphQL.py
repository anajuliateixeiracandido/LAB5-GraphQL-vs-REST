import requests
import time
import csv
import random
from datetime import datetime

API_URL = "https://api.github.com/graphql"

TOKENS = []

current_token_index = 0

def get_headers():
    """Retorna headers com o token atual em rotação"""
    global current_token_index
    token = TOKENS[current_token_index]
    current_token_index = (current_token_index + 1) % len(TOKENS)
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
    }

# 10 desenvolvedores trending do GitHub em 25/11/2025
# Fonte: https://github.com/trending/developers
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

REPETICOES = 33  # Número de repetições por consulta

def fazer_requisicao_com_retry(url, headers, data, max_tentativas=3):
    """Executa requisição com retry automático em caso de erro"""
    for tentativa in range(max_tentativas):
        try:
            return requests.post(url, headers=headers, json=data, timeout=30)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if tentativa < max_tentativas - 1:
                print(f"    ⚠️  Erro de conexão (tentativa {tentativa + 1}/{max_tentativas}), aguardando 5s...")
                time.sleep(5)
            else:
                print(f"    ✗ Falha após {max_tentativas} tentativas")
                raise

def query_repos(username):
    return f"""
    {{
      user(login: "{username}") {{
        repositories(first: 10, privacy: PUBLIC, orderBy: {{field: STARGAZERS, direction: DESC}}) {{
          nodes {{
            name
            stargazerCount
            url
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
        stargazerCount
        forkCount
        url
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
            createdAt
            state
            author {{
              login
            }}
          }}
        }}
      }}
    }}
    """

# Armazenar métricas de desempenho
metricas_data = []
id_execucao = 1

print("\n🚀 Iniciando coleta de dados GraphQL para 10 desenvolvedores trending (25/11/2025)...")
print(f"📊 Serão executadas {REPETICOES} repetições de cada consulta (C1, C2, C3)")
print(f"🎲 Ordem randomizada para cada usuário")
print(f"🔑 Usando rotação de {len(TOKENS)} tokens para evitar rate limiting\n")

for usuario in USUARIOS:
    print(f"\n{'='*60}")
    print(f"👤 Processando usuário: {usuario}")
    print(f"{'='*60}")
    
    # Primeiro, descobrir o repositório mais popular (fase de descoberta - não conta para métricas)
    print(f"  🔍 Descobrindo repositório mais popular...")
    data = {"query": query_repos(usuario)}
    response = fazer_requisicao_com_retry(API_URL, get_headers(), data)
    time.sleep(random.uniform(1, 3))
    
    if response.status_code != 200:
        print(f"  ✗ Erro ao buscar repositórios: {response.status_code}")
        continue
    
    result = response.json()
    if 'data' not in result or not result['data'] or not result['data']['user']:
        print(f"  ✗ Usuário não encontrado ou sem repositórios")
        continue
    
    repos = result['data']['user']['repositories']['nodes']
    if not repos:
        print(f"  ✗ Usuário sem repositórios públicos")
        continue
    
    repo_mais_popular = max(repos, key=lambda x: x['stargazerCount'])
    repo_name = repo_mais_popular['name']
    print(f"  ✓ Repositório mais popular: {repo_name} ({repo_mais_popular['stargazerCount']} ⭐)")
    
    # Criar lista de consultas para randomização
    consultas = []
    for i in range(REPETICOES):
        consultas.extend([
            ('C1', 'query_repos', usuario, None),
            ('C2', 'query_repo_details', usuario, repo_name),
            ('C3', 'query_repo_issues', usuario, repo_name)
        ])
    
    # Randomizar ordem das consultas
    random.shuffle(consultas)
    
    print(f"\n  🔄 Executando {len(consultas)} requisições randomizadas...")
    progresso = 0
    total = len(consultas)
    
    for consulta_tipo, func_name, user, repo in consultas:
        # Executar a query apropriada
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
        
        # Registrar métricas
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
        progresso += 1
        
        # Mostrar progresso a cada 10 requisições
        if progresso % 10 == 0:
            print(f"    Progresso: {progresso}/{total} ({(progresso/total)*100:.1f}%)")
        
        # Delay para evitar rate limiting
        time.sleep(random.uniform(1, 3))
    
    print(f"  ✓ Concluído: {total} requisições para {usuario}")

print("\n" + "="*60)
print("📊 Salvando métricas em CSV...")
print("="*60)

with open('metricas_graphql.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id_execucao', 'usuario', 'consulta', 'tipo_api', 'tempo_resposta_ms', 
                  'tamanho_resposta_kb', 'status_code', 'timestamp', 'observacoes']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(metricas_data)

print(f"✓ metricas_graphql.csv criado com {len(metricas_data)} medições")
print(f"\n🎉 Experimento GraphQL concluído!")
print(f"   • Total de requisições: {len(metricas_data)}")
print(f"   • Usuários processados: {len(USUARIOS)}")
print(f"   • Repetições por consulta: {REPETICOES}")
print(f"   • Consultas por usuário: {REPETICOES * 3} (C1, C2, C3)")