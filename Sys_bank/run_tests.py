import pytest, sys, os

#Diretótio dos testes
tests_dir = os.path.join(os.path.dirname(__file__), "tests")


# Diretório para salvar relatórios
reports_dir = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(reports_dir, exist_ok=True)

# Arquivo de saída do relatório HTML
report_file = os.path.join(os.path.dirname(__file__), "relatorio_testes.html")

# Executa os testes
# -v : verbose
# --html : gera relatório HTML
exit_code = pytest.main([tests_dir, "-v", f"--html={report_file}"])

sys.exit(exit_code)