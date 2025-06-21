from flask import Blueprint, request, jsonify
from src.models.escola import db, Turma, Aluno, Configuracao, HistoricoNotificacao
from datetime import datetime, date

escola_bp = Blueprint('escola', __name__)

# Modelos de mensagens predefinidas
MODELOS_MENSAGENS = {
    'faltas': """Escola {nome_escola}

Prezado(a) {responsavel_nome},

Informamos que o(a) aluno(a) {aluno_nome} da turma {turma_nome} faltou às aulas no dia {data_formatada}.

Solicitamos que entre em contato com a escola para esclarecimentos.""",
    'reuniao': """Escola {nome_escola}

Prezado(a) {responsavel_nome},

Convidamos para a reunião de pais e responsáveis do(a) aluno(a) {aluno_nome} da turma {turma_nome}, a ser realizada no dia {data_formatada}.

Sua presença é fundamental para discutirmos o desempenho escolar.""",
    'evento': """Escola {nome_escola}

Prezado(a) {responsavel_nome},

Convidamos você e o(a) aluno(a) {aluno_nome} da turma {turma_nome} para participar do evento escolar que ocorrerá no dia {data_formatada}.

Será uma oportunidade especial para integração e celebração.""",
    'convocacao': """Escola {nome_escola}

Prezado(a) {responsavel_nome},

Solicitamos sua presença urgente na escola para tratar de assuntos relacionados ao(a) aluno(a) {aluno_nome} da turma {turma_nome}.

Por favor, compareça o quanto antes.""",
    'feriado': """Escola {nome_escola}

Prezado(a) {responsavel_nome},

Informamos que não haverá aulas no dia {data_formatada} devido ao feriado escolar.

Retornaremos às atividades normalmente no próximo dia útil."""
}

