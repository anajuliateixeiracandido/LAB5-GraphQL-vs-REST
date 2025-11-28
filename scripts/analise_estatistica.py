"""
Analise Estatistica: REST vs GraphQL
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import shapiro, mannwhitneyu, pearsonr, spearmanr, ttest_ind
from datetime import datetime
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class AnalisadorRESTvsGraphQL:
    
    def __init__(self, arquivo_rest, arquivo_graphql):
        self.df_rest = pd.read_csv(arquivo_rest)
        self.df_graphql = pd.read_csv(arquivo_graphql)
        self.df_combinado = None
        self.resultados = {}
        self.alertas = []
        
    def validar_qualidade_dados(self):
        print("=" * 80)
        print(" VALIDAÇÃO DE QUALIDADE DOS DADOS")
        print("=" * 80)
        
        alertas_encontrados = []
        
        print("\n1. Verificando variacao nos tamanhos de resposta...")
        for tipo_api in ['REST', 'GraphQL']:
            df_api = self.df_rest if tipo_api == 'REST' else self.df_graphql
            df_api_200 = df_api[df_api['status_code'] == 200]
            
            for consulta in ['C1', 'C2', 'C3']:
                dados = df_api_200[df_api_200['consulta'] == consulta]['tamanho_resposta_kb']
                
                if len(dados) > 0:
                    valores_unicos = dados.nunique()
                    desvio_padrao = dados.std()
                    media = dados.mean()
                    cv = (desvio_padrao / media * 100) if media > 0 else 0
                    
                    print(f"   {tipo_api} {consulta}: {valores_unicos} valores unicos, CV={cv:.2f}%")
                    
                    # ALERTA: Todos os valores iguais
                    if valores_unicos == 1:
                        alerta = f"ATENCAO: {tipo_api} {consulta} tem TODOS os tamanhos identicos ({media:.2f} KB)"
                        alertas_encontrados.append(alerta)
                        print(f"      {alerta}")
                    
                    # ALERTA: Muito pouca variacao
                    elif cv < 5 and media > 1:
                        alerta = f"ATENCAO: {tipo_api} {consulta} tem variacao muito baixa (CV={cv:.1f}%)"
                        alertas_encontrados.append(alerta)
                        print(f"      {alerta}")
        
        # 2. Verificar se REST e GraphQL tem tamanhos similares (comparacao justa?)
        print("\n2. Verificando comparacao justa (tamanhos similares?)...")
        for consulta in ['C1', 'C2', 'C3']:
            rest_dados = self.df_rest[(self.df_rest['consulta'] == consulta) & 
                                      (self.df_rest['status_code'] == 200)]['tamanho_resposta_kb']
            graphql_dados = self.df_graphql[(self.df_graphql['consulta'] == consulta) & 
                                            (self.df_graphql['status_code'] == 200)]['tamanho_resposta_kb']
            
            if len(rest_dados) > 0 and len(graphql_dados) > 0:
                media_rest = rest_dados.mean()
                media_graphql = graphql_dados.mean()
                razao = media_rest / media_graphql if media_graphql > 0 else float('inf')
                
                print(f"   {consulta}: REST={media_rest:.2f}KB vs GraphQL={media_graphql:.2f}KB (razao={razao:.1f}x)")
                
                if razao > 10 or razao < 0.1:
                    alerta = f"ATENCAO: {consulta} tem diferenca de {razao:.1f}x - REST e GraphQL podem estar retornando DADOS DIFERENTES!"
                    alertas_encontrados.append(alerta)
                    print(f"      {alerta}")
        
        # 3. Verificar taxa de sucesso
        print("\n3. Verificando taxa de sucesso (status 200)...")
        for tipo_api in ['REST', 'GraphQL']:
            df_api = self.df_rest if tipo_api == 'REST' else self.df_graphql
            total = len(df_api)
            sucesso = len(df_api[df_api['status_code'] == 200])
            taxa = (sucesso / total * 100) if total > 0 else 0
            
            print(f"   {tipo_api}: {sucesso}/{total} ({taxa:.1f}%)")
            
            if taxa < 90:
                alerta = f"ATENCAO: {tipo_api} tem taxa de sucesso baixa ({taxa:.1f}%)"
                alertas_encontrados.append(alerta)
                print(f"      {alerta}")
        
        self.alertas = alertas_encontrados
        
        if alertas_encontrados:
            print(f"\nTOTAL DE ALERTAS: {len(alertas_encontrados)}")
            print("   Estes problemas serao incluidos no relatorio final.")
        else:
            print("\n Nenhum problema critico detectado!")
        
        return len(alertas_encontrados) == 0
    
    def preprocessar_dados(self):
        print("\n" + "=" * 80)
        print("1. PRÉ-PROCESSAMENTO DOS DADOS")
        print("=" * 80)
        
        rest_valido = self.df_rest[self.df_rest['status_code'] == 200].copy()
        graphql_valido = self.df_graphql[self.df_graphql['status_code'] == 200].copy()
        
        print(f"\nDados REST originais: {len(self.df_rest)} registros")
        print(f"Dados REST validos (status 200): {len(rest_valido)} registros ({len(rest_valido)/len(self.df_rest)*100:.1f}%)")
        print(f"\nDados GraphQL originais: {len(self.df_graphql)} registros")
        print(f"Dados GraphQL validos (status 200): {len(graphql_valido)} registros ({len(graphql_valido)/len(self.df_graphql)*100:.1f}%)")
        
        self.df_combinado = pd.concat([rest_valido, graphql_valido], ignore_index=True)
        
        print(f"\nTotal de registros validos combinados: {len(self.df_combinado)}")
        print(f"Consultas unicas: {sorted(self.df_combinado['consulta'].unique())}")
        print(f"Tipos de API: {sorted(self.df_combinado['tipo_api'].unique())}")
        
        return rest_valido, graphql_valido
    
    def estatisticas_descritivas(self, df_rest, df_graphql):
        print("\n" + "=" * 80)
        print("2. ESTATÍSTICAS DESCRITIVAS")
        print("=" * 80)
        
        consultas = ['C1', 'C2', 'C3']
        metricas = ['tempo_resposta_ms', 'tamanho_resposta_kb']
        
        for consulta in consultas:
            print(f"\n{'─' * 80}")
            print(f"CONSULTA: {consulta}")
            print('─' * 80)
            
            for metrica in metricas:
                print(f"\n  Metrica: {metrica.replace('_', ' ').title()}")
                print("  " + "─" * 76)
                
                rest_data = df_rest[df_rest['consulta'] == consulta][metrica]
                graphql_data = df_graphql[df_graphql['consulta'] == consulta][metrica]
                
                if len(rest_data) == 0 or len(graphql_data) == 0:
                    print(f"  ATENCAO: Dados insuficientes para {consulta} - {metrica}")
                    continue
                
                # Calcular estatisticas para REST
                stats_rest = self._calcular_estatisticas(rest_data, "REST")
                # Calcular estatisticas para GraphQL
                stats_graphql = self._calcular_estatisticas(graphql_data, "GraphQL")
                
                # Exibir comparacao
                print(f"\n  REST:")
                self._imprimir_estatisticas(stats_rest)
                print(f"\n  GraphQL:")
                self._imprimir_estatisticas(stats_graphql)
                
                # Armazenar resultados
                key = f"{consulta}_{metrica}"
                self.resultados[key] = {
                    'rest': stats_rest,
                    'graphql': stats_graphql,
                    'rest_data': rest_data.values,
                    'graphql_data': graphql_data.values
                }
    
    def _calcular_estatisticas(self, data, nome):
        """Calcula todas as estatisticas descritivas"""
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        
        stats_dict = {
            'n': len(data),
            'media': np.mean(data),
            'mediana': np.median(data),
            'moda': stats.mode(data, keepdims=True)[0][0] if len(data) > 0 else np.nan,
            'desvio_padrao': np.std(data, ddof=1),
            'variancia': np.var(data, ddof=1),
            'amplitude': np.max(data) - np.min(data),
            'minimo': np.min(data),
            'maximo': np.max(data),
            'q1': q1,
            'q2_mediana': np.median(data),
            'q3': q3,
            'iqr': iqr,
            'cv': (np.std(data, ddof=1) / np.mean(data)) * 100 if np.mean(data) != 0 else np.nan,
            'outliers_count': len(outliers),
            'outliers': outliers.tolist() if len(outliers) > 0 else [],
            'valores_unicos': len(np.unique(data))
        }
        
        return stats_dict
    
    def _imprimir_estatisticas(self, stats):
        print(f"    N: {stats['n']} ({stats['valores_unicos']} valores unicos)")
        print(f"    Media: {stats['media']:.2f}")
        print(f"    Mediana: {stats['mediana']:.2f}")
        print(f"    Moda: {stats['moda']:.2f}")
        print(f"    Desvio Padrao: {stats['desvio_padrao']:.2f}")
        print(f"    Variancia: {stats['variancia']:.2f}")
        print(f"    Amplitude: {stats['amplitude']:.2f} (min: {stats['minimo']:.2f}, max: {stats['maximo']:.2f})")
        print(f"    Q1: {stats['q1']:.2f} | Q2: {stats['q2_mediana']:.2f} | Q3: {stats['q3']:.2f}")
        print(f"    IQR: {stats['iqr']:.2f}")
        print(f"    Coeficiente de Variacao: {stats['cv']:.2f}%")
        print(f"    Outliers: {stats['outliers_count']}")
    
    def teste_normalidade(self):
        print("\n" + "=" * 80)
        print("3. TESTE DE NORMALIDADE (Shapiro-Wilk)")
        print("=" * 80)
        
        consultas = ['C1', 'C2', 'C3']
        metricas = ['tempo_resposta_ms', 'tamanho_resposta_kb']
        
        self.resultados_normalidade = {}
        
        for consulta in consultas:
            print(f"\n{'─' * 80}")
            print(f"CONSULTA: {consulta}")
            print('─' * 80)
            
            for metrica in metricas:
                key = f"{consulta}_{metrica}"
                
                if key not in self.resultados:
                    continue
                
                rest_data = self.resultados[key]['rest_data']
                graphql_data = self.resultados[key]['graphql_data']
                
                # Teste de Shapiro-Wilk em cada grupo
                stat_rest, p_rest = shapiro(rest_data)
                stat_graphql, p_graphql = shapiro(graphql_data)
                
                # Decisao
                alpha = 0.05
                rest_normal = p_rest > alpha
                graphql_normal = p_graphql > alpha
                ambos_normal = rest_normal and graphql_normal
                
                teste_recomendado = "t independente" if ambos_normal else "Mann-Whitney U"
                
                print(f"\n  Metrica: {metrica.replace('_', ' ').title()}")
                print(f"  REST - W: {stat_rest:.4f}, p-valor: {p_rest:.4f} {' Normal' if rest_normal else ' Nao-normal'}")
                print(f"  GraphQL - W: {stat_graphql:.4f}, p-valor: {p_graphql:.4f} {' Normal' if graphql_normal else ' Nao-normal'}")
                print(f"  Teste recomendado: {teste_recomendado}")
                
                self.resultados_normalidade[key] = {
                    'rest_w_stat': stat_rest,
                    'rest_p_value': p_rest,
                    'rest_normal': rest_normal,
                    'graphql_w_stat': stat_graphql,
                    'graphql_p_value': p_graphql,
                    'graphql_normal': graphql_normal,
                    'ambos_normal': ambos_normal,
                    'teste_recomendado': teste_recomendado
                }
    
    def teste_hipotese(self):
        print("\n" + "=" * 80)
        print("4. TESTE DE HIPÓTESES (AMOSTRAS INDEPENDENTES)")
        print("=" * 80)
        print("\nH₀: μ_REST = μ_GraphQL (nao ha diferenca)")
        print("H₁: μ_REST > μ_GraphQL (REST e maior - teste unilateral à direita)")
        
        consultas = ['C1', 'C2', 'C3']
        metricas = ['tempo_resposta_ms', 'tamanho_resposta_kb']
        
        self.resultados_hipotese = {}
        
        for consulta in consultas:
            print(f"\n{'─' * 80}")
            print(f"CONSULTA: {consulta}")
            print('─' * 80)
            
            for metrica in metricas:
                key = f"{consulta}_{metrica}"
                
                if key not in self.resultados_normalidade:
                    continue
                
                rest_data = self.resultados[key]['rest_data']
                graphql_data = self.resultados[key]['graphql_data']
                
                ambos_normal = self.resultados_normalidade[key]['ambos_normal']
                
                print(f"\n  Metrica: {metrica.replace('_', ' ').title()}")
                print(f"  n_REST: {len(rest_data)}, n_GraphQL: {len(graphql_data)}")
                
                if ambos_normal:
                    # Teste t independente (unilateral)
                    stat, p_value_bilateral = ttest_ind(rest_data, graphql_data, equal_var=False)
                    p_value = p_value_bilateral / 2 if stat > 0 else 1 - (p_value_bilateral / 2)
                    
                    print(f"  Teste: t independente (Welch, unilateral)")
                    print(f"  Estatistica t: {stat:.4f}")
                    print(f"  p-valor: {p_value:.4f}")
                    teste_usado = 't independente'
                else:
                    # Mann-Whitney U (unilateral)
                    stat, p_value = mannwhitneyu(rest_data, graphql_data, alternative='greater')
                    
                    print(f"  Teste: Mann-Whitney U (unilateral)")
                    print(f"  Estatistica U: {stat:.4f}")
                    print(f"  p-valor: {p_value:.4f}")
                    teste_usado = 'Mann-Whitney U'
                
                # Decisao
                alpha = 0.05
                rejeita_h0 = p_value < alpha
                
                print(f"  Rejeita H₀? {' SIM' if rejeita_h0 else ' NÃO'} (α = {alpha})")
                
                if rejeita_h0:
                    print(f"  Conclusao: REST apresenta valores SIGNIFICATIVAMENTE MAIORES que GraphQL")
                else:
                    print(f"  Conclusao: NÃO ha diferenca significativa entre REST e GraphQL")
                
                self.resultados_hipotese[key] = {
                    'teste': teste_usado,
                    'estatistica': stat,
                    'p_value': p_value,
                    'rejeita_h0': rejeita_h0,
                    'alpha': alpha
                }
    
    def tamanho_efeito_ic(self):
        print("\n" + "=" * 80)
        print("5. TAMANHO DO EFEITO E INTERVALO DE CONFIANÇA")
        print("=" * 80)
        print("\nATENCAO: Cohen's d > 3 indica possivel problema nos dados!")
        
        consultas = ['C1', 'C2', 'C3']
        metricas = ['tempo_resposta_ms', 'tamanho_resposta_kb']
        
        self.resultados_efeito = {}
        
        for consulta in consultas:
            print(f"\n{'─' * 80}")
            print(f"CONSULTA: {consulta}")
            print('─' * 80)
            
            for metrica in metricas:
                key = f"{consulta}_{metrica}"
                
                if key not in self.resultados:
                    continue
                
                rest_data = self.resultados[key]['rest_data']
                graphql_data = self.resultados[key]['graphql_data']
                
                # Cohen's d para amostras independentes
                n1, n2 = len(rest_data), len(graphql_data)
                mean1, mean2 = np.mean(rest_data), np.mean(graphql_data)
                s1, s2 = np.std(rest_data, ddof=1), np.std(graphql_data, ddof=1)
                
                # Desvio padrao pooled
                pooled_std = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
                cohens_d = (mean1 - mean2) / pooled_std if pooled_std > 0 else float('inf')
                
                # Interpretacao CORRIGIDA
                abs_d = abs(cohens_d)
                if abs_d < 0.2:
                    interpretacao = "PEQUENO"
                elif abs_d < 0.5:
                    interpretacao = "MÉDIO"
                elif abs_d < 0.8:
                    interpretacao = "GRANDE"
                elif abs_d < 3:
                    interpretacao = "MUITO GRANDE"
                else:
                    interpretacao = "EXTREMAMENTE GRANDE (SUSPEITO!)"
                
                # Intervalo de confianca 95%
                diff_mean = mean1 - mean2
                se_diff = np.sqrt((s1**2 / n1) + (s2**2 / n2))
                df = n1 + n2 - 2
                t_crit = stats.t.ppf(0.975, df)
                ic = (diff_mean - t_crit * se_diff, diff_mean + t_crit * se_diff)
                
                contem_zero = ic[0] <= 0 <= ic[1]
                
                print(f"\n  Metrica: {metrica.replace('_', ' ').title()}")
                print(f"  Cohen's d: {cohens_d:.4f}")
                print(f"  Interpretacao: {interpretacao}")
                
                # ALERTA CRÍTICO: Cohen's d extremo
                if abs_d > 3:
                    print(f"  ALERTA CRÍTICO: Cohen's d > 3 e EXTREMAMENTE raro!")
                    print(f"     Isso sugere que REST e GraphQL estao medindo DADOS DIFERENTES,")
                    print(f"     nao apenas 'formatos diferentes do mesmo dado'.")
                    self.alertas.append(f"Cohen's d extremo em {consulta} {metrica}: {cohens_d:.2f}")
                
                print(f"  IC 95% (diferenca): [{ic[0]:.2f}, {ic[1]:.2f}]")
                print(f"  IC contem zero? {' SIM' if contem_zero else ' NÃO'}")
                
                if not contem_zero:
                    print(f"  Conclusao: Diferenca SIGNIFICATIVA (IC nao contem 0)")
                else:
                    print(f"  Conclusao: Diferenca NÃO significativa (IC contem 0)")
                
                self.resultados_efeito[key] = {
                    'cohens_d': cohens_d,
                    'interpretacao': interpretacao,
                    'ic_95': ic,
                    'contem_zero': contem_zero,
                    'alerta_extremo': abs_d > 3
                }
    
    def analisar_correlacao(self):
        print("\n" + "=" * 80)
        print("6. ANALISE DE CORRELACAO")
        print("=" * 80)
        print("\nRelacao entre Tempo de Resposta e Tamanho de Resposta")
        print("\nObjetivo: Verificar se respostas maiores estao associadas a tempos maiores")
        print("-" * 80)
        
        for consulta in ['C1', 'C2', 'C3']:
            print(f"\n{consulta}:")
            print("  " + "-" * 76)
            
            for tipo_api in ['REST', 'GraphQL']:
                dados = self.df_combinado[
                    (self.df_combinado['consulta'] == consulta) & 
                    (self.df_combinado['tipo_api'] == tipo_api)
                ]
                
                if len(dados) < 3:
                    print(f"  {tipo_api}: Dados insuficientes")
                    continue
                
                tempo = dados['tempo_resposta_ms'].values
                tamanho = dados['tamanho_resposta_kb'].values
                
                stat_normal_tempo, p_tempo = shapiro(tempo)
                stat_normal_tamanho, p_tamanho = shapiro(tamanho)
                
                ambos_normais = (p_tempo > 0.05) and (p_tamanho > 0.05)
                
                if ambos_normais:
                    r, p_valor = pearsonr(tempo, tamanho)
                    teste_usado = "Pearson"
                else:
                    r, p_valor = spearmanr(tempo, tamanho)
                    teste_usado = "Spearman"
                
                significativo = "SIM" if p_valor < 0.05 else "NAO"
                
                if abs(r) < 0.3:
                    forca = "FRACA"
                elif abs(r) < 0.7:
                    forca = "MODERADA"
                else:
                    forca = "FORTE"
                
                direcao = "positiva" if r > 0 else "negativa"
                
                print(f"  {tipo_api}:")
                print(f"    Teste: {teste_usado}")
                print(f"    Coeficiente: r = {r:.4f}")
                print(f"    p-valor: {p_valor:.4f}")
                print(f"    Significativo? {significativo} (α = 0.05)")
                print(f"    Forca: {forca}")
                print(f"    Interpretacao: Correlacao {direcao} {forca.lower()}")
                
                if not (consulta == 'C1' and tipo_api == 'GraphQL'):
                    print()
    
    def gerar_relatorio_honesto(self):
        print("\n" + "=" * 80)
        print("6. GERANDO RELATÓRIO COMPLETO E HONESTO")
        print("=" * 80)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        relatorio = []
        relatorio.append("=" * 80)
        relatorio.append("RELATÓRIO COMPLETO: REST vs GraphQL")
        relatorio.append("Analise Estatistica Corrigida e Validada")
        relatorio.append("=" * 80)
        relatorio.append(f"Data da analise: {timestamp}")
        relatorio.append("")
        
        if self.alertas:
            relatorio.append("ALERTAS DE QUALIDADE DOS DADOS")
            relatorio.append("-" * 80)
            for i, alerta in enumerate(self.alertas, 1):
                relatorio.append(f"{i}. {alerta}")
            relatorio.append("")
            relatorio.append("ATENÇÃO: Estes alertas indicam possiveis problemas que devem ser")
            relatorio.append("considerados ao interpretar os resultados!")
            relatorio.append("")
        
        relatorio.append("RESUMO EXECUTIVO")
        relatorio.append("-" * 80)
        relatorio.append("")
        
        rejeicoes_tempo = 0
        rejeicoes_tamanho = 0
        
        for consulta in ['C1', 'C2', 'C3']:
            key_tempo = f"{consulta}_tempo_resposta_ms"
            key_tamanho = f"{consulta}_tamanho_resposta_kb"
            
            if key_tempo in self.resultados_hipotese and self.resultados_hipotese[key_tempo]['rejeita_h0']:
                rejeicoes_tempo += 1
            
            if key_tamanho in self.resultados_hipotese and self.resultados_hipotese[key_tamanho]['rejeita_h0']:
                rejeicoes_tamanho += 1
        
        relatorio.append(f"Tempo de Resposta: {rejeicoes_tempo}/3 consultas com diferenca significativa")
        relatorio.append(f"Tamanho da Resposta: {rejeicoes_tamanho}/3 consultas com diferenca significativa")
        relatorio.append("")
        
        for consulta in ['C1', 'C2', 'C3']:
            relatorio.append("")
            relatorio.append(f"CONSULTA {consulta}")
            relatorio.append("-" * 80)
            
            for metrica in ['tempo_resposta_ms', 'tamanho_resposta_kb']:
                key = f"{consulta}_{metrica}"
                
                if key not in self.resultados_hipotese:
                    continue
                
                metrica_label = "Tempo de Resposta (ms)" if metrica == "tempo_resposta_ms" else "Tamanho da Resposta (KB)"
                relatorio.append(f"\n{metrica_label}:")
                
                # Medias e valores unicos
                media_rest = self.resultados[key]['rest']['media']
                media_graphql = self.resultados[key]['graphql']['media']
                unicos_rest = self.resultados[key]['rest']['valores_unicos']
                unicos_graphql = self.resultados[key]['graphql']['valores_unicos']
                
                relatorio.append(f"  Media REST: {media_rest:.2f} ({unicos_rest} valores unicos)")
                relatorio.append(f"  Media GraphQL: {media_graphql:.2f} ({unicos_graphql} valores unicos)")
                relatorio.append(f"  Diferenca: {media_rest - media_graphql:.2f}")
                
                # Teste de hipotese
                hip = self.resultados_hipotese[key]
                relatorio.append(f"  Teste: {hip['teste']}")
                relatorio.append(f"  p-valor: {hip['p_value']:.4f}")
                relatorio.append(f"  Significativo: {'SIM' if hip['rejeita_h0'] else 'NÃO'}")
                
                # Tamanho do efeito
                if key in self.resultados_efeito:
                    efeito = self.resultados_efeito[key]
                    relatorio.append(f"  Cohen's d: {efeito['cohens_d']:.4f} ({efeito['interpretacao']})")
                    relatorio.append(f"  IC 95%: [{efeito['ic_95'][0]:.2f}, {efeito['ic_95'][1]:.2f}]")
                    
                    if efeito['alerta_extremo']:
                        relatorio.append(f"  ALERTA: Cohen's d extremo - possivel comparacao injusta!")
        
        # LIMITAÇÕES (NOVO!)
        relatorio.append("")
        relatorio.append("")
        relatorio.append("LIMITAÇÕES DO ESTUDO")
        relatorio.append("-" * 80)
        relatorio.append("")
        relatorio.append("Este estudo possui as seguintes limitacoes que devem ser consideradas:")
        relatorio.append("")
        
        if any('DADOS DIFERENTES' in alerta for alerta in self.alertas):
            relatorio.append("1. COMPARAÇÃO POSSIVELMENTE INJUSTA:")
            relatorio.append("   As queries REST e GraphQL podem nao estar retornando exatamente")
            relatorio.append("   os mesmos dados. GraphQL permite selecionar campos especificos,")
            relatorio.append("   enquanto REST retorna estruturas completas. Isso pode explicar")
            relatorio.append("   grandes diferencas nos tamanhos de resposta.")
            relatorio.append("")
        
        if any('valores unicos' in str(alerta).lower() or 'identicos' in str(alerta).lower() for alerta in self.alertas):
            relatorio.append("2. POSSÍVEL CACHE NÃO DOCUMENTADO:")
            relatorio.append("   Tamanhos de resposta muito constantes sugerem que pode haver")
            relatorio.append("   cache ou dados estaticos nao documentados. Isto reduz a validade")
            relatorio.append("   externa dos resultados.")
            relatorio.append("")
        
        relatorio.append("3. CONDIÇÕES DE REDE:")
        relatorio.append("   Testes realizados em ambiente especifico. Resultados podem variar")
        relatorio.append("   com diferentes condicoes de rede, carga do servidor, etc.")
        relatorio.append("")
        
        relatorio.append("")
        relatorio.append("CONCLUSÕES")
        relatorio.append("-" * 80)
        relatorio.append("")
        
        if rejeicoes_tamanho > rejeicoes_tempo:
            relatorio.append("GraphQL apresenta vantagem SIGNIFICATIVA no tamanho das respostas.")
        elif rejeicoes_tempo > rejeicoes_tamanho:
            relatorio.append("GraphQL apresenta vantagem SIGNIFICATIVA no tempo de resposta.")
        else:
            relatorio.append("Resultados mistos entre as metricas analisadas.")
        
        if self.alertas:
            relatorio.append("")
            relatorio.append("PORÉM, devido aos alertas de qualidade de dados identificados,")
            relatorio.append("recomenda-se cautela ao interpretar estas conclusoes.")
        
        relatorio.append("")
        relatorio.append("=" * 80)
        
        relatorio_texto = "\n".join(relatorio)
        
        with open('relatorio_analise_estatistica.txt', 'w', encoding='utf-8') as f:
            f.write(relatorio_texto)
        
        print("\n   Relatorio salvo: relatorio_analise_estatistica.txt")
        print("\n" + relatorio_texto)
    
    def executar_analise_completa(self):
        print("\n" + "=" * 80)
        print("ANÁLISE ESTATÍSTICA CORRIGIDA: REST vs GraphQL")
        print("Com validacoes de qualidade de dados e alertas")
        print("="*80)
        
        dados_validos = self.validar_qualidade_dados()
        
        if not dados_validos:
            print("\nATENCAO: Problemas de qualidade detectados!")
            print("A analise continuara, mas os resultados devem ser interpretados com cautela.")
            input("Pressione ENTER para continuar...")
        
        df_rest, df_graphql = self.preprocessar_dados()
        
        self.estatisticas_descritivas(df_rest, df_graphql)
        
        self.teste_normalidade()
        
        self.teste_hipotese()
        
        self.tamanho_efeito_ic()
        
        self.analisar_correlacao()
        
        self.gerar_relatorio_honesto()
        
        print("\n" + "=" * 80)
        print(" ANÁLISE COMPLETA FINALIZADA!")
        print("=" * 80)
        
        if self.alertas:
            print(f"\nATENCAO:  {len(self.alertas)} alertas identificados. Veja o relatorio para detalhes.")
        else:
            print("\n Nenhum problema critico identificado nos dados.")


def main():
    """Funcao principal"""
    import sys
    
    import os
    arquivo_rest = '../dados/metricas_rest.csv'
    arquivo_graphql = '../dados/metricas_graphql.csv'
    
    if not os.path.exists(arquivo_rest) or not os.path.exists(arquivo_graphql):
        print("ERRO: Arquivos CSV nao encontrados!")
        print(f"Procurando: {arquivo_rest} e {arquivo_graphql}")
        sys.exit(1)
    
    print(f"Usando arquivos:")
    print(f"   REST: {arquivo_rest}")
    print(f"   GraphQL: {arquivo_graphql}")
    
    analisador = AnalisadorRESTvsGraphQL(arquivo_rest, arquivo_graphql)
    
    analisador.executar_analise_completa()


if __name__ == "__main__":
    main()
