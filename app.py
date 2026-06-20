import streamlit as st
import pandas as pd
import os

# ==========================================
# 1. 藥物計算邏輯定義區
# ==========================================

def logic_l01(age_years, weight_kg):
    if age_years >= 12: dose = "20 ~ 30 ml"
    elif 6 <= age_years < 12: dose = "10 ~ 15 ml"
    elif 3 <= age_years < 6: dose = "5 ~ 7.5 ml"
    else: dose = "⚠️ 3歲以下請洽醫師"
    return dose

def logic_l02(age_years, weight_kg):
    if age_years < 0.5: return "⚠️ 6個月以下請洽醫師"
    if weight_kg <= 0: return "⚠️ 請輸入體重"
    low, high = weight_kg * 0.25, weight_kg * 0.5
    return f"🌡️ ≤39°C: {low:.1f} ml\n\n🔥 >39°C: {high:.1f} ml"

def logic_l03(age_years, weight_kg):
    if weight_kg >= 5.4:
        if 5.4 <= weight_kg <= 8.1: dose = "2.5 ml"
        elif 8.2 <= weight_kg <= 10.8: dose = "3.75 ~ 4 ml"
        elif 10.9 <= weight_kg <= 16.3: dose = "5 ml"
        elif 16.4 <= weight_kg <= 21.7: dose = "7.5 ml"
        elif 21.8 <= weight_kg <= 27.2: dose = "10 ml"
        elif 27.3 <= weight_kg <= 32.6: dose = "10 ~ 12.5 ml"
        elif 32.7 <= weight_kg <= 43.2: dose = "15 ml"
        else:
            low, high = weight_kg * 0.25, weight_kg * 0.5
            dose = f"{min(low, 20.0):.1f} ~ {min(high, 30.0):.1f} ml"
    elif age_years >= 0.5:
        if 0.5 <= age_years < 1: dose = "2.5 ml"
        else: dose = "5 ml"
    else: return "⚠️ 未滿6個月請洽醫師。"
    return f"✅ {dose}\n🕒 每 6 ~ 8 小時一次"

def logic_l04(age_years, weight_kg):
    if age_years < 2: return "⚠️ 2歲以下請洽醫師"
    if 2 <= age_years <= 6: base = "每次 5 ml"
    elif 7 <= age_years <= 14: base = "每次 10 ml"
    else: base = "14歲以上參考醫囑"
    return base

def logic_l05(age_years, weight_kg):
    if age_years >= 12: dose = "10 ~ 20 ml"
    elif 6 <= age_years < 12: dose = "6 ~ 10 ml"
    elif 2 <= age_years < 6: dose = "2 ~ 6 ml"
    else: dose = "⚠️ 2歲以下請洽醫師"
    return f"✅ 每次 {dose}\n🕒 每 4 小時一次"

def logic_l06(age_years, weight_kg):
    if weight_kg <= 0: return "⚠️ 請輸入體重。"
    hosp = weight_kg * 0.5
    d45 = (weight_kg * 22.5) / 62.5
    d90 = (weight_kg * 45) / 62.5
    return f"🏥 院內常用: 每次 {hosp:.1f} ml (Q8H)\n\n📖 適應症 Q12H:\n- 輕度: {d45:.1f} ml\n- 嚴重: {d90:.1f} ml"

def logic_l07(age_years, weight_kg):
    if age_years >= 12: dose, max_d = "10 ml", "40 ml"
    elif 6 <= age_years < 12: dose, max_d = "5 ml", "20 ml"
    else: return "⚠️ 6歲以下請洽醫師"
    return f"✅ 每次 {dose}\n🕒 每 4~6 小時\n⚠️ 最大: {max_d}"

def logic_l08(age_years, weight_kg):
    if age_years >= 6: dose, freq = "5 ml", "每日 1 ~ 2 次"
    else:
        if age_years < 1: age_dose = "2 ~ 3 ml"
        elif 1 <= age_years < 3: age_dose = "3 ~ 4 ml"
        else: age_dose = "4 ~ 5 ml"
        ref = f"\n⚖️ 體重參考: {weight_kg * 0.25:.1f} ml" if weight_kg > 0 else ""
        dose, freq = f"{age_dose}{ref}", "每日 2 ~ 3 次"
    return f"✅ 每次 {dose}\n🕒 {freq}"

def logic_l09(age_years, weight_kg):
    if age_years >= 6: dose = "10 ml"
    elif 2 <= age_years < 6: dose = "5 ml"
    else: return "⚠️ 2歲以下請洽醫師"
    return f"✅ 每次 {dose}\n🕒 每日一次"

