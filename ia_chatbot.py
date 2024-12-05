import json
import random
import pyttsx3
import speech_recognition as sr
from funcoes_sistema import executar_funcao

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

# Função para aprender novas informações
def aprender(entrada, resposta, memoria):
    entrada = entrada.lower().strip()
    if entrada not in memoria:
        memoria[entrada] = []
    if resposta not in memoria[entrada]:
        memoria[entrada].append(resposta)
    salvar_memoria(memoria)

# Função para corrigir respostas
def corrigir_resposta(entrada, resposta_correta, memoria):
    entrada = entrada.lower().strip()
    if entrada in memoria:
        memoria[entrada] = [resposta_correta]
    else:
        memoria[entrada] = [resposta_correta]
    salvar_memoria(memoria)

# Função para gerar resposta com base em entrada e memória
def gerar_resposta(entrada, memoria):
    entrada = entrada.lower().strip()

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
    print("Olá! Eu sou uma IA que aprende naturalmente. Vamos conversar? Diga 'sair' para encerrar.")
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

        if entrada.startswith("corrigir: "):
            partes = entrada[len("corrigir: "):].split(" -> ")
            if len(partes) == 2:
                frase, nova_resposta = partes
                corrigir_resposta(frase.strip(), nova_resposta.strip(), memoria)
                print("Chatbot: Obrigado pela correção! Aprendi a nova resposta.")
                continue

        if "abrir" in entrada or "executar" in entrada:
            resposta = executar_funcao(entrada)
        else:
            resposta = gerar_resposta(entrada, memoria)

        print(f"Chatbot: {resposta}")
        falar(resposta)

        if resposta.startswith("Interessante!") or resposta.startswith("Não sei muito"):
            nova_resposta = input("Como devo responder a isso no futuro? (ou deixe em branco para ignorar): ").strip()
            if nova_resposta:
                aprender(entrada, nova_resposta, memoria)

if __name__ == "__main__":
    chatbot()
