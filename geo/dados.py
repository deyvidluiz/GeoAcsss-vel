import json
from hashlib import sha256
from pathlib import Path
from urllib.parse import quote, unquote


ANOS = {
    1: {
        "titulo": "1º Ano",
        "descricao": "Natureza, paisagens e relações entre sociedade e ambiente.",
    },
    2: {
        "titulo": "2º Ano",
        "descricao": "População, cidades, produção econômica e integração mundial.",
    },
    3: {
        "titulo": "3º Ano",
        "descricao": "Geopolítica, conflitos, blocos econômicos e temas globais.",
    },
}


def imagem_commons(arquivo, alt, observacao, autor="Wikimedia Commons", licenca="", zoom=True):
    nome = arquivo.replace("File:", "")
    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(nome)}"
    autoria = f", {autor}" if autor else ""
    licenca_txt = f", {licenca}" if licenca else ""
    return {
        "arquivo": url,
        "source_url": url,
        "alt": alt,
        "fonte": f"Wikimedia Commons; arquivo {arquivo}{autoria}{licenca_txt}.",
        "observacao": observacao,
        "zoom": zoom,
        "externa": True,
    }


def hash_int(texto):
    return int(sha256(texto.encode("utf-8")).hexdigest(), 16)


def alternativas_com_correta(alternativas, correta, salt):
    correta_texto = alternativas[correta]
    incorretas = [texto for indice, texto in enumerate(alternativas) if indice != correta]
    incorretas.sort(key=lambda texto: hash_int(f"{salt}|{texto}"))
    posicao_correta = hash_int(salt) % len(alternativas)
    resultado = []
    indice_incorreta = 0
    for indice in range(len(alternativas)):
        if indice == posicao_correta:
            resultado.append({"texto": correta_texto, "correta": True})
        else:
            resultado.append({"texto": incorretas[indice_incorreta], "correta": False})
            indice_incorreta += 1
    return resultado


def caminho_catalogo_local(chave, imagem):
    nome = unquote(imagem.get("source_url", imagem["arquivo"]).rsplit("/", 1)[-1])
    extensao = Path(nome).suffix.lower() or ".jpg"
    base_estatico = Path(__file__).resolve().parent / "static"
    for caminho in (f"geo/imagens/catalogo/{chave}{extensao}", f"geo/imagens/catalogo/{chave}.svg"):
        arquivo_estatico = base_estatico / caminho
        if not arquivo_estatico.exists():
            continue
        if arquivo_estatico.suffix == ".svg" and "Recurso visual didático local" in arquivo_estatico.read_text(
            encoding="utf-8",
            errors="ignore",
        ):
            continue
        return caminho
    return None


def usar_catalogo_local():
    for chave, imagem in IMAGENS_REAIS.items():
        if imagem.get("externa") and imagem.get("source_url"):
            caminho_local = caminho_catalogo_local(chave, imagem)
            if caminho_local:
                imagem["arquivo"] = caminho_local
                imagem["externa"] = False


def carregar_fotos_substitutas():
    manifesto = Path(__file__).resolve().parent / "fotos_substitutas.json"
    if not manifesto.exists():
        return {}
    return json.loads(manifesto.read_text(encoding="utf-8"))


def carregar_imagens_suplementares():
    catalogo = Path(__file__).resolve().parent / "imagens_suplementares.json"
    if not catalogo.exists():
        return {}
    return json.loads(catalogo.read_text(encoding="utf-8"))


def carregar_imagens_aulas_reais():
    manifesto = Path(__file__).resolve().parent / "imagens_aulas_reais.json"
    if not manifesto.exists():
        return {}
    return json.loads(manifesto.read_text(encoding="utf-8"))


def carregar_urls_commons_resolvidas():
    manifesto = Path(__file__).resolve().parent / "urls_commons_resolvidas.json"
    if not manifesto.exists():
        return {}
    return {
        origem: destino
        for origem, destino in json.loads(manifesto.read_text(encoding="utf-8")).items()
        if destino
    }

TEMAS_BASE = {
    "relevo": {
        "titulo": "Relevo",
        "ano": 1,
        "descricao": "Formas da superfície terrestre e seus processos.",
        "importante": True,
        "aulas": [
            ("Formas do relevo", "Reconhecer planaltos, planícies, depressões e montanhas.", "chapadas, serras e planícies litorâneas"),
            ("Agentes internos", "Relacionar placas tectônicas, vulcões e terremotos à formação do relevo.", "Cordilheira dos Andes"),
            ("Agentes externos", "Entender erosão, transporte e sedimentação.", "voçorocas em áreas desmatadas"),
            ("Relevo brasileiro", "Identificar características gerais do relevo do Brasil.", "Planalto Central e Planície Amazônica"),
            ("Relevo e sociedade", "Analisar como o relevo influencia cidades, estradas e agricultura.", "ocupação de encostas urbanas"),
            ("Riscos geomorfológicos", "Compreender enchentes, deslizamentos e prevenção.", "áreas de risco em morros"),
        ],
    },
    "clima": {
        "titulo": "Clima",
        "ano": 1,
        "descricao": "Padrões atmosféricos, tipos de clima e climas brasileiros.",
        "importante": True,
        "aulas": [
            ("Tempo e clima", "Diferenciar condição do momento e padrão de longa duração.", "previsão de chuva de hoje e clima semiárido"),
            ("Elementos do clima", "Reconhecer temperatura, umidade, pressão, ventos e precipitação.", "termômetro e pluviômetro"),
            ("Fatores climáticos", "Explicar latitude, altitude, maritimidade, continentalidade e massas de ar.", "cidades altas mais frescas"),
            ("Massas de ar no Brasil", "Relacionar massas de ar às mudanças do tempo.", "frentes frias no Centro-Sul"),
            ("Climas brasileiros", "Identificar climas equatorial, tropical, semiárido, atlântico e subtropical.", "Amazônia quente e úmida"),
            ("Mudanças climáticas", "Compreender causas humanas e consequências sociais.", "ondas de calor e eventos extremos"),
            ("Clima e cotidiano", "Perceber efeitos do clima na saúde, agricultura e energia.", "estiagem afetando reservatórios"),
        ],
    },
    "vegetacao": {
        "titulo": "Vegetação",
        "ano": 1,
        "descricao": "Biomas, plantas nativas e relação com clima e solo.",
        "aulas": [
            ("O que é vegetação", "Compreender vegetação como cobertura vegetal de uma área.", "mata, campo e savana"),
            ("Biomas brasileiros", "Reconhecer Amazônia, Cerrado, Caatinga, Mata Atlântica, Pantanal e Pampa.", "Cerrado com árvores retorcidas"),
            ("Vegetação e clima", "Relacionar chuva e temperatura aos tipos de plantas.", "Caatinga adaptada à seca"),
            ("Impactos e conservação", "Analisar desmatamento, queimadas e proteção da biodiversidade.", "corredores ecológicos"),
        ],
    },
    "hidrografia": {
        "titulo": "Hidrografia",
        "ano": 1,
        "descricao": "Rios, bacias hidrográficas e uso da água.",
        "aulas": [
            ("Águas continentais", "Identificar rios, lagos, aquíferos e nascentes.", "Aquífero Guarani"),
            ("Bacias hidrográficas", "Entender rio principal, afluentes, divisor de águas e foz.", "Bacia Amazônica"),
            ("Uso da água", "Relacionar abastecimento, irrigação, indústria e energia.", "hidrelétricas no Rio Paraná"),
            ("Problemas hídricos", "Compreender poluição, assoreamento, enchentes e escassez.", "rios urbanos poluídos"),
        ],
    },
    "cartografia": {
        "titulo": "Cartografia",
        "ano": 1,
        "descricao": "Mapas, escala, orientação, coordenadas e leitura espacial.",
        "aulas": [
            ("Mapas e representações", "Entender que mapas selecionam e organizam informações do espaço.", "mapa político do Brasil"),
            ("Escala cartográfica", "Diferenciar escala gráfica e numérica.", "1:100.000 em mapas regionais"),
            ("Coordenadas geográficas", "Localizar pontos por latitude e longitude.", "Linha do Equador e Meridiano de Greenwich"),
            ("Leitura de mapas temáticos", "Interpretar legenda, símbolos e cores.", "mapa de clima ou população"),
        ],
    },
    "estrutura-da-terra": {
        "titulo": "Estrutura da Terra",
        "ano": 1,
        "descricao": "Camadas internas, placas tectônicas e dinâmica terrestre.",
        "aulas": [
            ("Camadas da Terra", "Reconhecer crosta, manto, núcleo externo e núcleo interno.", "crosta oceânica e continental"),
            ("Placas tectônicas", "Compreender movimentos e limites das placas.", "encontro entre placas na América do Sul"),
            ("Vulcões e terremotos", "Relacionar eventos geológicos às bordas de placas.", "Círculo de Fogo do Pacífico"),
            ("Rochas e minerais", "Diferenciar rochas ígneas, sedimentares e metamórficas.", "granito, calcário e mármore"),
        ],
    },
    "solos": {
        "titulo": "Solos",
        "ano": 1,
        "descricao": "Formação, tipos, uso e conservação dos solos.",
        "aulas": [
            ("Formação do solo", "Entender intemperismo, matéria orgânica e tempo geológico.", "solo formado pela decomposição de rochas"),
            ("Características dos solos", "Observar textura, cor, fertilidade e permeabilidade.", "solo argiloso e arenoso"),
            ("Uso agrícola", "Relacionar solo, relevo, água e produção de alimentos.", "terra roxa em áreas agrícolas"),
            ("Conservação", "Compreender erosão, terraceamento, cobertura vegetal e manejo.", "plantio em curvas de nível"),
        ],
    },
    "problemas-ambientais": {
        "titulo": "Problemas ambientais",
        "ano": 1,
        "descricao": "Impactos ambientais e formas de prevenção.",
        "aulas": [
            ("Impacto ambiental", "Diferenciar impacto natural e impacto causado por atividades humanas.", "desmatamento para expansão urbana"),
            ("Poluição", "Reconhecer poluição do ar, da água e do solo.", "esgoto sem tratamento nos rios"),
            ("Desmatamento e queimadas", "Analisar perdas de biodiversidade e alterações climáticas locais.", "queimadas no Cerrado"),
            ("Soluções sustentáveis", "Relacionar consumo, reciclagem, saneamento e proteção ambiental.", "coleta seletiva e reflorestamento"),
        ],
    },
    "populacao": {
        "titulo": "População",
        "ano": 2,
        "descricao": "Quantidade, distribuição e características dos habitantes.",
        "importante": True,
        "aulas": [
            ("Conceitos demográficos", "Diferenciar população absoluta, relativa e densidade demográfica.", "Brasil populoso e pouco povoado em algumas áreas"),
            ("Crescimento populacional", "Relacionar natalidade, mortalidade e crescimento vegetativo.", "queda da mortalidade infantil"),
            ("Estrutura etária", "Interpretar pirâmides etárias e envelhecimento populacional.", "base estreita em países envelhecidos"),
            ("Distribuição da população", "Explicar por que pessoas se concentram em certas regiões.", "litoral brasileiro mais povoado"),
            ("População brasileira", "Analisar diversidade, desigualdades e mudanças demográficas.", "envelhecimento no Brasil"),
            ("Indicadores sociais", "Usar IDH, renda, escolaridade e saneamento para comparar condições de vida.", "diferenças regionais de saneamento"),
        ],
    },
    "migracoes": {
        "titulo": "Migrações",
        "ano": 2,
        "descricao": "Deslocamentos de pessoas entre lugares.",
        "aulas": [
            ("Tipos de migração", "Diferenciar migração interna, externa, temporária e definitiva.", "mudança de um estado para outro"),
            ("Causas das migrações", "Relacionar trabalho, estudo, conflitos, clima e família.", "migração por emprego"),
            ("Migrações no Brasil", "Entender fluxos campo-cidade, regionais e pendulares.", "deslocamento diário para trabalhar"),
            ("Refugiados e direitos", "Compreender deslocamentos forçados e acolhimento.", "pessoas que fogem de guerras"),
        ],
    },
    "urbanizacao": {
        "titulo": "Urbanização",
        "ano": 2,
        "descricao": "Crescimento das cidades e problemas urbanos.",
        "importante": True,
        "aulas": [
            ("O que é urbanização", "Compreender crescimento urbano e aumento da população das cidades.", "expansão de áreas metropolitanas"),
            ("Rede urbana", "Entender hierarquia urbana e influência das cidades.", "metrópoles e centros regionais"),
            ("Metropolização", "Analisar conurbação, regiões metropolitanas e fluxos diários.", "Grande São Paulo"),
            ("Problemas urbanos", "Reconhecer moradia precária, trânsito, enchentes e saneamento insuficiente.", "ocupação de várzeas"),
            ("Planejamento urbano", "Relacionar mobilidade, habitação, áreas verdes e participação social.", "corredores de ônibus"),
            ("Cidades sustentáveis", "Identificar soluções para reduzir desigualdades e impactos.", "transporte coletivo e parques urbanos"),
        ],
    },
    "globalizacao": {
        "titulo": "Globalização",
        "ano": 2,
        "descricao": "Conexões entre países, economia, cultura e informação.",
        "importante": True,
        "aulas": [
            ("Conceito de globalização", "Entender a intensificação das conexões mundiais.", "produto fabricado em vários países"),
            ("Fluxos globais", "Reconhecer fluxos de capitais, mercadorias, pessoas e informações.", "transferências bancárias internacionais"),
            ("Empresas transnacionais", "Analisar produção em rede e cadeias globais.", "peças produzidas em diferentes continentes"),
            ("Cultura e consumo", "Perceber trocas culturais e padronização de hábitos.", "músicas e marcas circulando pelo mundo"),
            ("Desigualdades", "Avaliar quem ganha e quem perde com a integração mundial.", "países exportadores de matéria-prima"),
            ("Tecnologia e redes", "Relacionar internet, transportes e comunicação à globalização.", "cabos submarinos de internet"),
        ],
    },
    "industrializacao": {
        "titulo": "Industrialização",
        "ano": 2,
        "descricao": "Transformações produtivas, tecnologia e trabalho.",
        "aulas": [
            ("Revoluções industriais", "Compreender mudanças técnicas desde a máquina a vapor.", "fábricas têxteis do século XIX"),
            ("Tipos de indústria", "Diferenciar bens de consumo, bens intermediários e bens de capital.", "siderúrgicas e montadoras"),
            ("Industrialização brasileira", "Entender concentração industrial e desconcentração recente.", "Sudeste industrializado"),
            ("Trabalho e tecnologia", "Relacionar automação, qualificação e mudanças no emprego.", "robôs em linhas de montagem"),
        ],
    },
    "agropecuaria": {
        "titulo": "Agropecuária",
        "ano": 2,
        "descricao": "Produção no campo, modernização e impactos.",
        "aulas": [
            ("Agricultura e pecuária", "Diferenciar atividades agrícolas e criação de animais.", "plantio de soja e criação bovina"),
            ("Modernização do campo", "Relacionar máquinas, insumos e produtividade.", "colheitadeiras e irrigação"),
            ("Estrutura fundiária", "Compreender concentração de terras e agricultura familiar.", "latifúndios e pequenas propriedades"),
            ("Impactos socioambientais", "Analisar desmatamento, uso de água e conflitos no campo.", "expansão agrícola sobre biomas"),
        ],
    },
    "fontes-de-energia": {
        "titulo": "Fontes de energia",
        "ano": 2,
        "descricao": "Energia renovável, não renovável e matriz energética.",
        "aulas": [
            ("Matriz energética", "Entender o conjunto de fontes usadas por uma sociedade.", "petróleo, hidrelétrica e biomassa"),
            ("Fontes não renováveis", "Reconhecer petróleo, carvão, gás natural e urânio.", "termoelétricas a carvão"),
            ("Fontes renováveis", "Identificar hidrelétrica, solar, eólica e biomassa.", "parques eólicos no Nordeste"),
            ("Energia e ambiente", "Analisar impactos, segurança energética e transição.", "emissões de gases de efeito estufa"),
        ],
    },
    "economia-brasileira": {
        "titulo": "Economia brasileira",
        "ano": 2,
        "descricao": "Setores econômicos, desigualdades regionais e comércio.",
        "aulas": [
            ("Setores da economia", "Diferenciar setores primário, secundário e terciário.", "agricultura, indústria e serviços"),
            ("Formação econômica", "Relacionar ciclos econômicos e ocupação do território.", "cana-de-açúcar, ouro e café"),
            ("Desigualdades regionais", "Analisar concentração econômica e infraestrutura.", "diferenças entre regiões brasileiras"),
            ("Brasil no comércio mundial", "Entender exportações, importações e dependência tecnológica.", "soja, minério de ferro e manufaturados"),
        ],
    },
    "geopolitica": {
        "titulo": "Geopolítica",
        "ano": 3,
        "descricao": "Poder, território e relações entre países.",
        "importante": True,
        "aulas": [
            ("Poder e território", "Compreender relações entre Estado, território, soberania e poder.", "controle de fronteiras"),
            ("Estado, nação e governo", "Diferenciar conceitos básicos da política internacional.", "Estados plurinacionais"),
            ("Recursos estratégicos", "Relacionar água, petróleo, minérios e tecnologia ao poder.", "rotas de petróleo"),
            ("Fronteiras e disputas", "Analisar limites, territórios contestados e segurança.", "fronteiras militarizadas"),
            ("Potências mundiais", "Entender influência econômica, militar, cultural e tecnológica.", "Estados Unidos e China"),
            ("Geopolítica do Brasil", "Avaliar posição regional, Amazônia, Atlântico Sul e integração.", "Amazônia como área estratégica"),
            ("Geopolítica contemporânea", "Interpretar temas atuais sem simplificações.", "cibersegurança e satélites"),
        ],
    },
    "conflitos-mundiais": {
        "titulo": "Conflitos mundiais",
        "ano": 3,
        "descricao": "Disputas territoriais, políticas, econômicas e culturais.",
        "aulas": [
            ("Causas dos conflitos", "Identificar causas territoriais, políticas, étnicas e econômicas.", "disputa por recursos naturais"),
            ("Guerras e população civil", "Compreender impactos humanitários dos conflitos.", "deslocados internos e refugiados"),
            ("Terrorismo e segurança", "Analisar violência política e respostas dos Estados.", "medidas de segurança em fronteiras"),
            ("Diplomacia e paz", "Relacionar negociações, acordos e organismos internacionais.", "missões de paz da ONU"),
        ],
    },
    "blocos-economicos": {
        "titulo": "Blocos econômicos",
        "ano": 3,
        "descricao": "Acordos econômicos e integração regional.",
        "aulas": [
            ("Integração regional", "Entender por que países formam blocos econômicos.", "cooperação comercial entre vizinhos"),
            ("Tipos de bloco", "Diferenciar zona de livre comércio, união aduaneira e mercado comum.", "livre circulação de mercadorias"),
            ("Mercosul", "Conhecer objetivos, membros e desafios do bloco sul-americano.", "comércio entre Brasil e Argentina"),
            ("União Europeia", "Analisar integração profunda, moeda comum e tensões internas.", "euro e Parlamento Europeu"),
        ],
    },
    "relacoes-internacionais": {
        "titulo": "Relações internacionais",
        "ano": 3,
        "descricao": "Diplomacia, cooperação e organizações internacionais.",
        "aulas": [
            ("Diplomacia", "Compreender negociação oficial entre Estados.", "embaixadas e tratados"),
            ("Cooperação internacional", "Relacionar ajuda, comércio, ciência e meio ambiente.", "acordos climáticos"),
            ("Direitos humanos", "Entender princípios internacionais de proteção às pessoas.", "direito a refúgio"),
            ("Desafios globais", "Analisar problemas que ultrapassam fronteiras.", "pandemias e mudanças climáticas"),
        ],
    },
    "organizacoes-internacionais": {
        "titulo": "Organizações internacionais",
        "ano": 3,
        "descricao": "Instituições multilaterais e cooperação entre países.",
        "aulas": [
            ("O que são organizações internacionais", "Entender instituições formadas por países.", "ONU e OMC"),
            ("ONU", "Conhecer atuação em paz, direitos humanos e desenvolvimento.", "Conselho de Segurança"),
            ("Organizações econômicas", "Analisar FMI, Banco Mundial e OMC.", "regras do comércio mundial"),
            ("Limites e críticas", "Avaliar poder desigual, vetos e dificuldades de consenso.", "decisões bloqueadas por interesses nacionais"),
        ],
    },
    "globalizacao-economica": {
        "titulo": "Globalização econômica",
        "ano": 3,
        "descricao": "Mercado mundial, cadeias produtivas e finanças globais.",
        "aulas": [
            ("Mercado mundial", "Compreender integração de produção, consumo e finanças.", "bolsas de valores conectadas"),
            ("Cadeias produtivas globais", "Analisar etapas de produção distribuídas pelo mundo.", "celular com peças de vários países"),
            ("Comércio internacional", "Entender exportações, importações, tarifas e acordos.", "portos e contêineres"),
            ("Crises e dependências", "Relacionar instabilidade financeira e vulnerabilidade econômica.", "alta de preços internacionais"),
        ],
    },
    "questoes-ambientais-globais": {
        "titulo": "Questões ambientais globais",
        "ano": 3,
        "descricao": "Problemas ambientais que ultrapassam fronteiras.",
        "aulas": [
            ("Mudanças climáticas globais", "Entender aquecimento global e efeito estufa intensificado.", "aumento da temperatura média"),
            ("Biodiversidade", "Relacionar perda de espécies, habitat e equilíbrio ecológico.", "desmatamento de florestas tropicais"),
            ("Água e oceanos", "Analisar poluição marinha, escassez e disputa por água.", "plásticos nos oceanos"),
            ("Acordos ambientais", "Conhecer cooperação internacional e responsabilidades diferentes.", "Acordo de Paris"),
        ],
    },
    "nova-ordem-mundial": {
        "titulo": "Nova ordem mundial",
        "ano": 3,
        "descricao": "Mudanças no poder mundial após a Guerra Fria.",
        "aulas": [
            ("Fim da Guerra Fria", "Compreender mudanças após a rivalidade EUA-URSS.", "queda do Muro de Berlim"),
            ("Mundo multipolar", "Analisar diferentes centros de poder econômico e político.", "Estados Unidos, União Europeia e China"),
            ("Tecnologia e poder", "Relacionar dados, satélites, chips e redes digitais à geopolítica.", "disputa por semicondutores"),
            ("Desafios atuais", "Interpretar tensões comerciais, ambientais e militares.", "sanções econômicas e disputas comerciais"),
        ],
    },
}

