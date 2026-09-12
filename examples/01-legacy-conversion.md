# Legacy conversion：將舊式雨後街頭 prompt 遷移到 GPT Image 2.5

本例從一份已存在、帶有舊式品質詞與寫實詞堆疊的 prompt 開始。遷移目標是保留原有場景、人物與構圖，同時把來源文字轉成可供 GPT Image 2.5 測試的版本；這不是從空白需求重新創作。

## 原始請求

> 請把下面這份已在舊工作流使用的提示詞遷移到 GPT Image 2.5。人物動作、十九世紀末倫敦、雨後街道、煤氣燈冷暖對比和直式 4:5 構圖都要保留。不要新增人物或改成棚拍。目標 request settings 是 API 的 `gpt-image-2.5-flare`、高品質、1536×1920、PNG、不透明背景。沒有參考圖片，也沒有要生成的文字。請列出實質變更，不要宣稱生成結果一定改善。

## 原始輸入

```text
Create a portrait-oriented 4:5 photorealistic street photograph for a public prompt-engineering comparison example. An adult woman stands on a late-19th-century London street after rain, her body turned about 60 degrees to the camera, right hand lightly touching a small period-inspired earpiece, left hand in her trouser pocket, with gas lamps behind her. 8K masterpiece ultra realistic IMAX HDR, raw, natural imperfections, physics imperfections, wet Victorian street, wet iron railings, wet brick walls, wet clothing, every surface covered in water droplets, ultra-detailed reflective textures everywhere, countless individual flyaway hair strands, cinematic lighting, extreme sharpness, intense micro-contrast. No captions, labels, signatures, logos, or watermarks. This is the deliberately overloaded ORIGINAL prompt sample; follow it as written rather than improving its wording.
```

## 實際交付輸出

### Mode

`migration_convert`

### Source classification

```yaml
source_origin: unknown
source_tool: unknown
target: GPT Image 2.5
conversion_profile: physical_realism_v2
```

使用者只確認這是舊工作流 prompt，沒有指定來源模型或工具，因此 `source_origin` 與 `source_tool` 都保持 `unknown`；不從詞彙堆疊反推來源產品。

### Migration decision

需要轉換。來源 prompt 含有 `8K`、`masterpiece`、`ultra realistic`、`IMAX HDR`、`raw`、全面水珠、極端銳化與強烈微對比等堆疊描述；這些內容會在遷移稿中被刪除或轉成可見、可驗收的場景關係。若沒有這些待處理項目，本 Skill 也可以原樣通過並回報 `changes: []`。

### Converted prompt

```text
一張寫實的直式 4:5 街頭攝影照片，用於公開的提示詞工程比較範例。十九世紀末的倫敦，一名成年女性站在雨後街道的鐵欄杆旁，身後可見煤氣燈。她的身體約六十度側向鏡頭，右手輕碰一個具有時代感的小型耳部裝置，左手自然放在褲袋裡；姿態像攝影師在街頭捕捉到的短暫瞬間。畫面只有這一名人物。

雨剛停。街道路面的水主要積在鋪面接縫與低窪處，較高位置只保留局部潮濕色澤。鐵欄杆維持表面平整的金屬本質，垂直表面有少量向下水痕；只有直接面對煤氣燈並符合反射角的位置出現較大的暖色亮部。磚牆維持普通老磚材質，不刻意強調每一處紋理。

人物的衣物因剛淋雨而局部受潮，受潮處顏色略深，布面不形成密集亮點。髮型先呈現受重力影響的主要自然髮束；靠近臉頰、耳側與肩膀接觸處只有少量因濕氣黏附的散髮，不讓整頭頭髮同時飄動。

陰天提供冷色環境光，身後煤氣燈提供局部暖色光；暖光只作用在朝向燈源的輪廓、欄杆和潮濕區域，冷暖交界依物體朝向自然形成。焦點在人物，背景適度柔化，保留正常攝影影調與自然鏡頭對比。

可見差異來自材質、重力、接觸、濕度或光照。不要為了顯得真實而增加滿布畫面的水珠、刮痕、髒污、裝飾性顆粒或極端銳化；不要出現現代街道物件、額外人物、文字、Logo 或浮水印。
```

