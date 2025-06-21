from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.escola import db

class MensagemTemplate(db.Model):
    __tablename__ = 'mensagem_template'
    
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    template = db.Column(db.Text, nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'categoria': self.categoria,
            'titulo': self.titulo,
            'template': self.template,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

# Templates padrão para inicialização
TEMPLATES_PADRAO = [
    {
        'categoria': 'Alunos Faltosos',
        'titulo': 'Notificação de Falta',
        'template': '''Escola [Nome da Escola]

Prezado(a) [Nome do Responsável],

Informamos que o(a) aluno(a) [Nome do Aluno] da turma [Turma] faltou às aulas no dia [Data].

Solicitamos que entre em contato com a escola para esclarecimentos.

Atenciosamente,
Secretaria Escolar'''
    },
    {
        'categoria': 'Reunião de Pais',
        'titulo': 'Convocação para Reunião de Pais',
        'template': '''Escola [Nome da Escola]

Prezado(a) [Nome do Responsável],

Convocamos V.Sa. para participar da Reunião de Pais referente ao(à) aluno(a) [Nome do Aluno] da turma [Turma].

📅 Data: [Data]
🕐 Horário: [Horário]
📍 Local: [Local]

Sua presença é fundamental para o acompanhamento do desenvolvimento escolar de seu(sua) filho(a).

Atenciosamente,
Direção Escolar'''
    },
    {
        'categoria': 'Evento na Escola',
        'titulo': 'Convite para Evento Escolar',
        'template': '''Escola [Nome da Escola]

Prezado(a) [Nome do Responsável],

Temos o prazer de convidar V.Sa. e o(a) aluno(a) [Nome do Aluno] da turma [Turma] para participar do nosso evento:

🎉 Evento: [Nome do Evento]
📅 Data: [Data]
🕐 Horário: [Horário]
📍 Local: [Local]

Será um momento especial de confraternização e aprendizado. Contamos com a presença de toda a família!

Atenciosamente,
Equipe Escolar'''
    },
    {
        'categoria': 'Convocação do Responsável',
        'titulo': 'Convocação Urgente',
        'template': '''Escola [Nome da Escola]

Prezado(a) [Nome do Responsável],

Solicitamos urgentemente sua presença na escola para tratar de assuntos relacionados ao(à) aluno(a) [Nome do Aluno] da turma [Turma].

📅 Data: [Data]
🕐 Horário: [Horário]
📍 Local: Secretaria Escolar

Por favor, compareça no horário agendado ou entre em contato conosco para reagendar.

Atenciosamente,
Coordenação Pedagógica'''
    },
    {
        'categoria': 'Feriados na Escola',
        'titulo': 'Comunicado de Feriado/Recesso',
        'template': '''Escola [Nome da Escola]

Prezado(a) [Nome do Responsável],

Informamos que não haverá aulas no(s) seguinte(s) dia(s):

📅 Data(s): [Data]
📝 Motivo: [Motivo do Feriado]

As atividades escolares serão retomadas normalmente em [Data de Retorno].

Aproveitamos para desejar um excelente período de descanso para toda a família!

Atenciosamente,
Direção Escolar'''
    }
]