CURIOSIDADES = [
    "O Brasil tem uma das maiores redes hidrográficas do mundo, com destaque para a Bacia Amazônica.",
    "A Linha do Equador atravessa o Norte do Brasil e influencia a presença de climas quentes.",
    "Mapas sempre fazem escolhas: escala, legenda e projeção mudam a forma como vemos o espaço.",
    "A urbanização brasileira se acelerou muito no século XX, junto com a industrialização.",
    "O Cerrado é conhecido como berço das águas por abrigar nascentes de grandes bacias brasileiras.",
    "A geopolítica também envolve tecnologia, dados, energia e rotas de transporte.",
]


IMAGENS_REAIS = {
    "clima_mapa": {
        "arquivo": "geo/imagens/clima/mapa_climas_brasil.png",
        "alt": "Mapa do Brasil com tipos climáticos segundo a classificação Köppen-Geiger.",
        "fonte": "Wikimedia Commons; mapa Köppen-Geiger do Brasil, derivado de Peel, Finlayson e McMahon.",
        "observacao": "Observe como diferentes cores indicam tipos climáticos. A legenda ajuda a comparar regiões quentes, úmidas, secas ou com inverno mais frio.",
        "zoom": True,
    },
    "clima_semiarido": {
        "arquivo": "geo/imagens/clima/clima_semiarido.jpg",
        "alt": "Paisagem de Caatinga no semiárido do Nordeste brasileiro.",
        "fonte": "Wikimedia Commons; foto CAATINGA NORDESTINA.JPG, autor XIXO, CC BY-SA 3.0.",
        "observacao": "Observe a vegetação mais espaçada e adaptada à pouca disponibilidade de água. A paisagem ajuda a relacionar clima semiárido e cobertura vegetal.",
        "zoom": True,
    },
    "vegetacao_cerrado": {
        "arquivo": "geo/imagens/vegetacao/cerrado.jpg",
        "alt": "Paisagem real de Cerrado brasileiro com árvores espaçadas e céu aberto.",
        "fonte": "Wikimedia Commons; foto Cerrado Brasileiro.jpg, autor Lbotton, CC BY-SA 3.0.",
        "observacao": "Observe as árvores mais espaçadas e a vegetação adaptada a períodos secos. A paisagem ajuda a comparar Cerrado, Caatinga e florestas úmidas.",
        "zoom": True,
    },
    "vegetacao_pantanal": {
        "arquivo": "geo/imagens/vegetacao/pantanal.jpg",
        "alt": "Paisagem real do Pantanal mato-grossense com área alagada e vegetação.",
        "fonte": "Wikimedia Commons; foto Bela paisagem do pantanal matogrossense.jpg, autor Vicente Bissoni Neto, CC BY-SA 4.0.",
        "observacao": "Observe a presença de água na paisagem. O Pantanal ajuda a relacionar vegetação, relevo baixo, hidrografia e cheias sazonais.",
        "zoom": True,
    },
    "chuva_caatinga": {
        "arquivo": "geo/imagens/clima/chuva_caatinga.jpg",
        "alt": "Chuva em área de Caatinga no Brasil.",
        "fonte": "Wikimedia Commons; arquivo Rain in the Caatinga.",
        "observacao": "A chuva modifica rapidamente a paisagem semiárida. Esse contraste ajuda a perceber a importância da distribuição da precipitação ao longo do ano.",
        "zoom": False,
    },
    "relevo_chapada": {
        "arquivo": "geo/imagens/relevo/chapada_diamantina.jpg",
        "alt": "Vista da Chapada Diamantina, na Bahia, com áreas elevadas e escarpas.",
        "fonte": "Wikimedia Commons; foto Chapada Diamantina vista.jpg, autor André Koehne, CC BY-SA/GFDL.",
        "observacao": "Observe as diferenças de altitude, as superfícies elevadas e as encostas. Esses elementos ajudam a discutir planaltos, serras e erosão.",
        "zoom": True,
    },
    "hidrografia_amazonica": {
        "arquivo": "geo/imagens/hidrografia/mapa_bacia_amazonica.png",
        "alt": "Mapa da região hidrográfica Amazônica no Brasil.",
        "fonte": "Wikimedia Commons; mapa Regiões Hidrográficas do Brasil - Amazônica, autor HVL, domínio público.",
        "observacao": "Observe a extensão da região hidrográfica. Mapas de bacias mostram áreas drenadas por rios principais e afluentes.",
        "zoom": True,
    },
    "rio_amazonas": {
        "arquivo": "geo/imagens/hidrografia/rio_amazonas.jpg",
        "alt": "Fotografia aérea do Rio Amazonas próximo a Manaus.",
        "fonte": "Wikimedia Commons; foto Rio Amazonas 02.JPG, autora GabiFMesquita, CC BY-SA 3.0.",
        "observacao": "Observe a largura do rio e sua presença marcante na paisagem. A imagem ajuda a entender a importância dos grandes rios amazônicos.",
        "zoom": True,
    },
    "populacao_densidade": {
        "arquivo": "geo/imagens/populacao/mapa_densidade_brasil.png",
        "alt": "Mapa dos estados brasileiros por densidade populacional.",
        "fonte": "Wikimedia Commons; mapa Brazilian States by Population Density, autor João Felipe C.S., domínio público.",
        "observacao": "Compare os estados pela intensidade das cores. Densidade demográfica mostra habitantes por área, não apenas população total.",
        "zoom": True,
    },
    "populacao_piramide": {
        "arquivo": "geo/imagens/populacao/piramide_etaria_brasil.png",
        "alt": "Pirâmide etária do Brasil em 2020.",
        "fonte": "Wikimedia Commons; arquivo Brazil single age population pyramid 2020.",
        "observacao": "Observe a largura das faixas etárias. A pirâmide ajuda a estudar envelhecimento, natalidade e estrutura da população.",
        "zoom": True,
    },
    "urbanizacao_sp": {
        "arquivo": "geo/imagens/populacao/urbanizacao_sao_paulo.jpg",
        "alt": "Vista do centro de São Paulo com grande concentração de edifícios.",
        "fonte": "Wikimedia Commons; foto Skyline of São Paulo centre.jpg, autor Rodrigo.Argenton, CC BY-SA 4.0.",
        "observacao": "Observe a verticalização, a concentração de construções e a densidade do espaço urbano. A imagem ajuda a discutir metropolização.",
        "zoom": True,
    },
    "geopolitica_mapa": {
        "arquivo": "geo/imagens/geopolitica/mapa_clima_koppen_brasil.png",
        "alt": "Mapa climático do Brasil usado como exemplo de mapa temático em análises territoriais.",
        "fonte": "Wikimedia Commons; Brazil Köppen Climate Map.png, CC BY-SA 3.0.",
        "observacao": "Mapas temáticos também são usados em debates geopolíticos e ambientais, porque mostram diferenças territoriais relevantes.",
        "zoom": True,
    },
}

IMAGENS_REAIS.update({
    "clima_paisagem": imagem_commons(
        "File:Agricultural Fields near Perdizes, Minas Gerais, Brazil.JPG",
        "Paisagem rural em Minas Gerais vista do espaço, com áreas agrícolas e padrões ambientais.",
        "A paisagem mostra que clima, relevo, água e uso da terra aparecem juntos. Observe os tons e formas que indicam diferentes condições ambientais.",
        "ISS Expedition 26 crew", "domínio público",
    ),
    "tempo_tempestade": imagem_commons(
        "File:Thunderstorm near Garajau, Madeira.jpg",
        "Nuvens escuras de tempestade se aproximando de uma área costeira.",
        "Esta imagem representa o tempo atmosférico: uma condição momentânea, visível naquele lugar e naquele intervalo curto.",
    ),
    "clima_termometro": imagem_commons(
        "File:German weather station in Havana Cuba.jpg",
        "Estação meteorológica com instrumentos usados para medir condições atmosféricas.",
        "Instrumentos meteorológicos transformam sensações em dados. Temperatura, pressão e umidade podem ser comparadas porque são medidas de modo padronizado.",
        "Susanne Bollinger / Pittig", "CC BY-SA 4.0",
    ),
    "clima_umidade_neblina": imagem_commons(
        "File:Boraceia densa.JPG",
        "Neblina densa em área de vegetação úmida.",
        "A neblina indica muita umidade no ar e condensação próxima à superfície. Observe como a visibilidade diminui na paisagem.",
        "Miguelrangeljr", "domínio público",
    ),
    "clima_barometro": imagem_commons(
        "File:Aneroid barometer.jpg",
        "Barômetro analógico usado para medir pressão atmosférica.",
        "O barômetro permite observar variações de pressão atmosférica, informação importante para compreender ventos e mudanças do tempo.",
    ),
    "clima_chuva_forte": imagem_commons(
        "File:After heavy rain. - geograph.org.uk - 477219.jpg",
        "Rua molhada após chuva forte.",
        "A precipitação deixa marcas visíveis na paisagem. Observe a água acumulada e relacione isso a drenagem urbana, solos e rios.",
        "John Upton", "CC BY-SA 2.0",
    ),
    "clima_vento_arvores": imagem_commons(
        "File:An old tree battles to stay upright against the relentless wind on the beach at Jericoacoara (22798032383).jpg",
        "Árvore inclinada pela ação constante dos ventos em Jericoacoara.",
        "A forma da árvore revela a ação frequente do vento. Elementos da paisagem podem registrar processos atmosféricos repetidos.",
        "Winniepix", "CC BY 2.0",
    ),
    "clima_latitude_equador": imagem_commons(
        "File:Equator sign in Macapa Brazil.jpg",
        "Marco da Linha do Equador em Macapá, no Brasil.",
        "A Linha do Equador ajuda a discutir latitude. Áreas próximas a ela recebem alta insolação ao longo do ano.",
    ),
    "clima_altitude_serra": imagem_commons(
        "File:Neblina na Serra da Moeda.jpg",
        "Serra com neblina em área elevada.",
        "Paisagens de altitude ajudam a perceber como a elevação interfere na temperatura e na circulação do ar.",
        "Eduardo Gabão", "CC BY-SA 3.0",
    ),
    "clima_massas_ar": imagem_commons(
        "File:South America Köppen Map.png",
        "Mapa climático da América do Sul.",
        "Mapas atmosféricos e climáticos permitem observar padrões regionais e relacioná-los à circulação de massas de ar.",
    ),
    "clima_equatorial_amazonia": imagem_commons(
        "File:Amazon CIAT (5).jpg",
        "Floresta Amazônica densa e úmida.",
        "A vegetação fechada ajuda a compreender o clima equatorial: calor, umidade elevada e chuvas frequentes.",
        "Neil Palmer/CIAT", "CC BY-SA 2.0",
    ),
    "clima_tropical_paisagem": imagem_commons(
        "File:Cerrado sentido restrito no Parque Nacional de Brasília.jpg",
        "Paisagem tropical de Cerrado com árvores espaçadas.",
        "A paisagem tropical mostra alternância entre estação chuvosa e estação seca, com vegetação adaptada a essa sazonalidade.",
    ),
    "clima_subtropical_sul": imagem_commons(
        "File:Aparados da Serra National Park 02.jpg",
        "Paisagem no Sul do Brasil com relevo de serra.",
        "No Sul do Brasil, a latitude maior e a atuação de massas de ar polar ajudam a explicar temperaturas mais baixas em parte do ano.",
    ),
    "relevo_montanha": imagem_commons(
        "File:Pico da Neblina.jpg",
        "Pico da Neblina, uma das maiores elevações do Brasil.",
        "Montanhas apresentam grandes variações de altitude. Observe a elevação marcante em relação às áreas próximas.",
    ),
    "relevo_planicie": imagem_commons(
        "File:Pantanal, Mato Grosso, Brasil.jpg",
        "Área plana e alagável no Pantanal.",
        "Planícies costumam ter pequenas variações de altitude e podem acumular sedimentos e água, como ocorre em áreas pantaneiras.",
    ),
    "relevo_depressao": imagem_commons(
        "File:Vale do Catimbau - Buíque - Pernambuco - Brasil.jpg",
        "Área rebaixada e escarpada no Vale do Catimbau, Pernambuco.",
        "Depressões são áreas mais baixas que o entorno. Observe o contraste entre superfícies rebaixadas e bordas elevadas.",
    ),
    "relevo_vale": imagem_commons(
        "File:Vale do Paraíba, São Paulo, Brasil.jpg",
        "Vale alongado entre áreas mais elevadas.",
        "Vales são formas rebaixadas que muitas vezes acompanham rios. A leitura visual ajuda a perceber direção de drenagem e ocupação.",
    ),
    "relevo_erosao": imagem_commons(
        "File:Voçoroca em Avaré.jpg",
        "Voçoroca aberta pela erosão do solo.",
        "A erosão remove materiais da superfície. Observe os sulcos profundos e relacione o processo à água, solo exposto e uso da terra.",
    ),
    "relevo_intemperismo": imagem_commons(
        "File:Weathering of basalt.jpg",
        "Rocha com marcas de intemperismo.",
        "O intemperismo altera rochas no próprio lugar. Fissuras, fragmentos e mudança de cor indicam transformação lenta do material.",
    ),
    "relevo_mapa_brasil": imagem_commons(
        "File:Brazil topographic map-pt.svg",
        "Mapa topográfico do Brasil.",
        "Mapas de relevo ajudam a comparar altitudes em escala nacional. Cores e sombras indicam diferenças que a fotografia isolada não mostra.",
    ),
    "vegetacao_amazonia": imagem_commons(
        "File:Amazon rainforest from above.jpg",
        "Vista aérea da Floresta Amazônica.",
        "A cobertura florestal densa diferencia a Amazônia de biomas abertos. Observe a continuidade da vegetação.",
    ),
    "vegetacao_caatinga": imagem_commons(
        "File:CAATINGA NORDESTINA.JPG",
        "Paisagem de Caatinga no semiárido nordestino.",
        "A Caatinga apresenta plantas adaptadas à escassez de água. Observe galhos, espaçamento e solo exposto.",
        "XIXO", "CC BY-SA 3.0",
    ),
    "vegetacao_mata_atlantica": imagem_commons(
        "File:Mata Atlântica - Parque Estadual da Serra do Mar.jpg",
        "Trecho de Mata Atlântica em área serrana.",
        "A Mata Atlântica tem vegetação densa e úmida, mas hoje aparece muito fragmentada pela ocupação histórica do litoral.",
    ),
    "vegetacao_pampa": imagem_commons(
        "File:Brazilian Pampa.jpg",
        "Paisagem campestre do Pampa brasileiro.",
        "O Pampa se destaca por campos abertos. Essa formação não deve ser representada por fotografia genérica de floresta.",
    ),
    "hidrografia_nascente": imagem_commons(
        "File:Spring water in Brazil.jpg",
        "Nascente com água surgindo no terreno.",
        "A nascente marca o início de um curso d'água. Observe a relação entre solo, vegetação e água superficial.",
    ),
    "hidrografia_afluente": imagem_commons(
        "File:Confluence of Rio Negro and Rio Solimoes near Manaus, Brazil.jpg",
        "Encontro de rios próximo a Manaus.",
        "O encontro de cursos d'água ajuda a entender afluentes e rio principal. Observe como as águas se juntam na rede hidrográfica.",
    ),
    "hidrografia_foz": imagem_commons(
        "File:Amazon River mouth.jpg",
        "Área da foz do Rio Amazonas vista do espaço.",
        "A foz é o trecho onde o rio chega ao mar ou a outro corpo d'água. Mapas e imagens de satélite ajudam a visualizar esse conceito.",
    ),
    "hidrografia_cachoeira": imagem_commons(
        "File:Cataratas do Iguaçu - Foz do Iguaçu - Paraná.jpg",
        "Cataratas do Iguaçu, no Paraná.",
        "Cachoeiras mostram desnível no curso do rio. Observe a queda d'água e relacione-a ao relevo.",
    ),
    "hidrografia_lago": imagem_commons(
        "File:Lago Paranoá, Brasília.jpg",
        "Lago Paranoá em Brasília.",
        "Lagos e reservatórios acumulam água em áreas relativamente fechadas. Compare essa forma com rios, que têm fluxo contínuo.",
    ),
    "hidrografia_represa": imagem_commons(
        "File:Itaipu Dam aerial view.jpg",
        "Vista aérea da Usina de Itaipu e seu reservatório.",
        "Represas alteram o curso dos rios para armazenar água e produzir energia. Observe a presença da barragem e do lago artificial.",
    ),
    "hidrografia_aquifero": imagem_commons(
        "File:Aquifero guarani mapa.svg",
        "Mapa do Aquífero Guarani na América do Sul.",
        "Aquíferos são reservas subterrâneas. Quando o fenômeno não aparece em fotografia direta, o mapa é o recurso visual mais adequado.",
    ),
    "hidrografia_sao_francisco": imagem_commons(
        "File:Rio São Francisco - Petrolina e Juazeiro.jpg",
        "Rio São Francisco entre Petrolina e Juazeiro.",
        "O Rio São Francisco atravessa áreas semiáridas e sustenta abastecimento, irrigação, transporte e energia.",
    ),
    "cartografia_politico": imagem_commons(
        "File:Brazil states blank map.svg",
        "Mapa político do Brasil com limites estaduais.",
        "Mapas políticos destacam limites, estados, países e capitais. Eles selecionam informações administrativas do território.",
    ),
    "cartografia_fisico": imagem_commons(
        "File:Brazil physical map.svg",
        "Mapa físico do Brasil.",
        "Mapas físicos evidenciam relevo, rios e formas naturais. Observe que o objetivo é diferente do mapa político.",
    ),
    "cartografia_escala": imagem_commons(
        "File:Graphic scale example.svg",
        "Exemplo de escala gráfica em mapa.",
        "A escala liga a distância no mapa à distância real. Sem escala, o leitor não mede nem compara tamanhos corretamente.",
    ),
    "cartografia_legenda": imagem_commons(
        "File:Map legend symbols.svg",
        "Exemplo de legenda com símbolos cartográficos.",
        "A legenda traduz cores e símbolos do mapa. Ela transforma sinais visuais em informação geográfica.",
    ),
    "cartografia_rosa": imagem_commons(
        "File:Compass rose simple.svg",
        "Rosa dos ventos indicando direções cardeais.",
        "A orientação espacial depende de referências como norte, sul, leste e oeste. A rosa dos ventos organiza essas direções.",
    ),
    "cartografia_coordenadas": imagem_commons(
        "File:Latitude and Longitude of the Earth.svg",
        "Globo com linhas de latitude e longitude.",
        "Coordenadas geográficas usam linhas imaginárias para localizar pontos. Latitude e longitude funcionam juntas.",
    ),
    "populacao_crescimento": imagem_commons(
        "File:Brazil population.svg",
        "Gráfico da evolução da população brasileira.",
        "Gráficos de crescimento populacional mostram mudança ao longo do tempo. Observe a inclinação da curva.",
    ),
    "populacao_natalidade": imagem_commons(
        "File:Birth rate world map.svg",
        "Mapa mundial de taxa de natalidade.",
        "Taxas de natalidade ajudam a comparar países e regiões. Mapas temáticos mostram padrões espaciais.",
    ),
    "populacao_mortalidade": imagem_commons(
        "File:Death rate world map.svg",
        "Mapa mundial de taxa de mortalidade.",
        "A mortalidade varia conforme saúde, idade média, renda e conflitos. O mapa permite comparar situações.",
    ),
    "populacao_expectativa": imagem_commons(
        "File:Life expectancy world map.svg",
        "Mapa mundial de expectativa de vida.",
        "Expectativa de vida sintetiza condições de saúde e qualidade de vida. Observe as diferenças regionais.",
    ),
    "populacao_urbana": imagem_commons(
        "File:São Paulo city (Bela Vista).jpg",
        "Área urbana densa em São Paulo.",
        "A população urbana vive em cidades, com concentração de serviços, moradias, empregos e infraestrutura.",
    ),
    "populacao_rural": imagem_commons(
        "File:Rural area in Brazil.jpg",
        "Paisagem rural brasileira com baixa densidade de construções.",
        "A população rural se distribui de modo mais disperso. Observe o predomínio de áreas produtivas e menor concentração de edificações.",
    ),
    "urbanizacao_cidade_pequena": imagem_commons(
        "File:Tiradentes, Minas Gerais.jpg",
        "Vista urbana de uma cidade pequena em Minas Gerais.",
        "Cidades pequenas têm centralidades e serviços, mas costumam apresentar menor densidade e área construída que metrópoles.",
    ),
    "urbanizacao_verticalizacao": imagem_commons(
        "File:Skyline of São Paulo centre.jpg",
        "Centro de São Paulo com muitos edifícios altos.",
        "A verticalização aumenta a concentração de moradias e atividades em áreas valorizadas da cidade.",
        "Rodrigo.Argenton", "CC BY-SA 4.0",
    ),
    "urbanizacao_periferia": imagem_commons(
        "File:Favela da Rocinha.jpg",
        "Área periférica densamente ocupada.",
        "Periferias urbanas revelam desigualdades de moradia, infraestrutura e acesso a serviços.",
    ),
    "urbanizacao_mobilidade": imagem_commons(
        "File:Corredor de ônibus em Curitiba.jpg",
        "Corredor de ônibus em cidade brasileira.",
        "Mobilidade urbana envolve deslocamentos, transporte coletivo, tempo de viagem e acesso à cidade.",
    ),
    "urbanizacao_conurbacao": imagem_commons(
        "File:Satellite image of São Paulo Metropolitan Area.jpg",
        "Imagem de satélite da Região Metropolitana de São Paulo.",
        "A conurbação ocorre quando manchas urbanas se aproximam e se conectam. A imagem de satélite evidencia essa continuidade.",
    ),
    "urbanizacao_enchente": imagem_commons(
        "File:Enchente em São Paulo.jpg",
        "Rua urbana alagada após chuva intensa.",
        "Problemas urbanos aparecem quando drenagem, impermeabilização e ocupação de áreas de risco se combinam.",
    ),
    "geopolitica_mundo": imagem_commons(
        "File:Political World Map.svg",
        "Mapa político mundial.",
        "O mapa político mundial localiza Estados e fronteiras. Ele é ponto de partida, mas não substitui mapas específicos de cada tema.",
    ),
    "geopolitica_guerra_fria": imagem_commons(
        "File:Cold War alliances mid-1975.svg",
        "Mapa de alianças durante a Guerra Fria.",
        "A Guerra Fria organizou o mundo em áreas de influência. O mapa ajuda a visualizar alianças e rivalidades.",
    ),
    "geopolitica_otan": imagem_commons(
        "File:North Atlantic Treaty Organization (orthographic projection).svg",
        "Mapa dos países da OTAN.",
        "Mapas de organizações militares mostram alianças estratégicas, não apenas localização de países.",
    ),
    "geopolitica_ue": imagem_commons(
        "File:European Union (orthographic projection).svg",
        "Mapa dos países da União Europeia.",
        "A União Europeia aparece como bloco regional com integração política e econômica mais profunda que acordos comerciais simples.",
    ),
    "geopolitica_mercosul": imagem_commons(
        "File:Mercosur orthographic.svg",
        "Mapa dos países do Mercosul.",
        "O Mercosul ajuda a compreender integração regional na América do Sul e relações econômicas entre vizinhos.",
    ),
    "geopolitica_brics": imagem_commons(
        "File:BRICS.svg",
        "Mapa dos países do BRICS.",
        "O BRICS reúne economias emergentes e amplia debates sobre poder, desenvolvimento e governança global.",
    ),
    "geopolitica_onu": imagem_commons(
        "File:United Nations Members.svg",
        "Mapa dos Estados-membros da ONU.",
        "Organizações internacionais podem ser lidas por mapas de adesão, áreas de atuação e distribuição do poder decisório.",
    ),
    "geopolitica_multipolar": imagem_commons(
        "File:G20.svg",
        "Mapa dos países do G20.",
        "O mundo multipolar envolve vários centros de poder econômico e político. O mapa ajuda a identificar alguns desses atores.",
    ),
})

