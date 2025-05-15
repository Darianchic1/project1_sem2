"""Файл для дашборда"""

import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Авиа-дашборд",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ЗАГРУЗКА ДАННЫХ
@st.cache_data
def load_data():
    """Загрузка и кэширование данных"""
    return pd.read_csv("data/final_dataframe.csv")

@st.cache_data
def get_coordinates():
    """Словарь координат для городов"""
    return {
        'Коломбо': [6.9271, 79.8612],
        'Мале': [4.1755, 73.5093],
        'Ташкент': [41.2995, 69.2401],
        'Бангкок': [13.7563, 100.5018],
        'Белград': [44.7866, 20.4489],
        'Дубай': [25.276987, 55.296249],
        'Стамбул': [41.0082, 28.9784],
        'Манила': [14.5995, 120.9842],
        'Подгорица': [42.4411, 19.2636],
        'Маврикий': [-20.348404, 57.552152],
        'Токио': [35.6762, 139.6503],
        'Варадеро': [23.1460, -81.2752]
    }

# Загрузка данных
df = load_data()
city_coords = get_coordinates()


# НАВИГАЦИОННОЕ МЕНЮ
st.sidebar.title("Анализ популярных направлений")
pages = {
    "Главная": "Обзор данных и целей исследования",
    "Данные": "Исходные данные и базовый анализ",
    "EDA": "Углубленный разведочный анализ",
    "Тренды": "Анализ закономерностей",
    "Выводы": "Итоги и рекомендации"
}
page = st.sidebar.radio("Разделы:", list(pages.keys()))


# СОДЕРЖАНИЕ СТРАНИЦ
if page == "Главная":
    # Заголовок и описание
    st.title("Анализ цен на авиабилеты в майские праздники 2025")
    
    # Блок 1: Общая информация
    with st.container():
        st.header("📌 О данных")
        st.markdown("""
         **Датасет содержит:**  
        • 12 популярных направлений из 43 городов России и мира  
        • Цены на авиабилеты в период майских праздников 2025  
        • Разделение по типам отдыха: пляжный, городской, культурный 
        """)

        st.markdown("""
        ### Источник данных
        Данные получены с **AviaSales** — ведущего метапоисковика авиабилетов, 
        обрабатывающего предложения 800+ авиакомпаний и 200+ ticket-агентств. 
        """)
        
        # Ключевые метрики в колонках
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Средняя цена", "18 200 руб")
        with col2:
            st.metric("Самый дорогой билет", "54 792 руб")
        with col3:
            st.metric("Самый бюджетный", "1 057 руб")
    
    # Блок 2: Визуализация
    with st.container():
        st.map(pd.DataFrame({
        "lat": [6.9271, 4.1755, 41.2995, 25.2048],  # Координаты популярных направлений
        "lon": [79.8612, 73.5093, 69.2401, 55.2708],
        "city": ["Коломбо", "Мале", "Ташкент", "Дубай"]
    }), zoom=1)
    
    # Блок 3: Цели исследования
    with st.container():
        st.header("Ключевые вопросы")
        tabs = st.tabs(["География", "Цены", "Города"])
        with tabs[0]:
            st.markdown("- Какие направления самые популярные?  \n- Как распределены популярные направления на карте?  ")
        with tabs[1]:
            st.markdown("- Влияет ли тип отдыха на цену? \n-  Какие направления самые дорогие/дешёвые?  ")
        with tabs[2]:
            st.markdown("- Зависит ли стоимость от города вылета?\n- Из какого города самые выгодные перелёты?\n- Региональные особенности спроса")

    # Блок 4: Пример данных
    with st.container():
        st.subheader("Пример данных")
        st.dataframe(df.sample(5), height=200)

