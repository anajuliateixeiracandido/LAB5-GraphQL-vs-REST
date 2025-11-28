import requests
import time
import csv
import random
import sys
from datetime import datetime

API_URL = "https://api.github.com"

TOKENS = [
]

current_token_index = 0

def get_headers():
    global current_token_index
    if not TOKENS:
        print("❌ ERRO: Nenhum token configurado!")
        print("Por favor, adicione seus tokens GitHub no início do script.")
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
    if not TOKENS:
        print("❌ ERRO FATAL: Lista de tokens está vazia!")
        print("\n📝 INSTRUÇÕES:")
        print("1. Acesse: https://github.com/settings/tokens")
        print("2. Crie um token com permissões: repo, read:user")
        print("3. Adicione o token na lista TOKENS no início do script")
        return False
    
    print(f"🔑 Testando {len(TOKENS)} token(s)...")
    
    # Testar cada token
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
                data = response.json()
                username = data.get('login', 'desconhecido')
                print(f"  ✓ Token {i+1}: Válido (usuário: {username})")
                
                # Verificar rate limit
                tokens_validos += 1
            else:
                print(f"  ✗ Token {i+1}: Erro {response.status_code}")
        except Exception as e:
            print(f"  ✗ Token {i+1}: Exceção - {str(e)}")
    
    if tokens_validos == 0:
        print("\n❌ Nenhum token válido encontrado!")
        return False
    
    print(f"\n✓ {tokens_validos}/{len(TOKENS)} tokens válidos")
    return True

def fazer_requisicao_com_retry(func, *args, max_tentativas=3):
    for tentativa in range(max_tentativas):
        try:
            return func(*args)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if tentativa < max_tentativas - 1:
                print(f"    ⚠️  Erro de conexão (tentativa {tentativa + 1}/{max_tentativas}), aguardando 5s...")
                time.sleep(5)
            else:
                print(f"    ✗ Falha após {max_tentativas} tentativas")
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
    
    print("\n" + "="*80)
    print("🚀 Script REST - Coleta de Dados")
    print("="*80)
    
    if not validar_tokens():
        print("\n❌ Não é possível continuar sem tokens válidos.")
        print("Configure os tokens no início do script e tente novamente.")
        sys.exit(1)
    
    print(f"\n📊 Configuração do Experimento:")
    print(f"   • Usuários: {len(USUARIOS)}")
    print(f"   • Repetições por consulta: {REPETICOES}")
    print(f"   • Total de requisições: {len(USUARIOS)} × {REPETICOES} × 3 = {len(USUARIOS) * REPETICOES * 3}")
    print(f"   • Tokens disponíveis: {len(TOKENS)}")
    print(f"   • Ordem: Randomizada para cada usuário")
    
    input("\n⏸️  Pressione ENTER para iniciar a coleta...")
    
    for usuario in USUARIOS:
        print(f"{'='*80}")
        print(f"👤 Processando usuário: {usuario}")
        print(f"{'='*80}")
        
        print(f"  🔍 Descobrindo repositório mais popular...")
        response = fazer_requisicao_com_retry(fetch_popular_repos, usuario)
        time.sleep(random.uniform(1, 3))
        
        if response.status_code != 200:
            print(f"  ✗ Erro ao buscar repositórios: {response.status_code}")
            print(f"     Resposta: {response.text[:200]}")
            continue
        
        repos = response.json()
        if not repos:
            print(f"  ✗ Usuário sem repositórios públicos")
            continue
        
        repo_mais_popular = max(repos, key=lambda x: x['stargazers_count'])
        repo_name = repo_mais_popular['name']
        print(f"  ✓ Repositório mais popular: {repo_name} ({repo_mais_popular['stargazers_count']} ⭐)")
        
        consultas = []
        for i in range(REPETICOES):
            consultas.extend([
                ('C1', 'fetch_popular_repos', usuario, None),
                ('C2', 'fetch_repo_details', usuario, repo_name),
                ('C3', 'fetch_repo_issues', usuario, repo_name)
            ])
        
        random.shuffle(consultas)
        
        print(f"\n  🔄 Executando {len(consultas)} requisições randomizadas...")
        progresso = 0
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
            progresso += 1
            
            if progresso % 10 == 0:
                print(f"    Progresso: {progresso}/{total} ({(progresso/total)*100:.1f}%)")
            
            time.sleep(random.uniform(1, 3))
        
        print(f"  ✓ Concluído: {total} requisições para {usuario}")
    
    print("\n" + "="*80)
    print("📊 Salvando métricas em CSV...")
    print("="*80)
    
    with open('../dados/metricas_rest.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id_execucao', 'usuario', 'consulta', 'tipo_api', 'tempo_resposta_ms', 
                      'tamanho_resposta_kb', 'status_code', 'timestamp', 'observacoes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metricas_data)
    
    print(f"✓ ../dados/metricas_rest.csv criado com {len(metricas_data)} medições")
    
    sucesso = len([m for m in metricas_data if m['status_code'] == 200])
    print(f"\n📈 Estatísticas Finais:")
    print(f"   • Total de requisições: {len(metricas_data)}")
    print(f"   • Sucessos (status 200): {sucesso} ({sucesso/len(metricas_data)*100:.1f}%)")
    print(f"   • Usuários processados: {len(USUARIOS)}")
    print(f"   • Repetições por consulta: {REPETICOES}")
    print(f"\n🎉 Experimento REST concluído!")
    
    print(f"\n📦 Análise de Tamanhos (verificação de qualidade):")
    for consulta in ['C1', 'C2', 'C3']:
        tamanhos = [m['tamanho_resposta_kb'] for m in metricas_data 
                   if m['consulta'] == consulta and m['status_code'] == 200]
        if tamanhos:
            import statistics
            media = statistics.mean(tamanhos)
            desvio = statistics.stdev(tamanhos) if len(tamanhos) > 1 else 0
            minimo = min(tamanhos)
            maximo = max(tamanhos)
            tamanhos_unicos = len(set(tamanhos))
            
            print(f"   {consulta}: Média={media:.2f}KB, DP={desvio:.2f}KB, Min={minimo:.2f}KB, Max={maximo:.2f}KB")
            print(f"        Valores únicos: {tamanhos_unicos} de {len(tamanhos)} medições")
            
            if tamanhos_unicos == 1:
                print(f"        ⚠️  ALERTA CRÍTICO: TODOS os tamanhos são idênticos ({media:.2f}KB)!")
                print(f"            Isso é IMPOSSÍVEL em dados reais. Verificar:")
                print(f"            - Cache não documentado")
                print(f"            - Dados estáticos")
                print(f"            - Problema no script")
            elif desvio < 0.1 and media > 1:
                print(f"        ⚠️  ATENÇÃO: Baixíssima variação nos tamanhos!")
                print(f"            Verificar se dados realmente variam entre requisições.")

if __name__ == "__main__":
    main()
