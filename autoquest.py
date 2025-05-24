import csv
import random
import os
import sys

# Códigos de cores ANSI para estilizar a saída no terminal
VERMELHO = '\033[91m'
VERDE = '\033[92m'
AMARELO = '\033[93m'
AZUL = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BRANCO = '\033[97m'
LARANJA  = '\033[38;5;208m'
RESET = '\033[0m'

# Número máximo de perguntas por execução
MAX_DESAFIOS = 20

# Banner principal com arte ASCII
BANNER = r"""
 █████╗ ██╗   ██╗████████╗ ██████╗      ██████╗ ██╗   ██╗███████╗███████╗████████╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗    ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
███████║██║   ██║   ██║   ██║   ██║    ██║   ██║██║   ██║█████╗  ███████╗   ██║
██╔══██║██║   ██║   ██║   ██║   ██║    ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║
██║  ██║╚██████╔╝   ██║   ╚██████╔╝    ╚██████╔╝╚██████╔╝███████╗███████║   ██║
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝      ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝
"""

# Exibição dos conceitos básicos
def mostrar_banner_e_conceitos():
    print(f"{VERMELHO}{BANNER}")  
    print(f"{RESET}+{'=' * 80}+\n")

    print(f"{BRANCO}🧠{AZUL} Permissões no Linux:{RESET}")
    print(f"  {RESET}• {CYAN}r{BRANCO} = {CYAN}leitura {BRANCO}({CYAN}read{BRANCO}){RESET}")
    print(f"  {RESET}• {AMARELO}w{BRANCO} = {AMARELO}escrita {BRANCO}({AMARELO}write{BRANCO}){RESET}")
    print(f"  {RESET}• {VERMELHO}x{BRANCO} = {VERMELHO}execução {BRANCO}({VERMELHO}execute{BRANCO}){RESET}\n")

    print(f"{RESET}  Exemplo: -{CYAN}r{AMARELO}w{VERMELHO}x{CYAN}r{RESET}-{VERMELHO}x{CYAN}r{RESET}-- ( Usuário: {CYAN}r{AMARELO}w{VERMELHO}x{RESET} | Grupo: {CYAN}r{RESET}-{VERMELHO}x{RESET} | Outros: {CYAN}r{RESET}--)\n")

    print(f"{BRANCO}🔢{AZUL} Permissões Numéricas:{RESET}")
    print(f"  {RESET}• {MAGENTA}7{RESET} = {CYAN}r{AMARELO}w{VERMELHO}x{RESET} ({MAGENTA}4{RESET}+{MAGENTA}2{RESET}+{MAGENTA}1{RESET}) → {CYAN}leitura{RESET} + {AMARELO}escrita{RESET} + {VERMELHO}execução")
    print(f"  {RESET}• {MAGENTA}6{RESET} = {CYAN}r{AMARELO}w{RESET}- ({MAGENTA}4{RESET}+{MAGENTA}2{RESET})   → {CYAN}leitura {RESET}+ {AMARELO}escrita")
    print(f"  {RESET}• {MAGENTA}5{RESET} = {CYAN}r{RESET}-{VERMELHO}x{RESET} ({MAGENTA}4{RESET}+{MAGENTA}1{RESET})   → {CYAN}leitura {RESET}+ {VERMELHO}execução")
    print(f"  {RESET}• {MAGENTA}4{RESET} = {CYAN}r{RESET}-- ({MAGENTA}4{RESET})     → {CYAN}somente leitura")
    print(f"  {RESET}• {MAGENTA}3{RESET} = {RESET}-{AMARELO}w{VERMELHO}x{RESET} ({MAGENTA}2{RESET}+{MAGENTA}1{RESET})   → {AMARELO}escrita {RESET}+ {VERMELHO}execução")
    print(f"  {RESET}• {MAGENTA}2{RESET} = {RESET}-{AMARELO}w{RESET}- ({MAGENTA}2{RESET})     → {AMARELO}somente escrita")
    print(f"  {RESET}• {MAGENTA}1{RESET} = {RESET}--{VERMELHO}x{RESET} ({MAGENTA}1{RESET})     → {VERMELHO}somente execução")
    print(f"  {RESET}• {MAGENTA}0{RESET} = {RESET}--- ({MAGENTA}0{RESET})     → sem permissões\n")

    print(f"{BRANCO}🎯{AZUL} Exemplos Comuns:{RESET}")
    print(f"  {RESET}• {MAGENTA}777{RESET} = {CYAN}r{AMARELO}w{VERMELHO}x{CYAN}r{AMARELO}w{VERMELHO}x{CYAN}r{AMARELO}w{VERMELHO}x{RESET} → todos têm total acesso")
    print(f"  {RESET}• {MAGENTA}755{RESET} = {CYAN}r{AMARELO}w{VERMELHO}x{CYAN}r{RESET}-{VERMELHO}x{CYAN}r{RESET}-{VERMELHO}x{RESET} → dono tudo, grupo/outros só leitura/execução")
    print(f"  {RESET}• {MAGENTA}700{RESET} = {CYAN}r{AMARELO}w{VERMELHO}x{RESET}------ → só o dono tem acesso total")
    print(f"  {RESET}• {MAGENTA}644{RESET} = {CYAN}r{AMARELO}w{RESET}-{CYAN}r{RESET}--{CYAN}r{RESET}-- → dono leitura/escrita, outros só leitura")
    print(f"  {RESET}• {MAGENTA}440{RESET} = {CYAN}r{RESET}--{CYAN}r{RESET}----- → leitura para dono e grupo, nenhum para outros\n")

    print(f"{RESET}+{'=' * 80}+\n")

