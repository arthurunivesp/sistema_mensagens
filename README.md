# Notificador de Faltas - WhatsApp

Sistema de notificação automática via WhatsApp para responsáveis de alunos faltosos.

## Descrição

O **Notificador de Faltas - WhatsApp** é um aplicativo web desenvolvido em Flask que permite às escolas enviar notificações automáticas via WhatsApp para os responsáveis de alunos que faltaram às aulas. O sistema oferece uma interface intuitiva para gerenciar turmas, alunos e enviar mensagens em lote de forma eficiente.

## Características Principais

- **Gerenciamento de Turmas**: Adicione, edite e remova turmas escolares
- **Cadastro de Alunos**: Registre alunos com informações dos responsáveis
- **Envio Automático**: Envie notificações em lote via WhatsApp Web
- **Interface Intuitiva**: Interface web responsiva e fácil de usar
- **Histórico de Notificações**: Acompanhe todas as mensagens enviadas
- **Backup e Restauração**: Exporte e importe dados do sistema

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite
- **Automação WhatsApp**: Selenium WebDriver
- **Estilo**: CSS customizado com design responsivo

## Pré-requisitos

- Python 3.11 ou superior
- Google Chrome instalado
- Conexão com a internet
- Conta do WhatsApp

## Instalação

### 1. Clone ou baixe o projeto

```bash
# Se você tem o código em um repositório
git clone <url-do-repositorio>
cd whatsapp-notificador

# Ou extraia o arquivo ZIP baixado
```

### 2. Crie e ative o ambiente virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Linux/Mac
source venv/bin/activate

# Ativar no Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o aplicativo

```bash
python src/main.py
```

O aplicativo estará disponível em: `http://localhost:5000`

## Como Usar

### 1. Configuração Inicial

1. Acesse a aba **"Configurações"**
2. Preencha o nome da escola e telefone
3. Clique em **"Salvar Configurações"**

### 2. Conectar ao WhatsApp

1. Na aba **"Configurações"**, clique em **"Conectar WhatsApp"**
2. Uma janela do Chrome será aberta com o WhatsApp Web
3. Escaneie o QR Code com seu celular
4. Aguarde a confirmação de conexão

### 3. Gerenciar Turmas

1. Acesse a aba **"Gerenciar Turmas"**
2. Preencha o nome da turma e ano/série
3. Clique em **"Adicionar Turma"**

### 4. Cadastrar Alunos

1. Acesse a aba **"Gerenciar Alunos"**
2. Preencha as informações do aluno:
   - Nome completo
   - Turma
   - Nome do responsável
   - Telefone do responsável (com DDD)
3. Clique em **"Adicionar Aluno"**

### 5. Enviar Notificações

1. Acesse a aba **"Enviar Notificações"**
2. Selecione a turma
3. Escolha a data da falta
4. Marque os alunos faltosos
5. Adicione uma mensagem personalizada (opcional)
6. Clique em **"📱 Enviar Notificações via WhatsApp"**

## Estrutura do Projeto

```
whatsapp-notificador/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── escola.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── escola.py
│   ├── static/
│   │   └── index.html
│   ├── database/
│   │   └── app.db
│   ├── main.py
│   └── whatsapp_bot.py
├── venv/
├── requirements.txt
└── README.md
```

## Funcionalidades Detalhadas

### Gerenciamento de Turmas
- Adicionar novas turmas com nome e ano/série
- Visualizar lista de turmas cadastradas
- Remover turmas (apenas se não houver alunos vinculados)

### Gerenciamento de Alunos
- Cadastro completo com dados do responsável
- Filtro por turma
- Edição e remoção de alunos
- Validação de dados obrigatórios

### Sistema de Notificações
- Seleção múltipla de alunos faltosos
- Mensagem padrão personalizada por escola
- Mensagem adicional opcional
- Envio em lote com controle de intervalo
- Histórico completo de envios

### Integração WhatsApp
- Conexão via WhatsApp Web
- Automação com Selenium
- Detecção automática de QR Code
- Tratamento de erros de conexão
- Status de conexão em tempo real

## Mensagem Padrão

O sistema envia automaticamente uma mensagem no seguinte formato:

