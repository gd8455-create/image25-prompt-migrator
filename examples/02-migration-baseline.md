# Migration baseline：既有 prompt 首輪原樣通過

本例展示 Migrator 如何保存既有工作流的 baseline。第一輪的唯一變數是模型；來源 prompt 已能清楚表達畫面與文字需求，因此原樣通過並回報 `changes: []`。這也說明不是每份 prompt 都必須改寫。

## 原始請求

> 我要把這份既有的 `gpt-image-1` 工作流遷移到 `gpt-image-2.5-flare`。請先建立 baseline：首輪只切換模型，prompt、品質、尺寸、背景和格式都不准改，每個模型各跑四次。若 prompt 不需要先轉換，請原樣通過並回報 `changes: []`。先交付基準設定與驗收表，不要假裝已經跑過。

## 原始輸入

```text
Create a vertical editorial poster for a fictional coffee brand. Center one matte navy coffee bag on a pale stone plinth, viewed straight on. A small ceramic cup sits to the bag's right and casts a soft shadow to the left. Warm morning light enters from the upper right; the background is muted terracotta. Render the exact headline “ORBITAL COFFEE” once at the top in large cream uppercase sans-serif letters. Render the exact line “ROASTED FOR SLOW MORNINGS.” once below it in smaller cream uppercase letters. Keep both lines fully readable. Do not add any other words, labels, logos, signatures, or watermarks.
```

原始 request settings：

```yaml
model: gpt-image-1
quality: high
size: 1024x1536
background: opaque
output_format: png
```

## 實際交付輸出

### Mode

`migration_baseline`

### Source classification

```yaml
source_origin: older_image_model
source_tool: gpt-image-1
target: GPT Image 2.5
conversion_profile: none
```

### Source prompt

```text
Create a vertical editorial poster for a fictional coffee brand. Center one matte navy coffee bag on a pale stone plinth, viewed straight on. A small ceramic cup sits to the bag's right and casts a soft shadow to the left. Warm morning light enters from the upper right; the background is muted terracotta. Render the exact headline “ORBITAL COFFEE” once at the top in large cream uppercase sans-serif letters. Render the exact line “ROASTED FOR SLOW MORNINGS.” once below it in smaller cream uppercase letters. Keep both lines fully readable. Do not add any other words, labels, logos, signatures, or watermarks.
```

### Migration decision

首輪原樣通過。來源 prompt 的主體、構圖、光線、必要文字與排除條件已可直接用於等條件比較；為避免同時改動模型與文字，本輪不做重寫。

### Converted prompt

```text
Create a vertical editorial poster for a fictional coffee brand. Center one matte navy coffee bag on a pale stone plinth, viewed straight on. A small ceramic cup sits to the bag's right and casts a soft shadow to the left. Warm morning light enters from the upper right; the background is muted terracotta. Render the exact headline “ORBITAL COFFEE” once at the top in large cream uppercase sans-serif letters. Render the exact line “ROASTED FOR SLOW MORNINGS.” once below it in smaller cream uppercase letters. Keep both lines fully readable. Do not add any other words, labels, logos, signatures, or watermarks.
```

### Baseline prompt

```text
Create a vertical editorial poster for a fictional coffee brand. Center one matte navy coffee bag on a pale stone plinth, viewed straight on. A small ceramic cup sits to the bag's right and casts a soft shadow to the left. Warm morning light enters from the upper right; the background is muted terracotta. Render the exact headline “ORBITAL COFFEE” once at the top in large cream uppercase sans-serif letters. Render the exact line “ROASTED FOR SLOW MORNINGS.” once below it in smaller cream uppercase letters. Keep both lines fully readable. Do not add any other words, labels, logos, signatures, or watermarks.
```

`baseline_prompt`、`converted_prompt` 與 `source_prompt` 逐字相同。

### Changes

`[]`

首輪零改寫。`converted_prompt` 與 `source_prompt` 完全相同；沒有清理措辭、調整文字引號或新增限制。

### Baseline changes

`[]`

### Preserved requirements

- 海軍藍霧面咖啡袋置中、正面視角、淡色石台。
- 陶杯位於咖啡袋右側，柔和陰影向左。
- 右上方暖晨光與低彩度陶土色背景。
- 兩個必要字串的內容、次數、相對位置、大小、字體類型與顏色。
- 除登記文字以外不得新增任何文字、標籤、Logo、簽名或浮水印。

### Required rendered text

| 字串 | 次數 | 位置 | 樣式 | 例外關係 |
| --- | ---: | --- | --- | --- |
| `ORBITAL COFFEE` | 1 | 上方 | 大號、奶油色、大寫無襯線字 | 是「不得新增其他文字」的必要例外 |
| `ROASTED FOR SLOW MORNINGS.` | 1 | 標題下方 | 較小、奶油色、大寫字 | 是「不得新增其他文字」的必要例外；句點必須保留 |

### Reference roles

無；本基準沒有參考圖片。

### Source syntax handling

- 來源 prompt 是清楚的自然語言，沒有需要移除的第三方旗標、權重或節點語法。
- 原始 API controls 已和 prompt 分開，並在下方列為比較設定。
- `high` 等同出現在兩組請求中，只代表送出的品質標籤相同；最終畫質仍須由實際輸出評估。

### Request settings

來源系統參考 A 與 GPT Image 2.5 baseline B 只有 `model` 欄位不同：

| 設定 | 基準 A | 基準 B |
| --- | --- | --- |
| `model` | `gpt-image-1` | `gpt-image-2.5-flare` |
| `quality` | `high` | `high` |
| `size` | `1024x1536` | `1024x1536` |
| `background` | `opaque` | `opaque` |
| `output_format` | `png` | `png` |
| 重複次數 | 4 | 4 |

每次執行都保存完整 prompt、request settings、輸出識別資訊、延遲、成功或失敗、可取得的成本資料，以及人工 QA 結果。若執行環境還有會影響輸出的明示控制項，也必須一併記錄；無法跨模型對齊的控制應標為非等價變因，而不是假裝相同。

### QA／驗收

以下項目要對兩個模型的每張實際輸出逐一檢查，目前均為待執行：

- [ ] 主體數量、位置、正面視角與杯子相對位置符合提示詞。
- [ ] 材質和色彩符合霧面海軍藍咖啡袋、淡色石台、陶土色背景。
- [ ] 光線從右上方進入，杯子陰影向左，沒有明顯方向矛盾。
- [ ] `ORBITAL COFFEE` 逐字正確、只出現一次、位於上方且可讀。
- [ ] `ROASTED FOR SLOW MORNINGS.` 逐字正確、只出現一次、位置正確且保留句點。
- [ ] 沒有額外文字、標籤、Logo、簽名或浮水印。
- [ ] 每組四次執行都有完整設定、延遲、失敗與成本紀錄。
- [ ] 比較結論涵蓋四次輸出的變異，而不是只挑最好的一張。

### Unresolved

無。

## 後續受控變體

完成上述基準後，若實際結果顯示有待改善，才能測試轉換變體。每個後續變體應先寫出單一假設，例如「將必要文字改成獨立登記區塊，是否提高逐字正確率」，並保持其他條件不變。沒有實際輸出前，不得寫成已證實改善。

## 驗證界線

此文件建立的是可執行的遷移 baseline，沒有呼叫任何模型。`source_prompt`、`converted_prompt` 與 `baseline_prompt` 在文字內容上相同；QA、延遲、成本與四次輸出比較仍需實際執行後填寫。`changes: []` 只表示首輪沒有文字變更，不代表 GPT Image 2.5 的輸出已通過驗收。