elif page == "Данные":
    # Основной контент страницы
    st.header("Исходные данные")
    
    # Фильтры данных
    with st.expander("Фильтры", expanded=True):
        min_price = st.slider("Минимальная цена", float(df["price"].min()), float(df["price"].max()), float(df["price"].min()))
        filtered_df = df[df["price"] >= min_price]
    
    # Отображение данных
    st.dataframe(filtered_df, height=400, use_container_width=True)

    
    # Анализ данных
    st.header("Базовый анализ данных")

    # 1. Ключевые метрики в карточках
    st.subheader("Ключевые показатели")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric(
            label="Всего записей", 
            value=len(df),
            help="Общее количество записей в наборе данных"
        )
    with metric_col2:
        st.metric(
            label="Уникальных городов вылета", 
            value=df["origin_name"].nunique(),
            help="Количество различных городов отправления"
        )
    with metric_col3:
        avg_price = df['price'].mean()
        st.metric(
            label="Средняя стоимость", 
            value=f"{avg_price:,.2f} руб",
            help=f"Средняя цена билета (от {df['price'].min():,.0f} до {df['price'].max():,.0f} руб)"
        )

    # 2. Анализ распределения цен
    st.subheader("Анализ распределения цен на билеты")

    # Создаем вкладки для разных типов визуализации
    dist_tab1, dist_tab2 = st.tabs(["Гистограмма с боксиграммой", "Статистические показатели"])

    with dist_tab1:
        # Гистограмма с боксиграммой
        fig = px.histogram(
            df,
            x="price",
            nbins=30,
            title="Распределение цен на авиабилеты",
            labels={"price": "Цена (руб)", "count": "Количество билетов"},
            color_discrete_sequence=["#1f77b4"],
            opacity=0.8,
            marginal="box",
            hover_data=["origin_name", "destination_city"]
        )
        
        # Настройка внешнего вида
        fig.update_layout(
            bargap=0.1,
            xaxis_title="Цена билета (руб)",
            yaxis_title="Количество билетов",
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="lightgray"),
            yaxis=dict(showgrid=True, gridcolor="lightgray")
        )
        
        # Добавляем вертикальную линию среднего значения
        fig.add_vline(
            x=avg_price, 
            line_dash="dot",
            annotation_text=f"Среднее: {avg_price:,.0f} руб",
            annotation_position="top"
        )
        
        st.plotly_chart(fig, use_container_width=True)

    with dist_tab2:
        # Статистические показатели в виде колонок
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### Мода
            **{} руб**  
            Наиболее часто встречающаяся цена билета
            """.format(df["price"].mode()[0]))
        
        with col2:
            st.markdown("""
            ### Медиана
            **{} руб**  
            50% билетов дешевле этой цены
            """.format(df["price"].median()))
        
        with col3:
            st.markdown("""
            ### Среднее
            **{} руб**  
            Общий средний показатель по всем билетам
            """.format(round(df["price"].mean(), 2)))
        
        # Дополнительные показатели
        st.markdown("""
        #### Другие показатели:
        - **Стандартное отклонение:** {:.2f} руб
        - **Размах цен:** от {:,} до {:,} руб
        - **Квартили:** 
        - Q1 (25%): {:,} руб 
        - Q3 (75%): {:,} руб
        """.format(
            df["price"].std(),
            df["price"].min(),
            df["price"].max(),
            df["price"].quantile(0.25),
            df["price"].quantile(0.75)
        ))

# 3. Раздел «EDA»
elif page == "EDA":
    st.header("Первичный анализ данных")
    
    # 1. Карта направлений с plotly
    st.subheader("География популярных направлений")
    
    # Создаём DataFrame с координатами
    city_coords = {
        'Коломбо': [6.9271, 79.8612],
        'Мале': [4.1755, 73.5093],
        'Ташкент': [41.2995, 69.2401],
        'Бангкок': [13.7563, 100.5018],
        'Белград': [44.7866, 20.4489],
        'Дубай': [25.276987, 55.296249],
        'Стамбул': [41.0082, 28.9784],
        'Манила': [14.5995, 120.9842],
        'Подгорица': [42.4411, 19.2636],
        'Маврикий': [-20.348404, 57.552152],
        'Токио': [35.6762, 139.6503],
        'Варадеро': [23.1460, -81.2752]
    }
    
    # Группируем данные
    city_stats = df.groupby(['destination_city', 'destination_country']).agg(
        avg_price=('price', 'mean'),
        flight_count=('price', 'count')
    ).reset_index()
    
    # Добавляем координаты
    city_stats['lat'] = city_stats['destination_city'].map(lambda x: city_coords.get(x, [0,0])[0])
    city_stats['lon'] = city_stats['destination_city'].map(lambda x: city_coords.get(x, [0,0])[1])
    
    # Создаём интерактивную карту
    fig = px.scatter_geo(city_stats,
                        lat='lat',
                        lon='lon',
                        color='avg_price',
                        size='flight_count',
                        hover_name='destination_city',
                        hover_data=['destination_country', 'avg_price', 'flight_count'],
                        projection='natural earth',
                        title='Распределение направлений по средней цене и количеству рейсов',
                        color_continuous_scale='Viridis')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 2. Аналитические выводы по карте
    st.markdown("""
    ### Ключевые наблюдения:
    
    **1. Географические кластеры:**
    - **Азия/Океания:** 60% направлений, средние цены (15-25 тыс. руб)
    - **Европа:** 25% направлений, бюджетные варианты (Турция, Сербия)
    - **Америка/Африка:** 15%, премиум-сегмент (Куба, Маврикий)
    
    **2. Зависимость цены от расстояния:**
    - Ближнее зарубежье (Узбекистан, ОАЭ) — от 5 до 15 тыс. руб
    - Дальние направления (Япония, Куба) — от 25 тыс. руб
    """)

    # 3. Анализ цен по городам отправления (с фильтрацией)
    st.subheader("Сравнение цен по городам вылета (3+ направлений)")
    
    # Фильтруем города с 3+ направлениями
    city_counts = df['origin_name'].value_counts()
    valid_cities = city_counts[city_counts >= 3].index.tolist()
    filtered_df = df[df['origin_name'].isin(valid_cities)]
    
    # Рассчитываем средние цены
    avg_prices = filtered_df.groupby('origin_name', as_index=False)['price'].mean()
    min_price = avg_prices['price'].min()
    max_price = avg_prices['price'].max()
    
    # Создаем интерактивный график
    fig = px.bar(
        avg_prices.sort_values('price'),
        x='origin_name',
        y='price',
        color='price',
        color_continuous_scale=[(0, '#1f77b4'), (1, '#ff7f0e')],
        range_color=[min_price, max_price],
        title='Средняя стоимость авиабилетов из городов с 3+ направлениями',
        labels={'origin_name': 'Город отправления', 'price': 'Средняя цена (руб)'},
        text_auto='.0f',
        height=500
    )
    
    # Выделяем минимальное и максимальное значения
    fig.update_traces(
        marker_line_color='rgba(0,0,0,0.7)',
        marker_line_width=1.5,
        textposition='outside'
    )
    
    # Настройки отображения
    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis_range=[min_price*0.9, max_price*1.1],
        hovermode='x',
        coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 4. Выводы
    st.markdown("""
    ### Ключевые выводы:
    
    **1. Москва** (лучшее предложение):
    - Средняя цена: **{} руб** (на 25-40% ниже, чем в регионах)
    - Прямые рейсы в {} направлений
    - **Совет:** Используйте как пересадочный хаб
    
    **2. Владивосток, Иркутск и Красноярск** (специфический профиль):
    ```python
    # Направления из Владивостока:
    {}
    ```
    - Всего {} направлений (только Азия)
    - Средняя цена: **{} руб** (дешевле Москвы на азиатские направления)
    
    **3. Самые дорогие города**:
    - {}: **{} руб** (+{}% к Москве)
    - Причины: мало перевозчиков, сезонный спрос
    """.format(
        int(avg_prices[avg_prices['origin_name'] == 'Москва']['price'].values[0]),
        city_counts['Москва'],
        filtered_df[filtered_df['origin_name'] == 'Владивосток'][['destination_city', 'price']].to_string(index=False),
        city_counts['Владивосток'],
        int(avg_prices[avg_prices['origin_name'] == 'Владивосток']['price'].values[0]),
        avg_prices.sort_values('price', ascending=False).iloc[0]['origin_name'],
        int(avg_prices.sort_values('price', ascending=False).iloc[0]['price']),
        int((avg_prices.sort_values('price', ascending=False).iloc[0]['price'] / min_price - 1) * 100)
    ))

    # 4. Анализ цен по городам отправления и типам отдыха
    st.header("Анализ цен по городам отправления и типам отдыха")
    
    # Подготовка данных - фильтрация городов с 3+ направлениями
    city_counts = df['origin_name'].value_counts()
    filtered_df = df[df['origin_name'].isin(city_counts[city_counts > 2].index)]
    
    # Создание интерактивного графика
    fig = px.bar(
        filtered_df,
        x='origin_name',
        y='price',
        color='Type_of_rest',
        barmode='group',
        title='Средняя стоимость билетов по городам отправления и типам отдыха',
        labels={
            'origin_name': 'Город отправления',
            'price': 'Цена (руб)',
            'Type_of_rest': 'Тип отдыха'
        },
        color_discrete_sequence=px.colors.qualitative.Set2,
        hover_data=['destination_city']
    )
    
    # Настройка внешнего вида
    fig.update_layout(
        xaxis_tickangle=-45,
        yaxis_gridcolor='lightgray',
        plot_bgcolor='rgba(0,0,0,0)',
        legend_title_text='Тип отдыха',
        hovermode='x unified',
        height=600
    )
    
    # Добавление средних линий для каждого типа
    for rest_type in filtered_df['Type_of_rest'].unique():
        mean_price = filtered_df[filtered_df['Type_of_rest'] == rest_type]['price'].mean()
        fig.add_hline(
            y=mean_price, 
            line_dash='dot',
            line_color=px.colors.qualitative.Set2[list(filtered_df['Type_of_rest'].unique()).index(rest_type)],
            annotation_text=f'Среднее {rest_type}: {mean_price:,.0f} руб',
            annotation_position='top right'
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 5. Выводы
    st.subheader("Ключевые выводы:")
    dist_tab1, dist_tab2 = st.tabs(["Региональные различия", "Разница по типам отдыха"])

    with dist_tab1:
        st.markdown("""
        ### Региональные различия:
        - Самые высокие тарифы в **Минске** и **Казани** (до {:,} руб) из-за:
            - Ограниченного количества рейсов
            - Премиальных направлений
        - Самые низкие цены в **Москве** и **Иркутске** (от {:,} руб) благодаря:
            - Высокой конкуренции авиакомпаний
            - Выгодному географическому положению """.format(
            filtered_df['price'].max(),
            filtered_df['price'].min()
        ))

    with dist_tab2:
        # Статистические показатели в виде колонок
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### Пляжный отдых:
            - Дороже в Казани и Минске
            - Дешевле в Дубае и Стамбуле
            """)
        
        with col2:
            st.markdown("""
            ### Культурный отдых:
            - Самые доступные варианты в Стамбуле и Сочи
            - Дорогие билеты из Екатеринбурга и Санкт-Петербурга
            """)
        
        with col3:
            st.markdown("""
            ### Городской отдых:
            - Дешевле в Красноярске и Новосибирске
            - В Иркутске цены низкие из-за близости к Азии""")
    
    
    st.header("🌍 Распределение типов отдыха по регионам")
    
    # 1. Создаем функцию для группировки городов
    def get_geo_group(city):
        groups = {
            'Дальний Восток': ['Владивосток', 'Хабаровск'],
            'Урал': ['Екатеринбург', 'Уфа', 'Тюмень', 'Пермь', 'Челябинск'],
            'Сибирь': ['Иркутск', 'Красноярск', 'Новосибирск', 'Омск', 'Томск', 'Барнаул'],
            'Центральная Россия': ['Москва', 'Казань', 'Нижний Новгород', 'Самара', 'Воронеж',
                                  'Ярославль', 'Тула', 'Рязань', 'Смоленск', 'Тверь', 'Иваново'],
            'Северо-Запад': ['Санкт-Петербург', 'Калининград', 'Мурманск', 'Архангельск',
                            'Петрозаводск', 'Великий Новгород', 'Псков'],
            'Юг России': ['Сочи', 'Волгоград', 'Махачкала', 'Минеральные Воды',
                         'Владикавказ', 'Ставрополь', 'Краснодар', 'Ростов-на-Дону', 'Астрахань'],
            'Международные': ['Дубай', 'Абу-Даби', 'Мале', 'Бангкок', 'Коломбо', 'Сингапур',
                             'Минск', 'Пхукет', 'Стамбул', 'Эль-Нидо', 'Себу', 'Катиклан',
                             'Гонконг', 'Барселона', 'Баку', 'Вена', 'Белград', 'Астана',
                             'Пекин', 'Шанхай', 'Канкун', 'Пунта-Кана', 'Санто-Доминго', 'Мехико']
        }
        for group, cities in groups.items():
            if city in cities:
                return group
        return 'Другие'

    # 2. Применяем группировку
    df['geo_group'] = df['origin_name'].apply(get_geo_group)
    
    # 3. Создаем кросс-таблицу
    cross_tab = pd.crosstab(
        index=df['geo_group'],
        columns=df['Type_of_rest'],
        normalize='index'
    ).round(3) * 100
    
    # 4. Строим интерактивную тепловую карту
    fig = px.imshow(
        cross_tab,
        labels=dict(x="Тип отдыха", y="Регион", color="Доля, %"),
        color_continuous_scale='YlGnBu',
        text_auto=".1f",
        aspect="auto"
    )
    
    # 5. Настраиваем оформление
    fig.update_layout(
        title="Предпочтения типов отдыха по регионам (%)",
        xaxis_title="Тип отдыха",
        yaxis_title="Географическая группа",
        height=600,
        coloraxis_colorbar=dict(
            title="Доля, %",
            ticksuffix="%"
        )
    )
    
    # 6. Отображаем график
    st.plotly_chart(fig, use_container_width=True)
    
    # 8. Добавляем аналитические выводы
    st.markdown("""
    ### 🔍 Ключевые наблюдения:
    
    **1. Самые популярные типы отдыха по регионам:**
    ```python
    {}
    ```
    
    **2. Наибольшие предпочтения:**
    - **{}** - {:.1f}% предпочитают {}
    - **{}** - {:.1f}% предпочитают {}
    
    **3. Самые сбалансированные регионы:**
    {}
    """.format(
cross_tab.idxmax(axis=1).to_string(),
cross_tab.max(axis=1).idxmax(),
cross_tab.max(axis=1).max(),
cross_tab.idxmax(axis=1)[cross_tab.max(axis=1).idxmax()],
cross_tab.max(axis=1).idxmin(),
cross_tab.max(axis=1).min(),
cross_tab.idxmax(axis=1)[cross_tab.max(axis=1).idxmin()],
", ".join(cross_tab[(cross_tab.max(axis=1) - cross_tab.min(axis=1)) < 15].index.tolist())
))

