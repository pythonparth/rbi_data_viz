# RBI Liquidity Analysis & USD/INR Overlay

A reproducible, data-driven analysis of India’s monetary liquidity and external cushion from 2000–2025.  
This project visualizes **Currency in Circulation (CiC)**, **Broad Money (M3)**, **Net Foreign Exchange (FX) Assets**, and overlays **USD/INR** to interrogate when and why the rupee weakens.

---

## 📌 Introduction

The project began with a simple observation: **CiC grew more than threefold after 2017**.  
To avoid a one-dimensional view of liquidity, we added **M3** (to capture deposits) and **Net FX Assets** (RBI + commercial banks), then overlaid **USD/INR**.  
The result is a multi-layer macro dashboard connecting domestic liquidity composition to the rupee’s behavior.

**Goal:** Turn descriptive plots into an analytical tool that reveals the timing and mechanisms behind rupee moves.  
**Core lens:** Compare domestic liquidity growth (CiC, M3, and the gap `M3 − CiC`) against changes in Net FX Assets and market outcomes (USD/INR).

---

## 📊 Data Sources

- **RBI Monetary Aggregates:** Annual CiC and M3, 2000–2025.
- **Net FX Assets:**
  - Central bank: *Net Foreign Exchange Assets of the Central Bank*
  - Commercial banks: *Net Foreign Assets of Commercial Banks*
  - Combined and differenced to obtain annual change.
- **USD/INR:** Annual average or year-end rate.

> All monetary values expressed in ₹ Lakh crores.

---

## ⚙️ Methodology

1. **Series Preparation**
   - Resample to annual frequency.
   - Normalize units to ₹ Lakh crores.
   - Compute `fx_change` as YoY difference of combined FX assets.

2. **Key Constructs**
   - **Liquidity gap (bank money):**  
     `Gap = M3 − CiC` → approximates deposits and other non-cash components.
   - **Ratios (optional):**  
     `FX / M3` and `FX / CiC` → falling ratios signal external cushion not keeping pace.

3. **Correlation Snapshot**
   - Compute `pct_change` for M3, FX Assets, and USD/INR.
   - Build correlation matrix to test co-movements.
   - Weak full-period correlations → regime-specific dynamics dominate.

---

## 📈 Chart Layers

- **CiC line:** Physical notes/coins held by the public.
- **M3 line:** CiC + deposits + other liquid liabilities.
- **Net FX Asset change bars:** Annual change in combined RBI + commercial bank FX assets.
- **USD/INR (secondary y-axis):** Market outcome.

**Styling:**
```python
ax1.bar(fx_change.index, fx_change.values, color='purple', alpha=0.3, label='Net FX Asset Change')
ax1.legend(loc="upper left", fontsize=10)
```
---

## 🔍Key Insights

- Deposits expanding faster than cash:
Post‑2017, the gap (M3 − CiC) widens sharply → structural shift toward banked liquidity.
- Healthy in isolation, but in this dataset FX reserves growth lagged.
- FX cushion mismatch:
M3 growth outpaced Net FX Asset change by large margins in multiple years.
- Domestic liquidity expansion not proportionately backed by external assets → potential currency pressure.
- Regime-driven vulnerability:
Depreciation phases (USD/INR upswings) align with weak FX cushion during strong domestic liquidity growth.
- Patel era fingerprint:
CiC growth rate tripled post‑2017, deposits grew even faster → broad-based liquidity push.

<img width="1241" height="784" alt="image" src="https://github.com/user-attachments/assets/541af988-0ac0-455f-ae1c-7603924316ab" />

