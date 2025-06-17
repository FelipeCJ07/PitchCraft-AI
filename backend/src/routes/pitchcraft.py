from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from src.models.pitchcraft import db, Project, User, Presentation, ClientProfile, MarketIntelligence, Objection
from src.services.ai_service import AIService
from src.services.data_integration import DataIntegrationService
import json

pitchcraft_bp = Blueprint('pitchcraft', __name__)
ai_service = AIService()
data_service = DataIntegrationService()

@pitchcraft_bp.route('/projects', methods=['GET'])
@cross_origin()
def get_projects():
    """Listar todos os projetos"""
    try:
        projects = Project.query.all()
        return jsonify([{
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'project_type': p.project_type,
            'status': p.status,
            'created_at': p.created_at.isoformat(),
            'updated_at': p.updated_at.isoformat()
        } for p in projects])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pitchcraft_bp.route('/projects', methods=['POST'])
@cross_origin()
def create_project():
    """Criar um novo projeto"""
    try:
        data = request.get_json()
        
        # Criar usuário se não existir
        user = User.query.filter_by(email=data.get('user_email', 'demo@pitchcraft.ai')).first()
        if not user:
            user = User(
                email=data.get('user_email', 'demo@pitchcraft.ai'),
                name=data.get('user_name', 'Demo User'),
                company=data.get('user_company', 'Demo Company')
            )
            db.session.add(user)
            db.session.commit()
        
        project = Project(
            user_id=user.id,
            title=data['title'],
            description=data.get('description', ''),
            project_type=data.get('project_type', 'pitch_vendas'),
            target_audience=data.get('target_audience', ''),
            status='draft'
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'project_type': project.project_type,
            'status': project.status,
            'created_at': project.created_at.isoformat()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pitchcraft_bp.route('/projects/<int:project_id>', methods=['GET'])
@cross_origin()
def get_project(project_id):
    """Obter detalhes de um projeto específico"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # Buscar dados relacionados
        presentations = Presentation.query.filter_by(project_id=project_id).all()
        client_profile = ClientProfile.query.filter_by(project_id=project_id).first()
        market_intelligence = MarketIntelligence.query.filter_by(project_id=project_id).first()
        objections = Objection.query.filter_by(project_id=project_id).all()
        
        return jsonify({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'project_type': project.project_type,
            'target_audience': project.target_audience,
            'status': project.status,
            'created_at': project.created_at.isoformat(),
            'updated_at': project.updated_at.isoformat(),
            'presentations': [{
                'id': p.id,
                'title': p.title,
                'content': json.loads(p.content) if p.content else None,
                'style_config': json.loads(p.style_config) if p.style_config else None,
                'created_at': p.created_at.isoformat()
            } for p in presentations],
            'client_profile': {
                'company_name': client_profile.company_name if client_profile else None,
                'industry': client_profile.industry if client_profile else None,
                'size': client_profile.size if client_profile else None,
                'disc_profile': client_profile.disc_profile if client_profile else None,
                'pain_points': client_profile.pain_points if client_profile else None,
                'goals': client_profile.goals if client_profile else None,
                'decision_makers': json.loads(client_profile.decision_makers) if client_profile and client_profile.decision_makers else None
            } if client_profile else None,
            'market_intelligence': {
                'industry_trends': json.loads(market_intelligence.industry_trends) if market_intelligence and market_intelligence.industry_trends else None,
                'competitor_analysis': json.loads(market_intelligence.competitor_analysis) if market_intelligence and market_intelligence.competitor_analysis else None,
                'news_insights': json.loads(market_intelligence.news_insights) if market_intelligence and market_intelligence.news_insights else None,
                'market_opportunities': json.loads(market_intelligence.market_opportunities) if market_intelligence and market_intelligence.market_opportunities else None
            } if market_intelligence else None,
            'objections': [{
                'id': o.id,
                'objection_text': o.objection_text,
                'response_text': o.response_text,
                'category': o.category,
                'confidence_score': o.confidence_score
            } for o in objections]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pitchcraft_bp.route('/projects/<int:project_id>/generate-narrative', methods=['POST'])
@cross_origin()
def generate_narrative(project_id):
    """Gerar narrativa comercial usando IA"""
    try:
        data = request.get_json()
        project = Project.query.get_or_404(project_id)
        
        # Buscar dados do cliente e mercado
        client_profile = ClientProfile.query.filter_by(project_id=project_id).first()
        market_intelligence = MarketIntelligence.query.filter_by(project_id=project_id).first()
        
        # Preparar dados para a IA
        project_data = {
            'project_type': project.project_type,
            'description': project.description,
            'target_audience': project.target_audience
        }
        
        client_data = {}
        if client_profile:
            client_data = {
                'company_name': client_profile.company_name,
                'industry': client_profile.industry,
                'size': client_profile.size,
                'disc_profile': client_profile.disc_profile,
                'pain_points': client_profile.pain_points,
                'goals': client_profile.goals
            }
        
        market_data = {}
        if market_intelligence:
            market_data = {
                'industry_trends': json.loads(market_intelligence.industry_trends) if market_intelligence.industry_trends else {},
                'competitor_analysis': json.loads(market_intelligence.competitor_analysis) if market_intelligence.competitor_analysis else {},
                'market_opportunities': json.loads(market_intelligence.market_opportunities) if market_intelligence.market_opportunities else {}
            }
        
        # Gerar narrativa com IA
        narrative = ai_service.generate_narrative(project_data, client_data, market_data)
        
        return jsonify({
            'project_id': project_id,
            'narrative': narrative
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pitchcraft_bp.route('/projects/<int:project_id>/client-profile', methods=['POST'])
@cross_origin()
def create_or_update_client_profile(project_id):
    """Criar ou atualizar perfil do cliente"""
    try:
        data = request.get_json()
        project = Project.query.get_or_404(project_id)
        
        # Buscar perfil existente ou criar novo
        client_profile = ClientProfile.query.filter_by(project_id=project_id).first()
        if not client_profile:
            client_profile = ClientProfile(project_id=project_id)
        
        # Atualizar dados
        client_profile.company_name = data.get('company_name', '')
        client_profile.industry = data.get('industry', '')
        client_profile.size = data.get('size', '')
        client_profile.pain_points = data.get('pain_points', '')
        client_profile.goals = data.get('goals', '')
        client_profile.decision_makers = json.dumps(data.get('decision_makers', []))
        
        # Analisar perfil DISC se não fornecido
        if not data.get('disc_profile'):
            disc_profile = ai_service.analyze_disc_profile(data)
            client_profile.disc_profile = disc_profile
        else:
            client_profile.disc_profile = data.get('disc_profile')
        
        db.session.add(client_profile)
        db.session.commit()
        
        return jsonify({
            'id': client_profile.id,
            'company_name': client_profile.company_name,
            'industry': client_profile.industry,
            'size': client_profile.size,
            'disc_profile': client_profile.disc_profile,
            'pain_points': client_profile.pain_points,
            'goals': client_profile.goals,
            'decision_makers': json.loads(client_profile.decision_makers)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pitchcraft_bp.route('/projects/<int:project_id>/enrich-data', methods=['POST'])
@cross_origin()
def enrich_project_data(project_id):
    """Enriquecer dados do projeto com fontes externas"""
    try:
        data = request.get_json()
        project = Project.query.get_or_404(project_id)
        
        # Dados básicos para enriquecimento
        basic_data = {
            'company_name': data.get('company_name', ''),
            'industry': data.get('industry', ''),
            'website': data.get('website', '')
        }
        
        # Enriquecer dados
        enriched_data = data_service.enrich_client_profile(basic_data)
        
        # Salvar inteligência de mercado
        market_intelligence = MarketIntelligence.query.filter_by(project_id=project_id).first()
        if not market_intelligence:
            market_intelligence = MarketIntelligence(project_id=project_id)
        
        market_intelligence.industry_trends = json.dumps(enriched_data.get('industry_news', []))
        market_intelligence.competitor_analysis = json.dumps(enriched_data.get('competitor_analysis', {}))
        market_intelligence.news_insights = json.dumps(enriched_data.get('industry_news', []))
        market_intelligence.market_opportunities = json.dumps(enriched_data.get('competitor_analysis', {}).get('opportunities', []))
        
        db.session.add(market_intelligence)
        db.session.commit()
        
        return jsonify({
            'project_id': project_id,
            'enriched_data': enriched_data,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pitchcraft_bp.route('/projects/<int:project_id>/objections', methods=['POST'])
@cross_origin()
def generate_objections(project_id):
    """Gerar objeções e respostas"""
    try:
        project = Project.query.get_or_404(project_id)
        client_profile = ClientProfile.query.filter_by(project_id=project_id).first()
        
        project_data = {
            'description': project.description,
            'project_type': project.project_type
        }
        
        client_data = {}
        if client_profile:
            client_data = {
                'company_name': client_profile.company_name,
                'industry': client_profile.industry,
                'disc_profile': client_profile.disc_profile
            }
        
        # Gerar objeções com IA
        objections_data = ai_service.generate_objections_and_responses(project_data, client_data)
        
        # Salvar no banco
        for obj_data in objections_data:
            objection = Objection(
                project_id=project_id,
                objection_text=obj_data['objection'],
                response_text=obj_data['response'],
                category=obj_data['category'],
                confidence_score=obj_data['confidence_score']
            )
            db.session.add(objection)
        
        db.session.commit()
        
        return jsonify({
            'project_id': project_id,
            'objections': objections_data,
            'total_generated': len(objections_data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pitchcraft_bp.route('/projects/<int:project_id>/presentations', methods=['POST'])
@cross_origin()
def create_presentation(project_id):
    """Criar uma nova apresentação"""
    try:
        data = request.get_json()
        project = Project.query.get_or_404(project_id)
        
        # Se não há conteúdo, gerar automaticamente
        if not data.get('content'):
            # Buscar narrativa existente ou gerar nova
            narrative = data.get('narrative', {})
            if not narrative:
                # Gerar narrativa automaticamente
                client_profile = ClientProfile.query.filter_by(project_id=project_id).first()
                market_intelligence = MarketIntelligence.query.filter_by(project_id=project_id).first()
                
                project_data = {
                    'project_type': project.project_type,
                    'description': project.description,
                    'target_audience': project.target_audience
                }
                
                client_data = {}
                if client_profile:
                    client_data = {
                        'company_name': client_profile.company_name,
                        'industry': client_profile.industry,
                        'disc_profile': client_profile.disc_profile
                    }
                
                market_data = {}
                if market_intelligence:
                    market_data = {
                        'industry_trends': json.loads(market_intelligence.industry_trends) if market_intelligence.industry_trends else {}
                    }
                
                narrative = ai_service.generate_narrative(project_data, client_data, market_data)
            
            # Gerar slides baseados na narrativa
            style_config = data.get('style_config', {})
            slides_data = ai_service.generate_presentation_slides(narrative, style_config)
            content = slides_data
        else:
            content = data['content']
        
        presentation = Presentation(
            project_id=project_id,
            title=data.get('title', f'Apresentação - {project.title}'),
            content=json.dumps(content),
            style_config=json.dumps(data.get('style_config', {}))
        )
        
        db.session.add(presentation)
        db.session.commit()
        
        return jsonify({
            'id': presentation.id,
            'title': presentation.title,
            'content': json.loads(presentation.content),
            'style_config': json.loads(presentation.style_config),
            'created_at': presentation.created_at.isoformat()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pitchcraft_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'service': 'PitchCraft AI API',
        'version': '1.0.0'
    })