elif page == "Тренды":
    # Ценовые тренды
    city_counts = df['origin_name'].value_counts()
    filtered_df = df[df['origin_name'].isin(city_counts[city_counts > 2].index)]

    st.header("Анализ ценовых трендов")
    selected_city = st.selectbox(
            "Выберите город для анализа:",
            filtered_df['origin_name'].unique()
        ) 
    city_data = filtered_df[filtered_df['origin_name'] == selected_city]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Статистика по {selected_city}:**")
        st.dataframe(city_data.groupby('Type_of_rest')['price'].describe().style.format('{:.1f}'))
        
    with col2:
        st.markdown("**Топ направлений:**")
        st.dataframe(city_data.sort_values('price', ascending=False).head(3)[['destination_city', 'Type_of_rest', 'price']])

    #Сводная таблица цен по городам
    st.header("Сводная таблица цен")
    compare_cities = st.multiselect(
    "Сравните города отправления",
    options=df['origin_name'].unique(),
    default=["Москва", "Санкт-Петербург"]
    )
    comparison_df = df[df['origin_name'].isin(compare_cities)].groupby('origin_name').agg({
        'price': ['mean', 'min', 'max'],
        'destination_city': 'nunique'
    })
    st.dataframe(comparison_df.style.format('{:.1f}'))


    #Анализ "что если" с кнопкой
    st.subheader("Сценарий 'Что если'")
    base_city = st.selectbox("Город вылета", df['origin_name'].unique())
    budget = st.slider("Ваш бюджет (руб)", min_value=1000, value=20000)
    if st.button("Показать доступные направления"):
        result_df = df[(df['origin_name'] == base_city) & (df['price'] <= budget)]
        st.write(f"Найденo {len(result_df)} направлений:")
        st.dataframe(result_df)

    #Топ-5 самых выгодных направлений
    st.subheader("Самые выгодные предложения")
    col1, col2 = st.columns(2)
    with col1:
        city_filter = st.selectbox("Город отправления", ["Все"] + list(df['origin_name'].unique()))
    with col2:
        rest_type_filter = st.selectbox("Тип отдыха", ["Все"] + list(df['Type_of_rest'].unique()))

    filtered_df = df
    if city_filter != "Все":
        filtered_df = filtered_df[filtered_df['origin_name'] == city_filter]
    if rest_type_filter != "Все":
        filtered_df = filtered_df[filtered_df['Type_of_rest'] == rest_type_filter]

    top5 = filtered_df.sort_values('price').head(5)
    st.dataframe(top5)

