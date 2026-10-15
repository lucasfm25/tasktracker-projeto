"""TaskTracker: gerenciador simples de tarefas via terminal."""

import json
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
ARQUIVO_TAREFAS = DATA_DIR / "tarefas.json"

PRIORIDADES_VALIDAS = {
    "alta": "Alta",
    "média": "Média",
    "media": "Média",
    "baixa": "Baixa",
}
CAMPOS_OBRIGATORIOS = ("titulo", "descricao", "prioridade", "data_limite", "status")


def validar_titulo(titulo: str) -> bool:
    return bool(titulo and titulo.strip())


def normalizar_prioridade(valor: str) -> str | None:
    if not isinstance(valor, str):
        return None
    return PRIORIDADES_VALIDAS.get(valor.strip().casefold())


def carregar_tarefas(caminho: Path = ARQUIVO_TAREFAS) -> list[dict[str, str]]:
    if not caminho.exists():
        return []

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados: Any = json.load(arquivo)
    except json.JSONDecodeError as erro:
        raise ValueError(
            f"O arquivo {caminho} contém JSON inválido. "
            "Ele foi preservado para evitar perda de dados."
        ) from erro

    if not isinstance(dados, list):
        raise ValueError("O arquivo de tarefas deve conter uma lista JSON.")

    tarefas: list[dict[str, str]] = []
    for indice, tarefa in enumerate(dados, start=1):
        if not isinstance(tarefa, dict):
            raise ValueError(f"A tarefa número {indice} está em formato inválido.")

        if any(campo not in tarefa for campo in CAMPOS_OBRIGATORIOS):
            raise ValueError(f"A tarefa número {indice} não possui todos os campos obrigatórios.")

        if any(not isinstance(tarefa[campo], str) for campo in CAMPOS_OBRIGATORIOS):
            raise ValueError(f"A tarefa número {indice} possui campos com tipos inválidos.")

        if not validar_titulo(tarefa["titulo"]):
            raise ValueError(f"A tarefa número {indice} possui título vazio.")

        prioridade = normalizar_prioridade(tarefa["prioridade"])
        if prioridade is None:
            raise ValueError(f"A tarefa número {indice} possui prioridade inválida.")

        tarefa_validada = {campo: tarefa[campo] for campo in CAMPOS_OBRIGATORIOS}
        tarefa_validada["prioridade"] = prioridade
        tarefas.append(tarefa_validada)

    return tarefas


def salvar_tarefas(tarefas: list[dict[str, str]], caminho: Path = ARQUIVO_TAREFAS) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    arquivo_temporario = caminho.with_suffix(caminho.suffix + ".tmp")

    try:
        with arquivo_temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)
            arquivo.write("\n")
        arquivo_temporario.replace(caminho)
    finally:
        if arquivo_temporario.exists():
            arquivo_temporario.unlink()


def pedir_titulo() -> str:
    while True:
        titulo = input("Título da tarefa: ").strip()
        if validar_titulo(titulo):
            return titulo
        print("Erro: o título é obrigatório e não pode conter apenas espaços.")


def pedir_prioridade() -> str:
    while True:
        valor = input("Prioridade (Alta/Média/Baixa): ")
        prioridade = normalizar_prioridade(valor)
        if prioridade is not None:
            return prioridade
        print("Erro: escolha somente Alta, Média ou Baixa.")


def cadastrar_tarefa(tarefas: list[dict[str, str]]) -> None:
    print("\n--- Cadastro de tarefa ---")
    titulo = pedir_titulo()
    descricao = input("Descrição: ").strip()
    prioridade = pedir_prioridade()
    data_limite = input("Data limite (por exemplo 25/12/2026): ").strip()

    nova_tarefa = {
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "data_limite": data_limite,
        "status": "Pendente",
    }

    tarefas_atualizadas = [*tarefas, nova_tarefa]
    try:
        salvar_tarefas(tarefas_atualizadas)
    except OSError as erro:
        print(f"Não foi possível salvar a tarefa: {erro}")
        print("A tarefa não foi adicionada à lista. Verifique as permissões da pasta.")
        return

    tarefas.append(nova_tarefa)
    print("Tarefa cadastrada e salva com sucesso!")


def visualizar_tarefas(tarefas: list[dict[str, str]]) -> None:
    print("\n--- Tarefas cadastradas ---")
    if not tarefas:
        print("Nenhuma tarefa cadastrada no momento.")
        return

    for numero, tarefa in enumerate(tarefas, start=1):
        print(f"\nTarefa {numero}")
        print(f"  Título:      {tarefa['titulo']}")
        print(f"  Descrição:   {tarefa['descricao'] or 'Não informada'}")
        print(f"  Prioridade:  {tarefa['prioridade']}")
        print(f"  Data limite: {tarefa['data_limite'] or 'Não informada'}")
        print(f"  Status:      {tarefa['status']}")

    print(f"\nTotal de tarefas: {len(tarefas)}")


def executar_menu(tarefas: list[dict[str, str]]) -> None:
    while True:
        print("\n========== TASKTRACKER ==========")
        print("1. Cadastrar nova tarefa")
        print("2. Visualizar tarefas cadastradas")
        print("3. Sair da aplicação")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_tarefa(tarefas)
        elif opcao == "2":
            visualizar_tarefas(tarefas)
        elif opcao == "3":
            print("Até mais! Suas tarefas salvas estarão disponíveis na próxima execução.")
            return
        else:
            print("Opção inválida. Digite 1, 2 ou 3.")


def main() -> None:
    try:
        tarefas = carregar_tarefas()
    except (OSError, ValueError) as erro:
        print(f"Não foi possível carregar as tarefas: {erro}")
        print("Corrija o arquivo indicado antes de executar novamente.")
        return

    print("Bem-vindo ao TaskTracker!")
    try:
        executar_menu(tarefas)
    except (KeyboardInterrupt, EOFError):
        print("\nAplicação encerrada. As tarefas já salvas foram preservadas.")


if __name__ == "__main__":
    main()