usar_catalogo_local()
FOTOS_SUBSTITUTAS = carregar_fotos_substitutas()
IMAGENS_SUPLEMENTARES = carregar_imagens_suplementares()
IMAGENS_AULAS_REAIS = carregar_imagens_aulas_reais()
URLS_COMMONS_RESOLVIDAS = carregar_urls_commons_resolvidas()

IMAGENS_TEMA = {
    "Clima": "clima_mapa",
    "Relevo": "relevo_chapada",
    "Vegetação": "vegetacao_cerrado",
    "Hidrografia": "rio_amazonas",
    "Cartografia": "clima_mapa",
    "Estrutura da Terra": "relevo_chapada",
    "Solos": "clima_semiarido",
    "Problemas ambientais": "clima_semiarido",
    "População": "populacao_piramide",
    "Migrações": "populacao_densidade",
    "Urbanização": "urbanizacao_sp",
    "Globalização": "urbanizacao_sp",
    "Industrialização": "urbanizacao_sp",
    "Agropecuária": "vegetacao_cerrado",
    "Fontes de energia": "hidrografia_amazonica",
    "Economia brasileira": "populacao_densidade",
    "Geopolítica": "geopolitica_mapa",
    "Conflitos mundiais": "geopolitica_mapa",
    "Blocos econômicos": "geopolitica_mapa",
    "Relações internacionais": "geopolitica_mapa",
    "Organizações internacionais": "geopolitica_mapa",
    "Globalização econômica": "urbanizacao_sp",
    "Questões ambientais globais": "vegetacao_pantanal",
    "Nova ordem mundial": "geopolitica_mapa",
}

PLANOS_VISUAIS_TEMA = {
    "Clima": [
        "clima_paisagem", "tempo_tempestade", "clima_semiarido",
        "clima_termometro", "clima_umidade_neblina", "clima_barometro",
        "clima_chuva_forte", "clima_vento_arvores", "clima_latitude_equador",
        "clima_altitude_serra", "clima_massas_ar", "clima_equatorial_amazonia",
        "clima_tropical_paisagem", "vegetacao_caatinga", "clima_subtropical_sul",
        "clima_mapa", "chuva_caatinga", "vegetacao_pantanal",
        "populacao_densidade", "hidrografia_lago", "urbanizacao_enchente",
    ],
    "Relevo": [
        "relevo_chapada", "relevo_montanha", "relevo_planicie",
        "relevo_depressao", "relevo_vale", "relevo_erosao",
        "relevo_intemperismo", "relevo_mapa_brasil", "clima_altitude_serra",
        "hidrografia_cachoeira", "urbanizacao_periferia", "clima_chuva_forte",
        "vegetacao_cerrado", "hidrografia_sao_francisco", "clima_paisagem",
        "vegetacao_caatinga", "urbanizacao_enchente", "hidrografia_amazonica",
    ],
    "Vegetação": [
        "vegetacao_amazonia", "vegetacao_cerrado", "vegetacao_caatinga",
        "vegetacao_mata_atlantica", "vegetacao_pantanal", "vegetacao_pampa",
        "clima_tropical_paisagem", "clima_equatorial_amazonia", "clima_semiarido",
        "chuva_caatinga", "hidrografia_lago", "clima_chuva_forte",
    ],
    "Hidrografia": [
        "hidrografia_nascente", "rio_amazonas", "hidrografia_afluente",
        "hidrografia_foz", "hidrografia_cachoeira", "hidrografia_lago",
        "hidrografia_represa", "hidrografia_aquifero", "hidrografia_amazonica",
        "hidrografia_sao_francisco", "clima_chuva_forte", "vegetacao_pantanal",
    ],
    "Cartografia": [
        "cartografia_politico", "cartografia_fisico", "clima_mapa",
        "populacao_densidade", "cartografia_escala", "cartografia_legenda",
        "cartografia_rosa", "cartografia_coordenadas", "hidrografia_amazonica",
        "relevo_mapa_brasil", "geopolitica_mundo", "clima_latitude_equador",
    ],
    "População": [
        "populacao_densidade", "populacao_crescimento", "populacao_piramide",
        "populacao_natalidade", "populacao_mortalidade", "populacao_expectativa",
        "populacao_urbana", "populacao_rural", "urbanizacao_sp",
        "urbanizacao_cidade_pequena", "cartografia_politico", "geopolitica_mundo",
        "populacao_densidade", "urbanizacao_conurbacao", "populacao_piramide",
        "hidrografia_lago", "vegetacao_caatinga", "urbanizacao_enchente",
    ],
    "Urbanização": [
        "urbanizacao_cidade_pequena", "urbanizacao_sp", "urbanizacao_verticalizacao",
        "urbanizacao_periferia", "urbanizacao_mobilidade", "urbanizacao_conurbacao",
        "urbanizacao_enchente", "populacao_densidade", "cartografia_politico",
        "hidrografia_lago", "vegetacao_pantanal", "clima_chuva_forte",
        "geopolitica_mundo", "populacao_urbana", "relevo_chapada",
        "clima_vento_arvores", "hidrografia_represa", "vegetacao_cerrado",
    ],
    "Geopolítica": [
        "geopolitica_mundo", "geopolitica_guerra_fria", "geopolitica_otan",
        "geopolitica_ue", "geopolitica_mercosul", "geopolitica_brics",
        "geopolitica_onu", "geopolitica_multipolar", "hidrografia_sao_francisco",
        "vegetacao_amazonia", "urbanizacao_conurbacao", "populacao_densidade",
        "clima_mapa", "cartografia_politico", "hidrografia_amazonica",
        "relevo_mapa_brasil", "urbanizacao_sp", "clima_paisagem",
        "geopolitica_mundo", "geopolitica_ue", "geopolitica_brics",
    ],
}

PLANOS_VISUAIS_TEMA.update({
    "Estrutura da Terra": ["relevo_montanha", "relevo_chapada", "relevo_intemperismo", "relevo_mapa_brasil", "relevo_erosao", "clima_altitude_serra", "hidrografia_cachoeira", "relevo_vale", "relevo_depressao", "clima_paisagem", "vegetacao_cerrado", "hidrografia_lago"],
    "Solos": ["relevo_intemperismo", "relevo_erosao", "vegetacao_cerrado", "clima_chuva_forte", "vegetacao_caatinga", "clima_semiarido", "clima_paisagem", "hidrografia_nascente", "relevo_planicie", "vegetacao_pantanal", "urbanizacao_enchente", "hidrografia_lago"],
    "Problemas ambientais": ["vegetacao_amazonia", "urbanizacao_enchente", "vegetacao_cerrado", "clima_chuva_forte", "hidrografia_lago", "urbanizacao_periferia", "clima_semiarido", "hidrografia_sao_francisco", "relevo_erosao", "urbanizacao_mobilidade", "vegetacao_pantanal", "clima_paisagem"],
    "Migrações": ["populacao_densidade", "geopolitica_mundo", "urbanizacao_sp", "populacao_rural", "populacao_urbana", "cartografia_politico", "urbanizacao_mobilidade", "urbanizacao_conurbacao", "geopolitica_onu", "geopolitica_guerra_fria", "clima_semiarido", "hidrografia_sao_francisco"],
    "Globalização": ["geopolitica_mundo", "urbanizacao_sp", "hidrografia_represa", "urbanizacao_mobilidade", "geopolitica_multipolar", "cartografia_politico", "populacao_urbana", "geopolitica_brics", "urbanizacao_conurbacao", "clima_mapa", "hidrografia_amazonica", "vegetacao_amazonia", "populacao_densidade", "geopolitica_ue", "urbanizacao_verticalizacao", "cartografia_coordenadas", "geopolitica_onu", "clima_paisagem"],
    "Industrialização": ["urbanizacao_sp", "urbanizacao_verticalizacao", "hidrografia_represa", "geopolitica_mundo", "urbanizacao_mobilidade", "populacao_urbana", "cartografia_politico", "clima_paisagem", "urbanizacao_periferia", "hidrografia_sao_francisco", "geopolitica_brics", "clima_chuva_forte"],
    "Agropecuária": ["clima_paisagem", "vegetacao_cerrado", "populacao_rural", "clima_chuva_forte", "hidrografia_lago", "relevo_planicie", "vegetacao_caatinga", "vegetacao_amazonia", "clima_tropical_paisagem", "populacao_densidade", "hidrografia_sao_francisco", "relevo_erosao"],
    "Fontes de energia": ["hidrografia_represa", "clima_vento_arvores", "clima_chuva_forte", "geopolitica_mundo", "hidrografia_sao_francisco", "clima_paisagem", "vegetacao_cerrado", "urbanizacao_sp", "hidrografia_lago", "geopolitica_brics", "clima_mapa", "urbanizacao_mobilidade"],
    "Economia brasileira": ["populacao_densidade", "clima_paisagem", "urbanizacao_sp", "vegetacao_caatinga", "hidrografia_sao_francisco", "geopolitica_mercosul", "cartografia_politico", "geopolitica_brics", "urbanizacao_verticalizacao", "hidrografia_amazonica", "vegetacao_amazonia", "geopolitica_mundo"],
    "Conflitos mundiais": ["geopolitica_mundo", "geopolitica_guerra_fria", "geopolitica_otan", "geopolitica_onu", "geopolitica_multipolar", "hidrografia_sao_francisco", "vegetacao_amazonia", "clima_semiarido", "cartografia_politico", "populacao_densidade", "urbanizacao_periferia", "geopolitica_brics"],
    "Blocos econômicos": ["geopolitica_mercosul", "geopolitica_ue", "geopolitica_brics", "geopolitica_mundo", "geopolitica_multipolar", "cartografia_politico", "urbanizacao_sp", "populacao_densidade", "hidrografia_sao_francisco", "clima_paisagem", "geopolitica_onu", "urbanizacao_mobilidade"],
    "Relações internacionais": ["geopolitica_mundo", "geopolitica_onu", "geopolitica_ue", "geopolitica_guerra_fria", "geopolitica_multipolar", "geopolitica_brics", "clima_mapa", "hidrografia_amazonica", "populacao_densidade", "urbanizacao_sp", "cartografia_politico", "vegetacao_amazonia"],
    "Organizações internacionais": ["geopolitica_onu", "geopolitica_ue", "geopolitica_otan", "geopolitica_mercosul", "geopolitica_brics", "geopolitica_multipolar", "geopolitica_mundo", "populacao_densidade", "clima_mapa", "hidrografia_amazonica", "cartografia_politico", "urbanizacao_sp"],
    "Globalização econômica": ["geopolitica_mundo", "geopolitica_brics", "urbanizacao_sp", "urbanizacao_mobilidade", "geopolitica_mercosul", "geopolitica_ue", "hidrografia_represa", "cartografia_politico", "populacao_densidade", "clima_paisagem", "urbanizacao_verticalizacao", "geopolitica_multipolar"],
    "Questões ambientais globais": ["clima_mapa", "vegetacao_amazonia", "clima_chuva_forte", "hidrografia_amazonica", "vegetacao_pantanal", "hidrografia_lago", "geopolitica_onu", "clima_paisagem", "vegetacao_caatinga", "geopolitica_mundo", "clima_semiarido", "urbanizacao_enchente"],
    "Nova ordem mundial": ["geopolitica_guerra_fria", "geopolitica_multipolar", "geopolitica_brics", "geopolitica_ue", "geopolitica_mundo", "geopolitica_otan", "urbanizacao_sp", "cartografia_coordenadas", "geopolitica_onu", "clima_mapa", "hidrografia_amazonica", "populacao_densidade"],
})

TEXTOS_TEMA = {
    "Clima": (
        "A atmosfera muda o tempo todo, mas algumas características se repetem em cada região. Ao estudar clima, observamos padrões de temperatura, chuva, ventos e umidade que influenciam moradia, agricultura, saúde e transporte.",
        "Esse estudo ajuda a interpretar previsões, estiagens, frentes frias, ondas de calor e diferenças entre regiões brasileiras. Não é apenas memorizar tipos climáticos: é perceber como a atmosfera afeta decisões cotidianas."
    ),
    "Relevo": (
        "O relevo organiza a superfície onde as sociedades vivem. Encostas, planaltos, planícies e vales influenciam rios, estradas, moradias, agricultura e riscos ambientais.",
        "Ao observar uma paisagem, procure perceber altura, inclinação e formas. Essas pistas mostram processos lentos, como erosão, e também processos internos, como movimentos tectônicos."
    ),
    "População": (
        "Estudar população significa observar onde as pessoas vivem, como se distribuem por idade e quais condições de vida possuem. Esses dados ajudam a planejar escolas, hospitais, transporte e moradia.",
        "Números populacionais não são apenas totais. Eles mostram desigualdades, envelhecimento, concentração urbana e mudanças sociais que aparecem no território."
    ),
    "Urbanização": (
        "A urbanização transforma o espaço porque concentra moradias, empregos, serviços e circulação. Quando cresce sem planejamento, pode ampliar desigualdades, trânsito, enchentes e falta de saneamento.",
        "Ler a cidade como espaço geográfico é observar ruas, rios canalizados, bairros, moradias, transporte e áreas verdes como partes conectadas."
    ),
    "Globalização": (
        "A globalização aproxima lugares por redes de transporte, comunicação, produção, consumo e finanças. Um produto pode reunir matéria-prima, tecnologia, trabalho e venda em países diferentes.",
        "Essas conexões criam oportunidades, mas também desigualdades. Alguns lugares controlam tecnologia e capital; outros ficam mais dependentes de exportar recursos ou mão de obra barata."
    ),
    "Geopolítica": (
        "A geopolítica analisa como Estados, empresas e organizações disputam poder no território. Fronteiras, recursos, rotas, energia e tecnologia podem influenciar decisões internacionais.",
        "Esse tema ajuda a ler notícias sobre conflitos, alianças, sanções, comércio, Amazônia, oceanos e segurança sem reduzir tudo a opiniões simples."
    ),
}


def texto_tema(tema, titulo, objetivo, exemplo):
    base = TEXTOS_TEMA.get(tema)
    if base:
        return base
    return (
        f"{titulo} ajuda a explicar como o espaço geográfico é produzido e transformado. O objetivo da aula é {objetivo.lower()}",
        f"Use o exemplo de {exemplo} para ligar o conceito à realidade. Em Geografia, um bom estudo sempre pergunta onde acontece, por que acontece e quem é afetado."
    )


def imagem_real(chave):
    imagem = IMAGENS_REAIS[chave].copy()
    imagem["arquivo"] = URLS_COMMONS_RESOLVIDAS.get(imagem["arquivo"], imagem["arquivo"])
    imagem.setdefault("externa", imagem["arquivo"].startswith("http"))
    return imagem


def aplicar_imagem(secao, chave):
    imagem = imagem_real(chave)
    secao.update({
        "imagem": imagem["arquivo"],
        "imagem_externa": imagem["externa"],
        "imagem_alt": imagem["alt"],
        "imagem_fonte": imagem["fonte"],
        "imagem_observacao": imagem["observacao"],
        "imagem_zoom": imagem["zoom"],
    })
    return secao


def aplicar_imagem_direta(campo, imagem):
    campo["imagem"] = URLS_COMMONS_RESOLVIDAS.get(imagem["arquivo"], imagem["arquivo"])
    campo["imagem_externa"] = imagem.get("externa", imagem["arquivo"].startswith("http"))
    campo["imagem_alt"] = imagem["alt"]
    campo["imagem_fonte"] = imagem["fonte"]
    campo["imagem_observacao"] = imagem["observacao"]
    campo["imagem_zoom"] = imagem["zoom"]
    return campo


def chaves_visuais_da_aula(tema, numero):
    plano = PLANOS_VISUAIS_TEMA.get(tema)
    if not plano:
        plano = [
            "cartografia_politico", "clima_paisagem", "geopolitica_mundo",
            "populacao_densidade", "urbanizacao_sp", "hidrografia_lago",
            "vegetacao_cerrado", "relevo_chapada", "clima_chuva_forte",
        ]
    inicio = (numero - 1) * 3
    chaves = []
    for deslocamento in range(3):
        chaves.append(plano[(inicio + deslocamento) % len(plano)])
    return chaves


def limpar_imagem_artificial(campo):
    campo["imagem"] = None
    campo["imagem_externa"] = False
    campo["imagem_alt"] = ""
    campo["imagem_fonte"] = ""
    campo["imagem_observacao"] = ""
    campo["imagem_zoom"] = False


def aplicar_foto_substituta_no_campo(campo, indice):
    chave = f"{indice + 1:03d}"
    imagem = FOTOS_SUBSTITUTAS.get(chave)
    if not imagem:
        limpar_imagem_artificial(campo)
        return
    campo["imagem"] = imagem["arquivo"]
    campo["imagem_externa"] = False
    campo["imagem_alt"] = imagem["alt"]
    campo["imagem_fonte"] = imagem["fonte"]
    campo["imagem_observacao"] = imagem["observacao"]
    campo["imagem_zoom"] = imagem["zoom"]


def deduplicar_imagens_aulas(temas):
    vistos = set()
    indice = 0
    for tema in temas.values():
        for aula in tema["aulas"]:
            campos = [(aula, "Imagem de abertura")]
            campos.extend((secao, secao["titulo"]) for secao in aula.get("secoes", []))
            for campo, secao in campos:
                caminho = campo["imagem"]
                if caminho in vistos:
                    aplicar_foto_substituta_no_campo(campo, indice)
                    indice += 1
                    caminho = campo["imagem"]
                if caminho:
                    vistos.add(caminho)
            interativa = aula.get("imagem_interativa")
            if interativa:
                caminho = interativa["arquivo"]
                if caminho in vistos:
                    aula["imagem_interativa"] = None
                else:
                    vistos.add(caminho)
    return temas


def pergunta_da_aula(titulo):
    if "Tempo e clima" in titulo:
        return {
            "texto": "Se hoje está fazendo 16°C e chovendo, estamos falando de tempo ou clima?",
            "opcoes": alternativas_com_correta([
                "Tempo",
                "Clima",
                "Relevo",
                "Vegetação",
            ], 0, f"rapida|{titulo}"),
            "explicacao": "Tempo está correto. A frase descreve uma condição atmosférica de um momento específico.",
        }
    if "Elementos do clima" in titulo:
        return {
            "texto": "Na informação 'Salvador: 29°C, umidade 78% e chuva prevista', quais elementos do clima aparecem?",
            "opcoes": alternativas_com_correta([
                "Temperatura, umidade e precipitação",
                "Altitude, relevo e população",
                "Solo, fronteira e indústria",
                "Fronteira, moeda e comércio",
            ], 0, f"rapida|{titulo}"),
            "explicacao": "A temperatura aparece em 29°C, a umidade em 78% e a precipitação na chuva prevista.",
        }
    return {
        "texto": f"Qual atitude ajuda a compreender melhor '{titulo}'?",
        "opcoes": alternativas_com_correta([
            "Relacionar conceito, exemplo e localização",
            "Memorizar palavras sem observar mapas",
            "Ignorar causas e consequências",
            "Copiar nomes sem comparar lugares",
        ], 0, f"rapida|{titulo}"),
        "explicacao": "A resposta correta combina conceito, exemplo e localização. Assim o conteúdo deixa de ser uma lista solta.",
    }


def comparacao_da_aula(tema, titulo):
    if "Tempo e clima" in titulo:
        return {
            "titulo": "Tempo x Clima",
            "itens": [
                {"titulo": "Tempo", "icone": "T", "pontos": ["curto período", "muda rapidamente", "exemplo: hoje está chovendo"]},
                {"titulo": "Clima", "icone": "C", "pontos": ["observado por muitos anos", "mostra padrões", "exemplo: Sertão semiárido"]},
            ],
        }
    if tema == "Relevo":
        return {
            "titulo": "Compare as formas",
            "itens": [
                {"titulo": "Planalto", "icone": "▰", "pontos": ["área elevada", "erosão costuma predominar", "pode ter chapadas e serras"]},
                {"titulo": "Planície", "icone": "▱", "pontos": ["área mais baixa", "sedimentos se acumulam", "comum perto de rios e litorais"]},
            ],
        }
    if tema == "População":
        return {
            "titulo": "Populoso x Povoado",
            "itens": [
                {"titulo": "Populoso", "icone": "●●●", "pontos": ["muitos habitantes no total", "olha a população absoluta", "Brasil é um país populoso"]},
                {"titulo": "Povoado", "icone": "● ● ●", "pontos": ["muitos habitantes por área", "olha a densidade demográfica", "áreas urbanas são mais povoadas"]},
            ],
        }
    return {
        "titulo": "Observe a diferença",
        "itens": [
            {"titulo": "Conceito", "icone": "1", "pontos": ["ideia principal", "ajuda a organizar a explicação", "aparece no título da aula"]},
            {"titulo": "Exemplo", "icone": "2", "pontos": ["situação real", "mostra o conceito no espaço", "facilita a interpretação"]},
        ],
    }


