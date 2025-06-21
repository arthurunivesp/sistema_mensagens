from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.String(50), nullable=False)
    
    # Relacionamento com alunos
    alunos = db.relationship('Aluno', backref='turma', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Turma {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'ano': self.ano
        }

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    responsavel_nome = db.Column(db.String(200), nullable=False)
    responsavel_telefone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Aluno {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'turma_id': self.turma_id,
            'responsavel': {
                'nome': self.responsavel_nome,
                'telefone': self.responsavel_telefone
            }
        }

class Configuracao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Configuracao {self.chave}>'

    def to_dict(self):
        return {
            'chave': self.chave,
            'valor': self.valor
        }

class HistoricoNotificacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    data_falta = db.Column(db.Date, nullable=False)
    data_envio = db.Column(db.DateTime, nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # 'enviado', 'erro', 'pendente'
    
    # Relacionamento com aluno
    aluno = db.relationship('Aluno', backref='notificacoes')

    def __repr__(self):
        return f'<HistoricoNotificacao {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'aluno_id': self.aluno_id,
            'data_falta': self.data_falta.isoformat() if self.data_falta else None,
            'data_envio': self.data_envio.isoformat() if self.data_envio else None,
            'mensagem': self.mensagem,
            'status': self.status
        }

