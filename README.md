# Relatorio-de-Vendas
Relatorio mensal e semanal sobre o total de vendas separado por caixa, exibido em dashboard incluindo opção de impressão do relatorio

---

### README

```markdown
# Sistema de Vendas

Um sistema web simples para registro e análise de vendas, construído com Flask, Pandas e Chart.js. Permite inserção manual de vendas e visualização de dados em um dashboard interativo com gráficos e tabelas.

## Funcionalidades

- **Inserção de Vendas**: Adicione vendas manualmente com valor, caixa e data.
- **Dashboard Interativo**:
  - Filtre vendas por ano e mês.
  - Visualize o total mensal por caixa em um gráfico de pizza.
  - Veja vendas semanais por caixa em gráficos separados.
  - Consulte as últimas 10 vendas em uma tabela.
- **Armazenamento**: Dados salvos em um arquivo CSV (`vendas.csv`).

## Tecnologias Utilizadas
- **Backend**: Flask (Python)
- **Manipulação de Dados**: Pandas
- **Frontend**: HTML, Chart.js (gráficos), CSS (estilização)
- **Hospedagem Local**: Flask Development Server

## Como Usar

### Pré-requisitos
- Python 3.x instalado
- Navegador web moderno

### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/FlpsRodri/sistema-de-vendas.git
   cd sistema-de-vendas
