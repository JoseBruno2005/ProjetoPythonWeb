from flask import *
import dao
import dataanalise as da
import plotly.express as px

app = Flask(__name__)


@app.route('/cadastrarusuario', methods=['GET', 'POST'])
def redirecionar_cadastro_user():
    if request.method == 'GET':
         return render_template('cadastrar_usuario.html')
    elif request.method == 'POST':
        login = str(request.form.get('nome'))
        senha = str(request.form.get('senha'))

        if(dao.inseriruser(login, senha, dao.conectardb())):
            return render_template('index2.html')
        else:
            texto='e-mail já cadastrado'
            return render_template('cadastrar_usuario.html', msg=texto)

@app.route('/login', methods=['POST'])
def cadastrar_usuario():
    nome = str(request.form.get('nome'))
    senha = str(request.form.get('senha'))

    if dao.verificarlogin(nome, senha, dao.conectardb()):
        return render_template('menu.html')
    else:
        return render_template('index2.html')

@app.route('/grafvioleciapib', methods=['POST','GET'])
def gerarGrafViolenciaPib():
    if request.method == 'POST':
        filtro = int(request.form.get('valor'))
    else:
        filtro = 10

    dados = da.lerdados()
    dados.drop(dados.sort_values(by=['cvli'], ascending=False).head(3).index, inplace=True)
    dados.drop(dados.sort_values(by=['rendapercapita'], ascending=False).head(filtro).index, inplace=True)
    dados.drop(dados.sort_values(by=['rendapercapita'], ascending=True).head(2).index, inplace=True)

    fig = px.scatter(dados, x='rendapercapita', y='cvli', hover_data=['municipio'])
    return render_template('grafviolenciapib.html', plot=fig.to_html())

@app.route('/idh', methods=['POST', 'GET'])
def exibirgraficoidh():
    if request.method == 'POST':
        qtdcidade = int(request.form.get('quantidade'))
    else:
        qtdcidade = 10

    dados = da.lerdados()
    dados_top = dados.nlargest(qtdcidade, 'idh')
    fig4 = da.exibirgraficoidebidh(dados_top)
    return render_template('idh.html', idh=fig4.to_html())

@app.route('/tabela', methods=['POST', 'GET'])
def exibirtabela():
    if request.method == 'POST':
        coluna = str(request.form.get('coluna'))
    else:
        coluna = 'pib'

    fig5 = da.gerar_tabela(coluna)
    return render_template('tabela.html', tabela=fig5.to_html())



@app.route('/grafcorrelacao')
def gerarGrafCorrelacao():
    dados = da.lerdados()
    fig2 = da.exibirmapacorrelacoes(dados)

    return render_template('grafcorrelacao.html', mapa=fig2.to_html())

@app.route('/melhoresedu')
def exibirmunicipiosedu():
    data = da.lerdados()

    data['somaedu'] = data['idebanosiniciais'] + data["idebanosfinais"]
    print(data.sort_values(by=['somaedu'], ascending=False, inplace=True))
    fig = da.exibirgraficobarraseduc(data.head(15))

    return render_template('melhoresedu.html', figura=fig.to_html())


@app.route('/empregopib')
def empregopib():
    data = da.lerdados()

    fig3 = da.exibirgraficopibpemprego(data.head(10))
    return render_template('empregopib.html', pizza=fig3.to_html())

@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/')
def motormanda():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)