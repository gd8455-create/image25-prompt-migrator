# 來源轉接原則

本文件提供安全遷移原則，不是完整支援矩陣。產品版本、介面與參數會改變；只在來源已知、語法明確，且使用者資料或官方文件足以建立意義時做映射。

## 共通處理

將輸入拆成四類：

1. `semantic_content`：希望畫面呈現的主體、動作、場景、構圖、材質、光線、風格、文字與限制。
2. `source_controls`：來源工具的旗標、數值、節點、模型選擇、增強器或 UI 設定。
3. `reference_assets`：實際圖片、遮罩、模型資產或工作流上下文。
4. `unknown_syntax`：來源或作用仍無依據的 token、縮寫、權重或控制字串。

第一類直接轉成 GPT Image 2.5 的自然語言。第二類若有文件支持的可見畫面語意，可把該語意改寫成自然語言並記錄為語意保留，而不是控制等價；只有目標操作面已確認提供的對應控制才放入 request settings；沒有直接等價就標示 `no_direct_equivalent`。第三類保留真實資產角色，不把路徑或模型資產假裝成文字提示。第四類保持可追溯並列為 unresolved，不自行解碼。

## 舊 GPT Image 或 DALL·E 系列

既有自然語言若已清楚表達畫面與限制，可直接通過，`converted_prompt` 與 `source_prompt` 相同且 `changes: []`。不要因版本升級而強制擴寫。

舊 API 或介面設定仍需與提示詞分開。只依 GPT Image 2.5 目前操作面實際暴露的 model、quality、尺寸、背景和格式重新登記；不能假設舊值、別名或預設值自動等價。舊提示詞中的自然語言相容性也不代表成圖一定一致。

## Midjourney

Midjourney 參數是附加在文字提示末尾、但語法上獨立的控制；解析原始 `source_prompt` 時需辨認它們，且不能原樣塞入 GPT Image 2.5 提示詞。

- `--ar` 或 `--aspect`：來源與值明確時，保留其畫面比例意圖；若目標操作面支持相應尺寸，放入 request settings。移除旗標語法。
- `--no`：只把清楚列出的排除內容轉成精確限制，並檢查是否與必要文字、Logo 或場景元素衝突。不要保留 `--no` 字串。
- `--stylize` 或 `--s`：數值是 Midjourney 控制，沒有可假設的一對一 GPT Image 2.5 數值。可從來源文字保留已明示的藝術風格；若只有 stylize 數值，標示無直接等價，不猜出一種風格。
- 其他版本、seed、quality、style/reference 或 personalization 控制：依同一原則分流。URL 或參考控制只有在對應圖片實際提供時才建立 reference role。

官方來源：

- https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List
- https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize

## Stable Diffusion 與 ComfyUI

正向提示詞中的可見語意可以轉換。以下內容屬來源執行機制，不能原樣放入 GPT Image 2.5 提示詞：

- `negative_prompt` 或 KSampler negative conditioning：把其中清楚、必要且不衝突的排除語意改寫為自然語言限制；不保證與 diffusion 負向條件等價。
- CFG、steps、sampler、scheduler、seed、denoise：保留在來源紀錄，標示沒有可假設的提示詞等價物。
- `(term:1.2)` 等權重：只有來源語法已確認時，才能把相對強調改為普通語言；不攜帶數值權重。
- LoRA 名稱、檔案與強度：它們修改來源模型或文字編碼器，不是可移植的文字 token。若沒有實際參考圖或明確可見效果說明，標示無直接等價，不從 LoRA 名稱猜測人物或風格。
- ComfyUI 節點與工作流 JSON：作為來源上下文記錄，不嵌入目標提示詞。

官方來源：

- https://docs.comfy.org/tutorials/basic/text-to-image
- https://docs.comfy.org/tutorials/basic/lora
- https://platform.stability.ai/docs/api-reference

## FLUX

FLUX 自然語言中的可見語意可以轉換。`prompt_upsampling` 是來源端自動擴寫控制，不是 GPT Image 2.5 提示內容，不能原樣貼入。

若來源曾開啟 prompt upsampling，而只有擴寫前的文字可用，需記錄「實際執行提示可能包含不可見的來源端擴寫」，因此無法建立完全重現的基準。若擴寫後提示已提供，將它視為另一份可追溯來源，不猜測缺失內容。aspect ratio、seed、output format、raw mode 等控制也依共通規則分流。

官方來源：

- https://docs.bfl.ai/guides/prompting_summary
- https://docs.bfl.ai/guides/prompting_guide_flux2

## Gemini 與 Microsoft Copilot 的自然語言提示詞

保留自然語言中的成像任務、主體、背景、風格、構圖與限制。移除只服務來源聊天介面的寒暄、選單操作或回覆格式要求，前提是它們不影響成圖。

若提示詞是「把它改暖一點」等依賴對話或圖片的續句，相關上一輪文字和實際圖片角色也是來源的一部分；缺少時先索取，不自行想像。「Style」「Shape」等 UI 選擇只有使用者或匯出資料明確提供時才記錄。不要推測 Copilot 或 Gemini 背後的隱藏模型、預設參數或自動改寫內容。

官方來源：

- https://ai.google.dev/gemini-api/docs/image-generation
- https://support.microsoft.com/en-us/microsoft-copilot/using-image-generation-in-microsoft-copilot

## 未知來源

只遷移可直接讀懂的自然語言語意。任何看似旗標、權重、節點、模型別名或自訂 token 的內容都先列為 `unknown_syntax`。若其作用會實質改變畫面，詢問一個聚焦問題；仍無答案時交付已確定的轉換與 unresolved 清單，不宣稱完整等價。
