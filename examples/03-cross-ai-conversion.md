# Cross-AI conversion：將其他 AI 產出的工具 prompt 遷移到 GPT Image 2.5

本例從另一個 AI 助手為第三方影像工具產出的既有 prompt 開始。來源文字混合權重符號、負面提示詞與工具參數；Migrator 只做遷移，不重新發想商品、場景或文案，也不宣稱來源參數在 GPT Image 2.5 中有一對一等價物。

## 原始請求

> 另一個 AI 助手給了我下面這份香水海報 prompt，原本要貼到另一套影像生成工具。請轉成 GPT Image 2.5 可測試的版本。保留單一透明香水瓶、雨後黑石桌面、背後圓形暖光、墨綠背景、直式 2:3，以及標題 `AFTER RAIN`。不要自行增加花朵、人物或新文案。目標使用 `gpt-image-2.5-sunburst`、高品質、1024×1536、不透明 PNG。來源工具參數若沒有可靠對應，請明確標記，不要猜。

## 原始輸入

```text
PROMPT:
premium fragrance campaign poster::2, one transparent rectangular perfume bottle centered on a wet black-stone table::1.5, circular warm halo behind bottle, deep forest-green background, luxury editorial, hyperreal, masterpiece, 8k, dramatic cinematic reflections, razor sharp, product label clean, headline "AFTER RAIN" at top, no other copy

NEGATIVE PROMPT:
people, hands, flowers, extra bottles, duplicate product, warped glass, unreadable label, extra words, logo, watermark

PARAMETERS:
--ar 2:3 --stylize 750 --chaos 8 --seed 4412
```

來源：另一個 AI 助手為未指定版本的第三方影像工具產出的文字。沒有參考圖片，也沒有來源輸出可供比較。

## 實際交付輸出

### Mode

`migration_convert`

### Source classification

```yaml
source_origin: other_image_ai
source_tool: unknown
target: GPT Image 2.5
conversion_profile: physical_realism_v2
```

來源被確認為另一個 AI 助手為第三方影像工具產出的 prompt，但產品與版本未提供，因此不從旗標外觀猜測工具名稱。

### Migration decision

需要轉換。視覺需求可以保留，但 `::2`、`::1.5`、`NEGATIVE PROMPT` 與 `--...` 參數是來源格式的一部分，不能直接假設 GPT Image 2.5 會以相同方式解讀。

### Converted prompt

```text
用途：直式高級香水廣告海報。

主體與構圖：
畫面中央只有一個透明、長方形的香水瓶，正面朝向鏡頭，完整瓶身清楚可見。香水瓶放在雨後潮濕的黑色石材桌面上。瓶後有一個圓形、柔和的暖色光暈；背景是均勻而低彩度的深墨綠色。保持簡潔、對稱的精品編輯式構圖，商品是唯一視覺主體。

材質與光線：
玻璃保持筆直、對稱且透明，瓶身邊緣有受控高光。桌面只在接觸面與低窪處呈現合理濕度，反射對應香水瓶與後方圓形光源，不讓所有表面同時產生強烈亮點。瓶底與桌面有可信的接觸陰影。

必要文字：
在畫面上方水平置中，只呈現一次以下標題，逐字保持大小寫與空格：
"AFTER RAIN"
文字清楚可讀，與商品保持足夠間距。

限制：
畫面不得出現人物、手、花朵、額外香水瓶、重複商品、新文案、額外文字、Logo、簽名或浮水印。不得扭曲瓶身幾何或讓玻璃標籤變成無法辨識的亂碼。
```

### Changes

- 保存來源 prompt，並將 `::2` 與 `::1.5` 的權重寫法改成「商品是唯一視覺主體」及明確的置中、正面、完整瓶身要求。
- 將獨立的 `NEGATIVE PROMPT` 內容合併為普通限制句，保留人物、花朵、重複商品、額外文字與浮水印等排除意圖。
- 刪除 `masterpiece`、`8k`、`hyperreal`、`razor sharp` 等品質詞堆疊，改成可見的玻璃幾何、桌面濕度、反射、接觸陰影與文字可讀性要求。
- 將來源 `--ar 2:3` 的構圖意圖保留為直式 2:3，並以目標 request setting `1024x1536` 表達。
- `--stylize 750`、`--chaos 8` 與 `--seed 4412` 只保留在來源紀錄，沒有被宣稱或換算成 GPT Image 2.5 的等價參數。
- 沒有新增商品、場景物件、人物、文案、參考圖片或新的創意方向。

### Preserved requirements

- 單一透明長方形香水瓶，置中、正面、完整可見。
- 雨後潮濕的黑色石材桌面、瓶後圓形暖光與深墨綠背景。
- 直式 2:3、高級精品編輯式海報。
- `AFTER RAIN` 只出現一次且位於上方。
- 不得出現人物、手、花朵、額外瓶子、新文案、Logo 或浮水印。

### Required rendered text

| 字串 | 次數 | 位置 | 樣式 |
| --- | ---: | --- | --- |
| `AFTER RAIN` | 1 | 畫面上方水平置中 | 清楚可讀，保持大寫與原有空格 |

必要文字以外的內容不得出現在畫面中。

### Reference roles

無；來源沒有提供參考圖片。若實際遷移時附有產品圖，必須另外登記其角色與必須保留的瓶身、標籤及比例。

### Source syntax handling

```yaml
source_tool: unspecified_third_party_image_generator
source_syntax:
  aspect_ratio: "--ar 2:3"
  stylize: "--stylize 750"
  chaos: "--chaos 8"
  seed: "--seed 4412"
mapping_status:
  aspect_ratio: intent_preserved_in_target_size
  stylize: no_direct_equivalent
  chaos: no_direct_equivalent
  seed: no_direct_equivalent
```

### Request settings

```yaml
model: gpt-image-2.5-sunburst
operation: image_generation
quality: high
size: 1024x1536
background: opaque
output_format: png
```

### QA／驗收

以下項目要在實際生成後檢查，目前均為待驗證：

- [ ] 畫面只有一個香水瓶，置中、正面且完整可見。
- [ ] 瓶身為透明長方形，玻璃邊緣與標籤沒有明顯幾何扭曲。
- [ ] 黑色石桌的濕度與反射集中且能對應瓶身、暖色光暈與接觸位置。
- [ ] 圓形暖光位於瓶後，背景維持深墨綠且沒有新增裝飾物。
- [ ] `AFTER RAIN` 拼字、大小寫與空格正確，只出現一次且位於上方。
- [ ] 沒有人物、手、花朵、額外瓶子、重複商品、額外文字、Logo、簽名或浮水印。
- [ ] 輸出檔案確為 1024×1536 的不透明 PNG。
- [ ] 結果以實際畫面驗收，不把來源的 `stylize`、`chaos` 或 `seed` 當成已被等價重現。

### Unresolved

- 來源未標明第三方工具與版本，因此其權重與參數的原始語意無法完整驗證。
- `product label clean` 沒有提供瓶身標籤的逐字內容。遷移稿只要求標籤不要成為明顯亂碼；若標籤文字必須精確，使用者需要補充原文或參考圖。

## 驗證界線

這份範例只完成跨 AI 來源 prompt 的文字遷移，尚未呼叫 GPT Image 2.5，也沒有第三方來源輸出可做 A/B 比較。QA、文字正確率、玻璃幾何與光線效果仍需實際生成後檢查。本例只展示一種混合格式的處理方式，不代表完整支援所有工具、版本或參數。
