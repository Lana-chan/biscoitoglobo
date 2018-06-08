import json, requests, os


# API - https://dadosabertos.camara.leg.br/swagger/api.html
PATH = os.path.dirname(os.path.abspath(__file__)) + "/data/archive.json"

class Tramitacoes():
    def __init__(self, data={}):
        self.url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
        self.data = data
        self.results = requests.get(self.url, data)
        self.tramitacoes = json.loads(self.results.content.decode("utf-8"))['dados']

    def getDetalhe(self):
        for p in self.tramitacoes:
            r = requests.get(self.url+"/"+str(p['id']))
            p.update(json.loads(r.content.decode("utf-8"))['dados'])

    def getVotacoes(self):
        print("Getting Votacoes...")
        for p in self.tramitacoes:
            r = requests.get(self.url+"/"+str(p['id'])+"/votacoes")
            p['votacao'] = json.loads(r.content.decode("utf-8"))['dados']
            print(p['votacao'])

    def getAutor(self):
        print("Getting autores...")
        for p in self.tramitacoes:
            r = requests.get(self.url+"/"+str(p['id'])+"/autores")
            p['autores'] = json.loads(r.content.decode("utf-8"))['dados']
            for a in p['autores']:
                if a["uri"]:
                    r = requests.get(a["uri"])
                    a.update(json.loads(r.content.decode("utf-8"))['dados'])


def lockandload(data, path=PATH):
    t = Tramitacoes(data)
    t.getDetalhe()
    t.getAutor()
    arquivo = open(path, 'w')
    json.dump(t.tramitacoes, arquivo)
    return t.tramitacoes



#926 - Aguardando Apreciação pelo Senado Federal
#939 - Apreciação de Veto
#1140 - Transformado em Norma Juridica
data = {
    "siglaTipo" : ["PL","PLS","PEC"]
}


if os.path.isfile(PATH):
    tt = json.load(open(PATH, 'r'))
else:
    tt = lockandload(data)


from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def tramita():
    return render_template('tramita.html', projetos=tt)
