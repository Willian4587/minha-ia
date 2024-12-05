import os
import subprocess

def executar_funcao(entrada):
    if "abrir navegador" in entrada:
        return abrir_navegador()
    elif "rodar script" in entrada:
        return rodar_script()
    elif "abrir pasta" in entrada:
        return abrir_pasta()
    elif "abrir capcut" in entrada:
        return abrir_capcut()
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

def abrir_capcut():
    try:
        os.system(r'start "" "G:\meus programas\CapCut\Apps\CapCut.exe"')  # Substitua pelo caminho completo
        return "O CapCut foi aberto com sucesso!"
    except Exception as e:
        return f"Erro ao tentar abrir o CapCut: {e}"