def logic_l10(age_years, weight_kg):
    if age_years >= 12 or weight_kg >= 35: dose = "10 ~ 20 ml"
    elif weight_kg > 0: dose = f"{weight_kg * 0.25:.1f} ~ {weight_kg * 0.5:.1f} ml"
    else: dose = "10 ml"
    return f"✅ 每次 {dose}\n🕒 每日 3 ~ 4 次 (飯前)"

def logic_l11(age_years, weight_kg):
    if weight_kg <= 0: return "⚠️ 請輸入體重。"
    mild = (weight_kg * 37.5 / 4) / 25
    sev = (weight_kg * 87.5 / 4) / 25
    return f"✅ 一般(Q6H): {mild:.1f} ml\n🔥 嚴重(Q6H): {sev:.1f} ml"

def logic_l12(age_years, weight_kg):
    if weight_kg <= 0: return "⚠️ 請輸入體重。"
    three_day = min((weight_kg * 10) / 40, 12.5)
    return f"📅 3日療程: 每日一次 {three_day:.1f} ml"

def logic_l13(age_years, weight_kg):
    if weight_kg <= 0: return "⚠️ 請輸入體重。"
    if age_years < 1:
        weeks = age_years * 52
        daily = ((0.2 * weeks) + 5) * weight_kg
        dose = (daily / 4) / 5.34
        return f"👶 嬰兒(Q6H): 每次 {dose:.1f} ml"
    init = (min(weight_kg * 12, 300) / 4) / 5.34
    maint = (min(weight_kg * 20, 600) / 4) / 5.34
    return f"🧒 初始(Q6H): {init:.1f} ml\n🧒 維持(Q6H): {maint:.1f} ml"

def logic_l16(age_years, weight_kg):
    if weight_kg <= 0: return "⚠️ 請輸入體重。"
    gen_low = weight_kg * 0.1
    gen_high = weight_kg * 2.0
    if age_years < 12:
        asthma_dose = weight_kg * 1.5
        if age_years <= 2: max_limit = 20
        elif 3 <= age_years <= 5: max_limit = 30
        elif 6 <= age_years <= 11: max_limit = 40
        else: max_limit = 60
        asthma_val = min(max(weight_kg * 1, weight_kg * 2), max_limit)
        asthma_res = f"🫁 氣喘每日: {asthma_val:.1f} ml"
    else: asthma_res = "🫁 氣喘每日: 40 ~ 60 ml"
    return f"✅ 抗發炎: 每日 {gen_low:.1f}~{gen_high:.1f} ml\n{asthma_res}"

def logic_levetiracetam(age_years, weight_kg):
    """共通 Levetiracetam 邏輯 (L18, L915)"""
    if weight_kg <= 0 and age_years < 16: return "⚠️ 請輸入體重。"
    
    if 0.08 <= age_years < 0.5: # 1-6個月
        init, target = (weight_kg * 7)/100, (weight_kg * 21)/100
        res = f"👶 1-6M(Q12H): 初始 {init:.1f} ml, 目標 {target:.1f} ml"
    elif 0.5 <= age_years < 4: # 6個月-4歲
        init, target = (weight_kg * 10)/100, (weight_kg * 25)/100
        res = f"🧒 6M-4Y(Q12H): 初始 {init:.1f} ml, 目標 {target:.1f} ml"
    elif 4 <= age_years < 16: # 4-16歲
        init, target = (weight_kg * 10)/100, min((weight_kg * 30)/100, 15.0)
        res = f"👦 4-16Y(Q12H): 初始 {init:.1f} ml, 目標 {target:.1f} ml\n   (每日最大量 30ml)"
    else: # 16歲以上
        res = "🧑 16Y+(Q12H): 初始 5 ml (500mg), 目標 15 ml (1500mg)"
    
    return (f"🧠 癲癇治療(Q12H):\n{res}\n\n"
            f"⚠️ 安全提示: 勿突然停藥，以防抽搐頻率增加。")

def logic_l904(age_years, weight_kg):
    if weight_kg <= 0: return "⚠️ 請輸入體重。"
    if age_years >= 5:
        if 15 <= weight_kg < 20: autism = "初始: 0.25 ml, 4天後增至 0.5 ml"
        elif weight_kg >= 20:
            limit = 3.0 if weight_kg > 45 else 2.5
            autism = f"初始: 0.5 ml, 4天後增至 1.0 ml (上限 {limit})"
        else: autism = "洽醫師評估。"
    else: autism = "⚠️ 5歲以下洽醫師。"
    return f"🧩 自閉症/易怒:\n   {autism}"