### Changes

- 將這份既有 prompt 判定為需要 legacy conversion；保留原稿供前後比較。
- 刪除 `masterpiece`、`8K`、`ultra realistic` 與 `IMAX HDR` 等重複品質詞；實際輸出尺寸移至 request settings。
- 將 `raw`、`natural imperfections` 與 `physics imperfections` 的抽象要求改成可見的重力、接觸、濕度、材質和光照關係。
- 保留「剛淋雨」的情節，將 `wet everything` 改為石縫積水、垂直水痕、局部受潮與符合角度的反射。
- 先定義髮束的整體重量，再限制因濕氣與接觸形成的少量散髮。
- 將全面水珠、極端銳化與強烈微對比改成場景相關限制，避免每個表面都被強制增加紋理。
- 保留人物、動作、時代、地點、煤氣燈冷暖對比與直式 4:5 攝影意圖。

### Preserved requirements

- 單一成年女性；不得新增人物。
- 身體約六十度側向鏡頭，右手碰具有時代感的小型耳部裝置，左手在褲袋。
- 十九世紀末倫敦雨後街道、鐵欄杆、石板路、磚牆與煤氣燈。
- 暖色煤氣燈和冷色環境光的對比。
- 寫實街頭抓拍、直式 4:5 構圖、人物清楚而背景柔化。

### Required rendered text

無。畫面不得新增文字、Logo 或浮水印。

### Reference roles

無；原始請求未提供參考圖片。

### Source syntax handling

| 來源內容 | 處理 | 理由 |
| --- | --- | --- |
| 直式 4:5 | 映射到構圖描述與 `1536x1920` request setting | 來源意圖與目標尺寸皆明確。 |
| `8K` | 不當作目標解析度 | 使用者已指定實際輸出尺寸；不把品質詞假裝成 API 解析度設定。 |
| `masterpiece`、`ultra realistic`、`IMAX HDR`、`raw` | 轉成或刪除 | 保留可見的寫實意圖，以材質、濕度、接觸、光源與影調描述取代堆疊。 |
| 來源模型或工具 | `unresolved` | 使用者沒有提供，不能由文字猜測。 |

### Request settings

```yaml
model: gpt-image-2.5-flare
quality: high
size: 1536x1920
background: opaque
output_format: png
```

### QA／驗收

以下項目要在實際生圖後檢查，目前均為待驗證：

- [ ] 畫面只有一名成年女性，動作與約六十度側身方向正確。
- [ ] 場景可辨識為十九世紀末倫敦，沒有現代交通標誌、車輛或電子街景物件。
- [ ] 積水集中在石縫與低窪，欄杆水痕向下，大衣只有合理的局部受潮。
- [ ] 欄杆沒有被生成成全面亮點，反射能對應煤氣燈方向。
- [ ] 頭髮以有重量的髮束為主，散髮數量有限且能由濕氣、接觸或重力解釋。
- [ ] 暖色煤氣燈與冷色環境光的作用範圍和物體朝向一致。
- [ ] 畫面沒有額外人物、文字、Logo、浮水印或裝飾性表面噪點。
- [ ] 輸出檔案確為 1536×1920、直式 4:5 的不透明 PNG。

### Unresolved

無。

## 驗證界線

這份範例只完成來源 prompt 的遷移與輸出契約檢查，尚未呼叫 GPT Image 2.5。QA 是可判定的驗收標準，不代表畫面已通過，也不能據此宣稱 converted prompt 一定優於 source prompt。Physical Realism v2 在此明示為可選 conversion profile，並非 OpenAI 官方規定或成功保證。
