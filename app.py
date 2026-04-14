import streamlit as st
import pandas as pd
import os

# ------------------------------------------------------------
# КОНФИГУРАЦИЯ СТРАНИЦЫ
# ------------------------------------------------------------
st.set_page_config(
    page_title="ЖК Победа",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------------------
# CSS СТИЛИ
# ------------------------------------------------------------
st.markdown("""
<style>
    .main { background-color: #f5f5f5; }
    h1, h2, h3 { color: #2c3e50; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

    /* Стили для кнопок */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        height: 50px; /* Фиксированная высота */
    }

    /* Карточки квартир */
    .apt-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 5px solid #3498db;
    }

    /* Стояк */
    .stand-item {
        background: #ecf0f1;
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 6px;
        font-size: 14px;
    }
    .stand-item.active {
        background: #3498db;
        color: white;
        font-weight: bold;
    }

    /* Скрытие элементов */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# КОНФИГУРАЦИЯ ДОМОВ
# ------------------------------------------------------------
HOUSES = {
    "139/1": {"sections": [
        {"floors": list(range(2, 15)), "flat_range": (1, 65), "flats_per_floor": 5},
        {"floors": list(range(2, 17)), "flat_range": (66, 125), "flats_per_floor": 4},
        {"floors": list(range(2, 19)), "flat_range": (126, 193), "flats_per_floor": 4},
        {"floors": list(range(2, 17)), "flat_range": (194, 253), "flats_per_floor": 4},
        {"floors": list(range(2, 15)), "flat_range": (254, 305), "flats_per_floor": 4},
        {"floors": list(range(2, 17)), "flat_range": (306, 365), "flats_per_floor": 4},
        {"floors": list(range(2, 15)), "flat_range": (366, 416), "flats_per_floor": 4},
    ]},
    "139/2": {"sections": [
        {"floors": list(range(2, 17)), "flat_range": (1, 60), "flats_per_floor": 4},
        {"floors": list(range(3, 25)), "flat_range": (61, 126), "flats_per_floor": 3},
        {"floors": list(range(3, 17)), "flat_range": (127, 182), "flats_per_floor": 4},
        {"floors": list(range(3, 19)), "flat_range": (183, 262), "flats_per_floor": 5},
        {"floors": list(range(3, 19)), "flat_range": (263, 326), "flats_per_floor": 4},
        {"floors": list(range(3, 19)), "flat_range": (327, 406), "flats_per_floor": 5},
        {"floors": list(range(3, 17)), "flat_range": (407, 462), "flats_per_floor": 4},
        {"floors": list(range(3, 25)), "flat_range": (463, 528), "flats_per_floor": 3},
        {"floors": list(range(2, 17)), "flat_range": (529, 588), "flats_per_floor": 4},
    ]},
    "139/3": {"sections": [
        {"floors": list(range(2, 15)), "flat_range": (1, 51), "flats_per_floor": 4},
        {"floors": list(range(2, 15)), "flat_range": (52, 116), "flats_per_floor": 5},
        {"floors": list(range(2, 15)), "flat_range": (117, 168), "flats_per_floor": 4},
        {"floors": list(range(2, 17)), "flat_range": (169, 228), "flats_per_floor": 4},
        {"floors": list(range(2, 19)), "flat_range": (229, 296), "flats_per_floor": 4},
        {"floors": list(range(2, 17)), "flat_range": (297, 356), "flats_per_floor": 4},
        {"floors": list(range(2, 19)), "flat_range": (357, 424), "flats_per_floor": 4},
    ]},
    "139А/1": {"sections": [
        {"floors": list(range(2, 17)), "flat_range": (1, 60), "flats_per_floor": 4},
        {"floors": list(range(2, 15)), "flat_range": (61, 112), "flats_per_floor": 4},
        {"floors": list(range(2, 17)), "flat_range": (113, 172), "flats_per_floor": 4},
        {"floors": list(range(2, 15)), "flat_range": (173, 224), "flats_per_floor": 4},
        {"floors": list(range(2, 15)), "flat_range": (225, 276), "flats_per_floor": 4},
        {"floors": list(range(2, 17)), "flat_range": (277, 336), "flats_per_floor": 4},
        {"floors": list(range(2, 15)), "flat_range": (337, 388), "flats_per_floor": 4},
        {"floors": list(range(2, 13)), "flat_range": (389, 432), "flats_per_floor": 4},
    ]},
    "139А/2": {"sections": [
        {"floors": list(range(2, 15)), "flat_range": (1, 52), "flats_per_floor": 4},
        {"floors": list(range(2, 17)), "flat_range": (53, 112), "flats_per_floor": 4},
        {"floors": list(range(2, 19)), "flat_range": (113, 180), "flats_per_floor": 4},
        {"floors": list(range(2, 15)), "flat_range": (181, 232), "flats_per_floor": 4},
        {"floors": list(range(2, 15)), "flat_range": (233, 284), "flats_per_floor": 4},
        {"floors": list(range(2, 19)), "flat_range": (285, 352), "flats_per_floor": 4},
        {"floors": list(range(2, 15)), "flat_range": (353, 404), "flats_per_floor": 4},
        {"floors": list(range(2, 17)), "flat_range": (405, 464), "flats_per_floor": 4},
        {"floors": list(range(2, 19)), "flat_range": (465, 531), "flats_per_floor": 4},
    ]}
}


# ------------------------------------------------------------
# ЗАГРУЗКА ДАННЫХ
# ------------------------------------------------------------
@st.cache_data
def load_data():
    if os.path.exists("flats.csv"):
        try:
            df = pd.read_csv("flats.csv")
            df['number'] = pd.to_numeric(df['number'], errors='coerce').fillna(0).astype(int)
            df['area'] = pd.to_numeric(df['area'], errors='coerce').fillna(0.0)
            df['floor'] = pd.to_numeric(df['floor'], errors='coerce').fillna(0).astype(int)
            df['section'] = pd.to_numeric(df['section'], errors='coerce').fillna(0).astype(int)
            return df
        except Exception as e:
            st.error(f"Ошибка чтения flats.csv: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


df = load_data()


# ------------------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ------------------------------------------------------------
def calculate_rooms(area):
    """Улучшенная логика расчета комнат"""
    if pd.isna(area) or area <= 0:
        return "?"
    if area < 40:
        return 1
    elif area < 70:
        return 2
    else:
        return 3


def find_flat_location(house, flat_number, df):
    flat_number = int(flat_number)
    house_df = df[df["house"] == house]
    result = house_df[house_df["number"] == flat_number]

    if not result.empty:
        row = result.iloc[0]
        area = float(row['area'])
        return {
            'section': int(row['section']),
            'floor': int(row['floor']),
            'area': area,
            'rooms': int(row['rooms']) if pd.notna(row.get('rooms')) else calculate_rooms(area),
            'row': row
        }
    return None


def get_stand_neighbors(row, df):
    num = int(row['number'])
    section = int(row['section'])
    house = str(row['house'])

    sec_idx = section - 1
    if sec_idx >= len(HOUSES[house]["sections"]):
        return pd.DataFrame()

    sec_config = HOUSES[house]["sections"][sec_idx]
    flats_per_floor = sec_config["flats_per_floor"]
    start_num = sec_config["flat_range"][0]

    position_index = (num - start_num) % flats_per_floor

    neighbors = df[
        (df['house'] == house) &
        (df['section'] == section) &
        ((df['number'] - start_num) % flats_per_floor == position_index)
        ].sort_values('floor')

    return neighbors


def show_stand_details(row, df):
    stand_df = get_stand_neighbors(row, df)
    if not stand_df.empty:
        st.markdown("#### 🏗️ Стояк (вертикальные соседи)")
        for _, s_row in stand_df.iterrows():
            s_num = int(s_row['number'])
            s_area = float(s_row['area'])
            s_floor = int(s_row['floor'])
            # Используем calculate_rooms для гарантированной корректности
            s_rooms = int(s_row['rooms']) if pd.notna(s_row.get('rooms')) else calculate_rooms(s_area)

            is_current = s_num == int(row['number'])
            marker = "📍" if is_current else "  "
            bg_class = "active" if is_current else ""

            st.markdown(f"""
            <div class="stand-item {bg_class}">
                {marker} <b>Этаж {s_floor}:</b> Кв. {s_num} | {s_area:.1f} м² | {s_rooms} комн.
            </div>
            """, unsafe_allow_html=True)


# ------------------------------------------------------------
# ЛОГОТИП И ЗАГОЛОВОК
# ------------------------------------------------------------
col_logo, col_title = st.columns([1, 5])
with col_logo:
    try:
        # Ищем логотип с разными расширениями
        logo_paths = ["logo.png", "logo.jpg", "logo.png.jpg"]
        logo_found = False
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                st.image(logo_path, width=900)
                logo_found = True
                break
        if not logo_found:
            st.markdown("<div style='font-size: 60px; text-align: center;'>🏢</div>", unsafe_allow_html=True)
    except Exception as e:
        st.markdown("<div style='font-size: 60px; text-align: center;'>🏢</div>", unsafe_allow_html=True)

with col_title:
    st.title("ЖК Победа")
    st.markdown("ℹ️ *Данные носят информационный характер*")

st.markdown("---")

# ------------------------------------------------------------
# ИНИЦИАЛИЗАЦИЯ РЕЖИМА ПОИСКА
# ------------------------------------------------------------
if 'search_mode' not in st.session_state:
    st.session_state.search_mode = 1

# ------------------------------------------------------------
# 3 КНОПКИ НАВИГАЦИИ
# ------------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Поиск по дому и квартире",
                 use_container_width=True,
                 key="btn_mode1",
                 type="primary" if st.session_state.search_mode == 1 else "secondary"):
        st.session_state.search_mode = 1
        st.rerun()

with col2:
    if st.button("🔍 Поиск по квартире",
                 use_container_width=True,
                 key="btn_mode2",
                 type="primary" if st.session_state.search_mode == 2 else "secondary"):
        st.session_state.search_mode = 2
        st.rerun()

with col3:
    if st.button("🏢 Расширенный поиск",
                 use_container_width=True,
                 key="btn_mode3",
                 type="primary" if st.session_state.search_mode == 3 else "secondary"):
        st.session_state.search_mode = 3
        st.rerun()

st.markdown("---")

# ============================================================


# ============================================================
# РЕЖИМ 1: ПОИСК ПО ДОМУ И КВАРТИРЕ
# ============================================================
if st.session_state.search_mode == 1:
    st.subheader("1️⃣ Выберите дом")

    cols = st.columns(len(HOUSES))
    selected_house = None

    for i, house_name in enumerate(HOUSES.keys()):
        with cols[i]:
            if st.button(f"🏠 {house_name}", key=f"house_btn_{house_name}", use_container_width=True):
                st.session_state.selected_house_mode1 = house_name

    if 'selected_house_mode1' in st.session_state:
        selected_house = st.session_state.selected_house_mode1

    if selected_house:
        st.success(f"✅ Выбран дом: **{selected_house}**")

        st.subheader("2️⃣ Введите номер квартиры")
        apt_num = st.number_input("Номер квартиры", min_value=1, step=1,
                                  key="apt_num_mode1", label_visibility="collapsed")

        if apt_num > 0:
            location = find_flat_location(selected_house, apt_num, df)

            if location:
                st.success("✅ Найдено")
                st.markdown(f"""
                <div class="large-info" style="font-size: 24px; font-weight: bold; color: #2c3e50; margin: 20px 0; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    🚪 Подъезд: {location['section']}<br>
                    📌 Этаж: {location['floor']}
                </div>
                """, unsafe_allow_html=True)

                st.info(f"📐 Площадь: {location['area']:.1f} м² | 🛏 Комнат: {location['rooms']}")

                if st.button("🏗️ Показать стояк", key="stand_mode1"):
                    show_stand_details(location['row'], df)
            else:
                st.error(f"❌ Квартира {apt_num} не найдена в доме {selected_house}")

# ============================================================
# РЕЖИМ 2: ПОИСК ПО КВАРТИРЕ
# ============================================================
elif st.session_state.search_mode == 2:
    st.subheader("1️⃣ Выберите квартиру")

    col1, col2 = st.columns([3, 1])
    with col1:
        search_num = st.number_input("Введите номер квартиры", min_value=1, step=1,
                                     key="search_num_mode2", label_visibility="collapsed")
    with col2:
        search_btn = st.button("🔎 Найти", key="search_btn_mode2", use_container_width=True)

    if search_btn or search_num > 0:
        results = df[df["number"] == search_num]

        if results.empty:
            st.error(f"❌ Квартира №{search_num} не найдена")
        else:
            st.success(f"✅ Найдено совпадений: **{len(results)}**")

            for idx, (_, row) in enumerate(results.iterrows()):
                apt_num = int(row['number'])
                area = float(row['area'])
                floor = int(row['floor'])
                section = int(row['section'])
                house = str(row['house'])
                rooms = int(row['rooms']) if pd.notna(row.get('rooms')) else calculate_rooms(area)

                st.markdown(f"""
                <div class="apt-card">
                    <div style="font-size: 20px; font-weight: bold;">🏢 Дом {house}, Подъезд {section}, Этаж {floor}</div>
                    <div>🚪 Квартира: <b>{apt_num}</b></div>
                    <div>📐 Площадь: <b>{area:.1f} м²</b> | 🛏 Комнат: <b>{rooms}</b></div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("🏗️ Показать стояк", key=f"stand_mode2_{idx}"):
                    show_stand_details(row, df)

# ============================================================
# РЕЖИМ 3: РАСШИРЕННЫЙ ПОИСК ПО ДОМУ
# ============================================================
elif st.session_state.search_mode == 3:
    st.subheader("1️⃣ Выберите дом")

    cols = st.columns(len(HOUSES))
    selected_house = None

    for i, house_name in enumerate(HOUSES.keys()):
        with cols[i]:
            if st.button(f"🏠 {house_name}", key=f"house_btn_mode3_{house_name}", use_container_width=True):
                st.session_state.selected_house_mode3 = house_name

    if 'selected_house_mode3' in st.session_state:
        selected_house = st.session_state.selected_house_mode3

    if selected_house:
        st.success(f"✅ Выбран дом: **{selected_house}**")
        house_df = df[df["house"] == selected_house].copy()

        st.subheader("2️⃣ Выберите подъезд")
        sections = sorted(house_df["section"].unique())
        selected_section = st.selectbox("Подъезд", sections, key="section_mode3")

        if selected_section:
            st.subheader("3️⃣ Выберите этаж")
            sec_config = HOUSES[selected_house]["sections"][int(selected_section) - 1]
            available_floors = sorted(sec_config["floors"])
            selected_floor = st.selectbox("Этаж", available_floors, key="floor_mode3")

            if selected_floor:
                floor_df = house_df[(house_df["section"] == selected_section) &
                                    (house_df["floor"] == selected_floor)]

                if not floor_df.empty:
                    st.markdown(f"### 🏢 Квартиры на {selected_floor}-м этаже (Подъезд {selected_section})")

                    cols = st.columns(min(5, len(floor_df)))
                    for idx, (_, row) in enumerate(floor_df.iterrows()):
                        with cols[idx % 5]:
                            num = int(row['number'])
                            area = float(row['area'])
                            rooms = int(row['rooms']) if pd.notna(row.get('rooms')) else calculate_rooms(area)

                            if st.button(f"🚪 Кв. {num}\n{area:.1f} м², {rooms} комн.",
                                         key=f"apt_mode3_{num}_{selected_floor}",
                                         use_container_width=True):
                                st.session_state.selected_apt_mode3 = row

                    if 'selected_apt_mode3' in st.session_state:
                        apt_row = st.session_state.selected_apt_mode3
                        apt_num = int(apt_row['number'])
                        area = float(apt_row['area'])
                        rooms = int(apt_row['rooms']) if pd.notna(apt_row.get('rooms')) else calculate_rooms(area)

                        st.markdown("---")
                        st.markdown(f"#### 📍 Квартира {apt_num}")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"📐 Площадь: **{area:.1f} м²**")
                        with col2:
                            st.info(f"🛏 Комнат: **{rooms}**")

                        if st.button("🏗️ Показать стояк", key="stand_mode3", use_container_width=True):
                            show_stand_details(apt_row, df)

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; font-size: 12px;'>
    ЖК Победа © 2026 
</div>
""", unsafe_allow_html=True)