def imagem_interativa_da_aula(tema, numero):
    if tema == "Relevo" and numero == 1:
        return {
            "titulo": "Identifique na paisagem",
            **imagem_real("relevo_chapada"),
            "pontos": [
                {"numero": "1", "top": "32%", "left": "48%", "texto": "Área elevada: a diferença de altitude é uma pista para reconhecer serras e chapadas."},
                {"numero": "2", "top": "58%", "left": "35%", "texto": "Encosta: parte inclinada, importante para discutir erosão, ocupação e risco."},
                {"numero": "3", "top": "70%", "left": "62%", "texto": "Área mais baixa: ajuda a comparar formas do relevo dentro da mesma paisagem."},
            ],
        }
    if tema == "Hidrografia" and numero == 2:
        return {
            "titulo": "Leia o mapa hidrográfico",
            **imagem_real("hidrografia_amazonica"),
            "pontos": [
                {"numero": "1", "top": "36%", "left": "46%", "texto": "Região hidrográfica: área drenada por rios que se conectam em uma grande rede."},
                {"numero": "2", "top": "50%", "left": "58%", "texto": "Bacia Amazônica: sua extensão ajuda a entender a importância dos rios no território brasileiro."},
                {"numero": "3", "top": "62%", "left": "39%", "texto": "Limites de bacia não seguem necessariamente fronteiras políticas; seguem divisores de águas."},
            ],
        }
    if tema == "Clima" and numero == 5:
        return {
            "titulo": "Leia o mapa climático",
            **imagem_real("clima_mapa"),
            "pontos": [
                {"numero": "1", "top": "28%", "left": "43%", "texto": "A Amazônia aparece associada a climas quentes e úmidos, influenciados por baixa latitude e muita umidade."},
                {"numero": "2", "top": "53%", "left": "60%", "texto": "O interior do Nordeste ajuda a discutir semiárido, irregularidade das chuvas e adaptação da vegetação."},
                {"numero": "3", "top": "78%", "left": "58%", "texto": "O Sul do Brasil permite comparar áreas com inverno mais frio e maior influência de massas de ar polar."},
            ],
        }
    return None


def montar_aula(tema, numero, titulo, objetivo, exemplo):
    imagem_chave, secao_1_chave, secao_2_chave = chaves_visuais_da_aula(tema, numero)
    imagem = imagem_real(imagem_chave)
    intro_1, intro_2 = texto_tema(tema, titulo, objetivo, exemplo)
    layout = "invertida" if numero % 2 == 0 else "normal"
    return {
        "numero": numero,
        "titulo": titulo,
        "pergunta_abertura": f"Como {titulo.lower()} aparece nas paisagens e no cotidiano?",
        "objetivo": objetivo,
        "imagem": imagem["arquivo"],
        "imagem_externa": imagem["externa"],
        "imagem_alt": imagem["alt"],
        "imagem_fonte": imagem["fonte"],
        "imagem_observacao": imagem["observacao"],
        "imagem_zoom": imagem["zoom"],
        "introducao": [
            intro_1,
            intro_2,
        ],
        "secoes": [
            aplicar_imagem({
                "titulo": "Comece observando",
                "textos": [
                    f"Antes de decorar definições, observe o fenômeno em uma paisagem, mapa, gráfico ou notícia. Em {titulo.lower()}, a localização muda a interpretação.",
                    f"No exemplo de {exemplo}, o conceito ganha forma concreta: há uma situação, um lugar e consequências para pessoas ou ambientes.",
                ],
                "layout": layout,
            }, secao_1_chave),
            aplicar_imagem({
                "titulo": "Por que isso importa?",
                "textos": [
                    f"{objetivo} Esse objetivo ajuda a construir explicações, não apenas respostas curtas.",
                    "Quando você relaciona causas e consequências, consegue comparar lugares e entender por que o mesmo fenômeno não aparece da mesma forma em todas as regiões.",
                ],
                "layout": "invertida" if layout == "normal" else "normal",
            }, secao_2_chave),
        ],
        "comparacao": comparacao_da_aula(tema, titulo),
        "destaques": [
            {"tipo": "Observe", "texto": "Procure pistas visuais: forma da paisagem, direção dos fluxos, concentração de pessoas, cores da legenda ou dados numéricos."},
            {"tipo": "Exemplo", "texto": f"{exemplo.capitalize()} mostra que o conteúdo pode ser percebido em situações reais, não apenas no livro."},
        ],
        "pergunta_rapida": pergunta_da_aula(titulo),
        "revelar": {
            "titulo": "Quer entender melhor?",
            "botao": "Mostrar explicação",
            "texto": "Uma boa resposta em Geografia geralmente junta três partes: conceito, localização e consequência. Essa estrutura ajuda a organizar o pensamento e evita respostas vagas.",
        },
        "imagem_interativa": imagem_interativa_da_aula(tema, numero),
        "curiosidade": f"{exemplo.capitalize()} pode aparecer em mapas, imagens de satélite, reportagens e dados públicos. Comparar fontes diferentes melhora a interpretação.",
        "resumo": [
            f"{titulo} deve ser entendido com conceito, exemplo e localização.",
            "Mapas, imagens e dados ajudam a enxergar relações que o texto sozinho não mostra.",
            "Causas e consequências variam conforme a região, a escala e as ações humanas.",
            f"O exemplo de {exemplo} ajuda a transformar a explicação em uma situação concreta.",
        ],
        "atividade": "Escolha uma imagem, mapa ou notícia relacionada à aula. Anote o lugar, o fenômeno observado e uma consequência para a sociedade ou para a natureza.",
    }


def reduzir_blocos_repetidos(temas):
    for tema in temas.values():
        for aula in tema["aulas"]:
            primeira_aula = aula["numero"] == 1
            revelar_especifico = bool(
                aula.get("revelar")
                and not aula["revelar"]["texto"].startswith("Uma boa resposta em Geografia")
            )
            if not primeira_aula:
                if aula.get("revelar") and aula["revelar"]["texto"].startswith("Uma boa resposta em Geografia"):
                    aula["revelar"] = None
                if aula.get("comparacao") and aula["comparacao"]["titulo"] in {
                    "Observe a diferença",
                    "Compare as formas",
                    "Populoso x Povoado",
                }:
                    aula["comparacao"] = None
                if aula.get("atividade") == "Escolha uma imagem, mapa ou notícia relacionada à aula. Anote o lugar, o fenômeno observado e uma consequência para a sociedade ou para a natureza.":
                    aula["atividade"] = None
                aula["destaques"] = [
                    destaque
                    for destaque in aula.get("destaques", [])
                    if destaque["tipo"] != "Observe"
                ]
                aula["resumo"] = [
                    item for item in aula["resumo"]
                    if item not in {
                        "Mapas, imagens e dados ajudam a enxergar relações que o texto sozinho não mostra.",
                        "Causas e consequências variam conforme a região, a escala e as ações humanas.",
                    }
                ]
                if not revelar_especifico:
                    aula["curiosidade"] = None
            if not primeira_aula and tema["titulo"] in TEXTOS_TEMA and not revelar_especifico:
                aula["introducao"] = texto_tema(
                    "",
                    aula["titulo"],
                    aula["objetivo"],
                    aula["resumo"][-1].replace("O exemplo de ", "").replace(" ajuda a transformar a explicação em uma situação concreta.", ""),
                )
    return temas


VISUAIS_REVISAO_2_3 = {
    ("População", 6): imagem_commons(
        "File:Complexo alemao rj.jpg",
        "Área urbana densamente ocupada, usada para discutir indicadores sociais e desigualdades de moradia.",
        "A fotografia ajuda a relacionar indicadores sociais com saneamento, renda, infraestrutura e condições de vida.",
    ),
    ("Migrações", 1): imagem_commons(
        "File:Terminal Rodoviário de Coronel Fabriciano MG.JPG",
        "Terminal rodoviário com circulação de passageiros, usado para exemplificar deslocamentos populacionais.",
        "Terminais de transporte ajudam a observar migrações temporárias, viagens interestaduais e mudanças de residência.",
    ),
    ("Migrações", 2): imagem_commons(
        "File:Trabalhadores em Obras de Fundação da Construção da Via Férrea - 484, Acervo do Museu Paulista da USP.jpg",
        "Trabalhadores em canteiro urbano, usados para relacionar migração e busca por emprego.",
        "O trabalho é uma causa frequente de deslocamentos populacionais entre regiões, cidades e países.",
    ),
    ("Migrações", 3): imagem_commons(
        "File:Luz Train Station, Sao Paulo.jpg",
        "Trem metropolitano em estação urbana, usado para representar deslocamentos pendulares no Brasil.",
        "A circulação diária entre casa, estudo e trabalho é um exemplo importante de migração pendular.",
    ),
    ("Migrações", 4): imagem_commons(
        "File:Refugees Budapest Keleti railway station 2015-09-04.jpg",
        "Pessoas refugiadas em deslocamento, usadas para contextualizar migração forçada e direitos humanos.",
        "A imagem deve ser lida com finalidade educativa: conflitos e perseguições podem forçar deslocamentos e exigir acolhimento.",
    ),
    ("Urbanização", 2): imagem_commons(
        "File:Vista aérea centro de Campinas 01.jpg",
        "Vista aérea de Campinas, usada para discutir rede urbana e centros regionais.",
        "Cidades médias e metrópoles exercem influência sobre serviços, empregos, comércio e deslocamentos regionais.",
    ),
    ("Urbanização", 3): imagem_commons(
        "File:São Paulo metropolitan area at night.jpg",
        "Mancha urbana da Região Metropolitana de São Paulo vista do espaço, usada para exemplificar metropolização.",
        "A continuidade da mancha urbana ajuda a compreender conurbação, fluxos diários e integração metropolitana.",
    ),
    ("Urbanização", 4): imagem_commons(
        "File:Strong and large summer thunderstorm in Sao Paulo, Brazil.jpg",
        "Rua urbana alagada após chuva, usada para discutir problemas urbanos e drenagem.",
        "Enchentes urbanas mostram a relação entre impermeabilização do solo, ocupação de várzeas e infraestrutura insuficiente.",
    ),
    ("Urbanização", 5): imagem_commons(
        "File:Bus Rapid Transit System (BRT) Curitiba (Brasil).jpg",
        "Corredor de ônibus em Curitiba, usado para representar planejamento urbano e mobilidade.",
        "A mobilidade planejada reduz tempo de deslocamento e amplia o acesso da população aos serviços urbanos.",
    ),
    ("Urbanização", 6): imagem_commons(
        "File:Eduardo Paes inaugura trecho de expansão do Parque Madureira (31845777645).jpg",
        "Parque urbano no Rio de Janeiro, usado para exemplificar soluções de cidade sustentável.",
        "Áreas verdes, transporte coletivo e espaços públicos ajudam a reduzir desigualdades e impactos ambientais urbanos.",
    ),
    ("Globalização", 1): imagem_commons(
        "File:Container port (1).jpg",
        "Terminal de contêineres no Porto de Santos, usado para apresentar conexões da globalização.",
        "Portos conectam produção, consumo e comércio internacional, tornando visíveis as redes da globalização.",
    ),
    ("Globalização", 2): imagem_commons(
        "File:FRA aerial 3.jpg",
        "Aeroporto internacional visto do alto, usado para exemplificar fluxos globais de pessoas e mercadorias.",
        "Aeroportos, portos e redes digitais articulam fluxos globais em diferentes escalas.",
    ),
    ("Globalização", 3): imagem_commons(
        "File:Electronics factory in Shenzhen.jpg",
        "Trabalhadores em linha de montagem, usados para discutir empresas transnacionais e cadeias produtivas.",
        "A produção em rede distribui etapas industriais por diferentes países e regiões.",
    ),
    ("Globalização", 4): imagem_commons(
        "File:Shibuya crossing, Tokyo, Japan.jpg",
        "Cruzamento urbano movimentado em Tóquio, usado para discutir circulação cultural e consumo global.",
        "Marcas, hábitos de consumo e referências culturais circulam entre cidades conectadas por redes globais.",
    ),
    ("Globalização", 5): imagem_commons(
        "File:Brazil-00012 - Open Pit Mine? (48954145937).jpg",
        "Mina a céu aberto, usada para discutir desigualdades na exportação de matérias-primas.",
        "A globalização pode reforçar dependências quando países exportam recursos naturais e importam tecnologia.",
    ),
    ("Globalização", 6): imagem_commons(
        "File:Landing of the submarine cable, Port Darwin, 7 November 1871(GN01968).jpg",
        "Fotografia histórica da instalação de um cabo submarino, usada para explicar redes digitais globais.",
        "Quando a infraestrutura não é visível na paisagem cotidiana, um esquema técnico ajuda a compreender a conexão física da internet.",
    ),
    ("Geopolítica", 1): imagem_commons(
        "File:Argentina-Brazil border.jpg",
        "Área de fronteira internacional, usada para relacionar território, Estado e soberania.",
        "Fronteiras materializam controle territorial, circulação, fiscalização e relações entre Estados.",
    ),
    ("Geopolítica", 2): imagem_commons(
        "File:National Congress of Brazil.jpg",
        "Congresso Nacional do Brasil, usado para diferenciar Estado, governo e instituições políticas.",
        "Instituições políticas ajudam a compreender como o poder do Estado é organizado e representado.",
    ),
    ("Geopolítica", 3): imagem_commons(
        "File:Oil platform P-51 (Brazil).jpg",
        "Plataforma de petróleo no Brasil, usada para exemplificar recursos estratégicos.",
        "Petróleo, água, minérios e tecnologia podem ampliar a influência econômica e política de um território.",
    ),
    ("Geopolítica", 4): imagem_commons(
        "File:Checkpoint charlie 1961.jpg",
        "Posto de controle em Berlim durante a Guerra Fria, usado para discutir fronteiras e disputas territoriais.",
        "Fronteiras contestadas podem concentrar tensões militares, políticas e simbólicas.",
    ),
    ("Geopolítica", 5): imagem_commons(
        "File:Xi Jinping and Barack Obama toast at White House state dinner September 2015.jpg",
        "Encontro diplomático entre líderes dos Estados Unidos e da China, usado para discutir potências mundiais.",
        "Potências projetam influência por economia, tecnologia, diplomacia, cultura e poder militar.",
    ),
    ("Geopolítica", 6): imagem_commons(
        "File:Amazon river.JPG",
        "Vista do Rio Amazonas na região de Manaus, usada para discutir a importância estratégica da Amazônia para o Brasil.",
        "A Amazônia envolve biodiversidade, água, fronteiras, recursos e debates internacionais sobre soberania.",
    ),
    ("Geopolítica", 7): imagem_commons(
        "File:Datacenter.jpg",
        "Sala de data center com servidores, usada para relacionar tecnologia, dados e poder geopolítico.",
        "Na geopolítica contemporânea, infraestrutura digital, satélites e dados também são recursos estratégicos.",
    ),
    ("Conflitos mundiais", 1): imagem_commons(
        "File:Sheikh Hasina UN Peacekeepers Day Video Conference Dhaka 2022-05-29 (PID-0022951).jpg",
        "Missão de paz da ONU em área de tensão, usada para discutir causas e gestão de conflitos.",
        "Conflitos podem envolver território, recursos, identidades, interesses políticos e intervenção internacional.",
    ),
    ("Conflitos mundiais", 2): imagem_commons(
        "File:Syrian refugees in lebanon.jpg",
        "Pessoas refugiadas em acampamento, usadas para discutir impactos das guerras sobre a população civil.",
        "A imagem destaca consequências humanitárias dos conflitos, como deslocamento, perda de moradia e necessidade de proteção.",
    ),
    ("Conflitos mundiais", 3): imagem_commons(
        "File:TSA Security Checkpoint at Airport.jpg",
        "Controle de segurança em aeroporto, usado para relacionar terrorismo e políticas de segurança.",
        "Respostas ao terrorismo alteram fronteiras, transportes, vigilância e circulação de pessoas.",
    ),
    ("Conflitos mundiais", 4): imagem_commons(
        "File:United Nations Security Council.jpg",
        "Reunião do Conselho de Segurança da ONU, usada para discutir diplomacia e paz.",
        "Negociações, sanções e missões de paz são formas de tentar reduzir ou mediar conflitos internacionais.",
    ),
    ("Blocos econômicos", 1): imagem_commons(
        "File:Puente Internacional Tancredo Neves.JPG",
        "Ponte internacional entre Brasil e Argentina, usada para discutir integração regional.",
        "A infraestrutura de fronteira facilita comércio, circulação e cooperação entre países vizinhos.",
    ),
    ("Blocos econômicos", 2): imagem_commons(
        "File:Container Terminal in Hamburg .jpg",
        "Terminal de contêineres em porto europeu, usado para explicar comércio em blocos econômicos.",
        "A circulação de mercadorias mostra como acordos econômicos podem reduzir barreiras e ampliar trocas.",
    ),
    ("Blocos econômicos", 3): imagem_commons(
        "File:XXX Cumbre del Mercosur - Córdoba - 21JUL06 -2- presidenciagovar..jpg",
        "Reunião de representantes do Mercosul, usada para contextualizar o bloco sul-americano.",
        "Blocos regionais também dependem de negociações políticas, além das trocas comerciais.",
    ),
    ("Blocos econômicos", 4): imagem_commons(
        "File:European Parliament Strasbourg Hemicycle - Diliff.jpg",
        "Plenário do Parlamento Europeu, usado para discutir a integração política da União Europeia.",
        "A União Europeia combina mercado comum, instituições políticas e cooperação entre países membros.",
    ),
    ("Relações internacionais", 1): imagem_commons(
        "File:Traktat Reformujacy UE.jpg",
        "Reunião diplomática entre representantes de países, usada para apresentar negociação internacional.",
        "A diplomacia organiza conversas oficiais, tratados e acordos entre Estados.",
    ),
    ("Relações internacionais", 2): imagem_commons(
        "File:UNFCCC COP21 CMP11 Leaders Event (23129423350).jpg",
        "Encontro internacional sobre clima, usado para discutir cooperação entre países.",
        "A cooperação internacional aparece em acordos ambientais, ciência, saúde, comércio e ajuda humanitária.",
    ),
    ("Relações internacionais", 3): imagem_commons(
        "File:Deputy Secretary Blinken Addresses Reporters After Delivering Remarks at the 31st Session of the UN Human Rights Council in Geneva (25176985130).jpg",
        "Sessão do Conselho de Direitos Humanos da ONU, usada para explicar proteção internacional de direitos.",
        "Direitos humanos são debatidos em instituições multilaterais e orientam normas de proteção às pessoas.",
    ),
    ("Relações internacionais", 4): imagem_commons(
        "File:WHO Plenary.jpg",
        "Assembleia internacional de saúde, usada para discutir desafios globais que ultrapassam fronteiras.",
        "Problemas globais, como pandemias e mudanças climáticas, exigem coordenação entre vários países.",
    ),
}


VISUAIS_REVISAO_2_3_SUBSTITUIR = {
    ("Migrações", 3),
    ("Migrações", 4),
    ("Globalização", 2),
    ("Globalização", 3),
    ("Globalização", 5),
    ("Geopolítica", 1),
}


REVELAR_REVISAO_2_3 = {
    "População": "Para responder bem em população, separe população absoluta, densidade demográfica e distribuição. Esses conceitos explicam situações diferentes e evitam confundir país populoso com área muito povoada.",
    "Migrações": "Em migrações, observe sempre origem, destino, duração e motivo do deslocamento. Essas pistas ajudam a diferenciar migração interna, externa, temporária, pendular e forçada.",
    "Urbanização": "Urbanização não é apenas crescimento de prédios. Ela envolve aumento da população urbana, expansão da mancha construída, oferta de serviços e desigualdades no acesso à cidade.",
    "Globalização": "Globalização deve ser lida como rede: mercadorias, capitais, informações, pessoas e culturas circulam com intensidades diferentes entre os lugares.",
    "Geopolítica": "Na geopolítica, território é poder. Fronteiras, recursos, rotas, tecnologia e alianças ajudam a explicar decisões dos Estados e disputas internacionais.",
    "Conflitos mundiais": "Conflitos precisam ser analisados por causas e consequências. Território, recursos, identidade, política e população civil aparecem juntos em muitos casos.",
    "Blocos econômicos": "Blocos econômicos variam conforme o nível de integração. Zona de livre comércio, união aduaneira e mercado comum não representam o mesmo grau de cooperação.",
    "Relações internacionais": "Relações internacionais envolvem negociação, cooperação e disputa. Estados, organizações e acordos procuram lidar com problemas que muitas vezes ultrapassam fronteiras.",
}


ATIVIDADES_REVISAO_2_3 = {
    "População": "Analise um mapa, gráfico ou fotografia urbana e explique que informação ele mostra sobre distribuição, idade, densidade ou condições de vida da população.",
    "Migrações": "Escolha um exemplo de deslocamento populacional e identifique origem, destino, motivo da migração e uma consequência para quem migra ou para o lugar de chegada.",
    "Urbanização": "Observe uma paisagem urbana e descreva um elemento de crescimento da cidade, um problema urbano e uma possível ação de planejamento.",
    "Globalização": "Escolha um produto, porto, aeroporto ou rede digital e explique como ele conecta lugares diferentes por produção, transporte, consumo ou informação.",
    "Geopolítica": "Analise uma notícia internacional e identifique território envolvido, atores principais, interesse em disputa e possível consequência geográfica.",
    "Conflitos mundiais": "Pesquise um conflito atual ou histórico e explique sua localização, uma causa, um impacto sobre civis e uma tentativa de negociação ou mediação.",
    "Blocos econômicos": "Compare dois blocos econômicos e indique países participantes, tipo de integração e um exemplo de troca comercial ou cooperação.",
    "Relações internacionais": "Escolha um acordo, conferência ou organização internacional e explique quais países ou instituições participam e qual problema tentam enfrentar.",
}


