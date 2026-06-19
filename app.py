import streamlit as st
import pandas as pd
import os

# ==========================================
# 1. 藥物計算邏輯定義區
# ==========================================

def logic_l01(age_years, weight_kg):
    """L01: 安佳熱糖漿 ANTI-PHEN SYRUP"""
    if age_years >= 12:
        dose = "20 ~ 30 毫升 (ml)"
    elif 6 <= age_years < 12:
        dose = "10 ~ 15 毫升 (ml)"
    elif 3 <= age_years < 6:
        dose = "5 ~ 7.5 毫升 (ml)"
    else:
        dose = "⚠️ 3歲以下請洽醫師診治，不宜自行使用。"
    return dose

def logic_l02(age_years, weight_kg):
    """L02: 舒抑痛口服懸液 Idofen Susp. Syrup"""
    if age_years < 0.5:
        return "⚠️ 6個月以下嬰兒請洽醫師診治。"
    if weight_kg <= 0:
        return "⚠️ 請輸入體重以計算劑量。"
    
    # 5mg/kg = 0.25ml/kg ; 10mg/kg = 0.5ml/kg
    low_dose = weight_kg * 0.25
    high_dose = weight_kg * 0.5
    max_daily = weight_kg * 2.0
    
    return (f"🌡️ 輕微發燒(≤39°C): {low_dose:.1f} ml\n\n"
            f"🔥 高燒(>39°C)或疼痛: {high_dose:.1f} ml\n\n"
            f"🚫 每日極量: {max_daily:.1f} ml")

def logic_l04(age_years, weight_kg):
    """L04: 希普利敏液 Cypromin solution"""
    if age_years < 2:
        return "⚠️ 2歲以下幼兒請洽醫師診治用量。"

    if 2 <= age_years <= 6:
        base = "每次 5 ml (2mg)，每日 2~3 次\n(⚠️每日最大量 30ml)"
    elif 7 <= age_years <= 14:
        base = "每次 10 ml (4mg)，每日 2~3 次\n(⚠️每日最大量 40ml)"
    else:
        base = "14歲以上請參考醫囑。"

    if weight_kg > 0:
        daily_total = weight_kg * 0.625
        base += f"\n\n⚖️ 體重參考: 每日總量約 {daily_total:.1f} ml"
    
    return base

def logic_l05(age_years, weight_kg):
    """L05: 息咳液 Sortuss cough liquid"""
    if age_years >= 12:
        dose = "每次 10 ~ 20 毫升 (ml)"
    elif 6 <= age_years < 12:
        dose = "每次 6 ~ 10 毫升 (ml)"
    elif 2 <= age_years < 6:
        dose = "每次 2 ~ 6 毫升 (ml)"
    else:
        dose = "⚠️ 2歲以下幼兒請洽醫師診治。"
    
    return f"✅ {dose}\n\n🕒 每四小時服用一次。"

# 邏輯對照表 (這部分要跟 Excel 的 Logic_Type 欄位對上)
LOGIC_MAP = {
    "L01_Logic": logic_l01,
    "L02_Logic": logic_l02,
    "L04_Logic": logic_l04,
    "L05_Logic": logic_l05,
}

# ==========================================
# 2. 資料讀取與處理
# ==========================================

@st.cache_data
def load_medication_db():
    file_path = "meds.xlsx"
    if not os.path.exists(file_path):
        return None
    
    try:
        df = pd.read_excel(file_path)
        db = {}
        for _, row in df.iterrows():
            db[str(row['Location'])] = {
                "trade_name": row['Trade_Name'],
                "chinese_name": row['Chinese_Name'],
                "note": row['Note'],
                "logic_type": row['Logic_Type']
            }
        return db
    except Exception as e:
        st.error(f"讀取 Excel 發生錯誤: {e}")
        return None

# ==========================================
# 3. 網頁介面設計
# ==========================================
st.set_page_config(page_title="兒童藥物劑量計算系統", page_icon="💊", layout="centered")

st.title("💊 兒童藥物劑量計算系統")
st.markdown("請輸入病患資訊並勾選儲位，系統將自動計算建議劑量。")

# --- 區塊 1: 病患資訊 ---
st.subheader("👤 病患資訊")
col1, col2, col3 = st.columns(3)
with col1:
    age_y = st.number_input("年齡 (歲)", min_value=0, value=0, step=1)
with col2:
    age_m = st.number_input("年齡 (個月)", min_value=0, max_value=11, value=0, step=1)
with col3:
    weight_kg = st.number_input("體重 (KG)", min_value=0.0, value=0.0, step=0.1)

total_age_years = age_y + (age_m / 12.0)

# --- 區塊 2: 載入資料與選擇儲位 ---
MEDICATION_DB = load_medication_db()

if MEDICATION_DB is None:
    st.error("❌ 找不到 `meds.xlsx` 檔案或格式不正確，請確保檔案已上傳至 GitHub。")
else:
    st.divider()
    st.subheader("📦 請選擇藥物儲位")
    
    locations = sorted(MEDICATION_DB.keys())
    selected_locations = []
    
    # 每行顯示 4 個儲位，讓介面整齊
    cols = st.columns(4)
    for i, loc in enumerate(locations):
        med_info = MEDICATION_DB[loc]
        # 顯示格式: "L01 安佳熱糖..."
        display_label = f"{loc} {str(med_info['chinese_name'])[:4]}"
        if cols[i % 4].checkbox(display_label):
            selected_locations.append(loc)

    st.divider()

    # --- 區塊 3: 顯示結果 ---
    if selected_locations:
        st.subheader("📝 計算結果")
        for loc in selected_locations:
            med = MEDICATION_DB[loc]
            calc_func = LOGIC_MAP.get(med['logic_type'])
            
            if calc_func:
                dose_result = calc_func(total_age_years, weight_kg)
            else:
                dose_result = "⚠️ 尚未設定此藥物的計算邏輯。"

            with st.container():
                # 使用漂亮的外框顯示結果
                st.markdown(f"### 📍 儲位 {loc}: {med['chinese_name']}")
                st.write(f"**商品名:** {med['trade_name']}")
                
                if "⚠️" in dose_result:
                    st.error(f"**建議劑量:**\n\n{dose_result}")
                else:
                    st.success(f"**建議劑量:**\n\n{dose_result}")
                
                if pd.notna(med['note']):
                    st.info(f"💡 **備註:** {med['note']}")
                st.divider()
    else:
        st.info("👆 請勾選上方儲位以顯示劑量。")

st.caption("本系統劑量僅供參考，實際用藥請遵照醫師處方或藥品說明書。")
