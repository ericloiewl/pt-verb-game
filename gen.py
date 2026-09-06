import json

# ======================== 动词列表（词干） ========================
verbs = {
    # -AR
    "andar": "and", "cantar": "cant", "dançar": "danç", "estudar": "estud",
    "falar": "fal", "trabalhar": "trabalh", "olhar": "olh", "escutar": "escut",
    "pagar": "pag", "levar": "lev", "chegar": "cheg", "entrar": "entr",
    "ficar": "fic", "pensar": "pens", "esperar": "esper", "comprar": "compr",
    "visitar": "visit", "telefonar": "telefon", "jantar": "jant", "almoçar": "almoç",
    "caminhar": "caminh", "parar": "par", "começar": "começ", "tocar": "toc",
    "brincar": "brinc", "namorar": "namor", "morar": "mor", "usar": "us",
    "lavar": "lav", "secar": "sec", "pintar": "pint", "cozinhar": "cozinh",
    # -ER
    "comer": "com", "beber": "beb", "correr": "corr", "vender": "vend",
    "aprender": "aprend", "responder": "respond", "prometer": "promet",
    "sofrer": "sof", "dever": "dev",
    # -IR
    "abrir": "abr", "assistir": "assist", "decidir": "decid", "partir": "part",
    "dividir": "divid", "permitir": "permit", "cobrir": "cobr", "subir": "sub",
    "desistir": "desist",
}

def verb_type(infinitive):
    if infinitive.endswith("ar"):
        return "ar"
    elif infinitive.endswith("er"):
        return "er"
    else:
        return "ir"

# ======================== 变位生成器 ========================
def get_conjugations(stem, vtype, tense):
    if tense == "presente":
        if vtype == "ar":
            return {"eu": stem+"o", "tu": stem+"as", "ele/ela/você": stem+"a",
                    "nós": stem+"amos", "eles/elas/vocês": stem+"am"}
        elif vtype == "er":
            return {"eu": stem+"o", "tu": stem+"es", "ele/ela/você": stem+"e",
                    "nós": stem+"emos", "eles/elas/vocês": stem+"em"}
        else:
            return {"eu": stem+"o", "tu": stem+"es", "ele/ela/você": stem+"e",
                    "nós": stem+"imos", "eles/elas/vocês": stem+"em"}

    elif tense == "preterito_perfeito":
        if vtype == "ar":
            return {"eu": stem+"ei", "tu": stem+"aste", "ele/ela/você": stem+"ou",
                    "nós": stem+"ámos", "eles/elas/vocês": stem+"aram"}
        elif vtype == "er":
            return {"eu": stem+"i", "tu": stem+"este", "ele/ela/você": stem+"eu",
                    "nós": stem+"emos", "eles/elas/vocês": stem+"eram"}
        else:
            return {"eu": stem+"i", "tu": stem+"iste", "ele/ela/você": stem+"iu",
                    "nós": stem+"imos", "eles/elas/vocês": stem+"iram"}

    elif tense == "preterito_imperfeito":
        if vtype == "ar":
            return {"eu": stem+"ava", "tu": stem+"avas", "ele/ela/você": stem+"ava",
                    "nós": stem+"ávamos", "eles/elas/vocês": stem+"avam"}
        elif vtype == "er":
            return {"eu": stem+"ia", "tu": stem+"ias", "ele/ela/você": stem+"ia",
                    "nós": stem+"íamos", "eles/elas/vocês": stem+"iam"}
        else:
            return {"eu": stem+"ia", "tu": stem+"ias", "ele/ela/você": stem+"ia",
                    "nós": stem+"íamos", "eles/elas/vocês": stem+"iam"}

    elif tense == "futuro_presente":
        if vtype == "ar":
            return {"eu": stem+"arei", "tu": stem+"arás", "ele/ela/você": stem+"ará",
                    "nós": stem+"aremos", "eles/elas/vocês": stem+"arão"}
        elif vtype == "er":
            return {"eu": stem+"erei", "tu": stem+"erás", "ele/ela/você": stem+"erá",
                    "nós": stem+"eremos", "eles/elas/vocês": stem+"erão"}
        else:
            return {"eu": stem+"irei", "tu": stem+"irás", "ele/ela/você": stem+"irá",
                    "nós": stem+"iremos", "eles/elas/vocês": stem+"irão"}

    elif tense == "condicional":
        if vtype == "ar":
            return {"eu": stem+"aria", "tu": stem+"arias", "ele/ela/você": stem+"aria",
                    "nós": stem+"aríamos", "eles/elas/vocês": stem+"ariam"}
        elif vtype == "er":
            return {"eu": stem+"eria", "tu": stem+"erias", "ele/ela/você": stem+"eria",
                    "nós": stem+"eríamos", "eles/elas/vocês": stem+"eriam"}
        else:
            return {"eu": stem+"iria", "tu": stem+"irias", "ele/ela/você": stem+"iria",
                    "nós": stem+"iríamos", "eles/elas/vocês": stem+"iriam"}

    elif tense == "presente_subjuntivo":
        if vtype == "ar":
            return {"eu": stem+"e", "tu": stem+"es", "ele/ela/você": stem+"e",
                    "nós": stem+"emos", "eles/elas/vocês": stem+"em"}
        else:
            return {"eu": stem+"a", "tu": stem+"as", "ele/ela/você": stem+"a",
                    "nós": stem+"amos", "eles/elas/vocês": stem+"am"}

    elif tense == "preterito_imperfeito_subjuntivo":
        if vtype == "ar":
            return {"eu": stem+"asse", "tu": stem+"asses", "ele/ela/você": stem+"asse",
                    "nós": stem+"ássemos", "eles/elas/vocês": stem+"assem"}
        elif vtype == "er":
            return {"eu": stem+"esse", "tu": stem+"esses", "ele/ela/você": stem+"esse",
                    "nós": stem+"êssemos", "eles/elas/vocês": stem+"essem"}
        else:
            return {"eu": stem+"isse", "tu": stem+"isses", "ele/ela/você": stem+"isse",
                    "nós": stem+"íssemos", "eles/elas/vocês": stem+"issem"}

    elif tense == "imperativo_afirmativo":
        if vtype == "ar":
            return {"tu": stem+"a", "ele/ela/você": stem+"e",
                    "nós": stem+"emos", "eles/elas/vocês": stem+"em"}
        elif vtype == "er":
            return {"tu": stem+"e", "ele/ela/você": stem+"a",
                    "nós": stem+"amos", "eles/elas/vocês": stem+"am"}
        else:
            return {"tu": stem+"e", "ele/ela/você": stem+"a",
                    "nós": stem+"amos", "eles/elas/vocês": stem+"am"}
    return {}

