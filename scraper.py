import requests
from bs4 import BeautifulSoup
import pandas as pd

# ── Configuração ────────────────────────────────────────
# URL do site que vamos raspar
URL_BASE = "http://books.toscrape.com/catalogue/"
URL_INICIAL = "http://books.toscrape.com/catalogue/page-1.html"

# Dicionário que converte as estrelas por extenso em número
ESTRELAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

# ── Função que coleta os livros de uma página ───────────
def coletar_pagina(url):
    # Faz a requisição HTTP — como abrir a página no navegador
    resposta = requests.get(url)
    
    # Lê o HTML da página
    soup = BeautifulSoup(resposta.text, "html.parser")
    
    # Encontra todos os livros na página
    livros = soup.find_all("article", class_="product_pod")
    
    dados = []
    for livro in livros:
        titulo = livro.h3.a["title"]
        preco = livro.find("p", class_="price_color").text.strip()
        disponivel = livro.find("p", class_="instock availability").text.strip()
        estrelas_texto = livro.p["class"][1]
        estrelas = ESTRELAS.get(estrelas_texto, 0)
        
        dados.append({
            "Título": titulo,
            "Preço": preco,
            "Avaliação (estrelas)": estrelas,
            "Disponibilidade": disponivel
        })
    
    return dados, soup

# ── Loop pelas páginas ──────────────────────────────────
print("Iniciando coleta...")
todos_livros = []
url_atual = URL_INICIAL
pagina = 1

while pagina <= 5:  # Coleta as primeiras 5 páginas
    print(f"Coletando página {pagina}...")
    dados, soup = coletar_pagina(url_atual)
    todos_livros.extend(dados)
    
    # Verifica se tem próxima página
    proxima = soup.find("li", class_="next")
    if proxima:
        url_atual = URL_BASE + proxima.a["href"]
        pagina += 1
    else:
        break

# ── Salva no Excel ──────────────────────────────────────
df = pd.DataFrame(todos_livros)
df.to_excel("livros.xlsx", index=False)

print(f"\n✅ Coleta finalizada!")
print(f"📚 Total de livros coletados: {len(todos_livros)}")
print(f"💾 Arquivo salvo: livros.xlsx")