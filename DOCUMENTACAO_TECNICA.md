# PitchCraft AI - Documentação Técnica Completa

## Visão Geral do Projeto

O PitchCraft AI é uma plataforma revolucionária de Inteligência Comercial Autônoma que cria, otimiza e personaliza narrativas de negócios, vendas, marketing, investimentos e parcerias. A solução foi desenvolvida com extrema qualidade e funcionalidade, adaptando-se ao perfil do cliente-alvo, ao contexto de mercado e à estratégia da empresa.

### Características Principais

- **Geração Automática de Narrativas**: Utiliza IA avançada para criar narrativas comerciais personalizadas
- **Integração de Dados**: Extrai informações de múltiplas fontes (LinkedIn, CRM, sites, relatórios)
- **Apresentações Visuais**: Gera slides profissionais automaticamente
- **Análise DISC**: Identifica perfis comportamentais para personalização
- **Inteligência de Mercado**: Análise em tempo real de tendências e concorrentes
- **Simulador de Objeções**: Prepara respostas para objeções comuns
- **Interface Moderna**: Frontend responsivo e intuitivo

## Arquitetura do Sistema

### Stack Tecnológico

**Backend:**
- Python 3.11 com Flask
- SQLAlchemy para ORM
- PostgreSQL/SQLite para banco de dados
- Qdrant para banco vetorial
- APIs de IA: OpenAI GPT-4, Anthropic Claude, Google Gemini

**Frontend:**
- React 19 com Next.js
- Tailwind CSS para estilização
- shadcn/ui para componentes
- Lucide React para ícones

**Integrações:**
- LinkedIn API
- HubSpot/Salesforce CRM
- Google News API
- Web scraping para dados públicos

### Estrutura de Diretórios

```
pitchcraft-ai/
├── backend/
│   ├── src/
│   │   ├── models/          # Modelos de dados
│   │   ├── routes/          # Rotas da API
│   │   ├── services/        # Serviços de negócio
│   │   └── main.py          # Ponto de entrada
│   ├── venv/                # Ambiente virtual
│   └── requirements.txt     # Dependências
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── hooks/           # Hooks customizados
│   │   └── lib/             # Utilitários
│   └── package.json         # Dependências Node.js
└── docs/                    # Documentação
```

## Funcionalidades Implementadas

### 1. Gerador de Narrativas Comerciais

O sistema utiliza modelos de IA avançados para criar narrativas personalizadas baseadas em:

- Dados do projeto (tipo, descrição, público-alvo)
- Perfil do cliente (empresa, setor, tamanho, dores, objetivos)
- Inteligência de mercado (tendências, concorrentes, oportunidades)

**Estrutura da Narrativa:**
1. Introdução impactante
2. Identificação do problema
3. Apresentação da solução
4. Benefícios específicos
5. Prova social
6. Chamada para ação

### 2. Sistema de Integração de Dados

**Fontes de Dados Suportadas:**
- LinkedIn (dados da empresa e funcionários)
- CRM (HubSpot, Salesforce)
- Sites corporativos (web scraping)
- Google News (notícias do setor)
- Bases de dados públicas

**Processo de Enriquecimento:**
1. Coleta de dados básicos do cliente
2. Busca automática em fontes externas
3. Análise e estruturação das informações
4. Armazenamento no banco de dados
5. Disponibilização para geração de narrativas

### 3. Gerador de Apresentações Visuais

O sistema cria automaticamente slides profissionais baseados na narrativa gerada:

**Tipos de Slides:**
- Slide título com introdução
- Identificação de problemas (bullet points)
- Proposta de solução (diagramas)
- Benefícios (grid de ícones)
- Casos de sucesso (depoimentos)
- Próximos passos (timeline)

### 4. Análise de Perfil DISC

Implementação de algoritmo para identificar perfis comportamentais:

- **D (Dominância)**: Foco em resultados e controle
- **I (Influência)**: Orientado para pessoas e persuasão
- **S (Estabilidade)**: Busca harmonia e consistência
- **C (Conformidade)**: Valoriza precisão e qualidade

### 5. Simulador de Objeções

Sistema inteligente que:
- Identifica objeções comuns por setor/perfil
- Gera respostas personalizadas
- Categoriza por tipo (preço, timing, autoridade, necessidade)
- Atribui scores de confiança

## Modelos de Dados

### Principais Entidades

**User (Usuário)**
- id, email, name, company
- created_at, updated_at

**Project (Projeto)**
- id, user_id, title, description
- project_type, target_audience, status
- created_at, updated_at

**ClientProfile (Perfil do Cliente)**
- id, project_id, company_name, industry
- size, disc_profile, pain_points, goals
- decision_makers

**Presentation (Apresentação)**
- id, project_id, title, content
- style_config, created_at

