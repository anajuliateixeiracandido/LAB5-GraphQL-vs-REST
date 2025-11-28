import requests
import time
import csv
import random
import sys
from datetime import datetime

API_URL = "https://api.github.com"

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
        "Accept": "application/vnd.github+json",
        "Cache-Control": "no-cache",
        "X-GitHub-Api-Version": "2022-11-28"
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
            response = requests.get(
                f"{API_URL}/user",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                tokens_validos += 1
        except Exception:
            pass
    
    if tokens_validos == 0:
        return False
    
    return True

def fazer_requisicao_com_retry(func, *args, max_tentativas=3):
    for tentativa in range(max_tentativas):
        try:
            return func(*args)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if tentativa < max_tentativas - 1:
                time.sleep(5)
            else:
                raise

def fetch_popular_repos(username):
    url = f"{API_URL}/users/{username}/repos"
    params = {
        'per_page': 10,
        'sort': 'stars',
        'direction': 'desc',
        'type': 'public'
    }
    return requests.get(url, headers=get_headers(), params=params, timeout=30)

def fetch_repo_details(username, repo_name):
    url = f"{API_URL}/repos/{username}/{repo_name}"
    return requests.get(url, headers=get_headers(), timeout=30)

def fetch_repo_issues(username, repo_name):
    url = f"{API_URL}/repos/{username}/{repo_name}/issues"
    params = {
        'per_page': 10,
        'state': 'all',
        'sort': 'created',
        'direction': 'desc'
    }
    return requests.get(url, headers=get_headers(), params=params, timeout=30)

metricas_data = []
id_execucao = 1

def main():
    global id_execucao
    
    print("\nScript REST - Coleta de Dados")
    print("="*80)
    
    if not validar_tokens():
        print("ERRO: Tokens invalidos.")
        sys.exit(1)
    
    print(f"\nUsuarios: {len(USUARIOS)} | Repeticoes: {REPETICOES} | Total: {len(USUARIOS) * REPETICOES * 3}")
    
    for usuario in USUARIOS:
        print(f"\nProcessando usuario: {usuario}")
        
        response = fazer_requisicao_com_retry(fetch_popular_repos, usuario)
        time.sleep(random.uniform(1, 3))
        
        if response.status_code != 200:
            continue
        
        repos = response.json()
        if not repos:
            continue
        
        repo_mais_popular = max(repos, key=lambda x: x['stargazers_count'])
        repo_name = repo_mais_popular['name']
        
        consultas = []
        for i in range(REPETICOES):
            consultas.extend([
                ('C1', 'fetch_popular_repos', usuario, None),
                ('C2', 'fetch_repo_details', usuario, repo_name),
                ('C3', 'fetch_repo_issues', usuario, repo_name)
            ])
        
        random.shuffle(consultas)
        
        total = len(consultas)
        
        for consulta_tipo, func_name, user, repo in consultas:
            start_time = time.time()
            
            if func_name == 'fetch_popular_repos':
                response = fazer_requisicao_com_retry(fetch_popular_repos, user)
            elif func_name == 'fetch_repo_details':
                response = fazer_requisicao_com_retry(fetch_repo_details, user, repo)
            elif func_name == 'fetch_repo_issues':
                response = fazer_requisicao_com_retry(fetch_repo_issues, user, repo)
            
            tempo_resposta_ms = (time.time() - start_time) * 1000
            tamanho_resposta_kb = len(response.content) / 1024
            
            metricas_data.append({
                'id_execucao': id_execucao,
                'usuario': user,
                'consulta': consulta_tipo,
                'tipo_api': 'REST',
                'tempo_resposta_ms': round(tempo_resposta_ms, 2),
                'tamanho_resposta_kb': round(tamanho_resposta_kb, 2),
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat(),
                'observacoes': 'OK' if response.status_code == 200 else f'Erro {response.status_code}'
            })
            
            id_execucao += 1
            
            time.sleep(random.uniform(1, 3))
    
    print("\nSalvando metricas em CSV...")
    
    with open('../dados/metricas_rest.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
