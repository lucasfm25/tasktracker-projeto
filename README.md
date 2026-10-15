# TaskTracker

Gerenciador simples de tarefas executado no terminal, desenvolvido em Python 3 para a Fase 2 do Bootcamp II.

## Funcionalidades

- Cadastrar tarefas com título, descrição, prioridade, data limite e status.
- Exigir um título que não esteja vazio ou composto apenas por espaços.
- Aceitar somente as prioridades **Alta**, **Média** (também aceita `Media`) e **Baixa**, sem diferenciar maiúsculas e minúsculas.
- Definir automaticamente o status inicial como **Pendente**.
- Listar as tarefas cadastradas com os campos organizados.
- Salvar as tarefas em `data/tarefas.json`, mantendo os registros entre execuções.
- Tratar opções inválidas do menu e preservar o arquivo de dados se ele estiver com formato inválido.

## Tecnologias

- Python 3.10 ou superior
- Biblioteca padrão do Python (`json` e `pathlib`)
- `unittest` para os testes automatizados

Não é necessário instalar bibliotecas externas.

## Estrutura do projeto

```text
tasktracker-projeto/
├── README.md
├── .gitignore
├── docs/
│   └── planejamento_logico.pdf
├── data/
│   └── .gitkeep
├── src/
│   └── main.py
└── tests/
    └── test_main.py
```

O arquivo `data/tarefas.json` é criado automaticamente após o primeiro cadastro.

## Requisitos

Ter Python 3.10 ou superior instalado. No Windows, confira no PowerShell:

```powershell
py --version
```

## Como executar

Abra o terminal na pasta `tasktracker-projeto` e execute:

```powershell
py src/main.py
```

Se o comando `py` não estiver disponível, tente:

```powershell
python src/main.py
```

Use o menu para cadastrar tarefas, visualizar a lista ou sair. Os registros salvos continuam disponíveis quando o programa for aberto novamente.

## Como executar os testes

Na pasta raiz do projeto:

```powershell
py -m unittest discover -s tests -v
```

Os testes verificam a validação do título, as prioridades permitidas e a leitura/gravação dos dados.

## Exemplo de uso

```text
========== TASKTRACKER ==========
1. Cadastrar nova tarefa
2. Visualizar tarefas cadastradas
3. Sair da aplicação
Escolha uma opção: 1

--- Cadastro de tarefa ---
Título da tarefa (Obrigatório): Estudar Python
Descrição: Revisar funções e listas
Prioridade (Alta/Média/Baixa): média
Data limite: 25/12/2026
Tarefa cadastrada e salva com sucesso!
```