**MarketIntelligence (Inteligência de Mercado)**
- id, project_id, industry_trends
- competitor_analysis, news_insights
- market_opportunities

**Objection (Objeção)**
- id, project_id, objection_text
- response_text, category, confidence_score

## API Endpoints

### Projetos
- `GET /api/projects` - Listar projetos
- `POST /api/projects` - Criar projeto
- `GET /api/projects/{id}` - Obter projeto específico

### Perfil do Cliente
- `POST /api/projects/{id}/client-profile` - Criar/atualizar perfil

### Narrativas
- `POST /api/projects/{id}/generate-narrative` - Gerar narrativa

### Apresentações
- `POST /api/projects/{id}/presentations` - Criar apresentação

### Dados Externos
- `POST /api/projects/{id}/enrich-data` - Enriquecer dados

### Objeções
- `POST /api/projects/{id}/objections` - Gerar objeções

### Saúde
- `GET /api/health` - Verificação de saúde

## Interface do Usuário

### Dashboard Principal

O dashboard oferece uma visão geral completa:

**Métricas em Tempo Real:**
- Projetos ativos
- Narrativas geradas
- Apresentações criadas
- Taxa de sucesso

**Funcionalidades:**
- Criação rápida de projetos
- Navegação por abas intuitiva
- Formulários responsivos
- Feedback visual em tempo real

### Fluxo de Trabalho

1. **Criação do Projeto**: Definição de título, tipo, descrição e público-alvo
2. **Perfil do Cliente**: Coleta de informações detalhadas sobre o cliente
3. **Enriquecimento**: Busca automática de dados externos
4. **Geração de Narrativa**: Criação da narrativa personalizada
5. **Apresentação**: Geração automática de slides
6. **Objeções**: Preparação para possíveis objeções

## Segurança e Performance

### Medidas de Segurança

- Validação de entrada em todas as APIs
- Sanitização de dados de web scraping
- Controle de acesso baseado em usuário
- Logs de auditoria para operações críticas
- Configuração segura de variáveis de ambiente

### Otimizações de Performance

- Cache de dados de mercado
- Lazy loading no frontend
- Compressão de respostas da API
- Otimização de consultas ao banco
- CDN para assets estáticos

## Configuração e Deploy

### Variáveis de Ambiente

```bash
# APIs de IA
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key

# Banco de Dados
DATABASE_URL=postgresql://user:pass@host:port/db
QDRANT_URL=http://localhost:6333

# APIs Externas
LINKEDIN_API_KEY=your_linkedin_key
HUBSPOT_API_KEY=your_hubspot_key
SALESFORCE_API_KEY=your_salesforce_key

# Configurações
SECRET_KEY=your_secret_key
DEBUG=False
```

### Instalação Local

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python src/main.py
```

**Frontend:**
```bash
cd frontend
pnpm install
pnpm run dev
```

### Deploy em Produção

O sistema está preparado para deploy usando:
- Docker containers
- Kubernetes orchestration
- CI/CD pipelines
- Monitoramento com Prometheus/Grafana

## Funcionalidades Premium

### Analisador de Pitch
- Upload e análise de pitches existentes
- Sugestões de melhorias automáticas
- Comparação com benchmarks do setor

### Gerador de Pitch em Vídeo
- Avatar AI para apresentação
- Sincronização de áudio e slides
- Teleprompter integrado

### Validador Jurídico
- Checklist automático de cláusulas
- Verificação de compliance
- Alertas de riscos legais

### Análise de Risco
- Avaliação de riscos reputacionais
- Análise financeira do prospect
- Score de probabilidade de fechamento

## Roadmap Futuro

### Próximas Funcionalidades

1. **Conversational Pitch Builder**
   - Interface de voz para criação de pitches
   - Reconhecimento de fala em tempo real
   - Geração automática baseada em comandos de voz

2. **APIs Plug & Play**
   - Integração com PandaDoc
   - Conectores para DocSend
   - WhatsApp Business API
   - Plataformas de assinatura digital

3. **Machine Learning Avançado**
   - Modelos próprios fine-tuned
   - Análise preditiva de sucesso
   - Personalização baseada em histórico

4. **Expansão Internacional**
   - Suporte a múltiplos idiomas
   - Adaptação cultural automática
   - Compliance regional

## Conclusão

O PitchCraft AI representa uma solução completa e inovadora para automatização de narrativas comerciais. Com sua arquitetura robusta, funcionalidades avançadas e interface intuitiva, a plataforma está posicionada para revolucionar a forma como empresas criam e apresentam suas propostas comerciais.

A implementação atual demonstra alta qualidade técnica, escalabilidade e potencial para crescimento futuro, estabelecendo uma base sólida para expansão e evolução contínua da plataforma.

