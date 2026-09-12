# GPT Image 2.5 Prompt Migrator

[English](README.en.md)

[![Validate public skill](https://github.com/gd8455-create/image25-prompt-migrator/actions/workflows/ci.yml/badge.svg)](https://github.com/gd8455-create/image25-prompt-migrator/actions/workflows/ci.yml)

GPT Image 2.5 Prompt Migrator 是一個獨立的 Codex Skill，專門把**已經存在**的圖片生成或編輯提示詞，遷移成可供 GPT Image 2.5 使用與測試的版本。

它接受舊版 GPT Image 提示詞、其他影像工具的提示詞，以及其他 AI 助手產出的既有 image prompt。它不從空白需求開始代寫新提示詞，也不把所有提示詞都視為必須改寫：若來源內容已適合 GPT Image 2.5，會原樣通過並回報 `changes: []`。

> v1.0.0 · MIT 授權 · 可公開安裝的獨立影像處理 Skill；它不是 OpenAI 官方產品。

## 為什麼建立這個 Skill

模型或工具升級後，創作者往往已累積大量可用提示詞。這些提示詞可能混有舊模型習慣、特定工具語法、負面提示詞區塊、權重標記，或由其他 AI 助手產生但尚未針對 GPT Image 2.5 整理的內容。逐份重寫容易遺失原始意圖，也很難知道哪些地方真的被改過。

這個 Skill 提供一條可檢查的遷移流程：保留原始 prompt，辨識來源語法，分離 prompt 與 request settings，交付遷移稿、變更紀錄、保留條件與人工 QA。使用者可以判斷要採用、回退或繼續測試，而不是只得到一份看不出差異的新文字。

## 適用來源

| 來源 | 處理方式 |
| --- | --- |
| 舊版 GPT Image 的既有生成或編輯 prompt | 保留原意，整理已過時或混雜的寫法，建立 GPT Image 2.5 遷移稿。 |
| 其他影像生成或編輯工具的既有 prompt | 將可辨識的視覺意圖轉成 GPT Image 2.5 可讀的指令；不把工具專屬參數假裝成一對一等價控制。 |
| 其他 AI 助手產出的既有 image prompt | 檢查它是否仍沿用舊模型或跨工具格式，再做必要轉換。 |
| 已適合 GPT Image 2.5 的 prompt | 原樣通過，`changes: []`，不為了展示功能而強制改寫。 |

上表是常見來源範例，不代表對每個第三方工具、版本或語法提供完整相容性保證。無法可靠判讀的來源標記會保留在 `Unresolved`，交由使用者決定。旗標、權重、負面提示與來源設定的處理界線見 [來源轉接原則](skills/image25-prompt-migrator/references/source-adapters.md)。

## 範圍界線

這個 Skill 的輸入必須包含一份既有的圖片生成或編輯提示詞。它可以：

- 稽核長篇／JSON 場景提示詞，保留有用的視覺錨點，檢查正負指令衝突、數值假精準與參考圖角色；長度或 JSON 格式不代表較新、較好。
- 保存來源 prompt 與不可漂移的主體、身份、產品、構圖、文字及參考圖用途。
- 移除或轉述只對來源工具有意義的語法，並記錄每項實質變更。
- 將 `model`、`quality`、像素尺寸、背景與輸出格式等 request settings 和畫面指令分開。
- 為遷移前後建立 baseline、重複測試方式與可人工判定的 QA。
- 在寫實 prompt 的轉換中，用材質、重力、接觸、濕度、光源與相機所見的具體關係取代空泛堆疊詞。

它不負責從空白 brief 發想或撰寫全新的 image prompt，也不保證遷移後的圖片一定更好。若使用者需要從零開始創作，應使用一般提示詞撰寫或創意製作流程。

## 遷移工作流

1. 保存來源 prompt、來源工具或模型資訊，以及已知 request settings。
2. 先判斷是否需要轉換；已相容時原樣通過並回報 `changes: []`。
3. 需要轉換時，只改與 GPT Image 2.5 遷移有關的部分，保留創作意圖與必要限制。
4. 將無法對應的來源語法列為已移除、僅供追溯或 `Unresolved`，不捏造等價參數。
5. 交付可比較的遷移稿、變更紀錄、request settings 與生成後 QA。

模型遷移比較應先保存 baseline。第一輪可以只切換指定模型，保持 prompt、參考圖、尺寸、格式與品質設定不變；確認基準後，才一次改一個變因。這與 OpenAI 官方 GPT Image 2.5 遷移指南所建議的代表性輸入、固定比較條件與完整結果檢查一致。

長篇結構化來源的處理細節見[結構化場景稽核](skills/image25-prompt-migrator/references/structured-scenes.md)。

## 安裝

可在 Codex 中呼叫 `$skill-installer`，並指定本儲存庫內的 Skill 資料夾：

```text
$skill-installer https://github.com/gd8455-create/image25-prompt-migrator/tree/main/skills/image25-prompt-migrator
```

這個網址只指向 `skills/image25-prompt-migrator/`。若已下載整個儲存庫，也可使用隨附安裝器：

```powershell
python -X utf8 scripts/install.py
```

要測試到暫存或自訂的 skills 目錄，可加上 `--destination <skills-directory>`。若目的地已有同名 Skill，安裝器會停止；只有明確加上 `--force` 才會替換。

## 使用例句

舊版 prompt 轉換：

```text
使用 $image25-prompt-migrator，把下面這份舊版圖片生成提示詞遷移到 GPT Image 2.5。保留人物、構圖與文字需求，列出所有變更；如果不需要改，請原樣回傳並標示 changes: []。
```

跨 AI 轉換：

```text
使用 $image25-prompt-migrator，把這份另一個 AI 助手產出的 image prompt 轉成 GPT Image 2.5 版本。分離來源工具參數，不要假設每個參數都有一對一對應。
```

遷移 baseline：

```text
使用 $image25-prompt-migrator，為這份既有 prompt 建立 GPT Image 2.5 migration baseline。第一輪不要改寫 prompt，列出固定設定、重複測試方式與驗收指標。
```

## 範例

[`examples/`](examples/) 提供三份文字交付與一份真實的單次圖片驗收紀錄：

- [舊版提示詞轉換](examples/01-legacy-conversion.md)
- [遷移 baseline 與原樣通過](examples/02-migration-baseline.md)
- [跨 AI 提示詞轉換](examples/03-cross-ai-conversion.md)
- [轉換工作流的單次視覺驗收](examples/04-built-in-generation-evaluation.md)

第四份紀錄確實使用 Codex 內建圖片生成工具各執行一次，但工具沒有公開確切的後端模型名稱、seed 或取樣設定。因此它只能驗收這次「來源 prompt → 遷移稿 → 後續修正」流程的可見結果，不能當成 GPT Image 2.5 API 的受控基準，也不能證明遷移稿普遍優於來源 prompt。

## 儲存庫結構

```text
image25-prompt-migrator/
├─ skills/image25-prompt-migrator/
│  ├─ SKILL.md
│  ├─ LICENSE
│  ├─ agents/openai.yaml
│  └─ references/
├─ examples/
│  └─ assets/
├─ scripts/
│  ├─ install.py
│  └─ validate_repo.py
├─ tests/
├─ .github/workflows/
├─ README.md
├─ README.en.md
├─ CHANGELOG.md
├─ LICENSE
└─ SECURITY.md
```

公開安裝入口為 `skills/image25-prompt-migrator/`。 `examples/` 提供遷移行為與視覺驗收範例；`scripts/` 提供單一 Skill 安裝器與儲存庫檢查器；`tests/` 與 GitHub Actions 檢查公開包裝、Skill 結構及不應出現的私人內容。

## 驗證

在儲存庫根目錄執行：

```powershell
python -X utf8 scripts/validate_repo.py
python -X utf8 -m unittest discover -s tests -v
```

也可使用 Codex 內建的 Skill 結構驗證器：

```powershell
python -X utf8 "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "skills\image25-prompt-migrator"
```

結構驗證不等於 GPT Image 2.5 已實際生成並通過視覺驗收。遷移品質、文字正確率、身份保留、延遲與成本仍須用相同輸入實際、多次測試。

## 限制

- 核心 Skill 交付 prompt、request settings、變更紀錄與 QA，不會自行呼叫圖片生成 API。
- 第三方提示詞語法可能有版本差異；無法確認的標記不會被宣稱為 GPT Image 2.5 等價設定。
- 提示詞無法保證像素級不變。需要完全相同區域時，應使用遮罩、局部合成或其他確定性後製。
- API 模型與控制項可能和 ChatGPT 介面不同；本專案不把一個介面的設定描述成另一個介面的保證。
- 單次輸出只能作為該次案例的證據。是否採用遷移稿，仍應以代表性輸入、重複測試和使用者的驗收標準決定。

## 依據

模型名稱、參數界線與遷移測試原則以 OpenAI 官方文件為主要依據：

- [GPT Image 2.5 prompting guide](https://developers.openai.com/api/docs/guides/image-prompting)
- [Image generation API guide](https://developers.openai.com/api/docs/guides/image-generation)
- [GPT Image 2.5 Flare](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare)
- [GPT Image 2.5 Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)

## 授權

採用 [MIT License](LICENSE)。可使用、修改、散布與商用；散布時請保留著作權與授權聲明。Skill 資料夾也包含相同授權，確保單獨安裝時一併保留。
