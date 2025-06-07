# gerar_matriz_incidencia.py

import pandas as pd
import numpy as np
import unidecode

# === CONFIGURAÇÃO ===
ARQUIVO_FORMULARIO = "respostas_formulario.csv"  # nome do arquivo exportado do Google Forms
COLUNA_NOME = "Nome"
COLUNA_BANDAS = "Bandas favoritas"

# === LEITURA DO CSV ===
df = pd.read_csv(ARQUIVO_FORMULARIO)

# Verificando se as colunas existem
if COLUNA_NOME not in df.columns or COLUNA_BANDAS not in df.columns:
    raise ValueError("As colunas especificadas não existem no CSV. Verifique os nomes.")

# === FUNÇÃO DE PADRONIZAÇÃO ===
separadores = [',', ';']

def padronizar_bandas(texto):
    if pd.isna(texto):
        return []
    texto = str(texto)
    for sep in separadores:
        texto = texto.replace(sep, ',')
    bandas = [unidecode.unidecode(b.strip().lower()) for b in texto.split(',') if b.strip()]
    return bandas

# Aplicando a função
df[COLUNA_BANDAS] = df[COLUNA_BANDAS].apply(padronizar_bandas)

# === CRIAÇÃO DA MATRIZ DE INCIDÊNCIA ===
alunos = df[COLUNA_NOME].tolist()
todas_bandas = sorted(set(banda for lista in df[COLUNA_BANDAS] for banda in lista))

# Criando a matriz
matriz_inc = np.zeros((len(alunos), len(todas_bandas)), dtype=int)

for i, bandas_aluno in enumerate(df[COLUNA_BANDAS]):
    for banda in bandas_aluno:
        if banda in todas_bandas:
            j = todas_bandas.index(banda)
            matriz_inc[i][j] = 1

# DataFrame da matriz
matriz_df = pd.DataFrame(matriz_inc, index=alunos, columns=todas_bandas)

# === SALVANDO OS ARQUIVOS ===
df.to_csv("dataset.csv", index=False)
matriz_df.to_csv("matriz_incidencia.csv")

print("✅ Arquivos gerados:")
print(" - dataset.csv")
print(" - matriz_incidencia.csv")
