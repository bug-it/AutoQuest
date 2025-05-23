import csv
import random
import os
import sys

# Cores ANSI para terminal
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

MAX_DESAFIOS = 20  # Limite de perguntas por execução

# Banner ASCII AUTOQUEST
BANNER = r"""
 █████╗ ██╗   ██╗████████╗ ██████╗      ██████╗ ██╗   ██╗███████╗███████╗████████╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗    ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
███████║██║   ██║   ██║   ██║   ██║    ██║   ██║██║   ██║█████╗  ███████╗   ██║   
██╔══██║██║   ██║   ██║   ██║   ██║    ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   
██║  ██║╚██████╔╝   ██║   ╚██████╔╝    ╚██████╔╝╚██████╔╝███████╗███████║   ██║   
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝      ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
"""

def mostrar_banner_e_conceitos():
    print(BANNER)
    print(f"{BLUE}{BOLD}📘 CONCEITOS BÁSICOS{RESET}")
    print(f"{BLUE}" + "=" * 80 + f"{RESET}")

    print(f"{YELLOW}{BOLD}🧠 Permissões no Linux:{RESET}")
    print(f"  {CYAN}• r{RESET} = {GREEN}leitura (read){RESET}")
    print(f"  {CYAN}• w{RESET} = {GREEN}escrita (write){RESET}")
    print(f"  {CYAN}• x{RESET} = {GREEN}execução (execute){RESET}\n")

    print(f"{YELLOW}{BOLD}🧾 Ordem: Usuário (owner) | Grupo (group) | Outros (others){RESET}")
    print(f"  {MAGENTA}Exemplo: -rwxr-xr--{RESET} (Usuário: {GREEN}rwx{RESET} | Grupo: {GREEN}r-x{RESET} | Outros: {GREEN}r--{RESET})\n")

    print(f"{YELLOW}{BOLD}🔢 Permissões Numéricas:{RESET}")
    print(f"  {CYAN}• 7{RESET} = {GREEN}rwx (4+2+1){RESET} - leitura, escrita e execução")
    print(f"  {CYAN}• 6{RESET} = {GREEN}rw- (4+2){RESET}   - leitura e escrita")
    print(f"  {CYAN}• 5{RESET} = {GREEN}r-x (4+1){RESET}   - leitura e execução")
    print(f"  {CYAN}• 4{RESET} = {GREEN}r-- (4){RESET}     - somente leitura")
    print(f"  {CYAN}• 3{RESET} = {GREEN}-wx (2+1){RESET}   - escrita e execução")
    print(f"  {CYAN}• 2{RESET} = {GREEN}-w- (2){RESET}     - somente escrita")
    print(f"  {CYAN}• 1{RESET} = {GREEN}--x (1){RESET}     - somente execução")
    print(f"  {CYAN}• 0{RESET} = {GREEN}--- (0){RESET}     - sem permissões\n")

    print(f"{YELLOW}{BOLD}🎯 Exemplos Comuns:{RESET}")
    print(f"  {CYAN}• 777{RESET} = {GREEN}rwxrwxrwx{RESET} → todos têm total acesso")
    print(f"  {CYAN}• 755{RESET} = {GREEN}rwxr-xr-x{RESET} → dono tudo, grupo/outros só leitura/execução")
    print(f"  {CYAN}• 700{RESET} = {GREEN}rwx------{RESET} → só o dono tem acesso total")
    print(f"  {CYAN}• 644{RESET} = {GREEN}rw-r--r--{RESET} → dono leitura/escrita, outros só leitura")
    print(f"  {CYAN}• 440{RESET} = {GREEN}r--r-----{RESET} → leitura para dono e grupo, nenhum para outros")

    print(f"{BLUE}" + "=" * 80 + f"{RESET}\n")

def carregar_perguntas(caminho_arquivo):
    perguntas = []
    with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for linha in reader:
            perguntas.append({
                'pergunta': linha['pergunta'],
                'resposta': linha['resposta'],
                'exemplo': linha.get('exemplo', '')
            })
    return perguntas

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_resultado(acertos, erros, limite, total_csv):
    print(f"\n{YELLOW}{BOLD}Resultado {RESET}( {GREEN}Acertou {acertos} {RESET}/ {RED}Errou {erros} {RESET}/ {YELLOW}Limite {limite} {RESET}/ {WHITE}Total {total_csv} {RESET})\n")

def quiz(perguntas):
    total_csv = len(perguntas)
    limite = min(total_csv, MAX_DESAFIOS)
    perguntas = random.sample(perguntas, limite)

    limpar_tela()
    mostrar_banner_e_conceitos()

    try:
        input(f"{BOLD}Pressione ENTER para começar os desafios...{RESET}")
    except KeyboardInterrupt:
        print(f"\n{RED}Execução interrompida pelo usuário. Saindo...{RESET}")
        mostrar_resultado(0, 0, limite, total_csv)
        sys.exit(0)

    acertos = 0
    erros = 0
    for i, p in enumerate(perguntas, 1):
        limpar_tela()
        mostrar_banner_e_conceitos()

        print(f"{BOLD}{MAGENTA}🔐 DESAFIO  ({i}/{limite}){RESET}\n")
        print(f"{BOLD}{BLUE}{p['pergunta']}{RESET}")
        if p['exemplo']:
            print(f"Exemplo: {YELLOW}{p['exemplo']}{RESET}\n")

        try:
            resposta = input(f"{CYAN}Resposta: {RESET}").strip()
        except KeyboardInterrupt:
            print(f"\n{RED}Execução interrompida pelo usuário. Saindo...{RESET}")
            mostrar_resultado(acertos, erros, limite, total_csv)
            sys.exit(0)

        if resposta.lower() == p['resposta'].lower():
            print(f"{GREEN}✅ Resposta correta!{RESET}\n")
            acertos += 1
        else:
            print(f"{RED}❌ Resposta errada.{RESET} {GREEN}✅ Correto seria: {p['resposta']}{RESET}\n")
            erros += 1

        if i != limite:
            try:
                input(f"{BOLD}Pressione ENTER para continuar...{RESET}")
            except KeyboardInterrupt:
                print(f"\n{RED}Execução interrompida pelo usuário. Saindo...{RESET}")
                mostrar_resultado(acertos, erros, limite, total_csv)
                sys.exit(0)

    mostrar_resultado(acertos, erros, limite, total_csv)

if __name__ == "__main__":
    try:
        perguntas = carregar_perguntas('perguntas.csv')
        if not perguntas:
            print(f"{RED}Arquivo 'perguntas.csv' não contém perguntas.{RESET}")
        else:
            quiz(perguntas)
    except FileNotFoundError:
        print(f"{RED}Arquivo 'perguntas.csv' não encontrado. Coloque ele na mesma pasta do script.{RESET}")
    except Exception as e:
        print(f"{RED}Erro inesperado: {e}{RESET}")