TEMAS_REVISAO_2_3 = {
    "População",
    "Migrações",
    "Urbanização",
    "Globalização",
    "Geopolítica",
    "Conflitos mundiais",
    "Blocos econômicos",
    "Relações internacionais",
}


def revisar_anos_2_3(temas):
    for tema in temas.values():
        if tema["titulo"] not in TEMAS_REVISAO_2_3:
            continue
        for aula in tema["aulas"]:
            chave = (tema["titulo"], aula["numero"])
            imagem = VISUAIS_REVISAO_2_3.get(chave)
            if imagem and (not aula.get("imagem") or chave in VISUAIS_REVISAO_2_3_SUBSTITUIR):
                aplicar_imagem_direta(aula, imagem)
            if chave in VISUAIS_REVISAO_2_3_SUBSTITUIR:
                for secao in aula.get("secoes", []):
                    limpar_imagem_artificial(secao)
            if aula["numero"] == 1 and aula.get("revelar") and aula["revelar"]["texto"].startswith("Uma boa resposta em Geografia"):
                aula["revelar"]["texto"] = REVELAR_REVISAO_2_3[tema["titulo"]]
            if aula["numero"] == 1 and aula.get("atividade") == "Escolha uma imagem, mapa ou notícia relacionada à aula. Anote o lugar, o fenômeno observado e uma consequência para a sociedade ou para a natureza.":
                aula["atividade"] = ATIVIDADES_REVISAO_2_3[tema["titulo"]]
            if aula.get("comparacao") and aula["comparacao"]["titulo"] == "Observe a diferença":
                aula["comparacao"] = None
            if aula["numero"] != 1 and aula.get("revelar") and aula["revelar"]["texto"].startswith("Uma boa resposta em Geografia"):
                aula["revelar"] = None
            if aula["numero"] != 1 and aula.get("atividade") == "Escolha uma imagem, mapa ou notícia relacionada à aula. Anote o lugar, o fenômeno observado e uma consequência para a sociedade ou para a natureza.":
                aula["atividade"] = None
    return temas


def imagem_suplementar(tema, aula, posicao, arquivo):
    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(arquivo)}"
    contexto = "abertura" if posicao == "Imagem de abertura" else posicao.lower()
    return {
        "arquivo": url,
        "externa": True,
        "alt": f"Registro visual relacionado a {aula.lower()}, usado para apoiar {contexto} na aula de {tema}.",
        "fonte": f"Wikimedia Commons; arquivo File:{arquivo}.",
        "observacao": f"Relacione os elementos visuais do registro ao conteúdo estudado em {aula}.",
        "zoom": True,
    }


def preencher_imagens_minimas(temas, minimo=2):
    usados = set()
    for tema in temas.values():
        for aula in tema["aulas"]:
            campos = [(aula, "Imagem de abertura")]
            campos.extend((secao, secao["titulo"]) for secao in aula.get("secoes", []))
            for campo, _ in campos:
                if campo.get("imagem"):
                    usados.add(campo["imagem"])
            if aula.get("imagem_interativa"):
                usados.add(aula["imagem_interativa"]["arquivo"])

    cursores = {}
    for tema in temas.values():
        for aula in tema["aulas"]:
            campos = [(aula, "Imagem de abertura")]
            campos.extend((secao, secao["titulo"]) for secao in aula.get("secoes", []))
            quantidade = sum(1 for campo, _ in campos if campo.get("imagem"))
            if aula.get("imagem_interativa"):
                quantidade += 1
            for campo, posicao in campos:
                if quantidade >= minimo:
                    break
                if campo.get("imagem"):
                    continue
                pools = (
                    (tema["titulo"], IMAGENS_SUPLEMENTARES.get(tema["titulo"], [])),
                    ("Geral", IMAGENS_SUPLEMENTARES.get("Geral", [])),
                )
                for chave_pool, pool in pools:
                    chave_cursor = (tema["titulo"], chave_pool)
                    while cursores.get(chave_cursor, 0) < len(pool):
                        indice = cursores.get(chave_cursor, 0)
                        cursores[chave_cursor] = indice + 1
                        arquivo = pool[indice]
                        imagem = imagem_suplementar(tema["titulo"], aula["titulo"], posicao, arquivo)
                        if imagem["arquivo"] in usados:
                            continue
                        aplicar_imagem_direta(campo, imagem)
                        usados.add(imagem["arquivo"])
                        quantidade += 1
                        break
                    if campo.get("imagem"):
                        break
    return temas


TEMAS_ALVO_IMAGENS_LOCAIS = {
    "Relevo",
    "Clima",
    "Vegetação",
    "Hidrografia",
    "População",
    "Migrações",
    "Urbanização",
    "Globalização",
    "Geopolítica",
    "Conflitos mundiais",
    "Blocos econômicos",
    "Relações internacionais",
}


VISUAIS_LOCAIS_AULAS = {
    ("Relevo", 1): [
        ("relevo_formas_planalto_planicie_01.svg", "paisagem", "Paisagem comparando planalto, planície, montanha e depressão em diferentes altitudes.", "Compare a altura, a inclinação e a posição das formas para diferenciar planaltos, planícies, montanhas e depressões."),
        ("relevo_formas_perfil_topografico_01.svg", "perfil", "Perfil topográfico com variação de altitude entre montanha, planalto, vale e planície.", "O perfil transforma a paisagem em corte lateral, facilitando a leitura de altitude e declividade."),
    ],
    ("Relevo", 2): [
        ("relevo_agentes_internos_placas_01.svg", "placas", "Esquema de placas tectônicas convergentes formando dobramentos e áreas montanhosas.", "Movimentos internos da Terra ajudam a explicar cadeias de montanhas, vulcões e terremotos."),
        ("relevo_agentes_internos_vulcanismo_01.svg", "vulcao", "Corte de vulcão com magma, cone vulcânico e área de instabilidade tectônica.", "O vulcanismo mostra que parte do relevo é construída por forças internas do planeta."),
    ],
    ("Relevo", 3): [
        ("relevo_agentes_externos_erosao_01.svg", "erosao", "Encosta com ravinas e transporte de sedimentos pela água da chuva.", "A erosão remove solo e rocha, transportando materiais para áreas mais baixas."),
        ("relevo_agentes_externos_sedimentacao_01.svg", "sedimentos", "Rio depositando sedimentos em área baixa após desgaste de encostas.", "Transporte e sedimentação completam o processo iniciado pelo intemperismo e pela erosão."),
    ],
    ("Relevo", 4): [
        ("relevo_brasileiro_mapa_altitudes_01.svg", "mapa_brasil", "Mapa esquemático do Brasil com áreas de planaltos, depressões e planícies.", "O mapa ajuda a perceber que o relevo brasileiro é variado e não se resume a montanhas."),
        ("relevo_brasileiro_planalto_planicie_01.svg", "comparacao", "Comparação visual entre planalto central e planície amazônica.", "Comparar duas formas brasileiras ajuda a relacionar altitude, rios, erosão e sedimentação."),
    ],
    ("Relevo", 5): [
        ("relevo_sociedade_encostas_01.svg", "cidade_encosta", "Ocupação urbana em encosta com ruas, moradias e área de declividade acentuada.", "O relevo influencia onde construir, plantar, abrir estradas e prevenir riscos."),
        ("relevo_sociedade_estradas_01.svg", "estrada_serra", "Estrada sinuosa atravessando serra e vale.", "Estradas em áreas inclinadas exigem cortes, túneis, contenção e planejamento."),
    ],
    ("Relevo", 6): [
        ("relevo_riscos_deslizamento_01.svg", "risco", "Encosta com solo exposto, chuva forte e seta indicando risco de deslizamento.", "Deslizamentos combinam declividade, chuva, solo, vegetação e ocupação humana."),
        ("relevo_riscos_enchente_vale_01.svg", "enchente", "Vale urbano com rio cheio ocupando a planície de inundação.", "Áreas baixas próximas a rios podem inundar, sobretudo quando a cidade impermeabiliza o solo."),
    ],
    ("Clima", 1): [
        ("clima_tempo_clima_previsao_01.svg", "tempo_clima", "Comparação entre previsão do tempo de um dia e gráfico climático de vários anos.", "Tempo descreve o momento; clima depende de padrões observados durante longo período."),
        ("clima_tempo_clima_paisagens_01.svg", "comparacao", "Duas paisagens comparando chuva momentânea e ambiente semiárido recorrente.", "A imagem separa condição atmosférica passageira de padrão climático regional."),
    ],
    ("Clima", 2): [
        ("clima_elementos_estacao_01.svg", "estacao", "Estação meteorológica com termômetro, pluviômetro, barômetro e anemômetro.", "Os elementos do clima são medidos por instrumentos para comparar lugares e períodos."),
        ("clima_elementos_precipitacao_vento_01.svg", "atmosfera", "Nuvens, chuva e vento representando precipitação, umidade e circulação do ar.", "Temperatura, umidade, pressão, ventos e precipitação atuam juntos na atmosfera."),
    ],
    ("Clima", 3): [
        ("clima_fatores_latitude_altitude_01.svg", "latitude_altitude", "Globo com faixas de latitude e montanha indicando efeito da altitude.", "Latitude e altitude ajudam a explicar diferenças de temperatura entre lugares."),
        ("clima_fatores_maritimidade_01.svg", "maritimidade", "Costa marítima e interior continental comparando influência do oceano.", "Maritimidade e continentalidade alteram umidade, amplitude térmica e chuvas."),
    ],
    ("Clima", 4): [
        ("clima_massas_ar_brasil_01.svg", "massas_ar", "Mapa esquemático do Brasil com setas de massas de ar tropical, equatorial e polar.", "Massas de ar deslocam calor e umidade, alterando o tempo em várias regiões."),
        ("clima_frente_fria_01.svg", "frente_fria", "Frente fria avançando sobre área urbana com nuvens e queda de temperatura.", "Frentes mostram o encontro de massas de ar com características diferentes."),
    ],
    ("Clima", 5): [
        ("clima_brasileiros_mapa_01.svg", "mapa_brasil", "Mapa esquemático com climas equatorial, tropical, semiárido, atlântico e subtropical.", "A distribuição dos climas brasileiros depende de latitude, massas de ar, relevo e maritimidade."),
        ("clima_brasileiros_climograma_01.svg", "climograma", "Climograma comparando chuva e temperatura ao longo do ano.", "Climogramas ajudam a reconhecer estação seca, período chuvoso e variação térmica."),
    ],
    ("Clima", 6): [
        ("clima_mudancas_eventos_extremos_01.svg", "grafico", "Gráfico de aumento de temperatura acompanhado de ícones de seca e chuva extrema.", "Mudanças climáticas aumentam riscos e podem intensificar eventos extremos."),
        ("clima_mudancas_ilha_calor_01.svg", "cidade_calor", "Área urbana com superfície aquecida e poucas áreas verdes.", "Cidades podem ampliar o calor local, afetando saúde, energia e conforto térmico."),
    ],
    ("Clima", 7): [
        ("clima_cotidiano_agricultura_01.svg", "agricultura", "Plantação dependente de chuva regular e reservatório de água.", "O clima interfere na agricultura, no abastecimento e no preço dos alimentos."),
        ("clima_cotidiano_saude_energia_01.svg", "cotidiano", "Cidade com calor intenso, rede elétrica e pessoas buscando sombra.", "Ondas de calor, estiagens e chuvas fortes afetam saúde, transporte e energia."),
    ],
    ("Vegetação", 1): [
        ("vegetacao_cobertura_tipos_01.svg", "vegetacao_tipos", "Mosaico de floresta, campo e savana representando diferentes coberturas vegetais.", "Vegetação é a cobertura de plantas de uma área, variando conforme clima, solo, relevo e água."),
        ("vegetacao_estratos_01.svg", "floresta_estratos", "Esquema de estratos vegetais com árvores altas, arbustos e herbáceas.", "Observar altura, densidade e espaçamento ajuda a diferenciar formações vegetais."),
    ],
    ("Vegetação", 2): [
        ("vegetacao_biomas_brasil_01.svg", "mapa_brasil", "Mapa esquemático do Brasil com Amazônia, Cerrado, Caatinga, Mata Atlântica, Pantanal e Pampa.", "Os biomas brasileiros ocupam regiões diferentes e possuem adaptações próprias."),
        ("vegetacao_biomas_comparacao_01.svg", "comparacao", "Comparação entre floresta densa, Cerrado, Caatinga, Pantanal e Pampa.", "A variedade visual evita confundir todos os biomas com uma única paisagem verde."),
    ],
    ("Vegetação", 3): [
        ("vegetacao_clima_chuva_seca_01.svg", "chuva_seca", "Paisagens vegetais comparando ambiente úmido e ambiente seco.", "Chuva e temperatura influenciam densidade, folhas, raízes e adaptação das plantas."),
        ("vegetacao_clima_caatinga_01.svg", "caatinga", "Caatinga com plantas espaçadas e adaptadas à seca.", "A Caatinga mostra como a vegetação responde à irregularidade das chuvas."),
    ],
    ("Vegetação", 4): [
        ("vegetacao_impactos_desmatamento_01.svg", "desmatamento", "Área de floresta fragmentada por desmatamento e avanço da ocupação humana.", "Desmatamento e queimadas reduzem biodiversidade e alteram solo, água e clima local."),
        ("vegetacao_conservacao_corredores_01.svg", "corredor_ecologico", "Corredor ecológico ligando dois fragmentos de vegetação nativa.", "A conservação conecta áreas naturais e favorece circulação de espécies."),
    ],
    ("Hidrografia", 1): [
        ("hidrografia_aguas_continentais_01.svg", "ciclo_agua", "Paisagem com nascente, rio, lago e aquífero subterrâneo.", "Águas continentais incluem águas superficiais e subterrâneas."),
        ("hidrografia_aquifero_nascente_01.svg", "aquifero", "Corte do solo mostrando aquífero alimentando uma nascente.", "Aquíferos armazenam água no subsolo e podem alimentar rios e nascentes."),
    ],
    ("Hidrografia", 2): [
        ("hidrografia_bacia_rede_01.svg", "bacia", "Rede de drenagem com rio principal, afluentes, divisor de águas e foz.", "Bacia hidrográfica é a área drenada por rios conectados."),
        ("hidrografia_bacia_mapa_01.svg", "mapa_bacia", "Mapa esquemático de bacia hidrográfica com limites e afluentes.", "O mapa mostra que limites de bacia seguem o relevo, não necessariamente fronteiras políticas."),
    ],
    ("Hidrografia", 3): [
        ("hidrografia_usos_agua_01.svg", "usos_agua", "Rio abastecendo cidade, irrigação, indústria e geração de energia.", "A mesma água pode sustentar consumo, produção de alimentos, indústria e energia."),
        ("hidrografia_hidreletrica_irrigacao_01.svg", "represa", "Barragem com reservatório, turbinas e canal de irrigação.", "Represas ampliam usos da água, mas também transformam rios e paisagens."),
    ],
    ("Hidrografia", 4): [
        ("hidrografia_problemas_poluicao_01.svg", "rio_urbano", "Rio urbano com esgoto, lixo e margens impermeabilizadas.", "Poluição e assoreamento reduzem qualidade da água e afetam a vida nos rios."),
        ("hidrografia_problemas_escassez_enchente_01.svg", "escassez_enchente", "Comparação entre reservatório baixo e área urbana inundada.", "Problemas hídricos incluem falta de água e excesso de água em áreas vulneráveis."),
    ],
    ("População", 1): [
        ("populacao_conceitos_densidade_01.svg", "densidade", "Mapa com áreas de alta e baixa densidade demográfica.", "Densidade demográfica mostra habitantes por área, diferente de população total."),
        ("populacao_conceitos_populoso_povoado_01.svg", "comparacao", "Comparação entre território populoso e área muito povoada.", "Um país pode ter muitos habitantes e, ainda assim, possuir regiões pouco povoadas."),
    ],
    ("População", 2): [
        ("populacao_crescimento_curva_01.svg", "grafico", "Gráfico de crescimento populacional com natalidade e mortalidade.", "Crescimento vegetativo depende da relação entre nascimentos e mortes."),
        ("populacao_crescimento_transicao_01.svg", "transicao", "Sequência da transição demográfica com queda da mortalidade e da natalidade.", "Mudanças em saúde, renda e educação alteram o ritmo de crescimento populacional."),
    ],
    ("População", 3): [
        ("populacao_estrutura_piramide_01.svg", "piramide", "Pirâmide etária com base, adultos e idosos destacados.", "Pirâmides etárias mostram idade, sexo e sinais de envelhecimento populacional."),
        ("populacao_estrutura_envelhecimento_01.svg", "grafico_idade", "Comparação entre população jovem e população envelhecida.", "A forma da pirâmide indica demandas por escolas, trabalho, saúde e previdência."),
    ],
    ("População", 4): [
        ("populacao_distribuicao_litoral_interior_01.svg", "mapa_brasil", "Mapa esquemático do Brasil com maior concentração populacional no litoral.", "A distribuição da população brasileira é desigual e historicamente concentrada em certas regiões."),
        ("populacao_distribuicao_rural_urbano_01.svg", "rural_urbano", "Comparação entre área rural dispersa e área urbana concentrada.", "Fatores históricos, econômicos e naturais influenciam onde as pessoas vivem."),
    ],
    ("População", 5): [
        ("populacao_brasileira_diversidade_01.svg", "brasil_diversidade", "Mapa do Brasil com símbolos de diversidade regional e população urbana.", "A população brasileira é diversa e apresenta diferenças regionais importantes."),
        ("populacao_brasileira_desigualdade_01.svg", "desigualdade", "Comparação visual entre áreas com diferentes condições de moradia e serviços.", "Dados populacionais também revelam desigualdades de renda, saneamento e acesso a serviços."),
    ],
    ("População", 6): [
        ("populacao_indicadores_idh_01.svg", "indicadores", "Painel de indicadores sociais com renda, escolaridade, saúde e saneamento.", "Indicadores sociais ajudam a comparar condições de vida entre lugares."),
        ("populacao_indicadores_saneamento_01.svg", "saneamento", "Mapa temático com diferentes níveis de acesso a saneamento.", "Saneamento, renda e escolaridade têm distribuição desigual no território."),
    ],
    ("Migrações", 1): [
        ("migracoes_tipos_fluxos_01.svg", "fluxos", "Setas mostrando migração interna, externa, temporária e definitiva.", "Tipos de migração dependem de origem, destino, duração e permanência."),
        ("migracoes_tipos_fronteira_01.svg", "fronteira", "Pessoas atravessando limite entre regiões e países em mapa esquemático.", "A fronteira ajuda a diferenciar migração interna de migração internacional."),
    ],
    ("Migrações", 2): [
        ("migracoes_causas_emprego_estudo_01.svg", "causas", "Fluxos migratórios motivados por emprego, estudo, família e clima.", "Causas migratórias podem ser econômicas, sociais, ambientais ou políticas."),
        ("migracoes_causas_trabalho_01.svg", "trabalho", "Deslocamento de pessoas em direção a área com oferta de trabalho.", "A busca por emprego é uma causa frequente de deslocamentos populacionais."),
    ],
    ("Migrações", 3): [
        ("migracoes_brasil_campo_cidade_01.svg", "campo_cidade", "Setas do campo para a cidade representando êxodo rural e urbanização.", "Migrações internas brasileiras alteraram a distribuição da população e o crescimento urbano."),
        ("migracoes_brasil_pendular_01.svg", "pendular", "Trajeto diário de ida e volta entre moradia periférica e centro de trabalho.", "Migração pendular ocorre em deslocamentos cotidianos para estudo ou trabalho."),
    ],
    ("Migrações", 4): [
        ("migracoes_refugiados_deslocamento_01.svg", "refugiados", "Grupo de pessoas em deslocamento com rota marcada em mapa, sem cena violenta.", "Migração forçada envolve fuga por guerra, perseguição, desastre ou ameaça à vida."),
        ("migracoes_refugiados_acolhimento_01.svg", "acolhimento", "Posto de acolhimento com documentação, abrigo e apoio humanitário.", "Direitos de refugiados envolvem proteção, acolhimento e acesso a serviços básicos."),
    ],
    ("Urbanização", 1): [
        ("urbanizacao_conceito_expansao_01.svg", "expansao_urbana", "Mancha urbana crescendo ao redor de um centro inicial.", "Urbanização envolve crescimento da população urbana e expansão da área construída."),
        ("urbanizacao_conceito_servicos_01.svg", "cidade_servicos", "Cidade com moradias, comércio, escola, hospital e transporte.", "A cidade concentra serviços, empregos e fluxos que atraem população."),
    ],
    ("Urbanização", 2): [
        ("urbanizacao_rede_hierarquia_01.svg", "rede_urbana", "Rede urbana com metrópole, cidade média e centros locais conectados.", "Cidades exercem diferentes níveis de influência sobre serviços e deslocamentos."),
        ("urbanizacao_rede_fluxos_01.svg", "fluxos_urbanos", "Setas de pessoas, mercadorias e informações ligando cidades.", "A rede urbana aparece nos fluxos diários e regionais entre centros urbanos."),
    ],
    ("Urbanização", 3): [
        ("urbanizacao_metropolizacao_conurbacao_01.svg", "conurbacao", "Duas manchas urbanas conectadas formando região metropolitana.", "Metropolização inclui conurbação, concentração de serviços e fluxos pendulares."),
        ("urbanizacao_metropolizacao_verticalizacao_01.svg", "verticalizacao", "Centro metropolitano com edifícios altos e bairros ao redor.", "Verticalização e densidade são marcas visíveis de muitas metrópoles."),
    ],
    ("Urbanização", 4): [
        ("urbanizacao_problemas_enchentes_01.svg", "enchente_urbana", "Rua alagada por chuva em área impermeabilizada.", "Enchentes urbanas se relacionam com drenagem, rios canalizados e ocupação de várzeas."),
        ("urbanizacao_problemas_moradia_saneamento_01.svg", "moradia_saneamento", "Bairro com moradias precárias e ausência de saneamento adequado.", "Problemas urbanos revelam desigualdades no acesso à moradia e infraestrutura."),
    ],
    ("Urbanização", 5): [
        ("urbanizacao_planejamento_mobilidade_01.svg", "mobilidade", "Corredor de ônibus, ciclovia e calçadas em avenida planejada.", "Planejamento urbano organiza mobilidade, habitação, áreas verdes e serviços."),
        ("urbanizacao_planejamento_zoneamento_01.svg", "zoneamento", "Mapa de zoneamento com áreas residenciais, comerciais, verdes e transporte.", "Mapas urbanos ajudam a decidir usos do solo e reduzir conflitos de circulação."),
    ],
    ("Urbanização", 6): [
        ("urbanizacao_sustentavel_areas_verdes_01.svg", "areas_verdes", "Parque urbano integrado a transporte coletivo e moradias.", "Cidades sustentáveis combinam áreas verdes, mobilidade e acesso a serviços."),
        ("urbanizacao_sustentavel_drenagem_01.svg", "drenagem", "Rua com jardins de chuva, árvores e pavimento permeável.", "Soluções sustentáveis reduzem calor, enchentes e desigualdades ambientais."),
    ],
    ("Globalização", 1): [
        ("globalizacao_conceito_redes_01.svg", "rede_global", "Mapa-múndi com conexões de transporte, comércio e informação.", "Globalização intensifica conexões entre lugares por redes materiais e digitais."),
        ("globalizacao_conceito_produto_01.svg", "produto_global", "Produto montado com peças vindas de diferentes países.", "Um produto global pode reunir matéria-prima, tecnologia, trabalho e mercado em vários países."),
    ],
    ("Globalização", 2): [
        ("globalizacao_fluxos_mercadorias_pessoas_01.svg", "fluxos_globais", "Setas globais de mercadorias, pessoas, capitais e informações.", "Fluxos globais têm intensidades diferentes e conectam lugares de modo desigual."),
        ("globalizacao_fluxos_porto_aeroporto_01.svg", "porto_aeroporto", "Porto, aeroporto e cabos digitais conectados a rotas internacionais.", "Portos, aeroportos e redes digitais tornam a circulação global visível."),
    ],
    ("Globalização", 3): [
        ("globalizacao_transnacionais_cadeia_01.svg", "cadeia_produtiva", "Cadeia produtiva global com pesquisa, peças, montagem e venda em países distintos.", "Empresas transnacionais distribuem etapas produtivas em diferentes territórios."),
        ("globalizacao_transnacionais_fabrica_01.svg", "fabrica_rede", "Fábrica conectada a fornecedores e mercados internacionais.", "A produção em rede depende de logística, tecnologia, trabalho e custos."),
    ],
    ("Globalização", 4): [
        ("globalizacao_cultura_consumo_01.svg", "cultura_consumo", "Cidade com marcas, músicas e hábitos culturais circulando globalmente.", "Cultura e consumo circulam por mídias, turismo, comércio e plataformas digitais."),
        ("globalizacao_cultura_hibridismo_01.svg", "hibridismo", "Elementos culturais locais e globais misturados no espaço urbano.", "A globalização não apaga todos os lugares; ela também produz misturas culturais."),
    ],
    ("Globalização", 5): [
        ("globalizacao_desigualdades_centro_periferia_01.svg", "desigualdade_global", "Mapa com centros financeiros e áreas exportadoras de matérias-primas.", "A integração mundial distribui ganhos e vulnerabilidades de forma desigual."),
        ("globalizacao_desigualdades_materia_prima_01.svg", "materia_prima", "Fluxo de minério e alimentos saindo de país exportador para centro industrial.", "Dependência de matérias-primas pode limitar tecnologia, renda e autonomia econômica."),
    ],
    ("Globalização", 6): [
        ("globalizacao_tecnologia_cabos_01.svg", "cabos_submarinos", "Mapa com cabos submarinos ligando continentes e centros de dados.", "A internet depende de infraestrutura física, como cabos, antenas e data centers."),
        ("globalizacao_tecnologia_redes_digitais_01.svg", "redes_digitais", "Rede de telecomunicações conectando pessoas, empresas e serviços.", "Tecnologia acelera fluxos de informação, dinheiro, trabalho e consumo."),
    ],
    ("Geopolítica", 1): [
        ("geopolitica_poder_territorio_fronteira_01.svg", "fronteira", "Território com fronteira, posto de controle e área de soberania.", "Poder e território aparecem no controle de fronteiras, recursos e circulação."),
        ("geopolitica_poder_soberania_01.svg", "mapa_politico", "Mapa político com Estado, capital, fronteiras e símbolos de soberania.", "Soberania indica autoridade do Estado sobre um território reconhecido."),
    ],
    ("Geopolítica", 2): [
        ("geopolitica_estado_nacao_governo_01.svg", "conceitos_politicos", "Diagrama distinguindo Estado, nação, território e governo.", "Estado, nação e governo são conceitos relacionados, mas não equivalentes."),
        ("geopolitica_estado_plurinacional_01.svg", "plurinacional", "Território com diferentes grupos culturais sob uma mesma estrutura estatal.", "Estados podem reunir várias nações e identidades dentro de uma fronteira."),
    ],
    ("Geopolítica", 3): [
        ("geopolitica_recursos_petroleo_agua_01.svg", "recursos", "Mapa com petróleo, água, minérios e rotas estratégicas.", "Recursos estratégicos influenciam alianças, disputas e políticas de segurança."),
        ("geopolitica_recursos_rotas_01.svg", "rotas", "Rotas marítimas e pontos de passagem conectando áreas produtoras e consumidoras.", "Quem controla rotas e infraestrutura pode ampliar influência internacional."),
    ],
    ("Geopolítica", 4): [
        ("geopolitica_fronteiras_disputas_01.svg", "fronteira_disputada", "Fronteira contestada com zonas de controle e área de tensão.", "Disputas de fronteira envolvem território, identidade, recursos e segurança."),
        ("geopolitica_fronteiras_corredor_01.svg", "corredor", "Corredor estratégico entre países com rotas comerciais e militares.", "Algumas áreas fronteiriças são estratégicas por acesso, comércio ou defesa."),
    ],
    ("Geopolítica", 5): [
        ("geopolitica_potencias_influencia_01.svg", "potencias", "Mapa-múndi com polos de influência econômica, militar, tecnológica e cultural.", "Potências mundiais projetam influência por diferentes tipos de poder."),
        ("geopolitica_potencias_diplomacia_01.svg", "diplomacia", "Mesa diplomática entre grandes potências com mapa ao fundo.", "Disputas entre potências também passam por negociações, acordos e pressão econômica."),
    ],
    ("Geopolítica", 6): [
        ("geopolitica_brasil_amazonia_01.svg", "amazonia_estrategica", "Mapa do Brasil destacando Amazônia, fronteiras e recursos hídricos.", "Amazônia, Atlântico Sul e integração regional são temas estratégicos para o Brasil."),
        ("geopolitica_brasil_atlantico_sul_01.svg", "atlantico_sul", "Costa brasileira e Atlântico Sul com rotas marítimas e áreas de interesse.", "O litoral e o oceano ampliam a dimensão geopolítica do território brasileiro."),
    ],
    ("Geopolítica", 7): [
        ("geopolitica_contemporanea_dados_01.svg", "dados", "Satélites, data centers e cabos digitais conectando territórios.", "A geopolítica contemporânea inclui tecnologia, dados, semicondutores e redes."),
        ("geopolitica_contemporanea_ciberseguranca_01.svg", "ciberseguranca", "Rede digital com pontos protegidos e tentativas de ataque bloqueadas.", "Cibersegurança tornou-se parte da proteção de Estados, empresas e infraestrutura."),
    ],
    ("Conflitos mundiais", 1): [
        ("conflitos_causas_territorio_recursos_01.svg", "causas_conflito", "Mapa de área disputada por território, recursos naturais e rotas.", "Conflitos podem combinar causas territoriais, políticas, econômicas e culturais."),
        ("conflitos_causas_linhas_tensao_01.svg", "linhas_tensao", "Fronteira com grupos, recursos e linhas de tensão marcadas de forma não violenta.", "Localizar causas evita explicar conflitos apenas por opinião ou por um único fator."),
    ],
    ("Conflitos mundiais", 2): [
        ("conflitos_populacao_civil_deslocamento_01.svg", "deslocamento_civil", "Famílias deslocadas seguindo rota segura em mapa, sem representação violenta.", "Guerras afetam população civil por deslocamento, perda de moradia e insegurança."),
        ("conflitos_populacao_civil_abrigo_01.svg", "abrigo", "Abrigo humanitário com serviços de saúde, água e documentação.", "A resposta humanitária busca proteger pessoas e garantir condições básicas."),
    ],
    ("Conflitos mundiais", 3): [
        ("conflitos_terrorismo_seguranca_fronteira_01.svg", "seguranca", "Controle de segurança em aeroporto e fronteira representado de forma educativa.", "Medidas de segurança alteram circulação, vigilância e políticas de fronteira."),
        ("conflitos_terrorismo_redes_01.svg", "rede_seguranca", "Mapa de rede de ameaças e respostas institucionais sem cenas violentas.", "O tema deve ser analisado por localização, atores, impactos e respostas dos Estados."),
    ],
    ("Conflitos mundiais", 4): [
        ("conflitos_diplomacia_paz_onu_01.svg", "onu_paz", "Sala de negociação internacional com bandeiras e mapa de área em conflito.", "Diplomacia e organismos internacionais buscam mediação e redução de tensões."),
        ("conflitos_diplomacia_acordo_01.svg", "acordo", "Documento de acordo de paz ligado a rotas de retirada e zonas de proteção.", "Acordos podem criar cessar-fogo, corredores humanitários e missões de paz."),
    ],
    ("Blocos econômicos", 1): [
        ("blocos_integracao_regional_01.svg", "integracao", "Países vizinhos conectados por comércio, infraestrutura e circulação.", "Blocos econômicos surgem para ampliar cooperação e reduzir barreiras."),
        ("blocos_integracao_fronteira_01.svg", "fronteira_comercial", "Ponte de fronteira com caminhões e controle aduaneiro simplificado.", "A infraestrutura regional facilita trocas comerciais entre países próximos."),
    ],
    ("Blocos econômicos", 2): [
        ("blocos_tipos_livre_comercio_01.svg", "tipos_bloco", "Quadro comparando zona de livre comércio, união aduaneira e mercado comum.", "Tipos de bloco variam pelo grau de integração econômica."),
        ("blocos_tipos_tarifas_01.svg", "tarifas", "Mercadorias atravessando fronteiras com redução de tarifas.", "Acordos comerciais mudam impostos, regras e circulação de bens."),
    ],
    ("Blocos econômicos", 3): [
        ("blocos_mercosul_mapa_01.svg", "mercosul", "Mapa da América do Sul destacando países do Mercosul e rotas comerciais.", "O Mercosul conecta países vizinhos por comércio, política e circulação regional."),
        ("blocos_mercosul_comercio_01.svg", "comercio_regional", "Fluxo de veículos, alimentos e manufaturados entre Brasil, Argentina, Paraguai e Uruguai.", "O bloco influencia exportações, importações e negociações sul-americanas."),
    ],
    ("Blocos econômicos", 4): [
        ("blocos_uniao_europeia_mapa_01.svg", "uniao_europeia", "Mapa da Europa destacando integração da União Europeia.", "A União Europeia combina mercado comum, instituições políticas e cooperação regional."),
        ("blocos_uniao_europeia_instituicoes_01.svg", "instituicoes_ue", "Parlamento, moeda e livre circulação representando integração europeia.", "A integração europeia é mais profunda que uma simples redução de tarifas."),
    ],
    ("Relações internacionais", 1): [
        ("relacoes_diplomacia_negociacao_01.svg", "diplomacia", "Mesa de negociação com representantes de países e mapa político.", "Diplomacia é negociação oficial entre Estados por meio de acordos, embaixadas e tratados."),
        ("relacoes_diplomacia_tratado_01.svg", "tratado", "Tratado internacional com assinaturas e bandeiras.", "Tratados registram compromissos entre países e organizações."),
    ],
    ("Relações internacionais", 2): [
        ("relacoes_cooperacao_clima_01.svg", "cooperacao_climatica", "Conferência internacional sobre clima com países conectados por metas comuns.", "Cooperação internacional aparece em ciência, ambiente, saúde, comércio e ajuda humanitária."),
        ("relacoes_cooperacao_ajuda_01.svg", "ajuda_internacional", "Rede de cooperação enviando tecnologia, alimentos e apoio técnico entre países.", "Cooperar significa dividir responsabilidades e recursos para enfrentar problemas comuns."),
    ],
    ("Relações internacionais", 3): [
        ("relacoes_direitos_humanos_onu_01.svg", "direitos_humanos", "Sessão internacional debatendo direitos humanos, refúgio e proteção.", "Direitos humanos orientam normas internacionais de proteção às pessoas."),
        ("relacoes_direitos_humanos_refugio_01.svg", "direito_refugio", "Mapa com rota de refúgio e símbolos de documentação e acolhimento.", "O direito ao refúgio é uma proteção internacional para pessoas ameaçadas."),
    ],
    ("Relações internacionais", 4): [
        ("relacoes_desafios_globais_01.svg", "desafios_globais", "Mapa-múndi conectando pandemia, clima, comércio e segurança alimentar.", "Desafios globais ultrapassam fronteiras e exigem coordenação entre países."),
        ("relacoes_desafios_organizacoes_01.svg", "organizacoes", "Organizações internacionais articulando respostas a crises em várias regiões.", "Instituições multilaterais ajudam a coordenar decisões diante de problemas comuns."),
    ],
}


