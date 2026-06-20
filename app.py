import streamlit as st
import pandas as pd
import os

# ==========================================
# 1. 藥物計算邏輯定義區
# ==========================================

def logic_l01(age_years, weight_kg):
    """L01: 安佳熱糖漿"""
    if age_years >= 12: dose = "20 ~ 30 ml"
    elif 6 <= age_years < 12: dose = "10 ~ 15 ml"
    elif 3 <= age_years < 6: dose = "5 ~ 7.5 ml"
    else: dose = "⚠️ 3歲以下請洽醫師"
    return dose

def logic_l02(age_years, weight_kg):
    """L02: 舒抑痛 (同 L03，但保留原始邏輯作為對照)"""
    if age_years < 0.5: return "⚠️ 6個月以下請洽醫師"
    if weight_kg <= 0: return "⚠️ 請輸入體重"
    low, high = weight_kg * 0.25, weight_kg * 0.5
    return f"🌡️ ≤39°C: {low:.1f} ml\n\n🔥 >39°C: {high:.1f} ml"

def logic_l03(age_years, weight_kg):
    """L03: Ibuprofen Suspension 20mg/mL (Idofen)"""
    # 邏輯優先順序：體重 > 年齡
    if weight_kg >= 5.4:
        if 5.4 <= weight_kg <= 8.1: dose = "2.5 ml (50mg)"
        elif 8.2 <= weight_kg <= 10.8: dose = "3.75 ~ 4 ml (75~80mg)"
        elif 10.9 <= weight_kg <= 16.3: dose = "5 ml (100mg)"
        elif 16.4 <= weight_kg <= 21.7: dose = "7.5 ml (150mg)"
        elif 21.8 <= weight_kg <= 27.2: dose = "10 ml (200mg)"
        elif 27.3 <= weight_kg <= 32.6: dose = "10 ~ 12.5 ml (200~250mg)"
        elif 32.7 <= weight_kg <= 43.2: dose = "15 ml (300mg)"
        else: # 體重超過 43.2kg
            low, high = weight_kg * 0.25, weight_kg * 0.5
            dose = f"{min(low, 20.0):.1f} ~ {min(high, 30.0):.1f} ml"
    elif total_age_years >= 0.5: # 體重不足但有年齡 (>=6個月)
        if 0.5 <= age_years < 1: dose = "2.5 ml"
        elif 1 <= age_years < 2: dose = "3.75 ~ 4 ml"
        elif 2 <= age_years < 4: dose = "5 ml"
        elif 4 <= age_years < 6: dose = "7.5 ml"
        elif 6 <= age_years < 9: dose = "10 ml"
        elif 9 <= age_years < 11: dose = "10 ~ 12.5 ml"
        elif age_years == 11: dose = "15 ml"
        else: dose = "10 ~ 20 ml (200~400mg)"
    else:
        return "⚠️ 未滿6個月或體重不足 5.4kg，請洽醫師診治。"

    res = f"✅ 建議劑量: {dose}\n🕒 每 6 ~ 8 小時一次 (每日最多 4 次)"
    
    # 針對幼年型關節炎 (JIA) 的特別提示
    if weight_kg > 0:
        jia_low = (weight_kg * 30 / 3) / 20
        jia_high = (weight_kg * 40 / 3) / 20
        res += f"\n\n📖 JIA 參考 (每日3次): 每次 {jia_low:.1f} ~ {jia_high:.1f} ml"
    
    return res

def logic_l04(age_years, weight_kg):
    """L04: 希普利敏液"""
    if age_years < 2: return "⚠️ 2歲以下請洽醫師"
    if 2 <= age_years <= 6: base = "每次 5 ml (2mg)"
    elif 7 <= age_years <= 14: base = "每次 10 ml (4mg)"
    else: base = "14歲以上請參考醫囑"
    return base

def logic_l05(age_years, weight_kg):
    """L05: 息咳液"""
    if age_years >= 12: dose = "每次 10 ~ 20 ml"
    elif 6 <= age_years < 12: dose = "每次 6 ~ 10 ml"
    elif 2 <= age_years < 6: dose = "每次 2 ~ 6 ml"
    else: dose = "⚠️ 2歲以下請洽醫師"
    return dose

