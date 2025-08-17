# 1. Crie a pasta principal do projeto e entre nela
mkdir rede_doacoes
cd rede_doacoes

# 2. Crie a estrutura de pastas principal
mkdir app
mkdir app\static
mkdir app\static\css
mkdir app\templates
mkdir tests
mkdir migrations

# 3. Crie os arquivos Python vazios
type nul > run.py
type nul > config.py
type nul > .env
type nul > requirements.txt
type nul > .gitignore
type nul > app\__init__.py
type nul > app\models.py
type nul > app\routes.py
type nul > app\forms.py

# 4. Crie os arquivos de template HTML vazios
type nul > app\templates\base.html
type nul > app\templates\index.html
type nul > app\templates\login.html
type nul > app\templates\register.html
type nul > app\templates\dashboard.html
type nul > app\templates\create_donation.html

# 5. Crie o arquivo de teste inicial
type nul > tests\__init__.py
type nul > tests\test_basic.py