# Rotas para Turmas
@escola_bp.route('/turmas', methods=['GET'])
def get_turmas():
    try:
        turmas = Turma.query.all()
        return jsonify([turma.to_dict() for turma in turmas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@escola_bp.route('/turmas', methods=['POST'])
def create_turma():
    try:
        data = request.get_json()
        
        if not data or 'nome' not in data or 'ano' not in data:
            return jsonify({'error': 'Nome e ano são obrigatórios'}), 400
        
        turma = Turma(
            nome=data['nome'],
            ano=data['ano']
        )
        
        db.session.add(turma)
        db.session.commit()
        
        return jsonify(turma.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@escola_bp.route('/turmas/<int:turma_id>', methods=['DELETE'])
def delete_turma(turma_id):
    try:
        turma = Turma.query.get_or_404(turma_id)
        db.session.delete(turma)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Rotas para Alunos
@escola_bp.route('/alunos', methods=['GET'])
def get_alunos():
    try:
        turma_id = request.args.get('turma_id', type=int)
        
        if turma_id:
            alunos = Aluno.query.filter_by(turma_id=turma_id).all()
        else:
            alunos = Aluno.query.all()
        
        return jsonify([aluno.to_dict() for aluno in alunos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@escola_bp.route('/alunos', methods=['POST'])
def create_aluno():
    try:
        data = request.get_json()
        
        required_fields = ['nome', 'turma_id', 'responsavel_nome', 'responsavel_telefone']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
        
        turma = Turma.query.get(data['turma_id'])
        if not turma:
            return jsonify({'error': 'Turma não encontrada'}), 404
        
        aluno = Aluno(
            nome=data['nome'],
            turma_id=data['turma_id'],
            responsavel_nome=data['responsavel_nome'],
            responsavel_telefone=data['responsavel_telefone']
        )
        
        db.session.add(aluno)
        db.session.commit()
        
        return jsonify(aluno.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@escola_bp.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    try:
        aluno = Aluno.query.get_or_404(aluno_id)
        db.session.delete(aluno)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Rotas para Configurações
@escola_bp.route('/configuracoes', methods=['GET'])
def get_configuracoes():
    try:
        configs = Configuracao.query.all()
        result = {}
        for config in configs:
            result[config.chave] = config.valor
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@escola_bp.route('/configuracoes', methods=['POST'])
def save_configuracoes():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        for chave, valor in data.items():
            config = Configuracao.query.filter_by(chave=chave).first()
            if config:
                config.valor = valor
            else:
                config = Configuracao(chave=chave, valor=valor)
                db.session.add(config)
        
        db.session.commit()
        return jsonify({'message': 'Configurações salvas com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Rota para envio de notificações
@escola_bp.route('/notificacoes/enviar', methods=['POST'])
def enviar_notificacoes():
    try:
        data = request.get_json()
        
        required_fields = ['alunos_ids', 'categoria']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Alunos e categoria são obrigatórios'}), 400
        
        alunos_ids = data['alunos_ids']
        categoria = data['categoria']
        data_evento_str = data.get('data_evento', '')
        mensagem_personalizada = data.get('mensagem_personalizada', '')
        
        # Validar categoria
        if categoria not in MODELOS_MENSAGENS:
            return jsonify({'error': 'Categoria inválida'}), 400
        
        # Validar data se necessário
        data_evento = None
        if categoria in ['faltas', 'reuniao', 'evento', 'feriado']:
            if not data_evento_str:
                return jsonify({'error': 'Data do evento é obrigatória para esta categoria'}), 400
            try:
                data_evento = datetime.strptime(data_evento_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        # Buscar configurações da escola
        nome_escola_config = Configuracao.query.filter_by(chave='nome_escola').first()
        nome_escola = nome_escola_config.valor if nome_escola_config else 'Escola'
        
        # Importar o bot do WhatsApp
        from src.whatsapp_bot import whatsapp_bot
        
        # Verificar se o WhatsApp está conectado
        status = whatsapp_bot.get_status()
        if not status['connected']:
            return jsonify({'error': 'WhatsApp não está conectado. Por favor, conecte primeiro.'}), 400
        
        resultados = []
        contacts_messages = []
        
        for aluno_id in alunos_ids:
            aluno = Aluno.query.get(aluno_id)
            if not aluno:
                resultados.append({
                    'aluno_id': aluno_id,
                    'status': 'erro',
                    'mensagem': 'Aluno não encontrado'
                })
                continue
            
            # Montar mensagem
            mensagem_template = MODELOS_MENSAGENS[categoria]
            mensagem = mensagem_template.format(
                nome_escola=nome_escola,
                responsavel_nome=aluno.responsavel_nome,
                aluno_nome=aluno.nome,
                turma_nome=aluno.turma.nome,
                data_formatada=data_evento.strftime('%d/%m/%Y') if data_evento else ''
            )
            
            if mensagem_personalizada:
                mensagem += f"\n\n{mensagem_personalizada}"
            
            mensagem += "\n\nAtenciosamente,\nSecretaria Escolar"
            
            # Adicionar à lista de mensagens para envio em lote
            contacts_messages.append({
                'phone': aluno.responsavel_telefone,
                'message': mensagem,
                'aluno_id': aluno.id,
                'aluno_nome': aluno.nome,
                'responsavel_nome': aluno.responsavel_nome
            })
        
        # Enviar mensagens em lote
        try:
            success, results = whatsapp_bot.send_bulk_messages(contacts_messages)
            
            if success:
                # Salvar no histórico
                for i, result in enumerate(results):
                    contact_info = contacts_messages[i]
                    
                    historico = HistoricoNotificacao(
                        aluno_id=contact_info['aluno_id'],
                        data_falta=data_evento,  # Armazena data_evento como data_falta
                        data_envio=datetime.now(),
                        mensagem=contact_info['message'],
                        status='enviado' if result['success'] else 'erro'
                    )
                    
                    db.session.add(historico)
                    
                    resultados.append({
                        'aluno_id': contact_info['aluno_id'],
                        'aluno_nome': contact_info['aluno_nome'],
                        'responsavel_nome': contact_info['responsavel_nome'],
                        'responsavel_telefone': result['phone'],
                        'status': 'enviado' if result['success'] else 'erro',
                        'mensagem': result['message']
                    })
                
                db.session.commit()
                
                enviados = len([r for r in resultados if r["status"] == "enviado"])
                return jsonify({
                    'message': f'Processamento concluído. {enviados} notificações enviadas.',
                    'resultados': resultados
                })
            else:
                return jsonify({'error': 'Erro ao enviar mensagens via WhatsApp'}), 500
                
        except Exception as e:
            return jsonify({'error': f'Erro no envio via WhatsApp: {str(e)}'}), 500
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Rota para histórico de notificações
@escola_bp.route('/notificacoes/historico', methods=['GET'])
def get_historico_notificacoes():
    try:
        aluno_id = request.args.get('aluno_id', type=int)
        limit = request.args.get('limit', type=int, default=50)
        
        query = HistoricoNotificacao.query
        
        if aluno_id:
            query = query.filter_by(aluno_id=aluno_id)
        
        historico = query.order_by(HistoricoNotificacao.data_envio.desc()).limit(limit).all()
        
        result = []
        for item in historico:
            item_dict = item.to_dict()
            item_dict['aluno_nome'] = item.aluno.nome
            item_dict['turma_nome'] = item.aluno.turma.nome
            result.append(item_dict)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para status do WhatsApp
@escola_bp.route('/whatsapp/status', methods=['GET'])
def get_whatsapp_status():
    try:
        from src.whatsapp_bot import whatsapp_bot
        status = whatsapp_bot.get_status()
        return jsonify({
            'conectado': status['connected'],
            'driver_ativo': status['driver_active'],
            'ultima_verificacao': datetime.now().isoformat(),
            'mensagem': 'WhatsApp Web conectado' if status['connected'] else 'WhatsApp Web não conectado'
        })
    except Exception as e:
        return jsonify({
            'conectado': False,
            'driver_ativo': False,
            'ultima_verificacao': datetime.now().isoformat(),
            'mensagem': f'Erro ao verificar status: {str(e)}'
        })

@escola_bp.route('/whatsapp/conectar', methods=['POST'])
def conectar_whatsapp():
    try:
        from src.whatsapp_bot import whatsapp_bot
        success, message, qr_code = whatsapp_bot.connect_whatsapp()
        
        return jsonify({
            'conectado': success,
            'mensagem': message,
            'qr_code': qr_code
        })
    except Exception as e:
        return jsonify({
            'conectado': False,
            'mensagem': f'Erro ao conectar: {str(e)}',
            'qr_code': None
        }), 500

@escola_bp.route('/whatsapp/aguardar-conexao', methods=['POST'])
def aguardar_conexao_whatsapp():
    try:
        from src.whatsapp_bot import whatsapp_bot
        
        if not whatsapp_bot.driver:
            return jsonify({
                'conectado': False,
                'mensagem': 'WhatsApp não foi inicializado'
            }), 400
        
        success, message = whatsapp_bot.wait_for_connection(timeout=90)
        
        return jsonify({
            'conectado': success,
            'mensagem': message
        })
    except Exception as e:
        return jsonify({
            'conectado': False,
            'mensagem': f'Erro ao aguardar conexão: {str(e)}'
        }), 500

@escola_bp.route('/whatsapp/verificar-status', methods=['GET'])
def verificar_status_whatsapp():
    try:
        from src.whatsapp_bot import whatsapp_bot
        
        if not whatsapp_bot.driver:
            return jsonify({
                'conectado': False,
                'mensagem': 'WhatsApp não foi inicializado',
                'qr_code': None
            })
        
        connected, message = whatsapp_bot.check_connection_status()
        
        return jsonify({
            'conectado': connected,
            'mensagem': message,
            'qr_code': whatsapp_bot.qr_code_base64
        })
    except Exception as e:
        return jsonify({
            'conectado': False,
            'mensagem': f'Erro ao verificar status: {str(e)}',
            'qr_code': None
        }), 500

@escola_bp.route('/whatsapp/desconectar', methods=['POST'])
def desconectar_whatsapp():
    try:
        from src.whatsapp_bot import whatsapp_bot
        success, message = whatsapp_bot.disconnect()
        
        return jsonify({
            'conectado': False,
            'mensagem': message
        })
    except Exception as e:
        return jsonify({
            'conectado': False,
            'mensagem': f'Erro ao desconectar: {str(e)}'
        }), 500
    
    