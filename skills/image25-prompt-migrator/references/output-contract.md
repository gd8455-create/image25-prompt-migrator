# 輸出契約與完成條件

只在準備交付時讀取。本技能交付可追溯的提示詞遷移結果或比較計畫，不把尚未生成的結果描述成已通過驗證。

## 一般交付

每次交付至少包含：

1. 來源分類與完整 `source_prompt`。
2. 固定目標 `GPT Image 2.5` 與可直接使用的 `converted_prompt`。
3. 簡短、具體的 `changes`；原樣通過時為空陣列。
4. 已映射、無直接等價及仍不明的來源控制摘要。
5. 需要在目標工具設定的已知 request settings。
6. 與來源要求相符的 QA 項目及實質未決問題。

`migration_baseline` 另附未改寫的基準提示詞與可比較條件。`migration_repair` 另附先前轉換稿、觀察到的失敗與修復理由。

## 結構化欄位

只有下游工作流需要時才使用完整結構：

- `mode`：`migration_convert`、`migration_baseline` 或 `migration_repair`。
- `source_origin`：`older_image_model`、`other_image_ai` 或 `unknown`。
- `source_tool`：已知產品或模型；未建立時為 `unknown`。
- `source_prompt`：必填的來源全文。
- `target`：固定為 `GPT Image 2.5`。
- `converted_prompt`：轉換後全文；修復模式中為新的修復版本。
- `prior_converted_prompt`：只供修復模式使用，保存失敗的先前版本。
- `failure_evidence`：只供修復模式使用，記錄實際失敗輸出或可觀察的失敗描述。
- `changes`：相對來源的實質修改及理由；相容提示詞原樣通過時為空。
- `preserved_requirements`：不可漂移的來源要求。
- `source_syntax_handling`：逐項記錄已映射控制、`no_direct_equivalent` 與 `unresolved`，不得填入猜測語意。
- `fidelity_anchors`：需要時，列出能追溯到來源段落的少量核心要求及 QA；數量不限，不取代完整保留表。
- `constraint_audit`：需要時，登記衝突的來源位置、解決方式、理由、尚未確定處和驗收方式。
- `format_changes`：有抽取、JSON 逸出修復或重新序列化時另列，不冒充視覺改善。
- `conversion_profile`：`none` 或可選的 `physical_realism_v2`。
- `baseline_prompt`：只供基準模式使用，與 `source_prompt` 逐字相同。
- `baseline_changes`：只供基準模式使用，固定為空。
- `comparison_controls`：可比較的固定條件與無法對齊的跨平台變因。
- `required_rendered_text`：每個逐字字串的內容、大小寫、標點、次數、位置、字體、顏色和相對大小。
- `reference_roles`：每張實際參考圖的編號、用途、優先關係與組合方式，不含虛構路徑。
- `request_settings`：目標操作面已知的 model ID、quality、像素尺寸、背景與格式；未知值保持未知。
- `qa_checks`：能判定來源意圖是否被保留的驗收項目。
- `unresolved`：只有作者或來源資料才能解決的問題；沒有就留空。

## QA 選取

所有轉換至少檢查主體或身份、構圖、明示風格、必要逐字文字、排除條件和意外新增。再依來源加入：

- 圖片編輯提示詞：指定修改是否完成，來源要求保留的區域是否漂移。
- 多參考圖：身份、服裝、商品、構圖、背景與風格來源是否混用。
- 精確文字：每個字、大小寫、標點、次數、位置和可讀性。
- 透明素材：檔案是否真的含 alpha；棋盤格圖樣不算透明。
- 圖解或資料圖：標籤、箭頭、公式和資料是否人工核對。
- 遷移比較：完整輸入、可比較設定、多次輸出、失敗、延遲、成本與評分準則。
- 修復：觀察到的失敗是否改善，未失敗的來源要求是否維持。

## 完成條件

只有下列條件全部成立才算完成：

- 非空的 `source_prompt` 已保留且可追溯；來源分類有依據，未知時如實標示。
- 目標固定為 GPT Image 2.5，沒有被來源模型或工具名稱取代。
- `converted_prompt` 保留來源的明示創作意圖，沒有新增未授權的主體、身份、場景或風格。
- 來源專有控制只在意義明確時映射；沒有直接等價與未知語法已標示，沒有原樣冒充目標提示語法。
- 視覺提示詞與 request settings 已分開，沒有聲稱未暴露的參數已套用。
- 所有必要成像文字已逐字登記，廣泛禁止句沒有取消它們。
- `conversion_profile` 如實標示；Physical Realism v2 沒有被當作 GPT Image 2.5 官方要求或靜默預設。
- 基準模式的 `baseline_prompt` 與來源逐字相同，跨平台非等價控制已揭露。
- 修復模式同時具備來源、先前轉換稿和失敗證據；每項修復都能追溯至來源要求。
- JSON／長篇提示詞的有用細節未被任意裁掉；姿勢數值未被杜撰，明示數值如經簡化有授權與紀錄；正負指令、參考身份與必要文字已交叉檢查。
- QA 項目能判定本次遷移是否成功，未執行的生成或 A/B 測試沒有被寫成已通過。
- 交付內容可供使用者或下游工具直接採用，不停在提綱或待續狀態。

若唯一未完成事項是會實質改變成品的缺失來源上下文或未知語法，先完成可確定部分，再只提出一個必要問題。
