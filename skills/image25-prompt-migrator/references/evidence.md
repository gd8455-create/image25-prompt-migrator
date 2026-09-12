# 查證與主張界線｜2026-09-12

只在需要說明模型能力、平台差異、來源語法或方法依據時讀取。一般遷移依 [來源轉接原則](source-adapters.md) 即可。

## GPT Image 2.5 官方來源

- OpenAI Image prompting
  https://developers.openai.com/api/docs/guides/image-prompting
- OpenAI Image generation
  https://developers.openai.com/api/docs/guides/image-generation
- GPT Image 2.5 Sunburst
  https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst
- GPT Image 2.5 Flare
  https://developers.openai.com/api/docs/models/gpt-image-2.5-flare

官方文件支持以文字及圖片輸入進行生成或編輯，並把 model、quality、尺寸、背景和格式等 API 控制與畫面提示分開。本技能因此固定遷移目標為 GPT Image 2.5，將畫面語意放在 `converted_prompt`，將已暴露控制放在 request settings。

Flare 與 Sunburst 是 GPT Image 2.5 的 API model ID。使用者只指定 GPT Image 2.5、但未選操作面或型號時，不替他猜一個 ID。ChatGPT 介面與 API 可用控制可能不同，API 參數不能寫成所有介面的保證。

## 來源工具官方文件

- Midjourney parameters
  https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List
- Midjourney Stylize
  https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize
- ComfyUI text-to-image workflow
  https://docs.comfy.org/tutorials/basic/text-to-image
- ComfyUI LoRA workflow
  https://docs.comfy.org/tutorials/basic/lora
- Stability AI API reference
  https://platform.stability.ai/docs/api-reference
- Black Forest Labs FLUX prompting
  https://docs.bfl.ai/guides/prompting_summary
- Black Forest Labs FLUX.2 prompting and prompt upsampling
  https://docs.bfl.ai/guides/prompting_guide_flux2
- Google Gemini image generation
  https://ai.google.dev/gemini-api/docs/image-generation
- Microsoft Copilot image generation
  https://support.microsoft.com/en-us/microsoft-copilot/using-image-generation-in-microsoft-copilot

這些來源只能證明各工具自己的提示方式或控制含義，不能證明它們與 GPT Image 2.5 一對一相容。版本未確認、文件未涵蓋或來源不明時，必須標示 unknown 或 no direct equivalent。

## 遷移方法的界線

- `migration_convert` 是本技能設計的語意轉換方法，不是 OpenAI 或其他供應商發布的官方轉換器。
- 舊 GPT Image 自然語言提示詞允許原樣通過，是保守遷移策略，不保證不同模型生成相同圖片。
- `migration_baseline` 的公平性來自公開可比條件、逐字不變的來源提示詞和一致評分方式。跨平台專有參數無法對齊時必須揭露。
- `migration_repair` 只能依來源要求與已觀察失敗修復。成圖、測試紀錄，或使用者對實際輸出的明確失敗描述都可作證據；尚未生成或只有假設性風險時，只能提出驗證項目。
- Physical Realism v2 是本技能提供的可選 conversion profile，不是官方固定順序、模型 token 或負面提示上限。

未執行的 A/B 測試不得寫成已通過。也不要在沒有專門市場查證時宣稱本技能是唯一、第一個或沒有同類工具；可以準確說明它的範圍是把既有提示詞保守遷移到 GPT Image 2.5。
