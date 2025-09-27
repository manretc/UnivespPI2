# docs/conf.py
# Ficheiro de configuração para o Sphinx.

import os
import sys
# Aponta para a pasta raiz do projeto para que o Sphinx possa encontrar os módulos da app
sys.path.insert(0, os.path.abspath('..'))

# -- Informações do Projeto -----------------------------------------------------

project = 'Rede de Doações'
copyright = '2024, Seu Nome'
author = 'Seu Nome'

# -- Configurações Gerais ---------------------------------------------------

# Adiciona as extensões do Sphinx que vamos usar. 'autodoc' é a mais importante.
extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'pt_BR'

# -- Opções para a saída HTML -------------------------------------------------

# O tema visual da sua documentação. 'alabaster' é o padrão.
html_theme = 'alabaster'
html_static_path = ['_static']
