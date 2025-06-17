import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os

class DataIntegrationService:
    def __init__(self):
        self.linkedin_api_key = os.getenv('LINKEDIN_API_KEY')
        self.hubspot_api_key = os.getenv('HUBSPOT_API_KEY')
        self.salesforce_api_key = os.getenv('SALESFORCE_API_KEY')
        self.google_news_api_key = os.getenv('GOOGLE_NEWS_API_KEY')
    
    def scrape_company_website(self, website_url: str) -> Dict:
        """Extrair informações básicas do site da empresa"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(website_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair informações básicas
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ''
            
            # Buscar descrição
            description = soup.find('meta', attrs={'name': 'description'})
            description_text = description.get('content', '') if description else ''
            
            # Buscar palavras-chave
            keywords = soup.find('meta', attrs={'name': 'keywords'})
            keywords_text = keywords.get('content', '') if keywords else ''
            
            # Extrair texto principal
            main_content = []
            for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
                text = tag.get_text().strip()
                if text and len(text) > 20:
                    main_content.append(text)
            
            return {
                'url': website_url,
                'title': title_text,
                'description': description_text,
                'keywords': keywords_text,
                'main_content': main_content[:10],  # Primeiros 10 parágrafos
                'scraped_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Erro ao extrair dados do site: {str(e)}'}
    
    def get_company_linkedin_data(self, company_name: str) -> Dict:
        """Buscar dados da empresa no LinkedIn (simulado)"""
        # Em produção, usaria a API oficial do LinkedIn
        # Por enquanto, retornamos dados simulados
        
        return {
            'company_name': company_name,
            'industry': 'Tecnologia',
            'size': '51-200 funcionários',
            'headquarters': 'São Paulo, SP',
            'founded': '2015',
            'specialties': ['Software', 'Consultoria', 'Inovação'],
            'recent_posts': [
                {
                    'date': '2025-06-15',
                    'content': 'Lançamento de nova solução para o mercado',
                    'engagement': 150
                }
            ],
            'employees_growth': '+15% nos últimos 6 meses',
            'data_source': 'LinkedIn (simulado)'
        }
    
    def get_industry_news(self, industry: str, days_back: int = 30) -> List[Dict]:
        """Buscar notícias recentes do setor"""
        try:
            # Simulação de busca de notícias
            # Em produção, usaria Google News API ou similar
            
            news_items = [
                {
                    'title': f'Tendências em {industry} para 2025',
                    'summary': 'Principais inovações e mudanças esperadas no setor',
                    'source': 'TechNews',
                    'date': '2025-06-16',
                    'url': 'https://example.com/news1',
                    'relevance_score': 0.9
                },
                {
                    'title': f'Investimentos em {industry} crescem 25%',
                    'summary': 'Setor atrai mais investimentos devido à demanda crescente',
                    'source': 'BusinessDaily',
                    'date': '2025-06-14',
                    'url': 'https://example.com/news2',
                    'relevance_score': 0.8
                },
                {
                    'title': f'Regulamentação em {industry} muda panorama',
                    'summary': 'Novas regras impactam estratégias das empresas',
                    'source': 'IndustryReport',
                    'date': '2025-06-12',
                    'url': 'https://example.com/news3',
                    'relevance_score': 0.7
                }
            ]
            
            return news_items
            
        except Exception as e:
            return []
    
    def get_competitor_analysis(self, company_name: str, industry: str) -> Dict:
        """Análise de concorrentes (simulado)"""
        
        competitors = [
            {
                'name': 'Concorrente A',
                'market_share': '25%',
                'strengths': ['Preço competitivo', 'Ampla distribuição'],
                'weaknesses': ['Atendimento limitado', 'Tecnologia defasada'],
                'recent_moves': 'Lançou nova linha de produtos'
            },
            {
                'name': 'Concorrente B',
                'market_share': '18%',
                'strengths': ['Inovação', 'Brand recognition'],
                'weaknesses': ['Preço alto', 'Complexidade'],
                'recent_moves': 'Expansão para novos mercados'
            }
        ]
        
        return {
            'industry': industry,
            'total_competitors': len(competitors),
            'competitors': competitors,
            'market_trends': [
                'Crescimento de 12% ao ano',
                'Digitalização acelerada',
                'Foco em sustentabilidade'
            ],
            'opportunities': [
                'Mercado de pequenas empresas subatendido',
                'Demanda por soluções integradas',
                'Necessidade de automação'
            ],
            'analysis_date': datetime.utcnow().isoformat()
        }
    
    def get_crm_data(self, crm_type: str, contact_id: str) -> Dict:
        """Integração com CRM (simulado)"""
        
        # Simulação de dados do CRM
        crm_data = {
            'hubspot': {
                'contact_id': contact_id,
                'company': 'Empresa Demo',
                'industry': 'Tecnologia',
                'annual_revenue': 'R$ 5-10M',
                'employees': '50-100',
                'last_interaction': '2025-06-10',
                'deal_stage': 'Qualificado',
                'pain_points': ['Processos manuais', 'Falta de integração'],
                'budget': 'R$ 100-500k',
                'decision_timeline': '3-6 meses'
            },
            'salesforce': {
                'account_id': contact_id,
                'company': 'Empresa Demo SF',
                'industry': 'Manufatura',
                'annual_revenue': 'R$ 10-50M',
                'employees': '100-500',
                'last_interaction': '2025-06-08',
                'opportunity_stage': 'Proposta',
                'pain_points': ['Custos operacionais', 'Eficiência'],
                'budget': 'R$ 500k-1M',
                'decision_timeline': '6-12 meses'
            }
        }
        
        return crm_data.get(crm_type.lower(), {})
    
    def enrich_client_profile(self, basic_data: Dict) -> Dict:
        """Enriquecer perfil do cliente com dados de múltiplas fontes"""
        
        company_name = basic_data.get('company_name', '')
        industry = basic_data.get('industry', '')
        website = basic_data.get('website', '')
        
        enriched_profile = basic_data.copy()
        
        # Dados do LinkedIn
        if company_name:
            linkedin_data = self.get_company_linkedin_data(company_name)
            enriched_profile['linkedin_data'] = linkedin_data
        
        # Dados do site
        if website:
            website_data = self.scrape_company_website(website)
            enriched_profile['website_data'] = website_data
        
        # Notícias do setor
        if industry:
            news_data = self.get_industry_news(industry)
            enriched_profile['industry_news'] = news_data
        
        # Análise de concorrentes
        if company_name and industry:
            competitor_data = self.get_competitor_analysis(company_name, industry)
            enriched_profile['competitor_analysis'] = competitor_data
        
        enriched_profile['enrichment_date'] = datetime.utcnow().isoformat()
        
        return enriched_profile