# ======================== 后缀定义 ========================
default_suffixes = {
    "presente": ["todos os dias.", "agora.", "sempre."],
    "preterito_perfeito": ["ontem.", "na semana passada.", "já."],
    "preterito_imperfeito": ["antigamente.", "quando era criança.", "sempre."],
    "futuro_presente": ["amanhã.", "na próxima semana.", "em breve."],
    "condicional": ["se tivesse tempo.", "gostaria de", "poderia."],
    "presente_subjuntivo": ["que ele", "espero que", "é importante que"],
    "preterito_imperfeito_subjuntivo": ["se eu", "caso", "talvez"],
    "imperativo_afirmativo": ["faça isso!", "vamos", "não"]
}

# 保留原 comer 和 falar 的自定义后缀（其余用默认）
custom_suffixes = {
    "comer": {
        "presente": ["uma maçã.", "pão com manteiga.", "fruta no café da manhã.", "no restaurante italiano.", "bem demais.", "muito devagar."],
        "preterito_perfeito": ["uma maçã ontem.", "tudo o que tinha no prato.", "bem na festa.", "juntos no almoço.", "a pizza inteira."]
    },
    "falar": {
        "presente": ["português.", "alto demais.", "comigo agora.", "devagar por favor.", "sobre o projeto."],
        "preterito_perfeito": ["com ela ontem.", "bem na reunião?", "ao telefone.", "sobre isso.", "durante horas."]
    }
}

# ======================== 生成完整 JSON ========================
all_tenses = [
    "presente",
    "preterito_perfeito",
    "preterito_imperfeito",
    "futuro_presente",
    "condicional",
    "presente_subjuntivo",
    "preterito_imperfeito_subjuntivo",
    "imperativo_afirmativo"
]

data = []
for infinitive, stem in verbs.items():
    vtype = verb_type(infinitive)
    tenses = {}
    for tense in all_tenses:
        conj = get_conjugations(stem, vtype, tense)
        if infinitive in custom_suffixes and tense in custom_suffixes[infinitive]:
            suffixes = custom_suffixes[infinitive][tense]
        else:
            suffixes = default_suffixes.get(tense, ["."])
        tenses[tense] = {"conjugations": conj, "suffixes": suffixes}
    data.append({"infinitive": infinitive, "tenses": tenses})

# ======================== 写入文件 ========================
with open("verbos.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 文件 verbos.json 已成功生成！")