# 5. Раздел «Выводы»
elif page == "Выводы":
    st.header("Ключевые инсайты и рекомендации")
    
    # 1. Основные инсайты (в виде аккордеона)
    with st.expander("🔍 Основные выводы из анализа", expanded=True):
        st.markdown("""
        ### Динамика цен:
        - **Средняя стоимость билета:** 18 000 руб (разброс от 5 000 до 46 000 руб)
        - **Самые дорогие направления:** Куба (Варадеро), Маврикий, Мальдивы
        - **Бюджетные варианты:** Турция (Стамбул), ОАЭ (Дубай), Таиланд (Бангкок)

        ### Популярные маршруты:
        - **Топ-3 направления:** Коломбо (Шри-Ланка), Стамбул (Турция), Дубай (ОАЭ)
        - Москва — главный авиахаб с максимальным выбором рейсов
        - Региональные аэропорты предлагают меньше вариантов, но иногда выгодные цены

        ### География спроса:
        - 34% — пляжный отдых (Мальдивы, Шри-Ланка)
        - 33% — городской туризм (Стамбул, Дубай)
        - 33% — культурные поездки (Ташкент, Белград)
        """)

    # 2. Рекомендации (в виде карточек)
    st.subheader("Советы для путешественников (май 2026)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Выбор направления**  
        ▪ Для коротких поездок (4-5 дней): Стамбул, Ташкент  
        ▪ Комбинированные туры: Коломбо + Мальдивы  
        ▪ Внутренний туризм: Сочи, Кавказские Минеральные Воды
        """)
    
    with col2:
        st.success("""
        **Экономия на перелётах**  
        ▪ Бронируйте за 2-3 месяца  
        ▪ Сравнивайте цены из разных городов  
        ▪ Используйте стыковочные рейсы через Дубай/Стамбул
        """)
    
    with col3:
        st.warning("""
        **Региональные особенности**  
        ▪ Дальний Восток: Азия (Токио, Бангкок)  
        ▪ Юг России: пряые рейсы в ОАЭ  
        ▪ Урал/Сибирь: Турция, Шри-Ланка
        """)

    # 3. Дальнейшее развитие анализа
    st.subheader("Что можно улучшить?")
    st.markdown("""
    - **Добавить данные:**  
      ▪ Сезонную динамику цен (Новый год vs майские праздники)  
      ▪ Стоимость отелей и питания в пунктах назначения  
      ▪ Рейтинги авиакомпаний и удобство маршрутов
    
    - **Углубить анализ:**  
      ▪ Влияние длительности перелёта на цены  
      ▪ Карту доступности направлений из разных регионов  
      ▪ AI-предсказание оптимального времени бронирования
    """)

    # 4. Интерактивный элемент
    st.subheader("📌 Ваше мнение")
    user_feedback = st.selectbox(
        "Какой тип отдыха вы предпочитаете в мае?",
        ["Пляжный", "Городской", "Культурный", "Другое"]
    )
    if st.button("Отправить"):
        st.toast(f"Спасибо! Ваш выбор: {user_feedback}", icon="👍")