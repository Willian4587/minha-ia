import json
import random
import requests
import os
import subprocess
import pyttsx3
import speech_recognition as sr
import spacy
import openai

# Configuração do spaCy para processamento de NLP
nlp = spacy.load("pt_core_news_sm")

# Configuração da API do OpenAI
openai.api_key = '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'

# Variável global para habilitar ou desabilitar a pesquisa no Google
pesquisa_habilitada = True

# Função para carregar e salvar a memória
def carregar_memoria():
    try:
        with open("memoria.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}

def salvar_memoria(memoria):
    with open("memoria.json", "w") as arquivo:
        json.dump(memoria, arquivo, indent=4)

# Função para buscar informações na web usando a API do Google Custom Search
def buscar_no_google(query):
    if not pesquisa_habilitada:
        return "A pesquisa no Google está desativada."

    api_key = 'AIzaSyClNAmDvS7eSem3p-2EUE87tpkPFxJ9vNk'  # Substitua por sua chave de API
    cx = 'c56289fd300ba4e2b'  # Substitua pelo seu ID do motor de busca
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        resultados = response.json()
        if 'items' in resultados:
            return resultados['items'][0]['snippet']
        else:
            return "Desculpe, não encontrei nenhuma informação relevante."
    except requests.exceptions.RequestException as e:
        return f"Erro na busca: {e}"

# Função para gerar respostas utilizando o GPT-3
def gerar_resposta_gpt3(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Função para gerar resposta com base em entrada e memória
def gerar_resposta(entrada, memoria):
    entrada = entrada.lower().strip()

    # Comando para ativar ou desativar a pesquisa no Google
    global pesquisa_habilitada
    if entrada == "ativar pesquisa no google":
        pesquisa_habilitada = True
        return "A pesquisa no Google foi ativada."
    elif entrada == "desativar pesquisa no google":
        pesquisa_habilitada = False
        return "A pesquisa no Google foi desativada."

    # Detectar se é uma pergunta e usar o GPT-3 para responder
    palavras_perguntas = ["por que", "como", "o que", "qual", "quem", "onde", "quando"]
    if entrada.endswith("?") or any(entrada.startswith(p) for p in palavras_perguntas):
        resposta_web = buscar_no_google(entrada)
        if resposta_web == "Desculpe, não encontrei nenhuma informação relevante.":
            # Se não encontrar na web, use o GPT-3 para gerar uma resposta
            return gerar_resposta_gpt3(entrada)
        return resposta_web

    # Detecção e aprendizado de afirmações
    palavras_afirmacoes = [" é ", " são ", " significa ", " representa ", " descreve "]
    if any(p in entrada for p in palavras_afirmacoes):
        return aprender_fato(entrada, memoria)

    # Verificar memória
    if entrada in memoria:
        return random.choice(memoria[entrada])

    # Respostas dinâmicas e padrões
    respostas_dinamicas = [
        "Interessante! Pode me contar mais?",
        "Não sei muito sobre isso ainda. Quer me ensinar?",
        "Parece algo importante. Me diga mais!",
        "Hmm, estou curioso para aprender mais sobre isso.",
    ]
    return random.choice(respostas_dinamicas)

# Função para aprender fatos
def aprender_fato(entrada, memoria):
    partes = None
    for separador in [" é ", " são ", " significa ", " representa ", " descreve "]:
        if separador in entrada:
            partes = entrada.split(separador)
            break

    if partes and len(partes) == 2:
        chave = partes[0].strip()
        resposta = partes[1].strip()

        # Perguntar se a resposta está correta antes de salvar
        resposta_confirmacao = f"Você quis dizer que '{chave}' {separador} '{resposta}'? (sim/não)"
        print(f"Chatbot: {resposta_confirmacao}")
        resposta_usuario = input("Você: ").strip().lower()

        if resposta_usuario == 'sim':
            # Adicionar à memória ou expandir respostas existentes
            if chave in memoria:
                if resposta not in memoria[chave]:
                    memoria[chave].append(resposta)
            else:
                memoria[chave] = [resposta]

            salvar_memoria(memoria)
            return f"Entendi! Aprendi que '{chave}' {separador} '{resposta}'."
        else:
            return "Ok, não aprendi isso. Se quiser, me explique de outra forma."

    return "Não consegui entender. Pode explicar melhor?"

# Função para executar comandos do sistema
def executar_funcao(entrada):
    if "abrir navegador" in entrada:
        return abrir_navegador()
    elif "rodar script" in entrada:
        return rodar_script()
    elif "abrir pasta" in entrada:
        return abrir_pasta()
    else:
        return "Desculpe, não reconheci o comando."

# Funções auxiliares
def abrir_navegador():
    try:
        os.system("start chrome")  # Para Windows
        return "O navegador foi aberto com sucesso!"
    except Exception as e:
        return f"Erro ao tentar abrir o navegador: {e}"

def rodar_script():
    try:
        script_path = "script.py"  # Substitua pelo caminho do script que você quer rodar
        subprocess.run(["python", script_path], check=True)
        return f"O script '{script_path}' foi executado com sucesso!"
    except subprocess.CalledProcessError as e:
        return f"Erro ao rodar o script: {e}"

def abrir_pasta():
    try:
        os.system("start explorer")  # Para Windows
        return "A pasta foi aberta com sucesso!"
    except Exception as e:
        return f"Erro ao tentar abrir a pasta: {e}"

# Função para converter texto em fala
def falar(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    engine.say(texto)
    engine.runAndWait()

# Função para reconhecer voz
def reconhecer_voz():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale algo...")
        try:
            audio = recognizer.listen(source)
            texto = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {texto}")
            return texto
        except sr.UnknownValueError:
            print("Não entendi o que você disse.")
            return "Desculpe, não entendi."
        except sr.RequestError:
            print("Erro na conexão com o serviço de reconhecimento de voz.")
            return "Erro de conexão"

# Função principal do chatbot
def chatbot():
    print("Olá! Eu sou uma IA que aprende naturalmente e pode pesquisar na web. Vamos conversar? Diga 'sair' para encerrar.")
    memoria = carregar_memoria()

    modo_voz = input("Você gostaria de conversar por voz? (sim/não): ").strip().lower()
    usar_voz = modo_voz == "sim"

    while True:
        if usar_voz:
            entrada = reconhecer_voz()
        else:
            entrada = input("Você: ")

        if entrada.lower() == 'sair':
            print("Chatbot: Foi bom conversar com você. Até logo!")
            break

        resposta = gerar_resposta(entrada, memoria)
        print(f"Chatbot: {resposta}")
        falar(resposta)

if __name__ == "__main__":
    chatbot()
