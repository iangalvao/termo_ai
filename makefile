# Nome do ambiente virtual
VENV_NAME := .venv

# Comandos
PYTHON := python3
PIP := $(VENV_NAME)/bin/pip
ACTIVATE := . $(VENV_NAME)/bin/activate
REQUIREMENTS := requirements.txt
FREEZE_FILE := requirements-freeze.txt

# Alvo padrão
all: install

# Configura o ambiente virtual se não existir
setup-venv: $(REQUIREMENTS)
	@echo "Configurando o ambiente virtual..."
	@if [ ! -d "$(VENV_NAME)" ]; then \
		$(PYTHON) -m venv $(VENV_NAME); \
		$(ACTIVATE) && $(PIP) install --upgrade pip > /dev/null 2>&1; \
	fi

# Verifica e instala as dependências se necessário
check-deps: setup-venv
	@echo "Verificando dependências..."
	@$(ACTIVATE) && $(PIP) freeze | grep -F -f $(REQUIREMENTS) > $(FREEZE_FILE)
	@if ! cmp -s $(REQUIREMENTS) $(FREEZE_FILE); then \
		echo "Dependências não estão atualizadas, instalando..."; \
		$(ACTIVATE) && $(PIP) install -r $(REQUIREMENTS) > /dev/null 2>&1; \
	else \
		echo "Todas as dependências estão instaladas."; \
	fi
	@rm -f $(FREEZE_FILE)

# Instala as dependên

# Instala as dependências (só chamado por `check-deps`)
install: check-deps

# Executa o código Python
termo: install
	@echo "Executando o código..."
	@$(ACTIVATE) && $(PYTHON) -m game.mygame

# Remove o ambiente virtual e arquivos temporários
clean:
	@echo "Limpando o ambiente..."
	@rm -rf $(VENV_NAME)

.PHONY: all setup-venv check-deps install run clean
