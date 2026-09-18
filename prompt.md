你是一位精通歐洲葡萄牙語（pt-PT）的語言學資料生成器。請根據以下規則，生成用於葡文動詞時態填空遊戲的 JSON 資料。輸出必須是純 JSON，不要有任何解釋文字、不要用 markdown code fence。

## 1. 語言變體
- 只使用歐洲葡萄牙語（pt-PT），絕對不要混入巴西葡語（pt-BR）。
- 人稱分組必須依照語法變位，固定為以下 5 組：
  - eu
  - tu
  - ele/ela/você（第三人稱單數，共用同一變位）
  - nós
  - eles/elas/vocês（第三人稱複數，共用同一變位）
- 不要拆分 você 和 ele/ela，也不要拆分 vocês 和 eles/elas。
- 不要使用 vós（現代 pt-PT 口語已罕用）。
- 語用限制放在 notes 欄位，例如：
  - tu 是 pt-PT 的標準親密稱呼。
  - você 在 pt-PT 帶有距離感，部分地區可能被視為不禮貌。
  - vocês 是複數的禮貌/通用稱呼，變位同 eles/elas。
- 使用歐式葡語詞彙，例如：
  - autocarro（不是 ônibus）
  - comboio（不是 trem）
  - casa de banho（不是 banheiro）
  - pequeno-almoço（不是 café da manhã）
  - telemóvel（不是 celular）
  - frigorífico（不是 geladeira）
  - bilhete（不是 ingresso）
- 現在進行時使用 estar a + infinitivo（例如 estou a comer），不要用 gerúndio（estou comendo）。
- nós 的過去簡單式：-ar 動詞要帶重音，例如 andámos, falámos。
- 使用 pt-PT 的縮合介系詞：ao, à, aos, às, do, da, dos, das, no, na, nos, nas, pelo, pela, pelos, pelas, num, numa。

## 2. 時態清單（只生成這 8 個，不要多也不要少）

每個時態必須帶 `type` 欄位，值只能是 `"indicative"`、`"subjunctive"` 或 `"imperative"`。

| tense_key | 顯示名稱 | type |
|---|---|---|
| presente | presente · 現在式 | indicative |
| preterito_perfeito | pretérito perfeito · 簡單過去式 | indicative |
| preterito_imperfeito | pretérito imperfeito · 過去未完成式 | indicative |
| futuro_presente | futuro do presente · 未來式 | indicative |
| condicional | condicional · 條件式 | indicative |
| presente_subjuntivo | presente do conjuntivo · 現在虛擬式 | subjunctive |
| preterito_imperfeito_subjuntivo | pretérito imperfeito do conjuntivo · 過去未完成虛擬式 | subjunctive |
| imperativo_afirmativo | imperativo afirmativo · 肯定命令式 | imperative |

注意：
- 使用 `conjuntivo` 這個拼法（pt-PT 偏好），不要用 `subjuntivo`。
- 不要生成 `imperativo_negativo`、`futuro_subjuntivo`、任何複合時態、`infinitivo_pessoal`、`gerundio`、`participio` 作為獨立時態。
- 若某個動詞在某時態不適用（例如無人稱動詞沒有命令式），在該動詞的 notes 說明並省略該時態。

## 3. 每個時態的時間副詞
為每個時態提供 3-5 個自然搭配的時間副詞或句型開頭：

- presente: agora, todos os dias, normalmente, geralmente, às vezes
- preterito_perfeito: ontem, na semana passada, há dois dias, no ano passado, já
- preterito_imperfeito: antigamente, quando era criança, naquela época, sempre, todos os dias
- futuro_presente: amanhã, na próxima semana, no futuro, depois, em breve
- condicional: se tivesse tempo, se pudesse, naquela situação, gostaria de
- presente_subjuntivo: espero que, é importante que, talvez, duvido que
- preterito_imperfeito_subjuntivo: se eu, caso, talvez, como se
- imperativo_afirmativo: （通常不用時間副詞，留空陣列 []）

## 4. 動詞資料欄位
為每個動詞提供以下欄位：

