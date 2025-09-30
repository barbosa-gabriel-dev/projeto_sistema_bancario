import pytest, sys, os

# Diretório base do projeto
base_dir = os.path.dirname(__file__)

# Diretório dos testes
tests_dir = os.path.join(base_dir, "tests")

# Arquivo de teste específico
test_database = os.path.join(tests_dir, "test_database.py")

# Diretório para salvar relatórios
reports_dir = os.path.join(base_dir, "reports")
os.makedirs(reports_dir, exist_ok=True)

# Arquivo de saída do relatório HTML
report_file = os.path.join(base_dir, "relatorio_testes.html")

# Executa os testes
# -v : verbose
# --html : gera relatório HTML
exit_code = pytest.main([tests_dir, test_database, "-v", f"--html={report_file}"])

sys.exit(exit_code)
