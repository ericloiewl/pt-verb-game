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

| tense_key | 顯示名稱 |
|---|---|
| presente | presente · 現在式 |
| preterito_perfeito | pretérito perfeito · 簡單過去式 |
| preterito_imperfeito | pretérito imperfeito · 過去未完成式 |
| futuro_presente | futuro do presente · 未來式 |
| condicional | condicional · 條件式 |
| presente_subjuntivo | presente do conjuntivo · 現在虛擬式 |
| preterito_imperfeito_subjuntivo | pretérito imperfeito do conjuntivo · 過去未完成虛擬式 |
| imperativo_afirmativo | imperativo afirmativo · 肯定命令式 |

注意：
- 使用 `conjuntivo` 這個拼法（pt-PT 偏好），不要用 `subjuntivo`。
- 不要生成 `imperativo_negativo`、`futuro_subjuntivo`、任何複合時態、`infinitivo_pessoal`、`gerundio`、`participio` 作為獨立時態。
- 若某個動詞在某時態不適用（例如無人稱動詞沒有命令式），在該動詞的 notes 說明並省略該時態。
- 虛擬式必須帶自然的引導語（espero que、é importante que、talvez、duvido que、se、caso、como se…），不要寫成平淡的直述句。

## 3. 動詞資料欄位

{
  "infinitive": "原形",
  "translation_zh": "中文翻譯（多個義項用中文分號「；」分隔）",
  "translation_en": "英文翻譯",
  "notes": "語用、地區、字面反身動詞、不規則變位等說明，若無則 null",
  "phrases": {
    "presente": [
      "Todos os dias eu {como} uma maçã.",
      "Normalmente tu {comes} pão ao pequeno-almoço."
    ],
    "imperativo_afirmativo": [
      "{Come} a sopa, por favor."
    ]
  }
}

**只保留這 6 個欄位。不要輸出 type、group、transitivity、reflexive、preposition、participle、gerund、objects、sentence_template、tenses、conjugations、time_markers、special_templates。**

## 4. phrases 規則（最重要）

- `phrases` 的 key 是 tense_key，value 是**完整葡萄牙語句子的陣列**。程式不做任何組合，句子由你寫好、直接出題。
- **每個句子裡必須有且只有一個 `{...}` 標記**，標記內就是這句要考的變位形式，例如：
  - "Ontem eu {comi} uma maçã."
  - "Espero que ele {tenha} tempo."
  - "{Levanta-te} depressa, por favor!"
  - "Todos os dias nós {levantamo-nos} às sete."
- 標記內只放**動詞變位本身**（含反身代詞與連字號），絕不要把主語、時間副詞、賓語放進標記。
- 標記內**不要有多個動詞形式**；一句只考一個位置。
- 句子內除了這一個標記外，**不得出現任何其他大括號 `{` 或 `}`**。
- **同一個動詞不要在同一句裡出現第二種變位**（例如「quando eu comia…」裡的 comia 會干擾），除非那句刻意要考對比，此時未標記的形式必須語法正確。
- 句子要完整、自然、有語境，讀起來像真人寫的，不要像模板拼出來的；避免全部都是「時間副詞 + 主語 + 動詞 + 賓語」的同一個套路。
- 句子首字母大寫，句末有適當標點（. ! ?）。
- **每個 tense_key 提供 5 個句子，分別對應 eu、tu、ele/ela/você、nós、eles/elas/vocês**，主語要在句子裡出現（代詞或名詞皆可，但要讓人看得出是哪個人稱）。
- `imperativo_afirmativo` 提供 **4 個句子**，對應 tu、ele/ela/você、nós、eles/elas/vocês；**絕對不能有 eu**。
- 若句子是命令式，語氣要自然（動詞開頭或帶 por favor 等）。

## 5. 反身動詞規則
- 反身代詞與變位必須寫在標記裡，依時態類型決定位置：
  - indicative：代詞在動詞後，用連字號連接，例如 `{levanto-me}`、`{levantei-me}`、`{levantava-me}`、`{levantar-me-ei}`、`{levantar-me-ia}`。
  - conjunctive：代詞在動詞前（人稱代詞），例如句子裡寫成 "Espero que me {levante}..."，此時標記內是 `{levante}`，代詞在標記外。
  - imperative：代詞在動詞後，用連字號連接，例如 `{levanta-te}`、`{levante-se}`、`{levantemo-nos}`、`{levantem-se}`。
