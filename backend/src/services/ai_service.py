import openai
import anthropic
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime

class AIService:
    def __init__(self):
        # Configurar clientes de IA apenas se as chaves estiverem disponíveis
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and openai_key != 'demo_key_for_testing':
            self.openai_client = openai.OpenAI(api_key=openai_key)
        else:
            self.openai_client = None
            
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key and anthropic_key != 'demo_key_for_testing':
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
        else:
            self.anthropic_client = None
            
        google_key = os.getenv('GOOGLE_API_KEY')
        if google_key and google_key != 'demo_key_for_testing':
            genai.configure(api_key=google_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        else:
            self.gemini_model = None
        
        # Configurar Qdrant (Vector Database) apenas se disponível
        qdrant_url = os.getenv('QDRANT_URL', 'http://localhost:6333')
        qdrant_key = os.getenv('QDRANT_API_KEY')
        try:
            if qdrant_key and qdrant_key != 'demo_key_for_testing':
                self.qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_key)
            else:
                self.qdrant_client = None
        except Exception:
            self.qdrant_client = None
    
    def generate_narrative(self, project_data: Dict, client_profile: Dict, market_data: Dict) -> Dict:
        """Gerar narrativa comercial personalizada usando IA"""
        
        # Se não há cliente OpenAI disponível, retornar narrativa de exemplo
        if not self.openai_client:
            return self._generate_demo_narrative(project_data, client_profile)
        
        prompt = f"""
        Você é um especialista em narrativas comerciais. Crie uma narrativa persuasiva baseada nos seguintes dados:
        
        PROJETO:
        - Tipo: {project_data.get('project_type', 'pitch_vendas')}
        - Descrição: {project_data.get('description', '')}
        - Público-alvo: {project_data.get('target_audience', '')}
        
        PERFIL DO CLIENTE:
        - Empresa: {client_profile.get('company_name', '')}
        - Setor: {client_profile.get('industry', '')}
        - Tamanho: {client_profile.get('size', '')}
        - Perfil DISC: {client_profile.get('disc_profile', '')}
        - Dores: {client_profile.get('pain_points', '')}
        - Objetivos: {client_profile.get('goals', '')}
        
        INTELIGÊNCIA DE MERCADO:
        - Tendências: {market_data.get('industry_trends', '')}
        - Concorrentes: {market_data.get('competitor_analysis', '')}
        - Oportunidades: {market_data.get('market_opportunities', '')}
        
        Crie uma narrativa estruturada com:
        1. Introdução impactante
        2. Identificação do problema
        3. Apresentação da solução
        4. Benefícios específicos
        5. Prova social
        6. Chamada para ação
        
        Adapte o tom para o perfil DISC identificado.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            narrative_text = response.choices[0].message.content
            
            # Estruturar a resposta
            narrative = {
                'introduction': self._extract_section(narrative_text, 'introdução'),
                'problem_statement': self._extract_section(narrative_text, 'problema'),
                'solution_overview': self._extract_section(narrative_text, 'solução'),
                'benefits': self._extract_section(narrative_text, 'benefícios'),
                'social_proof': self._extract_section(narrative_text, 'prova social'),
                'call_to_action': self._extract_section(narrative_text, 'chamada para ação'),
                'full_text': narrative_text,
                'generated_at': datetime.utcnow().isoformat()
            }
            
            return narrative
            
        except Exception as e:
            return self._generate_demo_narrative(project_data, client_profile)
    
    def _generate_demo_narrative(self, project_data: Dict, client_profile: Dict) -> Dict:
        """Gerar narrativa de demonstração quando APIs não estão disponíveis"""
        company_name = client_profile.get('company_name', 'sua empresa')
        industry = client_profile.get('industry', 'seu setor')
        
        return {
            'introduction': f"Prezados executivos da {company_name}, é um prazer apresentar nossa proposta inovadora que transformará a forma como vocês operam no mercado de {industry}. Nossa solução foi desenvolvida especificamente para empresas visionárias como a sua.",
            'problem_statement': f"Sabemos que empresas do setor de {industry} enfrentam desafios únicos: processos manuais que consomem tempo, falta de integração entre sistemas, e dificuldades para escalar operações. Estes problemas impactam diretamente a produtividade e competitividade da {company_name}.",
            'solution_overview': f"Nossa plataforma oferece uma solução completa e integrada que automatiza processos críticos, centraliza informações e fornece insights em tempo real. Desenvolvida especificamente para o setor de {industry}, nossa tecnologia se adapta perfeitamente às necessidades da {company_name}.",
            'benefits': f"Com nossa solução, a {company_name} experimentará: redução de 40% no tempo de processamento, aumento de 25% na produtividade da equipe, economia de até R$ 500.000 anuais em custos operacionais, e melhoria significativa na satisfação dos clientes.",
            'social_proof': f"Já ajudamos mais de 150 empresas do setor de {industry} a transformar suas operações. Nossos clientes reportam ROI médio de 300% no primeiro ano e taxa de satisfação de 98%. Empresas similares à {company_name} viram resultados extraordinários em apenas 90 dias.",
            'call_to_action': f"Convidamos a {company_name} para uma demonstração personalizada onde mostraremos exatamente como nossa solução pode resolver seus desafios específicos. Vamos agendar uma reunião na próxima semana para discutir os próximos passos e iniciar sua jornada de transformação digital.",
            'full_text': f"Narrativa comercial completa para {company_name} no setor de {industry}.",
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def _extract_section(self, text: str, section: str) -> str:
        """Extrair seção específica do texto gerado"""
        # Implementação simplificada - em produção seria mais sofisticada
        lines = text.split('\n')
        section_content = []
        capturing = False
        
        for line in lines:
            if section.lower() in line.lower():
                capturing = True
                continue
            elif capturing and (line.startswith('#') or line.startswith('**')):
                break
            elif capturing:
                section_content.append(line)
        
        return '\n'.join(section_content).strip()
    
    def analyze_disc_profile(self, client_data: Dict) -> str:
        """Analisar perfil DISC do cliente baseado nos dados disponíveis"""
        
        if not self.openai_client:
            # Retornar perfil baseado em heurísticas simples
            industry = client_data.get('industry', '').lower()
            if 'tecnologia' in industry or 'software' in industry:
                return 'D'  # Dominância
            elif 'marketing' in industry or 'vendas' in industry:
                return 'I'  # Influência
            elif 'saúde' in industry or 'educação' in industry:
                return 'S'  # Estabilidade
            else:
                return 'C'  # Conformidade
        
        prompt = f"""
        Analise os dados do cliente e determine o perfil DISC predominante:
        
        DADOS DO CLIENTE:
        - Empresa: {client_data.get('company_name', '')}
        - Setor: {client_data.get('industry', '')}
        - Comunicação: {client_data.get('communication_style', '')}
        - Decisões: {client_data.get('decision_making', '')}
        - Prioridades: {client_data.get('priorities', '')}
        
        Retorne apenas uma letra: D (Dominância), I (Influência), S (Estabilidade), ou C (Conformidade)
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            disc_profile = response.choices[0].message.content.strip().upper()
            return disc_profile if disc_profile in ['D', 'I', 'S', 'C'] else 'D'
            
        except Exception as e:
            return 'D'  # Default
    
    def generate_objections_and_responses(self, project_data: Dict, client_profile: Dict) -> List[Dict]:
        """Gerar objeções comuns e respostas para o perfil do cliente"""
        
        if not self.openai_client:
            return self._generate_demo_objections(client_profile)
        
        prompt = f"""
        Baseado no projeto e perfil do cliente, gere 5 objeções comuns que podem surgir e suas respectivas respostas:
        
        PROJETO: {project_data.get('description', '')}
        CLIENTE: {client_profile.get('company_name', '')} - {client_profile.get('industry', '')}
        PERFIL DISC: {client_profile.get('disc_profile', 'D')}
        
        Para cada objeção, forneça:
        1. A objeção específica
        2. Uma resposta persuasiva
        3. Categoria (price, timing, authority, need)
        4. Score de confiança (0-1)
        
        Formato JSON:
        [
            {
                "objection": "texto da objeção",
                "response": "resposta persuasiva",
                "category": "categoria",
                "confidence_score": 0.8
            }
        ]
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            objections_text = response.choices[0].message.content
            
            # Tentar parsear JSON
            try:
                objections = json.loads(objections_text)
                return objections
            except json.JSONDecodeError:
                # Fallback para formato estruturado
                return self._generate_demo_objections(client_profile)
                
        except Exception as e:
            return self._generate_demo_objections(client_profile)
    
    def _generate_demo_objections(self, client_profile: Dict) -> List[Dict]:
        """Gerar objeções de demonstração"""
        company_name = client_profile.get('company_name', 'empresa')
        
        return [
            {
                "objection": f"O investimento está acima do orçamento previsto para este ano na {company_name}",
                "response": "Entendo perfeitamente a preocupação com o orçamento. Nossa proposta inclui opções de pagamento flexíveis e podemos demonstrar como o ROI no primeiro trimestre já justifica o investimento. Que tal analisarmos juntos as economias que vocês terão?",
                "category": "price",
                "confidence_score": 0.85
            },
            {
                "objection": "Não é o momento ideal para implementar uma nova solução",
                "response": "O timing é realmente crucial para o sucesso. Baseado na nossa experiência, empresas que implementam durante períodos de estabilidade têm 40% mais sucesso. Podemos estruturar um cronograma que se alinhe perfeitamente com seus ciclos operacionais.",
                "category": "timing",
                "confidence_score": 0.78
            },
            {
                "objection": "Preciso consultar outros stakeholders antes de tomar uma decisão",
                "response": "Claro, decisões estratégicas devem envolver toda a equipe. Posso preparar uma apresentação específica para os stakeholders, destacando os benefícios para cada área. Também oferecemos uma sessão de Q&A para esclarecer todas as dúvidas.",
                "category": "authority",
                "confidence_score": 0.82
            },
            {
                "objection": "Nossa solução atual atende nossas necessidades básicas",
                "response": "É ótimo que vocês tenham uma base sólida. Nossa proposta não é substituir o que funciona, mas potencializar seus resultados. Vamos mostrar como podemos integrar com seus sistemas atuais e adicionar capacidades que gerarão novos resultados.",
                "category": "need",
                "confidence_score": 0.75
            },
            {
                "objection": "Estamos preocupados com a complexidade da implementação",
                "response": "Compreendo essa preocupação. Nossa metodologia de implementação é gradual e conta com suporte 24/7. Temos uma equipe dedicada que garante transição suave, e 95% dos nossos clientes ficam operacionais em menos de 30 dias.",
                "category": "timing",
                "confidence_score": 0.88
            }
        ]
    
    def generate_presentation_slides(self, narrative: Dict, style_config: Dict) -> Dict:
        """Gerar estrutura de slides baseada na narrativa"""
        
        slides = [
            {
                "id": 1,
                "type": "title",
                "title": "Proposta Comercial Personalizada",
                "subtitle": "Solução Inovadora para Seu Negócio",
                "content": narrative.get('introduction', '')
            },
            {
                "id": 2,
                "type": "problem",
                "title": "Desafios Identificados",
                "content": narrative.get('problem_statement', ''),
                "visual_type": "bullet_points"
            },
            {
                "id": 3,
                "type": "solution",
                "title": "Nossa Proposta de Solução",
                "content": narrative.get('solution_overview', ''),
                "visual_type": "diagram"
            },
            {
                "id": 4,
                "type": "benefits",
                "title": "Benefícios e Resultados Esperados",
                "content": narrative.get('benefits', ''),
                "visual_type": "icons_grid"
            },
            {
                "id": 5,
                "type": "social_proof",
                "title": "Casos de Sucesso e Referências",
                "content": narrative.get('social_proof', ''),
                "visual_type": "testimonials"
            },
            {
                "id": 6,
                "type": "cta",
                "title": "Próximos Passos",
                "content": narrative.get('call_to_action', ''),
                "visual_type": "timeline"
            }
        ]
        
        return {
            "slides": slides,
            "style": style_config,
            "total_slides": len(slides),
            "estimated_duration": len(slides) * 2  # 2 minutos por slide
        }

