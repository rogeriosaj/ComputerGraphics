import os

# Caminho onde estão as imagens
pasta = "images"  # <- Substitua pelo caminho correto

# Lista de arquivos .jpg na pasta, ordenados por nome
arquivos = sorted([f for f in os.listdir(pasta) if f.endswith(".jpg")])

# Renomeia de 1.jpg até 498.jpg
for i, nome_arquivo in enumerate(arquivos, start=1):
    novo_nome = f"{i}.jpg"
    caminho_antigo = os.path.join(pasta, nome_arquivo)
    caminho_novo = os.path.join(pasta, novo_nome)

    # Renomear arquivo
    os.rename(caminho_antigo, caminho_novo)

print("Renomeação concluída com sucesso.")
