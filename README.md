# API de Gerenciamento de Motoristas e Caminhões

API REST desenvolvida em Flask para gerenciar motoristas, caminhões e suas atribuições.

## Estrutura do Projeto

```
/app/
  __init__.py → Cria e configura a aplicação Flask
  /models/
    __init__.py
    driver.py → Modelo de Motorista
    truck.py → Modelo de Caminhão
    assignment.py → Modelo de Atribuição
  /routes/
    __init__.py
    drivers.py → Rotas de Motoristas
    trucks.py → Rotas de Caminhões
    assignments.py → Rotas de Atribuições
  /utils/
    helpers.py → Funções auxiliares
config.py → Configurações da aplicação
run.py → Ponto de entrada da aplicação
```

## Requisitos

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-CORS

## Instalação

1. Clone o repositório:

```bash
git clone git@github.com:guintoki/trucks-backend.git
cd trucks-backend
```

2. Crie e ative o ambiente virtual:

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

No Linux/Mac:

```bash
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando o Projeto

1. Certifique-se de que o ambiente virtual está ativado (você verá `(venv)` no início do prompt)

2. Inicie o servidor de desenvolvimento:

```bash
python run.py
```

O servidor estará disponível em `http://localhost:5000`

## Endpoints da API

### Motoristas (Drivers)

- `GET /drivers` - Lista todos os motoristas
- `GET /drivers/<id>` - Obtém um motorista específico
- `POST /drivers` - Cria um novo motorista
- `PUT /drivers/<id>` - Atualiza um motorista
- `DELETE /drivers/<id>` - Remove um motorista

Exemplo de criação de motorista:

```json
{
  "name": "João Silva",
  "license_type": "E"
}
```

### Caminhões (Trucks)

- `GET /trucks` - Lista todos os caminhões
- `GET /trucks/<id>` - Obtém um caminhão específico
- `POST /trucks` - Cria um novo caminhão
- `PUT /trucks/<id>` - Atualiza um caminhão
- `DELETE /trucks/<id>` - Remove um caminhão

Exemplo de criação de caminhão:

```json
{
  "plate": "ABC1234",
  "min_license_type": "E"
}
```

### Atribuições (Assignments)

- `GET /assignments` - Lista todas as atribuições
- `GET /assignments/<id>` - Obtém uma atribuição específica
- `POST /assignments` - Cria uma nova atribuição
- `PUT /assignments/<id>` - Atualiza uma atribuição
- `DELETE /assignments/<id>` - Remove uma atribuição

Exemplo de criação de atribuição:

```json
{
  "driver_id": 1,
  "truck_id": 1,
  "date": "2024-04-03"
}
```

## Regras de Negócio

1. Tipos de Carteira (ordem crescente):

   - A
   - B
   - C
   - D
   - E

2. Validações:
   - Um motorista não pode ter mais de uma atribuição no mesmo dia
   - Um caminhão não pode ter mais de uma atribuição no mesmo dia
   - O motorista deve ter uma carteira compatível com o tipo mínimo exigido pelo caminhão
   - As datas devem estar no formato YYYY-MM-DD

## Configuração CORS

A API está configurada para aceitar requisições do frontend em `http://localhost:3000` com suporte a credenciais.

## Desenvolvimento

Para desenvolvimento, o servidor Flask está configurado com:

- Modo debug ativado
- Recarregamento automático
- CORS configurado para desenvolvimento local

## Gerenciando o Ambiente Virtual

- Para desativar o ambiente virtual:

```bash
deactivate
```

- Para atualizar as dependências após mudanças no requirements.txt:

```bash
pip install -r requirements.txt --upgrade
```

- Para ver as dependências instaladas:

```bash
pip freeze
```
