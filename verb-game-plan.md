# 葡萄牙語動詞變位填空遊戲 — 實作計劃

> **意圖摘要**：單一、自足、可直接以瀏覽器開啟的 HTML 檔案（CSS + JS 全部內嵌），實作歐洲葡萄牙語（PT-PT）動詞變位填空遊戲。資料、邏輯、介面皆依下方規格；本文件為生成階段與人類編輯者共用的「唯一來源」。

## 範圍（Range）

**涵蓋**
- 遊戲資料獨立於 `verb-data.js`（`window.VERB_DATA`），由 HTML 以 `<script src>` 載入。
- 隨機出題管線：動詞 → 時態（受勾選控制）→ 人稱 index 0–4 → 隨機 suffix → 隨機主詞顯示形。
- 輸入比對（忽略大小寫與前後空白），Enter 或按鈕送出。
- 即時答題回饋、正確答案、分數（答對數 / 總題數）。
- 時態勾選方塊，自動由 `verbData` 的時態鍵產生。
- 手機優先、單欄置中版面。

**不包含（此輪）**
- 伺服器 / 儲存 / 音效 / 計時器；不會擅自加入分數排行等未要求的東西。

## 資料模型（原樣保存）

資料獨立於 `verb-data.js`，以 `window.VERB_DATA` 陣列提供；HTML 以 `<script src="verb-data.js">` 載入，主邏輯讀取 `window.VERB_DATA`（非陣列或遺失時顯示「資料載入失敗」空狀態）：

```js
window.VERB_DATA = [
  {
    infinitive: "comer",
    tenses: {
      presente: {
        conjugations: {
          "eu": "como",
          "tu": "comes",
          "ele/ela/você": "come",
          "nós": "comemos",
          "eles/elas/vocês": "comem"
        },
        suffixes: [
          "uma maçã.",
          "pão com manteiga.",
          "fruta no café da manhã.",
          "no restaurante italiano.",
          "bem demais.",
          "muito devagar."
        ]
      },
      preterito_perfeito: {
        conjugations: {
          "eu": "comi",
          "tu": "comeste",
          "ele/ela/você": "comeu",
          "nós": "comemos",
          "eles/elas/vocês": "comeram"
        },
        suffixes: [
          "uma maçã ontem.",
          "tudo o que tinha no prato.",
          "bem na festa.",
          "juntos no almoço.",
          "a pizza inteira."
        ]
      }
    }
  },
  {
    infinitive: "falar",
    tenses: {
      presente: {
        conjugations: {
          "eu": "falo",
          "tu": "falas",
          "ele/ela/você": "fala",
          "nós": "falamos",
          "eles/elas/vocês": "falam"
        },
        suffixes: [
          "português.",
          "alto demais.",
          "comigo agora.",
          "devagar por favor.",
          "sobre o projeto."
        ]
      },
      preterito_perfeito: {
        conjugations: {
          "eu": "falei",
          "tu": "falaste",
          "ele/ela/você": "falou",
          "nós": "falámos",
          "eles/elas/vocês": "falaram"
        },
        suffixes: [
          "com ela ontem.",
          "bem na reunião?",
          "ao telefone.",
          "sobre isso.",
          "durante horas."
        ]
      }
    }
  }
];
```

語意規則：
- `conjugations` 為以人稱字串為鍵的 object；鍵必須與 HTML 內的 `PERSON` 陣列一致（`eu`、`tu`、`ele/ela/você`、`nós`、`eles/elas/vocês`）。
- `suffixes` 為該時態的共享句尾池；題目句於執行期拼裝為 `主詞 + " ___ " + suffix`，suffix 每次出題隨機抽取。
- 主詞顯示由 `PERSON_DISPLAY` 隨機池決定：`eu→Eu`、`tu→Tu`、`ele/ela/você→Ele/Ela/Você 隨機`、`nós→Nós`、`eles/elas/vocês→Eles/Elas/Vocês 隨機`；下方人稱提示行仍顯示完整鍵名。
- 出題時以「動詞原形（infinitive）」標示填空位置，另附人稱主詞提示，協助學習者對應。
- 時態鍵（presente、preterito_perfeito…）為動態：勾選、出題皆以 `Object.keys` 為準，未來新增時態不需改程式。
- 顯示層另有一份 `TENSE_META`（短葡文名 + 語氣分組），僅供 UI 使用、不影響出題邏輯；未收錄的鍵自動歸入 `Outros` 組。
- 兩個範例動詞值逐字保留，不可改動；僅允許「新增更多動詞物件」以擴充資料集。
- 邊界：某時態缺人稱鍵、值非字串、`suffixes` 非陣列或為空 → 自動跳過，不中斷遊戲。

