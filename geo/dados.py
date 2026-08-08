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
    return f"geo/imagens/catalogo/{chave}{extensao}"


def usar_catalogo_local():
    for chave, imagem in IMAGENS_REAIS.items():
        if imagem.get("externa") and imagem.get("source_url"):
            imagem["arquivo"] = caminho_catalogo_local(chave, imagem)
            imagem["externa"] = False

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


def diagrama_didatico(tema, aula, secao, indice):
    titulo = f"{tema}: {aula}"
    subtitulo = secao
    cor_fundo = ["#e9f3ff", "#edf8f0", "#fff7df", "#f4ecff"][indice % 4]
    cor_linha = ["#2f6f9f", "#198754", "#9a6a00", "#6f42c1"][indice % 4]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760" role="img" aria-label="{titulo} - {subtitulo}">
<rect width="1200" height="760" fill="{cor_fundo}"/>
<path d="M80 570 C250 450 360 500 500 390 S800 250 1120 330" fill="none" stroke="{cor_linha}" stroke-width="22" stroke-linecap="round"/>
<circle cx="260" cy="260" r="82" fill="#ffffff" stroke="{cor_linha}" stroke-width="12"/>
<rect x="490" y="180" width="420" height="118" rx="8" fill="#ffffff" stroke="{cor_linha}" stroke-width="10"/>
<rect x="170" y="455" width="260" height="90" rx="8" fill="#ffffff" stroke="{cor_linha}" stroke-width="10"/>
<rect x="670" y="475" width="300" height="90" rx="8" fill="#ffffff" stroke="{cor_linha}" stroke-width="10"/>
<text x="80" y="95" font-family="Arial, sans-serif" font-size="52" font-weight="700" fill="#202428">{titulo}</text>
<text x="80" y="155" font-family="Arial, sans-serif" font-size="34" fill="#202428">{subtitulo}</text>
<text x="515" y="253" font-family="Arial, sans-serif" font-size="34" fill="#202428">conceito</text>
<text x="215" y="512" font-family="Arial, sans-serif" font-size="30" fill="#202428">lugar</text>
<text x="705" y="532" font-family="Arial, sans-serif" font-size="30" fill="#202428">consequência</text>
</svg>"""
    return {
        "arquivo": f"data:image/svg+xml;charset=UTF-8,{quote(svg)}",
        "externa": True,
        "alt": f"Diagrama didático sobre {aula}, seção {secao}.",
        "fonte": "GeoAcessível; diagrama didático elaborado especificamente para esta aula.",
        "observacao": f"Este diagrama organiza {secao.lower()} em três pistas: conceito, lugar e consequência. Use-o para relacionar a imagem ao texto da aula.",
        "zoom": False,
    }


def aplicar_diagrama_no_campo(campo, tema, aula, secao, indice):
    imagem = diagrama_didatico(tema, aula, secao, indice)
    campo["imagem"] = imagem["arquivo"]
    campo["imagem_externa"] = imagem["externa"]
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
                    aplicar_diagrama_no_campo(campo, tema["titulo"], aula["titulo"], secao, indice)
                    indice += 1
                    caminho = campo["imagem"]
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


TEMAS = deduplicar_imagens_aulas(construir_temas())

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
        perguntas.append({
            "pergunta": f"Qual ideia aparece na aula '{aula['titulo']}'?",
            "alternativas": alternativas_com_correta(alternativas, 0, f"{slug}|generica|{indice}|{aula['titulo']}"),
            "explicacao": aula["revelar"]["texto"],
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