{
  "infinitive": "原形",
  "translation_zh": "中文翻譯",
  "translation_en": "英文翻譯",
  "type": "regular 或 irregular",
  "group": "-ar, -er, -ir, 或 irregular",
  "transitivity": "transitive, intransitive, transitive_indirect, copular, reflexive 等",
  "reflexive": true 或 false,
  "preposition": "de, a, para, em, com 等，若不需要則為 null",
  "participle": {
    "regular": "規則分詞",
    "irregular": "不規則分詞或 null",
    "double": "若有不規則和規則雙分詞，列出兩個，否則 null"
  },
  "gerund": "gerúndio 形式",
  "objects": ["3-5 個自然搭配的賓語或補語，使用 pt-PT，包含必要的冠詞和縮合介系詞"],
  "sentence_template": "{time_marker} {subject} {verb} {object}.",
  "notes": "任何語用、地區、變位不規則的說明，若無則 null",
  "tenses": {
    "presente": {
      "name": "presente · 現在式",
      "type": "indicative",
      "conjugations": {
        "eu": "...",
        "tu": "...",
        "ele/ela/você": "...",
        "nós": "...",
        "eles/elas/vocês": "..."
      },
      "time_markers": ["...", "..."],
      "special_templates": []
    },
    "preterito_perfeito": {
      "name": "pretérito perfeito · 簡單過去式",
      "type": "indicative",
      "conjugations": { ... },
      "time_markers": [ ... ],
      "special_templates": []
    },
    "preterito_imperfeito": {
      "name": "pretérito imperfeito · 過去未完成式",
      "type": "indicative",
      "conjugations": { ... },
      "time_markers": [ ... ],
      "special_templates": []
    },
    "futuro_presente": {
      "name": "futuro do presente · 未來式",
      "type": "indicative",
      "conjugations": { ... },
      "time_markers": [ ... ],
      "special_templates": []
    },
    "condicional": {
      "name": "condicional · 條件式",
      "type": "indicative",
      "conjugations": { ... },
      "time_markers": [ ... ],
      "special_templates": []
    },
    "presente_subjuntivo": {
      "name": "presente do conjuntivo · 現在虛擬式",
      "type": "subjunctive",
      "conjugations": { ... },
      "time_markers": [ ... ],
      "special_templates": [ ... ]
    },
    "preterito_imperfeito_subjuntivo": {
      "name": "pretérito imperfeito do conjuntivo · 過去未完成虛擬式",
      "type": "subjunctive",
      "conjugations": { ... },
      "time_markers": [ ... ],
      "special_templates": [ ... ]
    },
    "imperativo_afirmativo": {
      "name": "imperativo afirmativo · 肯定命令式",
      "type": "imperative",
      "conjugations": {
        "tu": "...",
        "ele/ela/você": "...",
        "nós": "...",
        "eles/elas/vocês": "..."
      },
      "time_markers": [],
      "special_templates": [ ... ]
    }
  }
}

## 5. 時態類型與模板規則

### 5.1 indicative（presente、preterito_perfeito、preterito_imperfeito、futuro_presente、condicional）
- 使用動詞層級的 `sentence_template`。
- `special_templates` 留空陣列 `[]`。
- 五個人稱全部都有：eu, tu, ele/ela/você, nós, eles/elas/vocês。

### 5.2 subjunctive（presente_subjuntivo、preterito_imperfeito_subjuntivo）
- `special_templates` 必須非空。
- `presente_subjuntivo` 範例：
  - "Espero que {subject} {verb} {object}."
  - "É importante que {subject} {verb} {object}."
  - "Talvez {subject} {verb} {object}."
- `preterito_imperfeito_subjuntivo` 範例：
  - "Se {subject} {verb} {object}, ..."
  - "Caso {subject} {verb} {object}, ..."
  - "Como se {subject} {verb} {object}."
- 五個人稱全部都有：eu, tu, ele/ela/você, nós, eles/elas/vocês。

### 5.3 imperative（imperativo_afirmativo）
- `special_templates` 必須非空。
- 範例：
  - "{verb} {object}!"
  - "Por favor, {verb} {object}!"
- 只有四個人稱：tu, ele/ela/você, nós, eles/elas/vocês。
- 絕對不能有 eu。

### 5.4 通用規則
- `special_templates` 中的 `{verb}` 會由變位取代，`{subject}` 由主語取代，`{object}` 由賓語取代。
- `{subject}` 在程式中被替換時，會根據變位鍵顯示自然的主語（例如 `ele/ela/você` 可能顯示 `Ele`、`Ela` 或 `Você`）。資料端只需提供正確的變位鍵。

## 6. 反身動詞規則
- 若 `reflexive` 為 true，`sentence_template` 需包含反身代詞的位置，例如：
  - "{time_marker} {subject} {reflexive_pronoun} {verb}."
- 反身代詞對照：
  - eu → me
  - tu → te
  - ele/ela/você → se
  - nós → nos
  - eles/elas/vocês → se