## 遊戲流程（狀態機）

1. `pickQuestion()`：勾選時態為空 → 進入空狀態；否則隨機取動詞 → 隨機取已勾選時態 → 隨機 index 0–4 → 組題。
2. 畫面顯示句子（`___` 以醒目標記呈現）+ 人稱提示。
3. 玩家輸入 → 送出（Enter 或按鈕）。
   - 送出後鎖定輸入與按鈕（防止重複送出），以 `trim().toLowerCase()` 與正確變位比較。
   - 正確 → 綠標記；錯誤 → 紅標記並顯示正確變位。
4. 每次送出：總題數 +1；答對則答對數 +1。按「下一題」續玩。

### 決策與取捨（供審查）
- **練習優先**：答錯仍可繼續、不扣分、不擋下一題——維持輕量練習節奏。
- **人稱提示**：句子已含主詞；額外顯示主詞人稱標籤（如 `eu`）便於學習者記憶。**預設開啟，可關閉。**
- **連擊 / 重新開始按鈕**：**預設不加**，保持簡潔；如需再加。

## 畫面結構（手機優先）

```
┌──────────────────────────┐
│ 標題列                    │
│ 時態收合面板（摘要列）    │  ←「出題時態 · 已選 N/M ▾」單行
│ 問題卡片（大字題目句）    │
│ 輸入框 + 送出/下一題按鈕  │
│ 回饋列（色彩 + 正確答案） │
└──────────────────────────┘
```

- 單欄、置中、`max-width` ≈ 520px。
- 手機無水平捲動、觸控目標 ≥ 44px。
- 題目字體大（卡片內醒目字級），輸入框單列。

### 時態選擇器（收合式分組面板）

- 以原生 `<details>/<summary>` 實作：收合時僅佔一行摘要列（`出題時態 · 已選 N/M` ＋ chevron），展開後顯示完整 chips，確保題目在首屏。
- chips 依語氣分組（`Indicativo / Conjuntivo / Imperativo / Outros`），每組一個小標；空組不顯示。
- chip 顯示短葡文名（`TENSE_META[k].short`，如 `pret. perfeito`），完整葡中名稱放 `title` 提示與題目卡的時態徽章。
- `TENSE_META` 未收錄的時態鍵自動 fallback（`short = key.replace(/_/g," ")`、歸入 `Outros` 組），新增時態仍不需改程式。
- 已選數為 0 時摘要列計數顯示警示色；空狀態文案引導使用者展開面板勾選；「全部勾選」後自動收合面板。

## 元件與狀態覆蓋（必備）

依互動品質規則，所有狀態皆需存在：
- **Populated**：出題中（主畫面）。
- **Empty**：所有時態皆未勾選 → 卡片顯示「請至少勾選一個時態」+「全部勾選」一鍵行動。
- **Edge**：`conjugations` 缺人稱鍵或值非字串、`suffixes` 非陣列/為空、`verb-data.js` 遺失或非陣列、或動詞無該時態 → 自動跳過該題或顯示資料載入失敗空狀態，不中斷遊戲。
- **Loading / Error**：純客戶端、無遠端資料，不需網路狀態；送出後短暫鎖定即為所需防呆。

## 視覺系統（生成階段以 OKLCH 定案）

- 深色舞台（近黑背景 + 頂部柔光）+ 高飽和強調色；強調色每畫面 ≤ 2 處。
- 標題用粗體顯示字型；題目句用較大正文字級；分數/徽章用等寬字。
- 正確綠 / 錯誤紅為狀態色，與主強調色分開。
- 色票以 OKLCH 推導寫入 `:root` 變數（不以原始 hex 散落）。
- **Dark mode**：預設跟隨系統 `prefers-color-scheme`；標題列右侧提供 ☀/月亮切換鈕可手動覆蓋，選擇存於 `localStorage.theme`（唯一 storage 例外，僅存 `"light"` / `"dark"`）。主題於 `<head>` 內嵌腳本先行設定 `data-theme` 以避免閃白；切換時同步更新 `<meta name="theme-color">`。深色配色以 `:root[data-theme="dark"]` 覆蓋同一組變數，未走變數的舊硬編碼色彩已全部變數化。
- `prefers-reduced-motion`：正確/錯誤資訊以色彩 + 文字呈現為主，動畫僅為次要，不單靠動畫傳遞狀態。