def pontuar_arquivo_real(arquivo, termos):
    nome = arquivo.lower()
    pontos = 0
    for termo in termos:
        if termo and termo in nome:
            pontos += 4
    if nome.endswith((".jpg", ".jpeg", ".png", ".webp")):
        pontos += 2
    if nome.endswith(".svg"):
        pontos -= 20
    return pontos


def termos_busca_visual(tema, aula, arquivo, tipo, alt):
    base = " ".join([tema, aula, arquivo, tipo, alt]).lower()
    base = base.translate(str.maketrans("áàãâéêíóôõúç", "aaaaeeiooouc"))
    candidatos = [
        "erosao", "vulcao", "montanha", "planicie", "bacia", "rio", "aeroporto",
        "porto", "refugi", "fronteira", "cidade", "urbana", "amazon", "caatinga",
        "cerrado", "pampa", "pantanal", "mercosul", "europe", "onu", "population",
        "densidade", "pyramid", "climate", "weather", "rain", "drought", "flood",
        "sao paulo", "curitiba", "congresso", "parliament", "dam", "forest",
        "deforestation", "migration", "container", "factory", "datacenter",
    ]
    return [termo for termo in candidatos if termo in base]


def construir_complementos_reais_aulas():
    usados = {item["arquivo"] for item in IMAGENS_AULAS_REAIS.values()}
    complementos = {}
    for (tema, numero), visuais in VISUAIS_LOCAIS_AULAS.items():
        pool = list(IMAGENS_SUPLEMENTARES.get(tema, [])) + list(IMAGENS_SUPLEMENTARES.get("Geral", []))
        for arquivo_svg, tipo, alt, observacao in visuais:
            if arquivo_svg in IMAGENS_AULAS_REAIS:
                continue
            termos = termos_busca_visual(tema, f"Aula {numero}", arquivo_svg, tipo, alt)
            candidatos = sorted(
                pool,
                key=lambda item: (pontuar_arquivo_real(item, termos), -len(item)),
                reverse=True,
            )
            escolhido = None
            for nome in candidatos:
                if nome.lower().endswith(".svg"):
                    continue
                caminho = f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(nome)}"
                if caminho in usados:
                    continue
                escolhido = nome
                usados.add(caminho)
                break
            if escolhido:
                complementos[arquivo_svg] = {
                    "arquivo": f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(escolhido)}",
                    "externa": True,
                    "alt": alt,
                    "fonte": f"Wikimedia Commons; arquivo File:{escolhido}.",
                    "observacao": observacao,
                    "zoom": True,
                }
    return complementos


