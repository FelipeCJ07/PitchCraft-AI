import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Brain, Target, Users, TrendingUp, MessageSquare, FileText, Sparkles, Zap } from 'lucide-react'
import './App.css'

const API_BASE_URL = 'http://localhost:5000/api'

function App() {
  const [projects, setProjects] = useState([])
  const [currentProject, setCurrentProject] = useState(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('dashboard')

  // Estados para criação de projeto
  const [newProject, setNewProject] = useState({
    title: '',
    description: '',
    project_type: 'pitch_vendas',
    target_audience: ''
  })

  // Estados para perfil do cliente
  const [clientProfile, setClientProfile] = useState({
    company_name: '',
    industry: '',
    size: '',
    pain_points: '',
    goals: '',
    website: ''
  })

  // Estados para narrativa e apresentação
  const [narrative, setNarrative] = useState(null)
  const [presentation, setPresentation] = useState(null)

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/projects`)
      const data = await response.json()
      setProjects(data)
    } catch (error) {
      console.error('Erro ao buscar projetos:', error)
    }
  }

  const createProject = async () => {
    if (!newProject.title) return

    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/projects`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newProject)
      })
      
      const data = await response.json()
      setProjects([...projects, data])
      setCurrentProject(data)
      setNewProject({ title: '', description: '', project_type: 'pitch_vendas', target_audience: '' })
      setActiveTab('client-profile')
    } catch (error) {
      console.error('Erro ao criar projeto:', error)
    } finally {
      setLoading(false)
    }
  }

  const saveClientProfile = async () => {
    if (!currentProject) return

    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/projects/${currentProject.id}/client-profile`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(clientProfile)
      })
      
      const data = await response.json()
      console.log('Perfil do cliente salvo:', data)
      
      // Enriquecer dados automaticamente
      await enrichProjectData()
    } catch (error) {
      console.error('Erro ao salvar perfil do cliente:', error)
    } finally {
      setLoading(false)
    }
  }

  const enrichProjectData = async () => {
    if (!currentProject) return

    try {
      const response = await fetch(`${API_BASE_URL}/projects/${currentProject.id}/enrich-data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(clientProfile)
      })
      
      const data = await response.json()
      console.log('Dados enriquecidos:', data)
    } catch (error) {
      console.error('Erro ao enriquecer dados:', error)
    }
  }

  const generateNarrative = async () => {
    if (!currentProject) return

    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/projects/${currentProject.id}/generate-narrative`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
      })
      
      const data = await response.json()
      setNarrative(data.narrative)
      setActiveTab('narrative')
    } catch (error) {
      console.error('Erro ao gerar narrativa:', error)
    } finally {
      setLoading(false)
    }
  }

  const generatePresentation = async () => {
    if (!currentProject) return

    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/projects/${currentProject.id}/presentations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: `Apresentação - ${currentProject.title}`,
          narrative: narrative
        })
      })
      
      const data = await response.json()
      setPresentation(data)
      setActiveTab('presentation')
    } catch (error) {
      console.error('Erro ao gerar apresentação:', error)
    } finally {
      setLoading(false)
    }
  }

  const generateObjections = async () => {
    if (!currentProject) return

    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/projects/${currentProject.id}/objections`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
      })
      
      const data = await response.json()
      console.log('Objeções geradas:', data)
    } catch (error) {
      console.error('Erro ao gerar objeções:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center justify-center gap-2">
            <Brain className="h-10 w-10 text-blue-600" />
            PitchCraft AI
          </h1>
          <p className="text-xl text-gray-600">O Arquitetor de Narrativas Comerciais Autônomo</p>
        </div>

        {/* Navigation */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="client-profile">Perfil do Cliente</TabsTrigger>
            <TabsTrigger value="narrative">Narrativa</TabsTrigger>
            <TabsTrigger value="presentation">Apresentação</TabsTrigger>
            <TabsTrigger value="objections">Objeções</TabsTrigger>
          </TabsList>

          {/* Dashboard */}
          <TabsContent value="dashboard" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Projetos Ativos</CardTitle>
                  <Target className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{projects.length}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Narrativas Geradas</CardTitle>
                  <FileText className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{narrative ? 1 : 0}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Apresentações</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{presentation ? 1 : 0}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Taxa de Sucesso</CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">95%</div>
                </CardContent>
              </Card>
            </div>

            {/* Criar Novo Projeto */}
            <Card>
              <CardHeader>
                <CardTitle>Criar Novo Projeto</CardTitle>
                <CardDescription>
                  Inicie um novo projeto de narrativa comercial
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="title">Título do Projeto</Label>
                    <Input
                      id="title"
                      placeholder="Ex: Pitch para Empresa XYZ"
                      value={newProject.title}
                      onChange={(e) => setNewProject({...newProject, title: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="project_type">Tipo de Projeto</Label>
                    <Select value={newProject.project_type} onValueChange={(value) => setNewProject({...newProject, project_type: value})}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="pitch_vendas">Pitch de Vendas</SelectItem>
                        <SelectItem value="proposta_comercial">Proposta Comercial</SelectItem>
                        <SelectItem value="apresentacao_institucional">Apresentação Institucional</SelectItem>
                        <SelectItem value="elevator_pitch">Elevator Pitch</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="description">Descrição</Label>
                  <Textarea
                    id="description"
                    placeholder="Descreva o objetivo e contexto do projeto..."
                    value={newProject.description}
                    onChange={(e) => setNewProject({...newProject, description: e.target.value})}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="target_audience">Público-Alvo</Label>
                  <Input
                    id="target_audience"
                    placeholder="Ex: Diretores de TI de empresas médias"
                    value={newProject.target_audience}
                    onChange={(e) => setNewProject({...newProject, target_audience: e.target.value})}
                  />
                </div>
                <Button onClick={createProject} disabled={loading} className="w-full">
                  {loading ? 'Criando...' : 'Criar Projeto'}
                </Button>
              </CardContent>
            </Card>

            {/* Lista de Projetos */}
            {projects.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Projetos Recentes</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {projects.map((project) => (
                      <div
                        key={project.id}
                        className="flex items-center justify-between p-3 border rounded-lg cursor-pointer hover:bg-gray-50"
                        onClick={() => setCurrentProject(project)}
                      >
                        <div>
                          <h3 className="font-medium">{project.title}</h3>
                          <p className="text-sm text-gray-500">{project.project_type}</p>
                        </div>
                        <Badge variant={project.status === 'completed' ? 'default' : 'secondary'}>
                          {project.status}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Perfil do Cliente */}
          <TabsContent value="client-profile" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Perfil do Cliente</CardTitle>
                <CardDescription>
                  Forneça informações sobre o cliente para personalizar a narrativa
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="company_name">Nome da Empresa</Label>
                    <Input
                      id="company_name"
                      placeholder="Ex: Empresa ABC Ltda"
                      value={clientProfile.company_name}
                      onChange={(e) => setClientProfile({...clientProfile, company_name: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="industry">Setor</Label>
                    <Input
                      id="industry"
                      placeholder="Ex: Tecnologia, Saúde, Educação"
                      value={clientProfile.industry}
                      onChange={(e) => setClientProfile({...clientProfile, industry: e.target.value})}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="size">Tamanho da Empresa</Label>
                    <Select value={clientProfile.size} onValueChange={(value) => setClientProfile({...clientProfile, size: value})}>
                      <SelectTrigger>
                        <SelectValue placeholder="Selecione o tamanho" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="startup">Startup (1-10 funcionários)</SelectItem>
                        <SelectItem value="pequena">Pequena (11-50 funcionários)</SelectItem>
                        <SelectItem value="media">Média (51-200 funcionários)</SelectItem>
                        <SelectItem value="grande">Grande (201-1000 funcionários)</SelectItem>
                        <SelectItem value="enterprise">Enterprise (1000+ funcionários)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="website">Website</Label>
                    <Input
                      id="website"
                      placeholder="https://www.empresa.com.br"
                      value={clientProfile.website}
                      onChange={(e) => setClientProfile({...clientProfile, website: e.target.value})}
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pain_points">Principais Dores/Desafios</Label>
                  <Textarea
                    id="pain_points"
                    placeholder="Descreva os principais problemas que o cliente enfrenta..."
                    value={clientProfile.pain_points}
                    onChange={(e) => setClientProfile({...clientProfile, pain_points: e.target.value})}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="goals">Objetivos e Metas</Label>
                  <Textarea
                    id="goals"
                    placeholder="Quais são os objetivos que o cliente quer alcançar..."
                    value={clientProfile.goals}
                    onChange={(e) => setClientProfile({...clientProfile, goals: e.target.value})}
                  />
                </div>
                <Button onClick={saveClientProfile} disabled={loading || !currentProject} className="w-full">
                  {loading ? 'Salvando...' : 'Salvar Perfil e Enriquecer Dados'}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Narrativa */}
          <TabsContent value="narrative" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5" />
                  Narrativa Comercial
                </CardTitle>
                <CardDescription>
                  Narrativa personalizada gerada por IA
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {!narrative ? (
                  <div className="text-center py-8">
                    <p className="text-gray-500 mb-4">Nenhuma narrativa gerada ainda</p>
                    <Button onClick={generateNarrative} disabled={loading || !currentProject}>
                      {loading ? 'Gerando...' : 'Gerar Narrativa com IA'}
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-6">
                    {narrative.introduction && (
                      <div>
                        <h3 className="font-semibold text-lg mb-2">Introdução</h3>
                        <p className="text-gray-700">{narrative.introduction}</p>
                      </div>
                    )}
                    {narrative.problem_statement && (
                      <div>
                        <h3 className="font-semibold text-lg mb-2">Identificação do Problema</h3>
                        <p className="text-gray-700">{narrative.problem_statement}</p>
                      </div>
                    )}
                    {narrative.solution_overview && (
                      <div>
                        <h3 className="font-semibold text-lg mb-2">Proposta de Solução</h3>
                        <p className="text-gray-700">{narrative.solution_overview}</p>
                      </div>
                    )}
                    {narrative.benefits && (
                      <div>
                        <h3 className="font-semibold text-lg mb-2">Benefícios</h3>
                        <p className="text-gray-700">{narrative.benefits}</p>
                      </div>
                    )}
                    {narrative.social_proof && (
                      <div>
                        <h3 className="font-semibold text-lg mb-2">Prova Social</h3>
                        <p className="text-gray-700">{narrative.social_proof}</p>
                      </div>
                    )}
                    {narrative.call_to_action && (
                      <div>
                        <h3 className="font-semibold text-lg mb-2">Chamada para Ação</h3>
                        <p className="text-gray-700">{narrative.call_to_action}</p>
                      </div>
                    )}
                    <div className="flex gap-2">
                      <Button onClick={generatePresentation} disabled={loading}>
                        {loading ? 'Gerando...' : 'Gerar Apresentação'}
                      </Button>
                      <Button onClick={generateObjections} variant="outline" disabled={loading}>
                        {loading ? 'Gerando...' : 'Gerar Objeções'}
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Apresentação */}
          <TabsContent value="presentation" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Apresentação Visual
                </CardTitle>
                <CardDescription>
                  Slides gerados automaticamente baseados na narrativa
                </CardDescription>
              </CardHeader>
              <CardContent>
                {!presentation ? (
                  <div className="text-center py-8">
                    <p className="text-gray-500 mb-4">Nenhuma apresentação gerada ainda</p>
                    <p className="text-sm text-gray-400">Gere uma narrativa primeiro para criar a apresentação</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold">{presentation.title}</h3>
                      <Badge>{presentation.content?.total_slides || 0} slides</Badge>
                    </div>
                    {presentation.content?.slides && (
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {presentation.content.slides.map((slide, index) => (
                          <Card key={slide.id} className="border-2 border-dashed border-gray-200">
                            <CardHeader className="pb-2">
                              <CardTitle className="text-sm">Slide {index + 1}</CardTitle>
                              <Badge variant="outline" className="w-fit">{slide.type}</Badge>
                            </CardHeader>
                            <CardContent>
                              <h4 className="font-medium mb-2">{slide.title}</h4>
                              <p className="text-sm text-gray-600 line-clamp-3">{slide.content}</p>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Objeções */}
          <TabsContent value="objections" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MessageSquare className="h-5 w-5" />
                  Simulador de Objeções
                </CardTitle>
                <CardDescription>
                  Objeções comuns e respostas preparadas
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8">
                  <p className="text-gray-500 mb-4">Funcionalidade em desenvolvimento</p>
                  <Button variant="outline" disabled>
                    <Zap className="h-4 w-4 mr-2" />
                    Gerar Objeções
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App
