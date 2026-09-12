# Examples

這裡提供三份既有 prompt 的遷移交付範例，以及一份真實的單次圖片驗收紀錄。所有範例都從已存在的圖片生成或編輯 prompt 開始；不示範從空白需求撰寫新 prompt。

| 範例 | 遷移情境 | 重點 |
| --- | --- | --- |
| [舊版提示詞轉換](01-legacy-conversion.md) | Legacy conversion | 把含有舊式品質詞堆疊的既有 prompt 轉為 GPT Image 2.5 候選稿，同時保留人物、年代、動作與構圖。 |
| [遷移 baseline](02-migration-baseline.md) | Baseline / pass-through | 第一輪只切換模型；來源 prompt 與其他輸入完全不變，`changes: []`。 |
| [跨 AI 提示詞轉換](03-cross-ai-conversion.md) | Cross-AI conversion | 將其他 AI 助手為另一影像工具產出的既有 prompt 轉為 GPT Image 2.5 指令，不捏造工具參數的一對一對應。 |
| [轉換工作流的單次視覺驗收](04-built-in-generation-evaluation.md) | Visual check | 比較來源 prompt 與遷移稿，記錄第一次 QA 失敗，再以後續編輯修正背景人物。 |

## 如何閱讀

前三份文字範例都包含：

1. 原始請求與來源 prompt。
2. Skill 應交付的遷移稿或原樣通過結果。
3. `Changes`、`Request settings`、保留條件與生成後 QA。
4. 無法確認的來源語法或仍待使用者決定的 `Unresolved`。
5. 清楚的驗證界線。

不需要轉換的 prompt 也是有效結果。第二份範例刻意保留來源內容，顯示 Migrator 應在 baseline 或已相容情況回報 `changes: []`，而不是為了產生差異而強制改寫。

第四份報告確實使用 Codex 內建圖片生成工具各執行一次，保存 prompt、三張輸出、檔案雜湊、尺寸、目視驗收與圖像差異結果。工具沒有公開確切的後端模型名稱、seed 或取樣設定，因此這份報告是 conversion workflow 的視覺檢查，不是 GPT Image 2.5 API 的受控基準。

第一次遷移稿結果仍出現被禁止的遠景人物，該項明確記為未通過；後續編輯移除背景人物後通過目視驗收，但未編輯區域並非像素完全相同。單次結果不能證明每次生成都會相同，也不能證明遷移稿普遍優於來源 prompt。