# Carrega perguntas do arquivo CSV
def carregar_perguntas(caminho_arquivo):
    perguntas = []
    try:
        with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for linha in reader:
                perguntas.append({
                    'pergunta': linha['pergunta'],
                    'resposta': linha['resposta'],
                    'exemplo': linha.get('exemplo', '')
                })
    except FileNotFoundError:
        print(f"{VERMELHO}Arquivo '{caminho_arquivo}' não encontrado.{RESET}")
        sys.exit(1)
    return perguntas

# Limpa a tela do terminal
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{BRANCO}+{'=' * 80}+{RESET}")
# Exibe o resultado final do jogador
def mostrar_resultado(nome, acertos, erros, limite, total_csv):
    print(f"{RESET}+{'=' * 80}+")
    print(f"\n{BRANCO}📊 {AZUL}RESULTADO")
    print(f"\n{RESET}( {VERDE}Acertou {acertos} {RESET}/ {VERMELHO}Errou {erros} {RESET}/ {AMARELO}Limite {limite} {RESET}/ {BRANCO}Total {total_csv} {RESET})\n")

    percentual = (acertos / limite) * 100
    if percentual >= 80:
        print(f"{BRANCO}🎉 {VERDE}Excelente, {MAGENTA}{nome}{VERDE}! Você mandou muito bem!{RESET}")
    elif 50 <= percentual < 80:
        print(f"{BRANCO}👍 {CYAN}Bom trabalho, {MAGENTA}{nome}{CYAN}! Mas ainda pode melhorar!{RESET}")
    else:
        print(f"{BRANCO}💪 {VERMELHO}Não desanime, {MAGENTA}{nome}{VERMELHO}! Continue praticando!{RESET}")

    print(f"\n{RESET}Script desenvolvido por: {VERDE}BUG IT{RESET}\n")
    print(f"{BRANCO}+{'=' * 80}+{RESET}\n")

# Função principal do quiz
def quiz(perguntas):
    total_csv = len(perguntas)
    limite = min(total_csv, MAX_DESAFIOS)
    perguntas = random.sample(perguntas, limite)

    limpar_tela()
    mostrar_banner_e_conceitos()

    try:
        nome = input(f"{BRANCO}👤{AZUL} Qual o seu nome? {MAGENTA}").strip()
    except KeyboardInterrupt:
        print(f"\n{VERMELHO}Execução interrompida pelo usuário. Saindo...{RESET}")
        sys.exit(0)

    print(f"\n{VERDE}Olá, {MAGENTA}{nome}{VERDE}! Prepare-se para o desafio!{RESET}\n")
    input(f"Pressione ENTER para começar...{RESET}")

    acertos = 0
    erros = 0
    for i, p in enumerate(perguntas, 1):
        limpar_tela()
        mostrar_banner_e_conceitos()

        print(f"{BRANCO}🔐{AZUL} DESAFIO  ({AMARELO}{i}{AZUL}/{AMARELO}{limite}{AZUL}){RESET}\n")
        print(f"{VERDE}{p['pergunta']}{RESET}")
        if p['exemplo']:
            print(f"Exemplo: {AMARELO}{p['exemplo']}{RESET}\n")

        try:
            resposta = input(f"{CYAN}Resposta: {RESET}").strip()
        except KeyboardInterrupt:
            print(f"\n{VERMELHO}Execução interrompida pelo usuário. Saindo...{RESET}\n")
            mostrar_resultado(nome, acertos, erros, limite, total_csv)
            sys.exit(0)

        if resposta.lower() == p['resposta'].lower():
            print(f"{VERDE}✅ Resposta correta!{RESET}\n")
            acertos += 1
        else:
            print(f"{VERMELHO}❌ Resposta errada.{RESET} {VERDE}✅ Correto seria: {p['resposta']}{RESET}\n")
            erros += 1

        if i != limite:
            try:
                input(f"Pressione ENTER para continuar...{RESET}")
            except KeyboardInterrupt:
                print(f"\n{VERMELHO}Execução interrompida pelo usuário. Saindo...{RESET}\n")
                mostrar_resultado(nome, acertos, erros, limite, total_csv)
                sys.exit(0)

    mostrar_resultado(nome, acertos, erros, limite, total_csv)

# Ponto de entrada do script
if __name__ == "__main__":
    perguntas = carregar_perguntas('perguntas.csv')
    if not perguntas:
        print(f"{VERMELHO}Arquivo 'perguntas.csv' está vazio ou com formato incorreto.{RESET}")
    else:
        quiz(perguntas)