- 需要正確處理重音和連字號；若變位本身已含連字號，不要重複加。
- 字面反身動詞（如 lembrar-se、esquecer-se）的介系詞搭配要正確，並在 notes 交代。

## 6. 質量檢查（生成後自我檢查）
- 變位是否符合 pt-PT 標準。
- tu 的變位是否正確（例如 tu falas, tu comes, tu bebes, tu vais, tu tens）。
- nós 的過去簡單式是否帶重音（-ar 動詞：andámos, falámos）。
- 縮合介系詞是否正確（ao, à, do, da, no, na, pelo, pela）。
- 時間副詞與時態是否匹配（presente 現在、perfeito 完成過去、imperfeito 過去習慣、futuro 未來、condicional 假設）。
- 賓語與動詞搭配是否自然。
- 反身動詞的代詞位置是否正確（依時態類型不同）。
- imperativo_afirmativo 是否只有 4 個句子（沒有 eu）。
- 每個句子是否**恰好一個** `{...}` 標記、標記內是否為非空的動詞形式。
- 每個 tense_key 是否 5 個句子（imperativo 4 個），且五個人稱都有覆蓋。
- 每個句子是否沒有除標記外的大括號。
- 若某搭配不自然，寧可省略，不要硬湊。
- 使用歐式葡語詞彙，避免巴西葡語。
- 時態只能是這 8 個，不得多也不得少。

## 7. 動詞選擇規則（由你決定）

### 7.1 你要自己挑動詞
- 不要等我提供動詞清單，請你自己挑選。
- 挑選標準：
  1. 高頻實用：日常對話、書面語中常見。
  2. 涵蓋不同類型：至少包含規則 -ar、規則 -er、規則 -ir、不規則、反身、需要介系詞的動詞。
  3. 難度遞進：優先挑初學者到中級（A1-B2）最常用的動詞。
  4. 搭配自然：每個動詞都能輕鬆寫出 5 個自然句子。
  5. 避免重複：不要挑語義或用法高度重疊的動詞。
- 建議的挑選順序（供參考，不強制）：
  1. 最核心：ser, estar, ter, ir, fazer, dizer, poder, querer, saber, vir
  2. 常用規則：falar, comer, beber, escrever, ler, ouvir, trabalhar, estudar, morar, comprar
  3. 常用不規則：ver, dar, trazer, pôr, sair, pedir, sentir, dormir, conhecer, seguir
  4. 需要介系詞：gostar (de), precisar (de), conseguir, assistir (a), acreditar (em), pensar (em), depender (de)
  5. 反身動詞：levantar-se, sentar-se, deitar-se, vestir-se, lavar-se, chamar-se, lembrar-se (de), esquecer-se (de)
  6. 更進階：haver, dever, parecer, tornar-se, manter, valer, caber

### 7.2 黑名單
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
  "chamar-se", "esquecer-se", "tornar-se", "manter", "caber",
  "ficar", "chegar", "ajudar", "encontrar", "acordar",
  "cozinhar", "começar", "perder", "aprender", "correr",
  "responder", "abrir", "decidir", "subir", "preferir",
  "rir", "divertir-se", "preocupar-se", "assistir (a)", "depender (de)"
]

### 7.3 數量
請生成 5 個動詞。若你判斷某個動詞太難或不適合，可以跳過並挑下一個，但最終數量要達到指定數量。

### 7.4 輸出前自我檢查
- 確認所有動詞都不在黑名單中。
- 確認沒有重複挑選同一個動詞。
- 確認涵蓋至少 3 種不同類型（規則 -ar、規則 -er、規則 -ir、不規則、反身、需要介系詞）。
- 確認每個動詞都有全部 8 個時態（除不適用者，需在 notes 說明）。
- 若某一批無法達到指定數量，寧可少給，也不要重複或硬湊。

## 8. 輸出格式
輸出為純 JSON 陣列，每個元素是一個動詞物件，結構如第 3 節。不要有任何解釋文字、不要用 markdown code fence。

若資料太長，可以分批輸出，但每次輸出都要是合法的 JSON 陣列。