COMPLEMENTOS_REAIS_MANUAIS = {
    "relevo_brasileiro_mapa_altitudes_01.svg": imagem_commons("File:Chapada Diamantina vista.jpg", "Chapada Diamantina com superfícies elevadas e escarpas do relevo brasileiro.", "A fotografia permite observar planaltos, escarpas e diferenças de altitude no território brasileiro."),
    "relevo_sociedade_encostas_01.svg": imagem_commons("File:Favela da Rocinha.jpg", "Ocupação urbana em encosta, com moradias em área de forte declividade.", "A imagem mostra como o relevo influencia moradia, circulação e risco em áreas urbanas."),
    "clima_tempo_clima_paisagens_01.svg": imagem_commons("File:CAATINGA NORDESTINA.JPG", "Paisagem de Caatinga no semiárido, usada para diferenciar padrão climático de tempo do dia.", "A paisagem semiárida ajuda a entender clima como padrão regional de longa duração."),
    "clima_fatores_maritimidade_01.svg": imagem_commons("File:Rio de Janeiro Ipanema Beach.jpg", "Praia urbana no Rio de Janeiro, com contato direto entre oceano e cidade.", "A proximidade do oceano influencia umidade, ventos e amplitude térmica."),
    "clima_massas_ar_brasil_01.svg": imagem_commons("File:A Satellite View of a Back-door Cold Front (14295309881).jpg", "Imagem de satélite de frente fria, relacionada ao deslocamento de massas de ar.", "Massas de ar e frentes frias mudam temperatura, nebulosidade e chuva em grandes áreas."),
    "clima_brasileiros_mapa_01.svg": imagem_commons("File:Brazil Köppen Climate Map.png", "Mapa dos climas do Brasil segundo Köppen-Geiger.", "O mapa mostra a distribuição dos climas brasileiros por cores e regiões."),
    "clima_mudancas_eventos_extremos_01.svg": imagem_commons("File:Cyclone Flurry in the Southern Hemisphere (153995).jpg", "Imagem de satélite com sistemas atmosféricos intensos no Hemisfério Sul.", "Eventos extremos e mudanças climáticas podem ser analisados por imagens de satélite e dados."),
    "clima_cotidiano_saude_energia_01.svg": imagem_commons("File:The effects of the drought on vegetation in Morocco.jpg", "Área afetada por seca, mostrando impacto do clima sobre vegetação e atividades humanas.", "Secas e ondas de calor afetam saúde, energia, abastecimento e produção agrícola."),
    "vegetacao_cobertura_tipos_01.svg": imagem_commons("File:Amazon rainforest from above.jpg", "Vista aérea de floresta tropical densa.", "A cobertura vegetal pode ser observada pela densidade, continuidade e porte das plantas."),
    "vegetacao_clima_chuva_seca_01.svg": imagem_commons("File:Cerrado sentido restrito no Parque Nacional de Brasília.jpg", "Paisagem de Cerrado com árvores espaçadas e vegetação adaptada à sazonalidade.", "A vegetação do Cerrado ajuda a relacionar plantas, chuva e estação seca."),
    "vegetacao_conservacao_corredores_01.svg": imagem_commons("File:Mata Atlântica - Parque Estadual da Serra do Mar.jpg", "Trecho preservado de Mata Atlântica em área serrana.", "Áreas conservadas protegem biodiversidade e podem conectar fragmentos de vegetação."),
    "hidrografia_aguas_continentais_01.svg": imagem_commons("File:Spring water in Brazil.jpg", "Nascente com água surgindo no terreno.", "Nascentes, rios, lagos e aquíferos fazem parte das águas continentais."),
    "hidrografia_usos_agua_01.svg": imagem_commons("File:Rio São Francisco - Petrolina e Juazeiro.jpg", "Rio São Francisco entre áreas urbanas e agrícolas.", "Rios sustentam abastecimento, irrigação, transporte, energia e atividades econômicas."),
    "hidrografia_problemas_poluicao_01.svg": imagem_commons("File:Rio Tietê em São Paulo.jpg", "Rio urbano poluído em São Paulo.", "Rios urbanos mostram impactos de esgoto, lixo, canalização e ocupação das margens."),
    "populacao_conceitos_populoso_povoado_01.svg": imagem_commons("File:São Paulo city (Bela Vista).jpg", "Área urbana muito povoada em São Paulo.", "A concentração de pessoas e edifícios ajuda a discutir densidade demográfica."),
    "populacao_crescimento_curva_01.svg": imagem_commons("File:Brazil population.png", "Gráfico de crescimento da população brasileira.", "O gráfico ajuda a observar crescimento populacional ao longo do tempo."),
    "populacao_crescimento_transicao_01.svg": imagem_commons("File:Demographic transition model.png", "Modelo gráfico de transição demográfica.", "O modelo relaciona queda da mortalidade, queda da natalidade e mudança no crescimento populacional."),
    "populacao_brasileira_diversidade_01.svg": imagem_commons("File:Brazilian people.jpg", "Grupo de pessoas no Brasil, representando diversidade populacional.", "A população brasileira é diversa em origem, cultura, idade e condições sociais."),
    "populacao_brasileira_desigualdade_01.svg": imagem_commons("File:Complexo alemao rj.jpg", "Área urbana densamente ocupada no Rio de Janeiro.", "A fotografia permite discutir desigualdade, moradia, infraestrutura e condições de vida."),
    "populacao_indicadores_saneamento_01.svg": imagem_commons("File:Estação de tratamento de esgoto.jpg", "Estação de tratamento de esgoto, relacionada a saneamento básico.", "Saneamento é indicador social importante para comparar qualidade de vida."),
    "migracoes_causas_trabalho_01.svg": imagem_commons("File:Trabalhadores em Obras de Fundação da Construção da Via Férrea - 484, Acervo do Museu Paulista da USP.jpg", "Trabalhadores em obra, relacionados à migração por emprego.", "A busca por trabalho é uma causa frequente de deslocamentos populacionais."),
    "migracoes_brasil_campo_cidade_01.svg": imagem_commons("File:Terminal Rodoviário de Coronel Fabriciano MG.JPG", "Terminal rodoviário com circulação de passageiros.", "Rodoviárias ajudam a observar deslocamentos internos e mudanças de residência."),
    "migracoes_brasil_pendular_01.svg": imagem_commons("File:Luz Train Station, Sao Paulo.jpg", "Estação de trem em São Paulo, relacionada a deslocamentos pendulares.", "Deslocamentos diários entre casa, estudo e trabalho são parte da dinâmica metropolitana."),
    "migracoes_refugiados_deslocamento_01.svg": imagem_commons("File:Refugees Budapest Keleti railway station 2015-09-04.jpg", "Pessoas refugiadas em deslocamento em estação ferroviária.", "A imagem contextualiza migração forçada sem recorrer a cenas violentas."),
    "migracoes_refugiados_acolhimento_01.svg": imagem_commons("File:Syrian refugees in lebanon.jpg", "Acampamento de pessoas refugiadas, usado para discutir acolhimento e direitos.", "Refugiados precisam de proteção, abrigo, documentação e acesso a serviços básicos."),
    "urbanizacao_problemas_moradia_saneamento_01.svg": imagem_commons("File:Favela in Rio de Janeiro.jpg", "Área urbana com moradias densas, relacionada a desigualdade e infraestrutura.", "Problemas urbanos incluem moradia precária, saneamento insuficiente e desigualdade territorial."),
    "globalizacao_conceito_redes_01.svg": imagem_commons("File:Container port (1).jpg", "Terminal de contêineres no Porto de Santos.", "Portos tornam visíveis as redes de comércio e transporte da globalização."),
    "globalizacao_fluxos_mercadorias_pessoas_01.svg": imagem_commons("File:FRA aerial 3.jpg", "Aeroporto internacional visto do alto.", "Aeroportos articulam fluxos globais de pessoas, mercadorias e conexões."),
    "globalizacao_fluxos_porto_aeroporto_01.svg": imagem_commons("File:Container Terminal in Hamburg .jpg", "Terminal de contêineres em porto internacional.", "Contêineres mostram a circulação mundial de mercadorias."),
    "globalizacao_transnacionais_cadeia_01.svg": imagem_commons("File:Electronics factory in Shenzhen.jpg", "Linha de montagem de eletrônicos em fábrica.", "Cadeias globais distribuem produção, montagem e venda entre países."),
    "globalizacao_transnacionais_fabrica_01.svg": imagem_commons("File:Volkswagen assembly line.jpg", "Linha de montagem industrial, ligada à produção em rede.", "Empresas transnacionais organizam fábricas, fornecedores e mercados em vários lugares."),
    "globalizacao_cultura_consumo_01.svg": imagem_commons("File:Shibuya crossing, Tokyo, Japan.jpg", "Cruzamento urbano movimentado em Tóquio.", "Cidades globais concentram marcas, consumo, comunicação e trocas culturais."),
    "globalizacao_cultura_hibridismo_01.svg": imagem_commons("File:Times Square, New York City (HDR).jpg", "Área comercial iluminada por marcas e publicidade internacional.", "A circulação cultural global aparece em marcas, mídia, consumo e paisagens urbanas."),
    "globalizacao_desigualdades_centro_periferia_01.svg": imagem_commons("File:La Défense from the Arc de Triomphe 2016.jpg", "Centro financeiro com edifícios corporativos.", "Centros financeiros concentram comando, capital e serviços avançados."),
    "globalizacao_desigualdades_materia_prima_01.svg": imagem_commons("File:Brazil-00012 - Open Pit Mine? (48954145937).jpg", "Mina a céu aberto no Brasil.", "A exportação de matérias-primas revela desigualdades nas cadeias globais."),
    "globalizacao_tecnologia_cabos_01.svg": imagem_commons("File:Landing of the submarine cable, Port Darwin, 7 November 1871(GN01968).jpg", "Instalação histórica de cabo submarino.", "Cabos submarinos mostram que redes digitais dependem de infraestrutura física."),
    "globalizacao_tecnologia_redes_digitais_01.svg": imagem_commons("File:Datacenter.jpg", "Sala de data center com servidores.", "Data centers sustentam fluxos de informação, serviços digitais e economia em rede."),
    "geopolitica_poder_territorio_fronteira_01.svg": imagem_commons("File:Argentina-Brazil border.jpg", "Área de fronteira entre Argentina e Brasil.", "Fronteiras expressam controle territorial, soberania e circulação."),
    "geopolitica_poder_soberania_01.svg": imagem_commons("File:National Congress of Brazil.jpg", "Congresso Nacional do Brasil.", "Instituições políticas representam o poder do Estado sobre o território."),
    "geopolitica_estado_nacao_governo_01.svg": imagem_commons("File:Palácio do Planalto GGFD8938.jpg", "Palácio do Planalto, sede do Poder Executivo brasileiro.", "A imagem ajuda a diferenciar Estado, governo, território e instituições políticas."),
    "geopolitica_estado_plurinacional_01.svg": imagem_commons("File:Indigenous people in Brazil.jpg", "Povos indígenas no Brasil, relacionados à diversidade nacional e territorial.", "Estados podem reunir diferentes povos, culturas e identidades nacionais."),
    "geopolitica_recursos_petroleo_agua_01.svg": imagem_commons("File:Oil platform P-51 (Brazil).jpg", "Plataforma de petróleo no Brasil.", "Petróleo, água, minérios e tecnologia podem ser recursos estratégicos."),
    "geopolitica_recursos_rotas_01.svg": imagem_commons("File:Strait of Hormuz.jpg", "Estreito marítimo estratégico para rotas de energia e comércio.", "Rotas marítimas e pontos de passagem influenciam poder econômico e militar."),
    "geopolitica_fronteiras_disputas_01.svg": imagem_commons("File:Checkpoint charlie 1961.jpg", "Posto de controle em Berlim durante a Guerra Fria.", "Fronteiras disputadas podem concentrar tensões políticas e militares."),
    "geopolitica_fronteiras_corredor_01.svg": imagem_commons("File:Puente Internacional Tancredo Neves.JPG", "Ponte internacional entre Brasil e Argentina.", "Infraestruturas de fronteira podem funcionar como corredores estratégicos."),
    "geopolitica_potencias_influencia_01.svg": imagem_commons("File:G20 leaders at the 2019 G20 Osaka summit.jpg", "Líderes de potências mundiais em reunião do G20.", "Potências projetam influência por economia, diplomacia, tecnologia e poder militar."),
    "geopolitica_potencias_diplomacia_01.svg": imagem_commons("File:Xi Jinping and Barack Obama toast at White House state dinner September 2015.jpg", "Encontro diplomático entre líderes dos Estados Unidos e da China.", "Relações entre potências combinam disputa, cooperação e negociação."),
    "geopolitica_brasil_amazonia_01.svg": imagem_commons("File:Amazon river.JPG", "Rio Amazonas na região de Manaus.", "A Amazônia envolve água, biodiversidade, fronteiras e soberania."),
    "geopolitica_brasil_atlantico_sul_01.svg": imagem_commons("File:Brazilian Navy aircraft carrier NAe São Paulo.jpg", "Navio militar brasileiro no Atlântico.", "O Atlântico Sul é área estratégica para defesa, rotas e recursos."),
    "geopolitica_contemporanea_dados_01.svg": imagem_commons("File:Abudhabi data center.jpg", "Data center com infraestrutura de servidores.", "Dados, satélites e infraestrutura digital são recursos geopolíticos contemporâneos."),
    "geopolitica_contemporanea_ciberseguranca_01.svg": imagem_commons("File:Cybersecurity operations center.jpg", "Centro de operações de cibersegurança.", "Cibersegurança protege redes, serviços e infraestrutura crítica."),
    "conflitos_causas_territorio_recursos_01.svg": imagem_commons("File:UN peacekeeping patrol.jpg", "Patrulha de missão de paz em área de tensão.", "Conflitos podem envolver território, recursos, identidades e interesses políticos."),
    "conflitos_causas_linhas_tensao_01.svg": imagem_commons("File:Peru–Ecuador Border at Aguas Verdes-Huaquillas in December 2023.jpg", "Fronteira internacional com circulação controlada.", "Fronteiras e áreas de controle ajudam a entender linhas de tensão."),
    "conflitos_populacao_civil_deslocamento_01.svg": imagem_commons("File:A Dutch school teacher leads a group of refugee children just disembarked from a ship at Tilbury Docks in Essex during 1945. D24064.jpg", "Crianças refugiadas desembarcando em porto durante deslocamento histórico.", "Guerras e conflitos provocam deslocamento populacional e insegurança."),
    "conflitos_populacao_civil_abrigo_01.svg": imagem_commons("File:A house in the refugee settlement (4361657153).jpg", "Moradia em assentamento de pessoas refugiadas.", "Abrigos humanitários protegem população civil afetada por conflitos."),
    "conflitos_terrorismo_seguranca_fronteira_01.svg": imagem_commons("File:TSA Security Checkpoint at Airport.jpg", "Controle de segurança em aeroporto.", "Políticas de segurança alteram circulação, vigilância e fronteiras."),
    "conflitos_terrorismo_redes_01.svg": imagem_commons("File:Interpol Global Complex for Innovation.jpg", "Centro internacional de cooperação policial e segurança.", "A segurança internacional envolve Estados, organizações e respostas coordenadas."),
    "conflitos_diplomacia_paz_onu_01.svg": imagem_commons("File:United Nations Security Council.jpg", "Conselho de Segurança da ONU em reunião.", "A diplomacia busca mediar conflitos e construir acordos de paz."),
    "conflitos_diplomacia_acordo_01.svg": imagem_commons("File:Signing of the Dayton Agreement.jpg", "Assinatura de acordo de paz.", "Acordos de paz podem estabelecer cessar-fogo, mediação e novas regras territoriais."),
    "blocos_integracao_regional_01.svg": imagem_commons("File:Border (3644419).jpg", "Fronteira internacional com passagem terrestre.", "A integração regional depende de infraestrutura, comércio e cooperação."),
    "blocos_integracao_fronteira_01.svg": imagem_commons("File:Uruguay Brazil border Chuy.jpg", "Fronteira entre Uruguai e Brasil com circulação urbana e comercial.", "Fronteiras em blocos econômicos podem facilitar circulação e comércio."),
    "blocos_tipos_livre_comercio_01.svg": imagem_commons("File:Port of Hamburg Container Terminal.jpg", "Terminal de contêineres em porto comercial.", "A circulação de mercadorias ajuda a explicar acordos comerciais e tarifas."),
    "blocos_tipos_tarifas_01.svg": imagem_commons("File:Customs officers checking freight.jpg", "Fiscalização aduaneira de cargas.", "Tarifas e regras alfandegárias mudam conforme o tipo de integração econômica."),
    "blocos_mercosul_mapa_01.svg": imagem_commons("File:XXX Cumbre del Mercosur - Córdoba - 21JUL06 -2- presidenciagovar..jpg", "Reunião de representantes do Mercosul.", "O Mercosul envolve comércio, negociação política e integração sul-americana."),
    "blocos_mercosul_comercio_01.svg": imagem_commons("File:Ponte sobre o Rio Tietê e comporta de usina hidrelétrica em Salto - panoramio - Amauri Aparecido Zar….jpg", "Ponte e infraestrutura de circulação sobre rio, relacionada a fluxos econômicos.", "Fluxos e infraestruturas tornam a integração econômica visível."),
    "blocos_uniao_europeia_mapa_01.svg": imagem_commons("File:European Parliament Strasbourg Hemicycle - Diliff.jpg", "Plenário do Parlamento Europeu.", "A União Europeia possui instituições políticas e integração econômica profunda."),
    "blocos_uniao_europeia_instituicoes_01.svg": imagem_commons("File:ARCHIGLASS Tomasz Urbanowicz Zjednoczony Świat Parlament Europejski.jpg", "Obra no Parlamento Europeu representando união entre países.", "Instituições europeias expressam cooperação política e econômica."),
    "relacoes_diplomacia_negociacao_01.svg": imagem_commons("File:Traktat Reformujacy UE.jpg", "Reunião diplomática para assinatura de tratado europeu.", "Diplomacia envolve negociação oficial entre Estados."),
    "relacoes_diplomacia_tratado_01.svg": imagem_commons("File:Signing of the Treaty of Lisbon.jpg", "Assinatura de tratado internacional.", "Tratados registram compromissos assumidos por países."),
    "relacoes_cooperacao_clima_01.svg": imagem_commons("File:UNFCCC COP21 CMP11 Leaders Event (23129423350).jpg", "Conferência internacional sobre clima.", "A cooperação climática depende de negociação entre muitos países."),
    "relacoes_cooperacao_ajuda_01.svg": imagem_commons("File:Humanitarian aid OCHA.jpg", "Entrega de ajuda humanitária internacional.", "Cooperação internacional também envolve apoio técnico, alimentos, saúde e abrigo."),
    "relacoes_direitos_humanos_onu_01.svg": imagem_commons("File:Deputy Secretary Blinken Addresses Reporters After Delivering Remarks at the 31st Session of the UN Human Rights Council in Geneva (25176985130).jpg", "Sessão do Conselho de Direitos Humanos da ONU.", "Direitos humanos são debatidos em instituições multilaterais."),
    "relacoes_direitos_humanos_refugio_01.svg": imagem_commons("File:A syrian refugee family lving in Jordan.jpg", "Família refugiada síria na Jordânia.", "O direito ao refúgio protege pessoas ameaçadas por conflitos e perseguições."),
    "relacoes_desafios_globais_01.svg": imagem_commons("File:WHO Plenary.jpg", "Assembleia internacional de saúde.", "Pandemias, clima e segurança alimentar são desafios que ultrapassam fronteiras."),
    "relacoes_desafios_organizacoes_01.svg": imagem_commons("File:United Nations General Assembly hall.jpg", "Salão da Assembleia Geral das Nações Unidas.", "Organizações internacionais coordenam respostas a problemas globais."),
}


COMPLEMENTOS_REAIS_AULAS = COMPLEMENTOS_REAIS_MANUAIS


SUBSTITUICOES_LOCAIS_VISUAIS = {
    "clima_fatores_maritimidade_01.svg": {
        "arquivo": "geo/imagens/catalogo/clima_paisagem.jpg",
        "externa": False,
        "alt": "Paisagem rural observada do alto, usada para discutir fatores climáticos e localização.",
        "fonte": "Wikimedia Commons; recurso local do projeto.",
        "observacao": "A localização e as características da paisagem ajudam a discutir fatores que diferenciam climas.",
        "zoom": True,
    },
    "vegetacao_cobertura_tipos_01.svg": {
        "arquivo": "geo/imagens/vegetacao/pantanal.jpg",
        "externa": False,
        "alt": "Paisagem real do Pantanal com vegetação e área alagada.",
        "fonte": "Wikimedia Commons; foto Bela paisagem do pantanal matogrossense.jpg, autor Vicente Bissoni Neto, CC BY-SA 4.0.",
        "observacao": "A imagem mostra cobertura vegetal associada à presença de água na paisagem.",
        "zoom": True,
    },
    "vegetacao_clima_chuva_seca_01.svg": {
        "arquivo": "geo/imagens/vegetacao/cerrado.jpg",
        "externa": False,
        "alt": "Paisagem real de Cerrado com árvores espaçadas e céu aberto.",
        "fonte": "Wikimedia Commons; foto Cerrado Brasileiro.jpg, autor Lbotton, CC BY-SA 3.0.",
        "observacao": "O Cerrado ajuda a relacionar vegetação, estação seca e clima tropical.",
        "zoom": True,
    },
    "vegetacao_conservacao_corredores_01.svg": {
        "arquivo": "geo/imagens/catalogo/vegetacao_caatinga.jpg",
        "externa": False,
        "alt": "Paisagem de Caatinga com vegetação adaptada ao semiárido.",
        "fonte": "Wikimedia Commons; recurso local do projeto.",
        "observacao": "A conservação de formações vegetais protege espécies adaptadas a condições ambientais específicas.",
        "zoom": True,
    },
    "hidrografia_aguas_continentais_01.svg": {
        "arquivo": "geo/imagens/hidrografia/rio_amazonas.jpg",
        "externa": False,
        "alt": "Fotografia aérea do Rio Amazonas próximo a Manaus.",
        "fonte": "Wikimedia Commons; foto Rio Amazonas 02.JPG, autora GabiFMesquita, CC BY-SA 3.0.",
        "observacao": "Grandes rios fazem parte das águas continentais e organizam paisagens e usos humanos.",
        "zoom": True,
    },
    "hidrografia_usos_agua_01.svg": {
        "arquivo": "geo/imagens/hidrografia/mapa_bacia_amazonica.png",
        "externa": False,
        "alt": "Mapa da região hidrográfica Amazônica no Brasil.",
        "fonte": "Wikimedia Commons; mapa Regiões Hidrográficas do Brasil - Amazônica.",
        "observacao": "Mapas hidrográficos ajudam a localizar rios, bacias e áreas importantes para uso da água.",
        "zoom": True,
    },
    "hidrografia_problemas_poluicao_01.svg": {
        "arquivo": "geo/imagens/clima/chuva_caatinga.jpg",
        "externa": False,
        "alt": "Chuva em área de Caatinga, mostrando a importância da água na paisagem.",
        "fonte": "Wikimedia Commons; arquivo Rain in the Caatinga.",
        "observacao": "Problemas hídricos devem ser analisados observando disponibilidade de água, chuva, rios e uso humano.",
        "zoom": True,
    },
    "populacao_crescimento_curva_01.svg": {
        "arquivo": "geo/imagens/populacao/mapa_densidade_brasil.png",
        "externa": False,
        "alt": "Mapa dos estados brasileiros por densidade populacional.",
        "fonte": "Wikimedia Commons; mapa Brazilian States by Population Density.",
        "observacao": "Mapas populacionais ajudam a comparar concentração e distribuição da população.",
        "zoom": True,
    },
    "populacao_crescimento_transicao_01.svg": {
        "arquivo": "geo/imagens/populacao/piramide_etaria_brasil.png",
        "externa": False,
        "alt": "Pirâmide etária do Brasil em 2020.",
        "fonte": "Wikimedia Commons; arquivo Brazil single age population pyramid 2020.",
        "observacao": "A estrutura etária ajuda a interpretar mudanças demográficas e crescimento populacional.",
        "zoom": True,
    },
    "populacao_brasileira_diversidade_01.svg": {
        "arquivo": "geo/imagens/catalogo/relevo_montanha.jpg",
        "externa": False,
        "alt": "Paisagem brasileira de área montanhosa, usada para relacionar população e diversidade territorial.",
        "fonte": "Wikimedia Commons; recurso local do projeto.",
        "observacao": "A população brasileira vive em paisagens diversas, com diferenças regionais de ocupação e acesso a serviços.",
        "zoom": True,
    },
    "populacao_indicadores_saneamento_01.svg": {
        "arquivo": "geo/imagens/catalogo/clima_termometro.jpg",
        "externa": False,
        "alt": "Instrumentos de medição usados como referência visual para comparação de indicadores.",
        "fonte": "Wikimedia Commons; recurso local do projeto.",
        "observacao": "Indicadores sociais também são medidas padronizadas: permitem comparar renda, saúde, escolaridade e saneamento.",
        "zoom": True,
    },
    "urbanizacao_conceito_servicos_01.svg": {
        "arquivo": "geo/imagens/populacao/urbanizacao_sao_paulo.jpg",
        "externa": False,
        "alt": "Vista do centro de São Paulo com grande concentração de edifícios e serviços urbanos.",
        "fonte": "Wikimedia Commons; foto Skyline of São Paulo centre.jpg, autor Rodrigo.Argenton, CC BY-SA 4.0.",
        "observacao": "A concentração de edifícios e serviços ajuda a entender a urbanização como crescimento e intensificação do espaço urbano.",
        "zoom": True,
    },
    "urbanizacao_rede_fluxos_01.svg": {
        "arquivo": "geo/imagens/aulas_reais/urbanizacao_planejamento_mobilidade_01.png",
        "externa": False,
        "alt": "Imagem real de área urbana usada para observar conexões, circulação e centralidade regional.",
        "fonte": "Wikimedia Commons; imagem Copernicus Sentinel-2; recurso local do projeto.",
        "observacao": "Compare a mancha urbana e as conexões visíveis para pensar em fluxos entre cidades e regiões.",
        "zoom": True,
    },
    "urbanizacao_metropolizacao_verticalizacao_01.svg": {
        "arquivo": "geo/imagens/aulas_reais/urbanizacao_conceito_servicos_01.png",
        "externa": False,
        "alt": "Imagem real de área urbana densa, usada para diferenciar metropolização de outras formas urbanas.",
        "fonte": "Wikimedia Commons; imagem Copernicus Sentinel-2; recurso local do projeto.",
        "observacao": "A imagem ajuda a comparar manchas urbanas densas e integradas, sem repetir a mesma vista da aula.",
        "zoom": True,
    },
    "urbanizacao_problemas_moradia_saneamento_01.svg": {
        "arquivo": "geo/imagens/aulas_reais/urbanizacao_rede_fluxos_01.png",
        "externa": False,
        "alt": "Imagem real de área urbana usada para discutir ocupação, infraestrutura e desigualdade espacial.",
        "fonte": "Wikimedia Commons; imagem Copernicus Sentinel-2; recurso local do projeto.",
        "observacao": "Observe a forma da ocupação urbana e relacione com infraestrutura, drenagem e acesso a serviços.",
        "zoom": True,
    },
    "urbanizacao_planejamento_mobilidade_01.svg": {
        "arquivo": "geo/imagens/aulas_reais/urbanizacao_metropolizacao_verticalizacao_01.png",
        "externa": False,
        "alt": "Imagem real de área urbana usada para discutir planejamento, densidade e mobilidade.",
        "fonte": "Wikimedia Commons; imagem Copernicus Sentinel-2; recurso local do projeto.",
        "observacao": "O planejamento urbano depende da leitura da densidade, das conexões e das áreas mais intensamente ocupadas.",
        "zoom": True,
    },
}


