# 完整案例導覽：從三條 PDE 到可審查的財金研究

這份導覽不是把最終研究計畫倒推成一個看似順利的故事，而是保留真正重要的轉折：刪除不需要的構想、縮小問題、接受審查攻擊、修補識別，並在沒有實證結果時停在誠實的 partial research plan。

## 起點

使用者最初關心 Laplace、heat 與 wave equation 是否可以放入金融預測，並曾考慮 Maxwell–Boltzmann 分配。這個起點同時包含：

- 一個跨領域數學工具；
- 尚未確定的金融現象；
- 未固定的 dependent variable；
- 不明確的資料需求；
- 可能把數學類比誤當經濟機制的風險。

若此時直接產生論文，文字可以很完整，但研究設計沒有可辨識性。

## 第一個關鍵決策：排除不需要的分支

使用者明確排除：

- Maxwell–Boltzmann；
- 訂單簿；
- 難以取得的高頻微觀資料。

Research OS 必須把這些限制寫入 context／decision，而不是只在當下回答中表示理解。後續 novelty、data 或 methodology 分支都不能悄悄把它們加回來。

對應 artifacts：

- [CONTEXT.md](.research/CONTEXT.md)
- [RDR-0001](.research/decisions/RDR-0001-scope-and-destination.md)

## 第二個關鍵決策：把漂亮敘事改成競爭性問題

原本最吸引人的敘事是：

```text
Wave → Diffusion → Equilibrium
```

但如果模型預先規定這個順序，最後觀察到相同順序並不是發現，而是模型設計的結果。修正後的核心問題改為：

> 全球股市波動衝擊究竟呈現有限速度的阻尼傳播，還是一般擴散？兩者能否由資料中的可拒絕限制區分？

Laplace relation 不再被強迫當作第三個可觀察 regime，而是作為去除 common mode 後的長期邊界條件。

對應 artifact：

- [Research Brief](.research/briefs/financial-wave-diffusion.md)

## 第三個關鍵決策：定義金融空間

物理 PDE 的空間距離通常固定且外生；金融網路的距離可能來自相關性、地理、時區、貿易或共同持倉。如果用同一批報酬估計相關性網路，再用該網路證明報酬衝擊沿網路傳播，就可能循環論證。

因此本案例把非同步交易與時間對齊列為核心識別威脅，而不是附錄中的 robustness check。候選網路必須有可辯護的外生或預先決定語義。

對應 artifacts：

- [RDR-0002](.research/decisions/RDR-0002-common-mode-and-equilibrium.md)
- [Model-separation protocol](.research/pilots/model-separation-protocol.md)

## 第四個關鍵決策：Wave 不能只靠 lag 判定

在離散時間式中加入落後變數，不足以證明 wave-like propagation。它也可能只是自我相關、二階 VAR 或 delayed diffusion。

因此 pilot 必須檢查至少一組能區分模型的限制，例如：

- 距離與首次顯著反應時間；
- graph spectral mode 的單調衰減或阻尼震盪；
- 模態頻率與 Laplacian eigenvalue 的系統關係；
- 有限傳播速度是否超越交易時區造成的機械落後；
- telegraph model 相對 diffusion、VAR 或 network autoregression 的樣本外增額表現。

如果這些限制在實際對齊資料上無法區分兩個模型，研究應 repair 或 kill，而不是把 persistence 重新命名為 wave。

## 第五個關鍵決策：沒有實證結果就不寫結果

目前案例的文獻邊界、完整對齊資料與 model-separation pilot 尚未完成。因此：

- novelty claim 維持 blocked；
- 研究計畫狀態為 conditional／partial；
- 沒有係數、顯著性、預測改善或穩健性結果；
- milestones 使用 evidence gates，而不是虛構日期。

對應 artifacts：

- [Claims ledger](.research/evidence/claims.yaml)
- [Reviewer pre-mortem](.research/reviews/referee-pre-mortem.md)
- [Academic research plan](.research/plans/PLAN-0001-financial-wave-diffusion.md)

## 從這個案例如何開始自己的研究？

可以直接使用：

```text
/research-auto

我想把[方程式／理論／其他領域概念]用於[領域]，
最後形成[研究計畫／proposal／paper blueprint]。
不要先假設它是新理論。請先檢查符號、單位、機制、
closest literature，以及資料能否區分它和普通替代模型。
限制：[資料、時間、排除項目]。
```

真正的成功條件不是保住原始構想，而是最後知道哪一部分值得留下、哪一部分必須刪除，以及剩下的研究如何被資料推翻。