### 像素小貓吉祥物（mascot）

- 以 inline SVG 像素畫（`<rect>` 格點 + `shape-rendering: crispEdges`，viewBox `0 0 24 20`）繪製 **Pusheen 風格側面胖貓**：頭左尾右、頭身合一的圓潤麵包身形、粗描邊 + 淺灰填色、圓點小眼 + 小嘴、粉色腮紅、背上 3 條與尾巴 2 條深灰條紋、右側上翹捲尾、底部三隻小短腳；零外部資源。
- 位置：問題卡片右下角、微凸出卡片底緣（absolute 定位，`bottom: -10px`），不影響單欄版面；`.q-hint` 加右側 padding 避免文字與貓咪重疊。
- 上色：描邊/眼嘴 `--cat-line`（`--fg`）、身體填色 `--cat-fill`（`--fg` 12% 混 surface）、條紋 `--cat-stripe`（`--fg` 42% 混 surface）、腮紅/愛心用固定粉色 `--cat-blush` / `--cat-pink`（**不隨 accent**，深色模式另調明度）、星星眼與淚滴 `--accent`、Zzz `--muted`；深淺色模式自動協調。
- 表情狀態機（外層 `data-mood` + CSS 顯示/隱藏對應 `<g data-m>` 群組）：
  | mood | 觸發時機 | 表情 |
  |---|---|---|
  | `idle` | 出題中 | 普通圓眼，尾巴輕擺 |
  | `happy` | 答對且 streak 1–2 | 彎眼 ^^ |
  | `star` | 答對且 streak ≥ 3 | 星星眼 + 兩顆浮動愛心 |
  | `sad` | 答錯（streak 歸零） | 耳朵下垂（CSS rotate）+ 淚滴 |
  | `sleep` | 空狀態（未勾時態／資料失敗） | 瞇眼 + Zzz |
- 換表情時以 `.pop` class 重觸發彈跳動畫（`cat-pop`）；`prefers-reduced-motion` 由既有全域規則自動停用動畫。
- 貓咪為純裝飾：`aria-hidden="true"`、`pointer-events: none`，不承載任何遊戲狀態資訊（分數/正誤仍以文字呈現）。

### 連續答對（streak，簡單版）

- `state.streak`：答對 +1、答錯歸零；**僅作為貓咪表情升級依據，不顯示數字、不影響計分**。

## 待辦與開放問題 (TODO)

- [ ] `pickQuestion` 與勾選連動的完整實作。
- [ ] 人稱提示是否顯示 —— **待使用者確認**（預設：顯示）。
- [ ] 是否加入連續答對（streak）或「重新開始」—— **已定案：加入簡單版 streak（僅貓咪表情反應，不顯示數字）**；「重新開始」按鈕仍預設不加。
- [ ] 使用者後續會以完整動詞資料取代範例 —— 程式必須對任意動詞 / 時態數量皆可運作（迴圈生成勾選、組題）。

## 驗收檢查（Done means）

1. 瀏覽器直接開啟即可遊玩，無任何外部請求。
2. 題目＝「動詞原形佔位 + 人稱提示 + 完整句子」。
3. 任一勾選組合皆能出題；全不勾選顯示空狀態與行動。
4. `"  COMEM "`、`"comem"`、`"ComEm"` 三者皆判為正確。
5. Enter 與按鈕皆可送出；送出後不接受重複送出。
6. 答錯顯示正確變位；分數正確累計（答對數 / 總題數）。
7. 手機寬度無水平捲動、觸控目標達標。

## Next step

請過目本計劃並直接編輯本檔，特別確認兩項**待使用者確認**的預設（人稱提示是否顯示、是否加 streak / 重新開始按鈕）。確認後回覆「照此生成」（或直接下達生成指令），即可切換到設計模式產出最終交付檔 `verb-game.html`。