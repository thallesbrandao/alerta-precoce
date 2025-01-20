# Sistema de Alerta Precoce para Desastres Naturais

Um sistema de monitoramento e alerta desenvolvido em Python para prevenção de desastres naturais na região do Vale do Itajaí, Santa Catarina. O projeto faz parte de uma iniciativa de extensão universitária da UNINTER.

## 🎯 Sobre o Projeto

Este sistema monitora condições climáticas em tempo real para prever e alertar sobre possíveis desastres naturais, focando principalmente em enchentes e deslizamentos. O projeto atende aos Objetivos de Desenvolvimento Sustentável (ODS) da ONU números 11 (Cidades e Comunidades Sustentáveis) e 13 (Ação contra a Mudança Global do Clima).

## 🔧 Tecnologias Utilizadas

- Python 3.8+
- BeautifulSoup4 para web scraping
- Requests para integração com APIs
- NumPy para processamento numérico
- Scikit-learn para análise preditiva
- SMTPLib para sistema de notificações

## 📋 Pré-requisitos

```bash
Python 3.8 ou superior
Pip (gerenciador de pacotes Python)
```

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone git@github.com:thallesbrandao/alerta-precoce.git
cd alerta-precoce
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o arquivo config.json:
```json
{
    "email": "seu_email@example.com",
    "senha": "sua_senha",
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "cache_duration": 300
}
```

## 💻 Como Usar

1. Execute o programa principal:
```bash
python main.py
```

2. O sistema irá:
- Coletar dados meteorológicos automaticamente
- Analisar condições de risco
- Enviar alertas quando necessário

## 🏗️ Estrutura do Projeto

```
sistema-alerta-desastres/
├── main.py               # Arquivo principal
├── config.json          # Configurações do sistema
├── requirements.txt     # Dependências
├── README.md           # Documentação
└── logs/               # Registros do sistema
```

## 🔍 Funcionalidades Principais

- Monitoramento em tempo real de condições climáticas
- Análise preditiva usando machine learning
- Sistema automático de notificações
- Cache de dados para otimização
- Registro detalhado de eventos

## 📊 Endpoints da API

O sistema utiliza a API do Climatempo para obter dados meteorológicos:

- GET /previsao-do-tempo/agora/cidade/{id}/{cidade}-sc
  - Retorna dados atuais de temperatura, umidade e precipitação

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Nova Feature'`)
4. Push para a Branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

- **Thalles Brandão** - [GitHub](https://github.com/thallesbrandao)

## 📄 Referências

- [Documentação Python](https://docs.python.org/3/)
- [Climatempo API](https://advisor.climatempo.com.br/)
- [ODS - ONU](https://brasil.un.org/pt-br/sdgs)

---
Desenvolvido como parte do projeto de extensão da UNINTER - 2024