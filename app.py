from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from datetime import datetime


app = Flask(__name__)

CSV_FILE = 'vendas.csv'

def salvar_venda(data):
    df = pd.DataFrame([data])
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(CSV_FILE, index=False)

def carregar_vendas():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce', dayfirst=False)
        df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
        df = df.dropna(subset=['Data', 'Valor'])
        return df
    return pd.DataFrame(columns=['Valor', 'Caixa', 'Data'])

def gerar_analises(df):
    df['Semana'] = df['Data'].dt.to_period('W-MON').apply(lambda r: r.start_time)
    df['Mes'] = df['Data'].dt.month_name()
    por_caixa = df.groupby('Caixa')['Valor'].sum().reset_index()
    por_semana = df.groupby('Semana')['Valor'].sum().reset_index()
    por_mes = df.groupby('Mes')['Valor'].sum().reset_index()
    return por_caixa, por_semana, por_mes

def gerar_dados_graficos(df, ano, mes):
    df['Ano'] = df['Data'].dt.year
    df['MesNum'] = df['Data'].dt.month
    df['Semana'] = df['Data'].dt.to_period('W-MON').apply(lambda r: r.start_time)

    df_filtrado = df[(df['Ano'] == ano) & (df['MesNum'] == mes)]

    total_por_caixa_mes = df_filtrado.groupby('Caixa')['Valor'].sum().reset_index()
    semanas = sorted(df_filtrado['Semana'].unique())
    graficos_semanais = []
    for semana in semanas:
        semana_df = df_filtrado[df_filtrado['Semana'] == semana]
        por_caixa_semana = semana_df.groupby('Caixa')['Valor'].sum().reset_index()
        graficos_semanais.append({
            'semana': semana.strftime('%d/%m/%Y'),
            'dados': por_caixa_semana.to_dict(orient='records')
        })

    return total_por_caixa_mes.to_dict(orient='records'), graficos_semanais

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/adicionar', methods=['POST'])
def adicionar():
    valor = float(request.form['valor'])
    caixa = request.form['caixa']
    data = datetime.strptime(request.form['data'], '%Y-%m-%d')
    salvar_venda({'Valor': valor, 'Caixa': caixa, 'Data': data.strftime('%Y-%m-%d')})
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    df = carregar_vendas()
    ano = datetime.now().year
    mes = datetime.now().month
    if request.method == 'POST':
        ano = int(request.form['ano'])
        mes = int(request.form['mes'])

    por_caixa, por_semana, por_mes = gerar_analises(df)
    ultimas_vendas = df.sort_values(by='Data', ascending=False).head(10)
    grafico_mes, graficos_semanais = gerar_dados_graficos(df, ano, mes)

    return render_template('dashboard.html', vendas=ultimas_vendas.to_dict(orient='records'),
                           por_caixa=por_caixa.to_dict(orient='records'),
                           por_dia=por_semana.to_dict(orient='records'),
                           por_mes=por_mes.to_dict(orient='records'),
                           grafico_mes=grafico_mes,
                           graficos_semanais=graficos_semanais,
                           mes_selecionado=mes, ano_selecionado=ano)

if __name__ == '__main__':

    app.run(debug=True)
