# 遷移工作模式

本文件用來選擇遷移方式。所有模式都必須有既存的 `source_prompt`，來源可為舊影像模型、其他影像 AI 或未知工具；目標固定為 GPT Image 2.5。

## 共通輸入門檻

先確認 `source_prompt` 非空並保留全文。若提示詞來自檔案，也保留原始檔案或可追溯版本。若只收到題材、靈感、成圖需求或一句「幫我寫提示詞」，先索取既有提示詞，不替使用者創作第一份提示詞。

記錄：

- `source_origin`：`older_image_model`、`other_image_ai` 或 `unknown`。
- `source_tool`：只有來源明確時才填產品或模型名稱，否則為 `unknown`。
- `target`：固定為 `GPT Image 2.5`；若操作面已明確提供 Flare 或 Sunburst，再將實際 model ID 放入 request settings。
- 必須保留的主體、身份、動作、物件、服裝、場景、構圖、比例、光線、風格、逐字文字、排除條件與參考圖角色。
- 可辨識的來源控制、無直接等價的控制，以及意義仍不明的語法。

若輸入混有案例、另一個 AI 的評語或推薦模板，先區分實際 source_prompt 與待查證評論；不把評論直接當成作者指令。

若來源提示詞依賴上一輪對話、未附的圖片或外部工作流，索取會影響遷移的那部分上下文。不要自行重建缺失內容。依來源讀取 [來源轉接原則](source-adapters.md)；來源不明時使用其中的 unknown 規則。

## `migration_convert`：主要轉換

這是預設模式。從 `source_prompt` 抽取可見畫面意圖與明示限制，改寫成 GPT Image 2.5 可直接理解的自然語言。使用 [轉換模式](prompting-patterns.md) 整理必要內容，但不得用模板補入來源沒有的創作設定。

把來源工具的提示詞語意、執行控制、參考資產與未知語法分開處理：

1. 保留所有明示且不矛盾的畫面需求。
2. 只有來源與語法意義已有依據時才映射專有控制。
3. 將 GPT Image 2.5 操作面確實暴露的對應控制放入 request settings，不將來源旗標或節點字串原樣貼進提示詞。
4. 沒有直接等價時標示 `no_direct_equivalent`；意義不明時標示 `unresolved`，不猜測。
5. 來源若是已相容且清楚的舊 GPT Image 自然語言提示詞，可原樣通過，`changes: []`。

Physical Realism v2 只是一個可選 `conversion_profile`。不要靜默套用；使用時需記錄它改了什麼，也要能從結果追溯到未套用設定檔前的遷移判斷。

## `migration_baseline`：可選公平比較

只在使用者要求比較，或需要實證判斷轉換是否有幫助時使用。它是主要轉換的補充，不取代 `converted_prompt`。

GPT Image 2.5 基準輪使用未改寫的 `source_prompt`，且 `baseline_prompt` 必須與來源逐字相同、`baseline_changes: []`。再以同一個 GPT Image 2.5 操作面和可比較設定測試 `converted_prompt`。若來源系統也可執行，可另外保留來源系統輸出作參考，但不要把跨平台無法對齊的設定說成相同。

只固定真正可比的參考圖、尺寸或比例、品質層級、背景、格式、重複次數與評分準則。來源端的 stylize、CFG、steps、LoRA、prompt upsampling 等控制若無直接等價，記錄為非等價變因，不放入 GPT Image 2.5 提示詞。保存完整輸入、輸出、失敗、延遲與成本資料；未實際執行時只交付測試計畫。

## `migration_repair`：失敗後修復

只有以下三項都存在時才能使用：原始 `source_prompt`、先前的 `converted_prompt`，以及具體且已觀察到的失敗證據。證據可以是成圖、測試紀錄，或使用者對實際輸出的明確描述。若尚未做過轉換，回到 `migration_convert`；若沒有觀察到失敗，不把偏好性擴寫包裝成修復。

先把每個失敗對回來源中的保留要求，再只修正造成失敗、遺漏或歧義的部分。保留未失敗的內容與已確認的來源語意。修復不能藉機加入來源沒有的新主體、身份、場景或風格，也不能用猜測的來源語法作理由。

交付 `prior_converted_prompt`、`failure_evidence`、修復後的 `converted_prompt` 與逐項變更理由。沒有再次生圖就不得宣稱修復已通過。
