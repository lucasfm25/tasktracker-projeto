import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import carregar_tarefas, normalizar_prioridade, salvar_tarefas, validar_titulo


class TestValidacoes(unittest.TestCase):
    def test_titulo_valido(self):
        self.assertTrue(validar_titulo("Estudar Python"))

    def test_titulo_vazio_ou_so_com_espacos_e_invalido(self):
        self.assertFalse(validar_titulo(""))
        self.assertFalse(validar_titulo("   \t  "))

    def test_prioridades_validas_sao_padronizadas(self):
        self.assertEqual(normalizar_prioridade("alta"), "Alta")
        self.assertEqual(normalizar_prioridade("MÉDIA"), "Média")
        self.assertEqual(normalizar_prioridade("Media"), "Média")
        self.assertEqual(normalizar_prioridade("baixa"), "Baixa")

    def test_prioridade_invalida_retorna_none(self):
        self.assertIsNone(normalizar_prioridade("Urgente"))
        self.assertIsNone(normalizar_prioridade(""))


class TestPersistencia(unittest.TestCase):
    def test_arquivo_inexistente_retorna_lista_vazia(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "tarefas.json"
            self.assertEqual(carregar_tarefas(caminho), [])

    def test_salvar_e_carregar_preserva_os_dados(self):
        tarefas = [
            {
                "titulo": "Estudar Python",
                "descricao": "Revisar listas",
                "prioridade": "Alta",
                "data_limite": "25/12/2026",
                "status": "Pendente",
            }
        ]
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "dados" / "tarefas.json"
            salvar_tarefas(tarefas, caminho)
            self.assertEqual(carregar_tarefas(caminho), tarefas)


if __name__ == "__main__":
    unittest.main()