```
Escola [Nome da Escola]

Prezado(a) [Nome do Responsável],

Informamos que o(a) aluno(a) [Nome do Aluno] da turma [Nome da Turma] faltou às aulas no dia [Data da Falta].

Solicitamos que entre em contato com a escola para esclarecimentos.

[Mensagem Personalizada - se fornecida]

Atenciosamente,
Secretaria Escolar
```

## Backup e Restauração

### Exportar Dados
1. Acesse **"Configurações"**
2. Clique em **"Exportar Dados"**
3. Um arquivo JSON será baixado com todos os dados

### Importar Dados
1. Acesse **"Configurações"**
2. Clique em **"Importar Dados"**
3. Selecione o arquivo JSON de backup
4. Confirme a importação

## Solução de Problemas

### WhatsApp não conecta
- Verifique se o Chrome está instalado
- Certifique-se de que o WhatsApp Web está funcionando no navegador
- Tente desconectar e conectar novamente
- Verifique a conexão com a internet

### Mensagens não são enviadas
- Confirme se o WhatsApp está conectado (status na aba Configurações)
- Verifique se os números de telefone estão corretos (com DDD)
- Certifique-se de que os contatos têm WhatsApp
- Aguarde alguns segundos entre envios para evitar bloqueios

### Erro ao adicionar alunos/turmas
- Verifique se todos os campos obrigatórios estão preenchidos
- Certifique-se de que não há caracteres especiais nos nomes
- Tente recarregar a página

## Limitações e Considerações

### Limitações Técnicas
- Requer conexão constante com a internet
- Depende da estabilidade do WhatsApp Web
- Limitado pela política de uso do WhatsApp
- Não funciona com WhatsApp Business API oficial

### Considerações de Uso
- **Uso Responsável**: Este sistema utiliza automação não oficial do WhatsApp
- **Risco de Bloqueio**: O uso excessivo pode resultar em bloqueio temporário da conta
- **Intervalos**: Respeite intervalos entre mensagens (3 segundos por padrão)
- **Termos de Serviço**: O uso é de responsabilidade do usuário

### Recomendações
- Use apenas para notificações escolares legítimas
- Não envie spam ou mensagens promocionais
- Mantenha intervalos adequados entre envios
- Monitore o status da conexão regularmente
- Faça backups regulares dos dados

## Suporte e Manutenção

### Logs do Sistema
Os logs são exibidos no console onde o aplicativo está executando. Para debugar problemas:

1. Execute o aplicativo no terminal
2. Observe as mensagens de erro
3. Verifique a conectividade do WhatsApp
4. Reinicie o aplicativo se necessário

### Atualizações
Para manter o sistema funcionando:

1. Mantenha o Chrome atualizado
2. Verifique atualizações das dependências Python
3. Monitore mudanças no WhatsApp Web
4. Faça backups antes de atualizações

## Desenvolvimento e Personalização

### Estrutura do Código
- `main.py`: Ponto de entrada da aplicação
- `models/`: Modelos de dados (SQLAlchemy)
- `routes/`: Rotas da API REST
- `whatsapp_bot.py`: Lógica de automação do WhatsApp
- `static/index.html`: Interface do usuário

### Personalizações Possíveis
- Modificar template de mensagem
- Adicionar novos campos de aluno
- Implementar relatórios
- Integrar com outros sistemas escolares
- Adicionar autenticação de usuários

## Licença e Responsabilidade

Este software é fornecido "como está", sem garantias de qualquer tipo. O uso é de inteira responsabilidade do usuário, incluindo o cumprimento dos termos de serviço do WhatsApp.

**Importante**: Este sistema utiliza automação não oficial do WhatsApp Web. O WhatsApp pode alterar suas políticas ou interface a qualquer momento, o que pode afetar o funcionamento do sistema.

## Contato e Suporte

Para dúvidas, sugestões ou problemas:
- Consulte a documentação acima
- Verifique os logs do sistema
- Teste a conectividade básica do WhatsApp Web

---

**Desenvolvido para facilitar a comunicação entre escolas e responsáveis, promovendo maior transparência no acompanhamento escolar.**