- 不同時態的代詞位置：
  - indicative：代詞在動詞後，用連字號連接，例如 `levanto-me`、`levantei-me`、`levantava-me`、`levantar-me-ei`、`levantar-me-ia`。
  - subjunctive：代詞在動詞前，例如 `que me levante`、`se me levantasse`。
  - imperative：代詞在動詞後，用連字號連接，例如 `levanta-te!`、`levante-se!`、`levantemo-nos!`、`levantem-se!`。
- 需要正確處理重音和連字號；若變位本身已含連字號，不要重複加。

## 7. 質量檢查
生成後請自我檢查：
- 變位是否符合 pt-PT 標準。
- tu 的變位是否正確（例如 tu falas, tu comes, tu bebes, tu vais, tu tens）。
- nós 的過去簡單式是否帶重音（-ar 動詞：andámos, falámos）。
- 縮合介系詞是否正確（ao, à, do, da, no, na, pelo, pela）。
- 時間副詞與時態是否匹配。
- 賓語與動詞搭配是否自然。
- 反身動詞的代詞位置是否正確（依時態類型不同）。
- 每個時態的 `type` 欄位是否正確。
- imperativo_afirmativo 是否只有 4 個人稱（沒有 eu）。
- subjunctive 和 imperative 的 `special_templates` 是否非空。
- indicative 的 `special_templates` 是否為空陣列。
- 若某搭配不自然，寧可省略，不要硬湊。
- 使用歐式葡語詞彙，避免巴西葡語。
- 人稱分組必須是 eu, tu, ele/ela/você, nós, eles/elas/vocês，不得拆分。
- 時態只能是這 8 個，不得多也不得少。

## 8. 動詞選擇規則（由你決定）

### 8.1 你要自己挑動詞
- 不要等我提供動詞清單，請你自己挑選。
- 挑選標準：
  1. 高頻實用：日常對話、書面語中常見。
  2. 涵蓋不同類型：至少包含規則 -ar、規則 -er、規則 -ir、不規則、反身、需要介系詞的動詞。
  3. 難度遞進：優先挑初學者到中級（A1-B2）最常用的動詞。
  4. 搭配自然：每個動詞都能輕鬆造出 3-5 個自然句子。
  5. 避免重複：不要挑語義或用法高度重疊的動詞。
- 建議的挑選順序（供參考，不強制）：
  1. 最核心：ser, estar, ter, ir, fazer, dizer, poder, querer, saber, vir
  2. 常用規則：falar, comer, beber, escrever, ler, ouvir, trabalhar, estudar, morar, comprar
  3. 常用不規則：ver, dar, trazer, pôr, sair, pedir, sentir, dormir, conhecer, seguir
  4. 需要介系詞：gostar (de), precisar (de), conseguir, assistir (a), acreditar (em), pensar (em), depender (de)
  5. 反身動詞：levantar-se, sentar-se, deitar-se, vestir-se, lavar-se, chamar-se, lembrar-se (de), esquecer-se (de)
  6. 更進階：haver, dever, parecer, tornar-se, manter, valer, caber

### 8.2 黑名單
以下動詞已經生成過，請不要再次挑選：

[
  "falar", "comer", "partir", "ser", "lembrar-se",
  "estar", "ter", "ir", "fazer", "dizer",
  "poder", "querer", "saber", "vir", "dar",
  "beber", "escrever", "ler", "ouvir", "ver",
  "trabalhar", "estudar", "morar", "comprar", "conhecer",
  "trazer", "pôr", "sair", "pedir", "seguir",
  "sentir", "dormir", "haver", "dever", "parecer",
  "gostar", "precisar", "conseguir", "acreditar", "pensar",
  "levantar-se", "sentar-se", "deitar-se", "vestir-se", "lavar-se",
  "chamar-se", "esquecer-se", "tornar-se", "manter", "caber"
]

### 8.3 數量
請生成 5 個動詞。若你判斷某個動詞太難或不適合，可以跳過並挑下一個，但最終數量要達到指定數量。

### 8.4 輸出前自我檢查
- 確認所有動詞都不在黑名單中。
- 確認沒有重複挑選同一個動詞。
- 確認涵蓋至少 3 種不同類型（規則 -ar、規則 -er、規則 -ir、不規則、反身、需要介系詞）。
- 確認每個動詞都有全部 8 個時態（除不適用者，需在 notes 說明）。
- 若某一批無法達到指定數量，寧可少給，也不要重複或硬湊。

## 9. 輸出格式
輸出為純 JSON 陣列，每個元素是一個動詞物件，結構如第 4 節。不要有任何解釋文字、不要用 markdown code fence。

若資料太長，可以分批輸出，但每次輸出都要是合法的 JSON 陣列。