def logic_l908(age_years, weight_kg):
    if weight_kg <= 0 and age_years < 17: return "⚠️ 請輸入體重。"
    if age_years < 4:
        init = (weight_kg * 9) / 60
        res = f"👶 未滿4歲: 每次 {init/2:.1f} ml (Q12H)"
    elif 4 <= age_years <= 16:
        if 20 <= weight_kg < 35: maint = "10 ~ 20 ml"
        elif 35 <= weight_kg < 60: maint = "15 ~ 30 ml"
        else: maint = "25 ~ 35 ml"
        res = f"👦 4-16歲: 每日總量 {maint} (分2次)"
    else: res = "🧑 17歲+: 每次 10 ml (Q12H)"
    return f"🧠 癲癇治療(Q12H):\n{res}"

def logic_l911(age_years, weight_kg):
    if age_years < 1: dose = "2 ml"
    else: dose = "4 ~ 6 ml"
    return f"✅ 每次 {dose}\n🕒 每日 4 次 (含於口中)"

def logic_l912(age_years, weight_kg):
    if weight_kg <= 0: return "⚠️ 請輸入體重。"
    warn = "⚠️ 2歲以下風險高。" if age_years < 2 else ""
    init = (weight_kg * 12.5) / 200
    maint = (weight_kg * 45) / 200
    return f"{warn}🧠 癲癇總量:\n初始: {init:.1f} ml/day, 維持: {maint:.1f} ml/day"

LOGIC_MAP = {
    "L01_Logic": logic_l01, "L02_Logic": logic_l02, "L03_Logic": logic_l03,
    "L04_Logic": logic_l04, "L05_Logic": logic_l05, "L06_Logic": logic_l06,
    "L07_Logic": logic_l07, "L08_Logic": logic_l08, "L09_Logic": logic_l09,
    "L10_Logic": logic_l10, "L11_Logic": logic_l11, "L12_Logic": logic_l12,
    "L13_Logic": logic_l13, "L16_Logic": logic_l16, 
    "L18_Logic": logic_levetiracetam, # 使用共通邏輯
    "L904_Logic": logic_l904, "L908_Logic": logic_l908, 
    "L911_Logic": logic_l911, "L912_Logic": logic_l912,
    "L915_Logic": logic_levetiracetam, # L915 使用相同邏輯
}

# ==========================================
# 2. 資料讀取 (加強防呆版)
# ==========================================

def load_medication_db():
    file_path = "meds.xlsx"
    if not os.path.exists(file_path): return None
    try:
        df = pd.read_excel(file_path, engine='openpyxl').fillna("")
        db = {str(row['Location']).strip(): {
            "trade_name": str(row['Trade_Name']),
            "chinese_name": str(row['Chinese_Name']),
            "note": str(row['Note']),
            "logic_type": str(row['Logic_Type'])
        } for _, row in df.iterrows() if str(row['Location']).strip()}
        return db
    except Exception: return None

# ==========================================
# 3. 網頁介面
# ==========================================
st.set_page_config(page_title="藥物劑量計算系統", page_icon="💊")
st.title("💊 兒童藥物劑量計算系統")

col1, col2, col3 = st.columns(3)
with col1: age_y = st.number_input("年齡 (歲)", 0, 18, 0)
with col2: age_m = st.number_input("年齡 (個月)", 0, 11, 0)
with col3: weight_kg = st.number_input("體重 (KG)", 0.0, 100.0, 0.0, format="%.1f")
total_age_years = age_y + (age_m / 12.0)

MEDICATION_DB = load_medication_db()

if MEDICATION_DB:
    st.divider()
    st.subheader("📦 選擇藥物儲位")
    locations = sorted(MEDICATION_DB.keys())
    selected = []
    cols = st.columns(4)
    for i, loc in enumerate(locations):
        name = MEDICATION_DB[loc]['chinese_name']
        if cols[i % 4].checkbox(f"{loc} {name[:4]}" if name else loc):
            selected.append(loc)
            
    if selected:
        st.divider()
        for loc in selected:
            med = MEDICATION_DB[loc]
            calc = LOGIC_MAP.get(med['logic_type'])
            res = calc(total_age_years, weight_kg) if calc else "⚠️ 未設定邏輯"
            with st.expander(f"📍 {loc} {med['chinese_name']}", expanded=True):
                st.write(f"**商品名:** {med['trade_name']}")
                if "⚠️" in res: st.error(res)
                else: st.success(res)
                if med['note']: st.info(f"💡 備註: {med['note']}")