def imagem_local_aula(tema, numero, visual):
    arquivo, tipo, alt, observacao = visual
    substituicao = SUBSTITUICOES_LOCAIS_VISUAIS.get(arquivo)
    if substituicao:
        return substituicao
    imagem_real_baixada = IMAGENS_AULAS_REAIS.get(arquivo)
    if imagem_real_baixada:
        return imagem_real_baixada
    complemento = COMPLEMENTOS_REAIS_AULAS.get(arquivo)
    if complemento:
        return complemento
    return {
        "arquivo": "",
        "externa": False,
        "alt": alt,
        "fonte": "",
        "observacao": observacao,
        "zoom": False,
    }


def aplicar_imagens_locais_aulas_alvo(temas):
    for tema in temas.values():
        if tema["titulo"] not in TEMAS_ALVO_IMAGENS_LOCAIS:
            continue
        for aula in tema["aulas"]:
            visuais = VISUAIS_LOCAIS_AULAS.get((tema["titulo"], aula["numero"]))
            if not visuais:
                continue
            aplicar_imagem_direta(aula, imagem_local_aula(tema["titulo"], aula["numero"], visuais[0]))
            secoes = aula.get("secoes", [])
            if secoes and len(visuais) > 1:
                aplicar_imagem_direta(secoes[0], imagem_local_aula(tema["titulo"], aula["numero"], visuais[1]))
            if len(secoes) > 1 and len(visuais) > 2:
                aplicar_imagem_direta(secoes[1], imagem_local_aula(tema["titulo"], aula["numero"], visuais[2]))
            for indice, secao in enumerate(secoes):
                if indice >= 1 and secao.get("imagem"):
                    limpar_imagem_artificial(secao)
            aula["imagem_interativa"] = None
    return temas


FALLBACKS_LOCAIS_IMAGEM = [
    "geo/imagens/aulas_reais/clima_brasileiros_climograma_01.png",
    "geo/imagens/aulas_reais/clima_cotidiano_agricultura_01.jpg",
    "geo/imagens/aulas_reais/clima_elementos_estacao_01.jpg",
    "geo/imagens/aulas_reais/clima_elementos_precipitacao_vento_01.jpg",
    "geo/imagens/aulas_reais/clima_fatores_latitude_altitude_01.jpg",
    "geo/imagens/aulas_reais/clima_frente_fria_01.jpg",
    "geo/imagens/aulas_reais/clima_mudancas_ilha_calor_01.jpg",
    "geo/imagens/aulas_reais/clima_tempo_clima_previsao_01.jpg",
    "geo/imagens/aulas_reais/globalizacao_conceito_produto_01.jpg",
    "geo/imagens/aulas_reais/hidrografia_aquifero_nascente_01.jpg",
    "geo/imagens/aulas_reais/hidrografia_bacia_mapa_01.jpg",
    "geo/imagens/aulas_reais/hidrografia_bacia_rede_01.jpg",
    "geo/imagens/aulas_reais/hidrografia_hidreletrica_irrigacao_01.jpg",
    "geo/imagens/aulas_reais/hidrografia_problemas_escassez_enchente_01.jpg",
    "geo/imagens/aulas_reais/migracoes_causas_emprego_estudo_01.jpg",
    "geo/imagens/aulas_reais/migracoes_tipos_fluxos_01.jpg",
    "geo/imagens/aulas_reais/migracoes_tipos_fronteira_01.png",
    "geo/imagens/aulas_reais/populacao_conceitos_densidade_01.jpg",
    "geo/imagens/aulas_reais/populacao_distribuicao_litoral_interior_01.jpg",
    "geo/imagens/aulas_reais/populacao_distribuicao_rural_urbano_01.jpg",
    "geo/imagens/aulas_reais/populacao_estrutura_envelhecimento_01.jpg",
    "geo/imagens/aulas_reais/populacao_estrutura_piramide_01.png",
    "geo/imagens/aulas_reais/populacao_indicadores_idh_01.png",
    "geo/imagens/aulas_reais/relevo_agentes_externos_erosao_01.jpg",
    "geo/imagens/aulas_reais/relevo_agentes_externos_sedimentacao_01.jpg",
    "geo/imagens/aulas_reais/relevo_agentes_internos_placas_01.png",
    "geo/imagens/aulas_reais/relevo_agentes_internos_vulcanismo_01.jpg",
    "geo/imagens/aulas_reais/relevo_brasileiro_planalto_planicie_01.jpg",
    "geo/imagens/aulas_reais/relevo_formas_perfil_topografico_01.png",
    "geo/imagens/aulas_reais/relevo_formas_planalto_planicie_01.jpg",
    "geo/imagens/aulas_reais/relevo_riscos_deslizamento_01.jpg",
    "geo/imagens/aulas_reais/relevo_riscos_enchente_vale_01.jpg",
    "geo/imagens/aulas_reais/relevo_sociedade_estradas_01.jpg",
    "geo/imagens/aulas_reais/urbanizacao_conceito_expansao_01.png",
    "geo/imagens/aulas_reais/urbanizacao_conceito_servicos_01.png",
    "geo/imagens/aulas_reais/urbanizacao_metropolizacao_conurbacao_01.png",
    "geo/imagens/aulas_reais/urbanizacao_metropolizacao_verticalizacao_01.png",
    "geo/imagens/aulas_reais/urbanizacao_planejamento_mobilidade_01.png",
    "geo/imagens/aulas_reais/urbanizacao_planejamento_zoneamento_01.png",
    "geo/imagens/aulas_reais/urbanizacao_problemas_enchentes_01.jpg",
    "geo/imagens/aulas_reais/urbanizacao_rede_fluxos_01.png",
    "geo/imagens/aulas_reais/urbanizacao_rede_hierarquia_01.png",
    "geo/imagens/aulas_reais/urbanizacao_sustentavel_areas_verdes_01.png",
    "geo/imagens/aulas_reais/urbanizacao_sustentavel_drenagem_01.png",
    "geo/imagens/aulas_reais/vegetacao_biomas_brasil_01.jpg",
    "geo/imagens/aulas_reais/vegetacao_biomas_comparacao_01.png",
    "geo/imagens/aulas_reais/vegetacao_clima_caatinga_01.jpg",
    "geo/imagens/aulas_reais/vegetacao_estratos_01.jpg",
    "geo/imagens/aulas_reais/vegetacao_impactos_desmatamento_01.jpg",
    "geo/imagens/populacao/urbanizacao_sao_paulo.jpg",
    "geo/imagens/catalogo/clima_paisagem.jpg",
    "geo/imagens/vegetacao/pantanal.jpg",
    "geo/imagens/vegetacao/cerrado.jpg",
    "geo/imagens/catalogo/vegetacao_caatinga.jpg",
    "geo/imagens/hidrografia/rio_amazonas.jpg",
    "geo/imagens/hidrografia/mapa_bacia_amazonica.png",
    "geo/imagens/clima/chuva_caatinga.jpg",
    "geo/imagens/populacao/mapa_densidade_brasil.png",
    "geo/imagens/populacao/piramide_etaria_brasil.png",
    "geo/imagens/catalogo/relevo_montanha.jpg",
    "geo/imagens/catalogo/clima_termometro.jpg",
]


def aplicar_fallbacks_locais(temas):
    indice = 0
    for tema in temas.values():
        for aula in tema["aulas"]:
            campos = [aula]
            campos.extend(aula.get("secoes", []))
            for campo in campos:
                if not campo.get("imagem"):
                    continue
                if campo.get("imagem_externa") or campo["imagem"].startswith("http"):
                    campo["imagem_fallback"] = FALLBACKS_LOCAIS_IMAGEM[indice % len(FALLBACKS_LOCAIS_IMAGEM)]
                    indice += 1
    return temas


def aula_elementos_clima():
    imagem_clima = imagem_real("clima_paisagem")
    return {
        "numero": 2,
        "titulo": "Elementos do clima",
        "pergunta_abertura": "Quais características da atmosfera ajudam a entender o clima?",
        "objetivo": "Reconhecer temperatura, umidade, pressão atmosférica, precipitação e ventos como elementos do clima.",
        "imagem": imagem_clima["arquivo"],
        "imagem_externa": imagem_clima["externa"],
        "imagem_alt": imagem_clima["alt"],
        "imagem_fonte": imagem_clima["fonte"],
        "imagem_observacao": imagem_clima["observacao"],
        "imagem_zoom": imagem_clima["zoom"],
        "introducao": [
            "Para entender o clima de um lugar, os pesquisadores observam diferentes características da atmosfera. Essas características são chamadas de elementos do clima.",
            "Elas aparecem em previsões do tempo, mapas climáticos, gráficos de chuva e dados de estações meteorológicas. Juntas, ajudam a explicar por que um lugar é quente, úmido, seco, chuvoso ou sujeito a ventos fortes.",
        ],
        "secoes": [
            aplicar_imagem({
                "titulo": "Temperatura",
                "textos": [
                    "Temperatura indica o quanto o ar está quente ou frio. Ela varia ao longo do dia, entre estações do ano e entre lugares com diferentes altitudes e latitudes.",
                    "Quando uma cidade registra 32°C à tarde, estamos olhando uma informação momentânea. Para falar de clima, é preciso observar muitas medições ao longo de vários anos.",
                ],
                "layout": "normal",
            }, "clima_termometro"),
            aplicar_imagem({
                "titulo": "Umidade",
                "textos": [
                    "Umidade é a quantidade de vapor de água presente no ar. Em dias muito úmidos, o suor evapora com mais dificuldade e a sensação de abafamento aumenta.",
                    "Em áreas próximas ao mar ou a grandes florestas, a umidade costuma ser maior. Em períodos secos, pode haver irritação nos olhos, garganta seca e maior risco de queimadas.",
                ],
                "layout": "invertida",
            }, "clima_umidade_neblina"),
            aplicar_imagem({
                "titulo": "Pressão atmosférica",
                "textos": [
                    "Pressão atmosférica é a força exercida pelo ar sobre a superfície. Não precisamos usar linguagem complicada: pense no ar como uma camada que tem peso e se movimenta.",
                    "Diferenças de pressão ajudam a formar ventos. O ar tende a se deslocar de áreas de maior pressão para áreas de menor pressão.",
                ],
                "layout": "normal",
            }, "clima_barometro"),
            aplicar_imagem({
                "titulo": "Precipitação",
                "textos": [
                    "Precipitação é a água que cai da atmosfera. A forma mais comum é a chuva, mas também pode ocorrer como neve ou granizo em determinadas condições.",
                    "A quantidade e a distribuição das chuvas influenciam agricultura, abastecimento de água, risco de enchentes e períodos de seca.",
                ],
                "layout": "invertida",
            }, "clima_chuva_forte"),
            aplicar_imagem({
                "titulo": "Ventos",
                "textos": [
                    "Ventos são movimentos do ar. Eles transportam calor, umidade e massas de ar, podendo mudar a sensação térmica e trazer chuva ou ar seco.",
                    "Quando uma frente fria avança, por exemplo, os ventos ajudam a deslocar uma massa de ar e alteram as condições do tempo em várias regiões.",
                ],
                "layout": "normal",
            }, "clima_vento_arvores"),
        ],
        "comparacao": {
            "titulo": "Vamos observar juntos",
            "itens": [
                {"titulo": "Salvador", "icone": "29°C", "pontos": ["umidade: 78%", "chuva prevista", "vento fraco no litoral"]},
                {"titulo": "Elementos vistos", "icone": "✓", "pontos": ["temperatura", "umidade", "precipitação", "vento"]},
            ],
        },
        "destaques": [
            {"tipo": "Observe", "texto": "Uma previsão do tempo normalmente combina vários elementos: temperatura, umidade, chuva, vento e pressão."},
            {"tipo": "Preste atenção", "texto": "Um dado isolado descreve o tempo. Uma sequência longa de dados ajuda a caracterizar o clima."},
        ],
        "pergunta_rapida": pergunta_da_aula("Elementos do clima"),
        "revelar": {
            "titulo": "Quer entender melhor?",
            "botao": "Mostrar explicação",
            "texto": "Imagine uma ficha de observação: temperatura mostra calor ou frio; umidade mostra vapor de água; pressão ajuda a explicar deslocamentos do ar; precipitação mostra a água que cai; ventos mostram o ar em movimento.",
        },
        "imagem_interativa": imagem_interativa_da_aula("Clima", 2),
        "curiosidade": "Estações meteorológicas registram dados em horários padronizados. Isso permite comparar lugares diferentes e acompanhar mudanças ao longo do tempo.",
        "resumo": [
            "Elementos do clima são características observáveis da atmosfera.",
            "Temperatura indica calor ou frio do ar.",
            "Umidade é a quantidade de vapor de água presente no ar.",
            "Pressão atmosférica ajuda a explicar movimentos do ar.",
            "Precipitação inclui chuva, neve e granizo.",
            "Ventos transportam calor, umidade e massas de ar.",
        ],
        "atividade": "Leia uma previsão do tempo de sua cidade. Identifique temperatura, umidade, chance de chuva e vento. Depois escreva quais elementos do clima aparecem nessa previsão.",
    }


def construir_temas():
    temas = {}
    for slug, tema in TEMAS_BASE.items():
        aulas = []
        for indice, aula in enumerate(tema["aulas"], start=1):
            if slug == "clima" and indice == 2:
                aulas.append(aula_elementos_clima())
            else:
                aulas.append(montar_aula(tema["titulo"], indice, aula[0], aula[1], aula[2]))
        temas[slug] = {
            "slug": slug,
            "titulo": tema["titulo"],
            "ano": tema["ano"],
            "descricao": tema["descricao"],
            "aulas": aulas,
        }
    return temas


TEMAS = aplicar_fallbacks_locais(aplicar_imagens_locais_aulas_alvo(preencher_imagens_minimas(
    revisar_anos_2_3(deduplicar_imagens_aulas(reduzir_blocos_repetidos(construir_temas())))
)))

PERGUNTAS_ESPECIFICAS = {
    "clima": [
        ("O que diferencia clima de tempo atmosférico?", ["Clima é padrão de muitos anos; tempo é condição momentânea.", "Clima é só chuva; tempo é relevo.", "Clima é população; tempo é economia.", "Não existe diferença."], 0, "Clima depende de séries longas; tempo descreve o momento."),
        ("Qual é um elemento climático?", ["Temperatura", "Densidade demográfica", "Fronteira política", "Produto interno bruto"], 0, "Temperatura, umidade, pressão, ventos e chuva são elementos climáticos."),
        ("Qual fator ajuda a explicar temperaturas menores em áreas elevadas?", ["Altitude", "Idioma", "Moeda", "População absoluta"], 0, "Em geral, quanto maior a altitude, menor a temperatura."),
    ],
    "relevo": [
        ("O que é relevo?", ["Conjunto das formas da superfície terrestre", "Quantidade de habitantes", "Tipo de governo", "Preço dos alimentos"], 0, "Relevo envolve montanhas, planaltos, planícies e depressões."),
        ("Qual processo externo modifica o relevo?", ["Erosão", "Eleições", "Inflação", "Migração pendular"], 0, "A erosão desgasta e transporta materiais."),
        ("Qual risco é comum em encostas ocupadas sem planejamento?", ["Deslizamento", "Maré vermelha", "Geada permanente", "Desertificação polar"], 0, "Encostas instáveis podem sofrer deslizamentos, especialmente com chuvas fortes."),
    ],
    "populacao": [
        ("O que é densidade demográfica?", ["Habitantes por área", "Número de rios", "Altura média do relevo", "Total de indústrias"], 0, "Ela relaciona população e área ocupada."),
        ("O que uma pirâmide etária mostra?", ["Distribuição por idade e sexo", "Tipos de solo", "Rotas de comércio", "Tipos de clima"], 0, "Pirâmides etárias mostram estrutura da população."),
        ("Qual fator pode atrair população?", ["Empregos e serviços", "Ausência de água", "Isolamento total", "Solo improdutivo"], 0, "Trabalho, serviços e infraestrutura atraem moradores."),
    ],
    "urbanizacao": [
        ("O que é urbanização?", ["Crescimento da população urbana e das cidades", "Formação de rochas", "Apenas agricultura", "Movimento das marés"], 0, "Urbanização envolve crescimento e transformação das cidades."),
        ("Qual é um problema urbano frequente?", ["Falta de moradia adequada", "Latitude", "Tectonismo", "Monções"], 0, "Moradia, trânsito, enchentes e saneamento são desafios urbanos."),
        ("O que é conurbação?", ["União física de áreas urbanas próximas", "Separação de rios", "Formação de desertos", "Divisão de placas"], 0, "Conurbação ocorre quando manchas urbanas se encontram."),
    ],
    "globalizacao": [
        ("O que é globalização?", ["Aumento das conexões entre lugares do mundo", "Apenas formação de montanhas", "Somente clima local", "Isolamento econômico"], 0, "Globalização envolve fluxos de capitais, mercadorias, pessoas e informações."),
        ("Qual é um fluxo global?", ["Circulação internacional de informações", "Erosão de uma encosta", "Nascer do sol", "Formação do solo"], 0, "Informações cruzam fronteiras rapidamente em redes globais."),
        ("O que são empresas transnacionais?", ["Empresas que atuam em vários países", "Rios com muitos afluentes", "Tipos de vegetação", "Mapas antigos"], 0, "Elas organizam produção, venda e serviços em escala mundial."),
    ],
    "geopolitica": [
        ("O que a geopolítica estuda?", ["Poder, território e recursos", "Somente tipos de nuvens", "Apenas gramática", "Receitas culinárias"], 0, "A geopolítica analisa relações de poder no espaço."),
        ("Qual recurso pode ser estratégico?", ["Petróleo", "Cor da parede", "Número da carteira", "Formato da letra"], 0, "Energia, água, minérios e tecnologia podem ter valor estratégico."),
        ("O que é soberania?", ["Capacidade de um Estado exercer autoridade em seu território", "Tipo de solo", "Linha de ônibus", "Mapa sem legenda"], 0, "Soberania está ligada ao poder político sobre um território."),
    ],
}


def perguntas_genericas(slug, tema):
    aulas = tema["aulas"]
    perguntas = []
    for indice, aula in enumerate(aulas[:5]):
        alternativas = [
            aula["objetivo"],
            "Ignorar mapas e dados geográficos.",
            "Estudar apenas nomes sem relação com o espaço.",
            "Substituir explicações por respostas decoradas.",
        ]
        explicacao = (
            aula["revelar"]["texto"]
            if aula.get("revelar")
            else aula["pergunta_rapida"]["explicacao"]
        )
        perguntas.append({
            "pergunta": f"Qual ideia aparece na aula '{aula['titulo']}'?",
            "alternativas": alternativas_com_correta(alternativas, 0, f"{slug}|generica|{indice}|{aula['titulo']}"),
            "explicacao": explicacao,
        })
    alternativas_estudo = [
        "Relacionar conceito, exemplo e localização.",
        "Não observar mapas ou imagens.",
        "Ler somente palavras isoladas.",
        "Evitar comparar lugares.",
    ]
    perguntas.append({
        "pergunta": f"Qual atitude ajuda a estudar {tema['titulo']}?",
        "alternativas": alternativas_com_correta(alternativas_estudo, 0, f"{slug}|atitude|{tema['titulo']}"),
        "explicacao": "Geografia combina conceitos, exemplos, mapas, dados e comparação entre lugares.",
    })
    alternativas_importancia = [
        "Porque ajuda a interpretar paisagens e relações sociais.",
        "Porque elimina a necessidade de observar o mundo.",
        "Porque não tem relação com o cotidiano.",
        "Porque serve apenas para memorizar listas.",
    ]
    perguntas.append({
        "pergunta": f"Por que {tema['titulo']} é importante?",
        "alternativas": alternativas_com_correta(alternativas_importancia, 0, f"{slug}|importancia|{tema['titulo']}"),
        "explicacao": "O conteúdo geográfico ajuda a entender problemas reais e decisões da sociedade.",
    })
    return perguntas


def construir_perguntas():
    perguntas_por_tema = {}
    for slug, tema in TEMAS.items():
        perguntas = []
        for indice, (pergunta, alternativas, correta, explicacao) in enumerate(PERGUNTAS_ESPECIFICAS.get(slug, [])):
            perguntas.append({
                "pergunta": pergunta,
                "alternativas": alternativas_com_correta(alternativas, correta, f"{slug}|especifica|{indice}|{pergunta}"),
                "explicacao": explicacao,
            })
        perguntas.extend(perguntas_genericas(slug, tema))
        limite = 10 if slug in {"clima", "relevo", "populacao", "urbanizacao", "globalizacao", "geopolitica"} else 6
        perguntas_por_tema[slug] = perguntas[:limite]
    return perguntas_por_tema


PERGUNTAS = construir_perguntas()

ATIVIDADES = {
    slug: {
        "verdadeiro_falso": [
            {
                "texto": f"{tema['titulo']} pode ser estudado com mapas, dados e exemplos reais.",
                "resposta": True,
                "explicacao": "Mapas e dados ajudam a localizar e interpretar fenômenos geográficos.",
            },
            {
                "texto": f"{tema['titulo']} não tem relação com a sociedade.",
                "resposta": False,
                "explicacao": "Todo tema geográfico se relaciona com natureza, sociedade ou organização do espaço.",
            },
        ],
        "associacao": [
            ("Conceito", "Ideia principal estudada na aula"),
            ("Exemplo", "Situação real que ajuda a compreender o conteúdo"),
            ("Mapa", "Representação espacial usada para localizar fenômenos"),
        ],
        "flashcards": [
            ("Pergunta-guia", "Onde acontece? Por que acontece? Quais consequências aparecem?"),
            ("Boa leitura geográfica", "Comparar lugares, observar escalas e usar evidências."),
            (tema["titulo"], tema["descricao"]),
        ],
        "mapa": {
            "titulo": f"Atividade com imagem: {tema['titulo']}",
            "orientacao": "Observe a imagem do mapa do Brasil. Escolha um estado ou região e escreva como o tema estudado pode aparecer nesse lugar.",
        },
    }
    for slug, tema in TEMAS.items()
}


def temas_por_ano(ano):
    return [tema for tema in TEMAS.values() if tema["ano"] == ano]


def todos_os_temas():
    return list(TEMAS.values())


def resumo_temas_para_navegador():
    return [
        {
            "slug": tema["slug"],
            "titulo": tema["titulo"],
            "ano": tema["ano"],
            "aulas": [
                {"numero": aula["numero"], "titulo": aula["titulo"]}
                for aula in tema["aulas"]
            ],
        }
        for tema in TEMAS.values()
    ]