def logic_l06(age_years, weight_kg):
    """L06: 諾快寧口服懸液 (Curam)"""
    if weight_kg <= 0: return "⚠️ 請輸入體重以計算劑量。"
    hosp_dose = weight_kg * 0.5
    infant_q12 = (weight_kg * 15) / 62.5
    dose_45 = (weight_kg * 22.5) / 62.5
    dose_90 = (weight_kg * 45) / 62.5
    if age_years < 0.25:
        res = f"👶 <3個月嬰兒: 每次 {infant_q12:.1f} ml (Q12H)"
    else:
        res = (f"🏥 院內常用: 每次 {hosp_dose:.1f} ml (Q8H)\n\n"
               f"📖 依適應症參考 (Q12H):\n"
               f"- 鼻竇炎/輕中度: 每次 {dose_45:.1f} ml\n"
               f"- 中耳炎/肺炎: 每次 {dose_90:.1f} ml")
    if weight_kg >= 40: res += "\n\n⚠️ 體重已達 40kg，請考慮改用成人劑量。"
    return res

def logic_l07(age_years, weight_kg):
    """L07: 鼻解糖漿"""
    if age_years >= 12:
        dose = "每次 10 ml"
        max_d = "40 ml (4次)"
    elif 6 <= age_years < 12:
        dose = "每次 5 ml"
        max_d = "20 ml (4次)"
    else: return "⚠️ 6歲以下請洽醫師"
    return f"✅ {dose}\n🕒 每 4~6 小時一次\n⚠️ 每日最大: {max_d}"

LOGIC_MAP = {
    "L01_Logic": logic_l01,
    "L02_Logic": logic_l02,
    "L03_Logic": logic_l03, # Ibuprofen
    "L04_Logic": logic_l04,
    "L05_Logic": logic_l05,
    "L06_Logic": logic_l06, # Curam
    "L07_Logic": logic_l07,
}

# ==========================================
# 2. 資料讀取 (加強防呆版)
# ==========================================

def load_medication_db():
    file_path = "meds.xlsx"
    if not os.path.exists(file_path):
        st.error(f"❌ 找不到 {file_path}")
        return None
    try:
        df = pd.read_excel(file_path, engine='openpyxl').fillna("")
        db = {}
        for _, row in df.iterrows():
            loc = str(row['Location']).strip()
            if not loc: continue
            db[loc] = {
                "trade_name": str(row['Trade_Name']),
                "chinese_name": str(row['Chinese_Name']),
                "note": str(row['Note']),
                "logic_type": str(row['Logic_Type'])
            }
        return db
    except Exception as e:
        st.error(f"❌ 讀取錯誤: {e}")
        return None

# ==========================================
# 3. 網頁介面
# ==========================================
st.set_page_config(page_title="藥物劑量計算系統", page_icon="💊")
st.title("💊 兒童藥物劑量計算系統")

col1, col2, col3 = st.columns(3)
with col1: age_y = st.number_input("年齡 (歲)", 0, 18, 0)
with col2: age_m = st.number_input("年齡 (月)", 0, 11, 0)
with col3: weight_kg = st.number_input("體重 (KG)", 0.0, 100.0, 0.0)
total_age_years = age_y + (age_m / 12.0)

MEDICATION_DB = load_medication_db()

if MEDICATION_DB:
    st.divider()
    st.subheader("📦 選擇藥物儲位")
    locations = sorted(MEDICATION_DB.keys())
    selected = []
    cols = st.columns(4)
    for i, loc in enumerate(locations):
        chi_name = MEDICATION_DB[loc]['chinese_name']
        display_name = f"{loc} {chi_name[:4]}" if chi_name else loc
        if cols[i % 4].checkbox(display_name):
            selected.append(loc)
            
    if selected:
        st.divider()
        for loc in selected:
            med = MEDICATION_DB[loc]
            calc_func = LOGIC_MAP.get(med['logic_type'])
            res = calc_func(total_age_years, weight_kg) if calc_func else "⚠️ 未設定邏輯"
            with st.expander(f"📍 {loc} {med['chinese_name']}", expanded=True):
                st.write(f"**商品名:** {med['trade_name']}")
                if "⚠️" in res: st.error(res)
                else: st.success(res)
                if med['note']: st.info(f"💡 備註: {med['note']}")
