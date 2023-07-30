# импортируем библиотеки
import pandas as pd
import numpy as np
import streamlit as st
import xlrd

# импортируем пакет
import dill

# загрузим ранее сохраненный конвейер
with open('pipeline_for_deployment.pkl', 'rb') as f:
    pipe = dill.load(f)

# функция запуска веб-интерфейса
def run():
    from PIL import Image
    image = Image.open('logo.jpg')
    
    st.sidebar.image(image)
    
    question = ("В каком режиме вы хотели бы сделать прогноз, Онлайн\n"
               "(Online) или загрузкой файла данных(Batch)?")
    
    add_selectbox = st.sidebar.selectbox(question, ("Online", "Batch", "Загрузить данные"))
    
    sidebar_ttl = ("Прогнозирование неуспеваемости с использованием\n"
                  "метода логистической регрессии.")
    
    st.sidebar.info(sidebar_ttl)
    st.title("Прогнозирование неуспеваемости")
    
    if add_selectbox == "Online":
        
        Gender = st.radio("Пол студента", ["М", "Ж"],
                          index = 0)
        Obshezitie = st.radio("Нуждается в общежитии", ["", "нет", "да"],
                              index = 0)
        Grazdanstvo = st.selectbox("Гражданство", ["Россия", "Узбекистан",
                                                   "Казахстан", "Монголия", 
                                                   "Другие страны"],
                                   index = 0, help = "выберите гражданство из раскрывающегося списка")
        if Grazdanstvo == "Россия":
            Inostranec = st.radio("Иностранец", ["нет", "да"],
                              index = 0, disabled = True)
        else:
            Inostranec = st.radio("Иностранец", ["нет", "да"],
                              index = 1, disabled = True)
        TipDogovora = st.radio("Тип договора", ["бюджетник", "целевик", "платник"],
                               index = 0)
        if TipDogovora == "бюджетник":
            VidZatrat = st.radio("Вид затрат", ["бюджет", "по договору"],
                                 index = 0, disabled = True)
            CelevoiPriem = st.radio("Целевой прием", ["да", "нет"],
                                    index = 1, disabled = True)
        if TipDogovora == "целевик":
            VidZatrat = st.radio("Вид затрат", ["бюджет", "по договору"],
                                 index = 0, disabled = True)
            CelevoiPriem = st.radio("Целевой прием", ["да", "нет"],
                                    index = 0, disabled = True)
        if TipDogovora == "платник":
            VidZatrat = st.radio("Вид затрат", ["бюджет", "по договору"],
                                 index = 1, disabled = True)
            CelevoiPriem = st.radio("Целевой прием", ["да", "нет"],
                                    index = 1, disabled = True)

        Facultet = st.radio("Формирующее подразделение", ["Автоматизация и интеллектуальные технологии (Факультет)",
                                              "Промышленное и гражданское строительство (Факультет)",
                                              "Транспортные и энергетические системы (Факультет)",
                                              "Транспортное строительство (Факультет)",
                                              "Управление перевозками и логистика (Факультет)",
                                              "Экономика и менеджмент (Факультет)"],
                                index = 0)
        
        if Facultet == "Автоматизация и интеллектуальные технологии (Факультет)":
            NapravleniePodgotovki = st.selectbox("Направление подготовки",
                                                 ["",
                                                  "09.03.01 Информатика и вычислительная техника (направление бакалавров, ВО 2013)",
                                                  "10.05.03 Информационная безопасность автоматизированных систем (специальность ВО, ВО 2013)",
                                                  "23.05.05 Системы обеспечения движения поездов (специальность ВО, ВО 2013)",
                                                  "38.03.05 Бизнес-информатика (направление бакалавров, ВО 2013)"],
                                                  index = 0, help = "выберите направление подготовки из раскрывающегося списка")
            if NapravleniePodgotovki == "":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = False)
            if NapravleniePodgotovki == "10.05.03 Информационная безопасность автоматизированных систем (специальность ВО, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 2, horizontal = True, disabled = True)
            if NapravleniePodgotovki == "23.05.05 Системы обеспечения движения поездов (специальность ВО, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 1, horizontal = True, disabled = True) 
            if NapravleniePodgotovki == "09.03.01 Информатика и вычислительная техника (направление бакалавров, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = True)
            if NapravleniePodgotovki == "38.03.05 Бизнес-информатика (направление бакалавров, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = True)
        if Facultet == "Промышленное и гражданское строительство (Факультет)":
            NapravleniePodgotovki = st.selectbox("Направление подготовки",
                                                     ["",
                                                      "08.03.01 Строительство (направление бакалавров, ВО 2013)",
                                                      "08.05.01 Строительство уникальных зданий и сооружений (специальность ВО, ВО 2013)",
                                                      "20.03.01 Техносферная безопасность (направление бакалавров, ВО 2013)",
                                                      "27.03.01 Стандартизация и метрология (направление бакалавров, ВО 2013)"],
                                                     index = 0, help = "выберите направление подготовки из раскрывающегося списка")
            if NapravleniePodgotovki == "":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = False)
            if NapravleniePodgotovki == "08.05.01 Строительство уникальных зданий и сооружений (специальность ВО, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 3, horizontal = True, disabled = True)      
            if NapravleniePodgotovki == "08.03.01 Строительство (направление бакалавров, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = True)
            if NapravleniePodgotovki == "20.03.01 Техносферная безопасность (направление бакалавров, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = True)
            if NapravleniePodgotovki == "27.03.01 Стандартизация и метрология (направление бакалавров, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = True)
        if Facultet == "Транспортные и энергетические системы (Факультет)":
            NapravleniePodgotovki = st.selectbox("Направление подготовки",
                                                ["",
                                                 "23.03.03 Эксплуатация транспортно-технологических машин и комплексов (направление бакалавров, ВО 2013)",
                                                 "23.05.01 Наземные транспортно-технологические средства (специальность ВО, ВО 2013)",
                                                 "23.05.03 Подвижной состав железных дорог (специальность ВО, ВО 2013)"],
                                                index = 0, help = "выберите направление подготовки из раскрывающегося списка")
            if NapravleniePodgotovki == "":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = False)
            if NapravleniePodgotovki == "23.05.01 Наземные транспортно-технологические средства (специальность ВО, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 1, horizontal = True, disabled = True)
            if NapravleniePodgotovki == "23.05.03 Подвижной состав железных дорог (специальность ВО, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 1, horizontal = True, disabled = True)
            if NapravleniePodgotovki == "23.03.03 Эксплуатация транспортно-технологических машин и комплексов (направление бакалавров, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = True)
        if Facultet == "Транспортное строительство (Факультет)":
            NapravleniePodgotovki = st.selectbox("Направление подготовки",
                                                ["",
                                                "23.05.06 Строительство железных дорог, мостов и транспортных тоннелей (специальность ВО, ВО 2013)"],
                                                index = 0, help = "выберите направление подготовки из раскрывающегося списка")
            if NapravleniePodgotovki == "":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = False)
            if NapravleniePodgotovki == "23.05.06 Строительство железных дорог, мостов и транспортных тоннелей (специальность ВО, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 1, horizontal = True, disabled = True)
        if Facultet == "Управление перевозками и логистика (Факультет)":
            NapravleniePodgotovki = st.selectbox("Направление подготовки",
                                                ["",
                                                "23.05.04 Эксплуатация железных дорог (специальность ВО, ВО 2013)",
                                                "38.03.02 Менеджмент (направление бакалавров, ВО 2013)"],
                                                 index = 0, help = "выберите направление подготовки из раскрывающегося списка")
            if NapravleniePodgotovki == "":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = False)
            if NapravleniePodgotovki == "23.05.04 Эксплуатация железных дорог (специальность ВО, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 1, horizontal = True, disabled = True)
            if NapravleniePodgotovki == "38.03.02 Менеджмент (направление бакалавров, ВО 2013)":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = True)
        if Facultet == "Экономика и менеджмент (Факультет)":
            NapravleniePodgotovki = st.selectbox("Направление подготовки",
                                                ["",
                                                "37.03.01 Психология (направление бакалавров, ВО 2013)",
                                                "38.03.01 Экономика (направление бакалавров, ВО 2013)",
                                                "38.03.02 Менеджмент (направление бакалавров, ВО 2013)"],
                                                index = 0, help = "выберите направление подготовки из раскрывающегося списка")
            if NapravleniePodgotovki == "":
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = False)
            else:
                SrokObucheniya = st.radio("Срок обучения по направлению подготовки", ["4 года", "5 лет", "5,5 лет", "6 лет"],
                                      index = 0, horizontal = True, disabled = True)
        Obrazovanie = st.selectbox("Полученное довузовское образование",
                                   ["",
                                    "Среднее общее образование, получено в год поступления",
                                    "Среднее общее образование, получено за год до поступления",
                                    "Среднее общее образование, получено за два года до поступления",
                                    "Среднее общее образование, получено за три года до поступления",
                                    "Среднее профессиональное образование, получено в год поступления"],
                                    index = 0, help = "выберите довузовское образование из раскрывающегося списка")
        if Obrazovanie == "":
            SrBallDokObr = st.number_input('Средний балл документа о довузовском образовании',
                                           min_value = 3.00, max_value = 5.00,
                                           value = 3.00,
                                           help = "для ввода среднего балла укажите полученное довузовское образование",
                                           disabled = True)
        else:
            SrBallDokObr = st.number_input('Средний балл документа о довузовском образовании',
                                           min_value = 3.00, max_value = 5.00,
                                           value = 3.00,
                                           help = "введите средний балла с точностью до 2-х знаков после запятой")
        SdavalEge = st.radio("Сдавал ЕГЭ", ["", "нет", "да"],
                             index = 0)
        if SdavalEge == "да":
            EgeMath = st.slider('Математика ЕГЭ', min_value = 36, max_value = 100,
                                value = 36, step = 1)
            EgeRus = st.slider('Русский язык ЕГЭ', min_value = 36, max_value = 100,
                               value = 36, step = 1)
        else:
            EgeMath = st.slider('Математика ЕГЭ', min_value = 36, max_value = 100,
                                value = 36, step = 1, disabled = True,
                                help = "для ввода баллов укажите, что сдавали ЕГЭ")
            EgeRus = st.slider('Русский язык ЕГЭ', min_value = 36, max_value = 100,
                               value = 36, step = 1, disabled = True,
                               help = "для ввода баллов укажите, что сдавали ЕГЭ")
        
        input_dict = {
            'Пол': Gender,
            'Нуждается в общежитии': Obshezitie,
            'Гражданство': Grazdanstvo,
            'Иностранец': Inostranec,
            'Тип договора': TipDogovora,
            'Вид затрат': VidZatrat,
            'Целевой прием': CelevoiPriem,
            'Факультет': Facultet,
            'Направление подготовки': NapravleniePodgotovki,
            'Срок обучения': SrokObucheniya,
            'Полученное образование': Obrazovanie,
            'Сдавал ЕГЭ': SdavalEge,
            'Ср. балл док-та об образовании': SrBallDokObr,
            'Математика ЕГЭ': EgeMath,
            'Русский язык ЕГЭ': EgeRus
        }
        input_df = pd.DataFrame([input_dict])
              
        if st.button("Получить прогноз"):
            
            # выделим категориальные переменные
            categoric_columns = [c for c in input_df.columns if input_df[c].dtype.name == 'object']

            # присвоим категориальным переменным тип str
            # тип str формирует для пропусков отдельную категорию nan
            for c in categoric_columns:
                if c in input_df.columns:
                    input_df[c] = input_df[c].astype('str')

            # создадим функцию обработки
            # категорий переменной 'Полученное образование'
            # в зависимости от года набора
            def GodNabora(year):
                return year
            def Nabor(GodNabora):
                Edu = input_df.copy()
                # запишем словарь переименования возможныж категорий
                d = {'Среднее общее образование, {} г.'.format(GodNabora):'Среднее общее образование, получено в год поступления',
                'Среднее общее образование, {} г.'.format(GodNabora-1):'Среднее общее образование, получено за год до поступления',
                'Среднее общее образование, {} г.'.format(GodNabora-2):'Среднее общее образование, получено за два года до поступления',
                'Среднее общее образование, {} г.'.format(GodNabora-3):'Среднее общее образование, получено за три года до поступления',
                'Среднее профессиональное образование, {} г.'.format(GodNabora):'Среднее профессиональное образование, получено в год поступления',
                        'Другое образование':'Другое образование', 'nan':'nan'}
                # заменим категории по словарю
                Edu['Полученное образование'] = Edu['Полученное образование'].map(d)
                # объединим категории переменной 'Полученное образование'
                # в категорию 'Другое образование' кроме категорий
                # 'Среднее общее образование, получено в год поступления'
                # 'Среднее общее образование, получено за год до поступления'
                # 'Среднее общее образование, получено за два года до поступления'
                # 'Среднее общее образование, получено за три года до поступления'
                # 'Среднее профессиональное образование, получено в год поступления'
                # 'nan'
                Edu['Полученное образование'] = [x if x in ['Среднее общее образование, получено в год поступления',
                                                           'Среднее общее образование, получено за год до поступления',
                                                           'Среднее общее образование, получено за два года до поступления',
                                                           'Среднее общее образование, получено за три года до поступления',
                                                           'Среднее профессиональное образование, получено в год поступления',
                                                           'nan']
                                                else 'Другое образование'
                                                for x in Edu['Полученное образование']]
                return Edu['Полученное образование']

            # создадим функцию объединения редких категорий
            # независимой переменной 'Гражданство'
            # в зависимости от размера наименьшей допустимой категории
            # задаваемой в % от объема всей выборки
            def PercentRestOfWorld(percent):
                return percent
            def RestOfWorld(PercentRestOfWorld):
                Nation = input_df.copy()
                Nation['Гражданство'][Nation.groupby('Гражданство')['Гражданство'].transform('count') < PercentRestOfWorld * len(Nation) / 100] = 'Другие страны'   
                return Nation['Гражданство']

            # создадим фукнцию порога исключения из анализа независимых переменных
            # у которых доля битых данных первышает этот порог
            # задаваемый в % от объемах всей выборки
            def OutOfAnalysis(threshold):
                return threshold / 100

            # запишем функцию предварительной обработки данных
            def preprocessing(df, GodNabora, PercentRestOfWorld, OutOfAnalysis):

                # назначим синий цвет сообщениям
                def out_red(text):
                    print("\033[34m{}".format(text))
                out_red("")

                # сообщим о категориях переменной 'Полученное образование'
                print("Наименование категорий для {:.0f} года набора:".format(GodNabora))
                print(Nabor(GodNabora).value_counts())

                # назначим зеленый цвет сообщениям
                def out_red(text):
                    print("\033[32m{}".format(text))
                out_red("")

                # сообщим о категориях переменной 'Гражданство'
                print("Объединение категорий с частотами меньше {:.0f}% от объема всей выборки:".format(PercentRestOfWorld))
                print(RestOfWorld(PercentRestOfWorld).value_counts())

                # выделим категориальные переменные
                categorical_columns = [c for c in df.columns if df[c].dtype.name == 'object']
                del categorical_columns[0:2]

                # выделим количественные переменные
                numerical_columns = [c for c in df.columns if df[c].dtype.name != 'object']

                # заполним датафрейм обработанными данными
                df['Полученное образование'] = Nabor(GodNabora)
                df['Гражданство'] = RestOfWorld(PercentRestOfWorld)

                # заменим пропуски в категориальных переменных нулями
                for c in categorical_columns:
                    df[c] = np.where((df[c] == 'nan'), 0, df[c])

                # заменим пропуски и значения меньше 3 баллов
                # независимой переменной 'Ср. балл док-та об образовании'
                # значением 0 баллов
                df['Ср. балл док-та об образовании'] = np.where((df['Ср. балл док-та об образовании'].isnull()) |
                                                             (df['Ср. балл док-та об образовании'] < 3),
                                                             0,
                                                             df['Ср. балл док-та об образовании'])
                # заменим пропуски и значения меньше 36 баллов
                # независимых переменных 'Русский язык ЕГЭ' и 'Математика ЕГЭ'
                # значением 0 баллов
                df['Русский язык ЕГЭ'] = np.where((df['Русский язык ЕГЭ'].isnull()) |
                                                             (df['Русский язык ЕГЭ'] < 36),
                                                             0,
                                                             df['Русский язык ЕГЭ'])
                df['Математика ЕГЭ'] = np.where((df['Математика ЕГЭ'].isnull()) |
                                                             (df['Математика ЕГЭ'] < 36),
                                                             0,
                                                             df['Математика ЕГЭ']) 

                # преобразуем независимые переменные 'Русский язык ЕГЭ' и 'Математика ЕГЭ' 
                # из типа float в тип int
                for i in ['Русский язык ЕГЭ', 'Математика ЕГЭ']:
                    if i in df.columns:
                        df[i] = df[i].astype('int64')       

                # назначим красный цвет сообщениям 
                def out_red(text):
                    print("\033[31m{}".format(text))
                out_red("")

                # сообщим об исключении переменных из анализа
                print("Исключены из анализа переменные с более {:.0f}% битых данных:".format(OutOfAnalysis * 100))

                # исключены из анализа независимые переменные
                # с числом нулевых значений больше порогового % от объема выборки
                for c in df:
                    if len(df[df[c] == 0]) > OutOfAnalysis * len(df):
                        print(c, "-", len(df[df[c] == 0]), "пропусков")
                        del df[c]
                print('*** конец списка ***')

                return df         
            
            # выполняем предварительную обработку новых данных
            preprocessing(input_df, GodNabora(2023), PercentRestOfWorld(2), OutOfAnalysis(50))
            # вычисляем вероятности для новых данных
            output = pipe.predict_proba(input_df)[0, 1]

            if output >= .4:
                st.markdown(
                    """
                    <style>
                    .stProgress > div > div > div > div {
                    background-color: red;
                    }
                    </style>""",
                    unsafe_allow_html=True,
                )
                st.progress(value = output, text = "Высокая вероятность неуспеваемости: {:.0f}%".format(output * 100))
            if (.25 <= output < .4):
                st.markdown(
                    """
                    <style>
                    .stProgress > div > div > div > div {
                    background-color: orange;
                    }
                    </style>""",
                    unsafe_allow_html=True,
                )
                st.progress(value = output, text = "Средняя вероятность неуспеваемости: {:.0f}%".format(output * 100))
            if (output < .25):
                st.markdown(
                    """
                    <style>
                    .stProgress > div > div > div > div {
                    background-color: green;
                    }
                    </style>""",
                    unsafe_allow_html=True,
                )
                st.progress(value = output, text = "Низкая вероятность неуспеваемости: {:.0f}%".format(output * 100))
        
    if add_selectbox == "Batch":
        
        file_upload_ttl = ("Загрузите csv-файл с новыми данными\n"
                          "для вычисления вероятностей:")
        file_upload = st.file_uploader(file_upload_ttl, type = ['csv'])
        
        if file_upload is not None:
            newdata = pd.read_csv(file_upload, sep = ';')
            
            # выделим категориальные переменные
            categoric_columns = [c for c in newdata.columns if newdata[c].dtype.name == 'object']

            # присвоим категориальным переменным тип str
            # тип str формирует для пропусков отдельную категорию nan
            for c in categoric_columns:
                if c in newdata.columns:
                    newdata[c] = newdata[c].astype('str')

            # создадим функцию обработки
            # категорий переменной 'Полученное образование'
            # в зависимости от года набора
            def GodNabora(year):
                return year
            def Nabor(GodNabora):
                Edu = newdata.copy()
                # запишем словарь переименования возможныж категорий
                d = {'Среднее общее образование, {} г.'.format(GodNabora):'Среднее общее образование, получено в год поступления',
                'Среднее общее образование, {} г.'.format(GodNabora-1):'Среднее общее образование, получено за год до поступления',
                'Среднее общее образование, {} г.'.format(GodNabora-2):'Среднее общее образование, получено за два года до поступления',
                'Среднее общее образование, {} г.'.format(GodNabora-3):'Среднее общее образование, получено за три года до поступления',
                'Среднее профессиональное образование, {} г.'.format(GodNabora):'Среднее профессиональное образование, получено в год поступления',
                        'Другое образование':'Другое образование', 'nan':'nan'}
                # заменим категории по словарю
                Edu['Полученное образование'] = Edu['Полученное образование'].map(d)
                # объединим категории переменной 'Полученное образование'
                # в категорию 'Другое образование' кроме категорий
                # 'Среднее общее образование, получено в год поступления'
                # 'Среднее общее образование, получено за год до поступления'
                # 'Среднее общее образование, получено за два года до поступления'
                # 'Среднее общее образование, получено за три года до поступления'
                # 'Среднее профессиональное образование, получено в год поступления'
                # 'nan'
                Edu['Полученное образование'] = [x if x in ['Среднее общее образование, получено в год поступления',
                                                           'Среднее общее образование, получено за год до поступления',
                                                           'Среднее общее образование, получено за два года до поступления',
                                                           'Среднее общее образование, получено за три года до поступления',
                                                           'Среднее профессиональное образование, получено в год поступления',
                                                           'nan']
                                                else 'Другое образование'
                                                for x in Edu['Полученное образование']]
                return Edu['Полученное образование']

            # создадим функцию объединения редких категорий
            # независимой переменной 'Гражданство'
            # в зависимости от размера наименьшей допустимой категории
            # задаваемой в % от объема всей выборки
            def PercentRestOfWorld(percent):
                return percent
            def RestOfWorld(PercentRestOfWorld):
                Nation = newdata.copy()
                Nation['Гражданство'][Nation.groupby('Гражданство')['Гражданство'].transform('count') < PercentRestOfWorld * len(Nation) / 100] = 'Другие страны'   
                return Nation['Гражданство']

            # создадим фукнцию порога исключения из анализа независимых переменных
            # у которых доля битых данных первышает этот порог
            # задаваемый в % от объемах всей выборки
            def OutOfAnalysis(threshold):
                return threshold / 100

            # запишем функцию предварительной обработки данных
            def preprocessing(df, GodNabora, PercentRestOfWorld, OutOfAnalysis):

                # назначим синий цвет сообщениям
                def out_red(text):
                    print("\033[34m{}".format(text))
                out_red("")

                # сообщим о категориях переменной 'Полученное образование'
                print("Наименование категорий для {:.0f} года набора:".format(GodNabora))
                print(Nabor(GodNabora).value_counts())

                # назначим зеленый цвет сообщениям
                def out_red(text):
                    print("\033[32m{}".format(text))
                out_red("")

                # сообщим о категориях переменной 'Гражданство'
                print("Объединение категорий с частотами меньше {:.0f}% от объема всей выборки:".format(PercentRestOfWorld))
                print(RestOfWorld(PercentRestOfWorld).value_counts())

                # выделим категориальные переменные
                categorical_columns = [c for c in df.columns if df[c].dtype.name == 'object']
                del categorical_columns[0:2]

                # выделим количественные переменные
                numerical_columns = [c for c in df.columns if df[c].dtype.name != 'object']

                # заполним датафрейм обработанными данными
                df['Полученное образование'] = Nabor(GodNabora)
                df['Гражданство'] = RestOfWorld(PercentRestOfWorld)

                # заменим пропуски в категориальных переменных нулями
                for c in categorical_columns:
                    df[c] = np.where((df[c] == 'nan'), 0, df[c])

                # заменим пропуски и значения меньше 3 баллов
                # независимой переменной 'Ср. балл док-та об образовании'
                # значением 0 баллов
                df['Ср. балл док-та об образовании'] = np.where((df['Ср. балл док-та об образовании'].isnull()) |
                                                             (df['Ср. балл док-та об образовании'] < 3),
                                                             0,
                                                             df['Ср. балл док-та об образовании'])
                # заменим пропуски и значения меньше 36 баллов
                # независимых переменных 'Русский язык ЕГЭ' и 'Математика ЕГЭ'
                # значением 0 баллов
                df['Русский язык ЕГЭ'] = np.where((df['Русский язык ЕГЭ'].isnull()) |
                                                             (df['Русский язык ЕГЭ'] < 36),
                                                             0,
                                                             df['Русский язык ЕГЭ'])
                df['Математика ЕГЭ'] = np.where((df['Математика ЕГЭ'].isnull()) |
                                                             (df['Математика ЕГЭ'] < 36),
                                                             0,
                                                             df['Математика ЕГЭ']) 

                # преобразуем независимые переменные 'Русский язык ЕГЭ' и 'Математика ЕГЭ' 
                # из типа float в тип int
                for i in ['Русский язык ЕГЭ', 'Математика ЕГЭ']:
                    if i in df.columns:
                        df[i] = df[i].astype('int64')       

                # назначим красный цвет сообщениям 
                def out_red(text):
                    print("\033[31m{}".format(text))
                out_red("")

                # сообщим об исключении переменных из анализа
                print("Исключены из анализа переменные с более {:.0f}% битых данных:".format(OutOfAnalysis * 100))

                # исключены из анализа независимые переменные
                # с числом нулевых значений больше порогового % от объема выборки
                for c in df:
                    if len(df[df[c] == 0]) > OutOfAnalysis * len(df):
                        print(c, "-", len(df[df[c] == 0]), "пропусков")
                        del df[c]
                print('*** конец списка ***')

                return df         
            
            # выполняем предварительную обработку новых данных
            preprocessing(newdata, GodNabora(2023), PercentRestOfWorld(2), OutOfAnalysis(50))
            
            # вычисляем вероятности для новых данных
            prob = pipe.predict_proba(newdata)[:, 1]
            probproc = np.round(prob, 2) * 100
            prob_id = newdata[['ФИО', 'Группа']]
            prob_id.insert(loc = 2, column = 'Вероятность неуспеваемости, %', value = probproc)
            
            # вывод вероятностей на веб-странице
            st.success("Вероятности неуспеваемости студентов по загруженным данным:")
            st.write(prob_id)

    if add_selectbox == "Загрузить данные":
        
        file_upload_ttl = ("Загрузите Excel-файл с данными абитуриентов\n"
                          "для построения модели:")
        file_upload = st.file_uploader(file_upload_ttl,
                                       type = ['xls' or 'xlsx'],
                                       accept_multiple_files = False,
                                       help = 'принимаются файлы с расширением xls или xlsx')
        
        if file_upload is not None:
            df_abit = pd.DataFrame()
            data_abit = pd.read_excel(file_upload,
                                      sheet_name = "Абитуриенты",
                                      header = 9)
            df_abit = pd.concat([df_abit, data_abit],
                                ignore_index = True)
            # вывод данных на веб-странице
            st.success("Данные абитуриентов:")
            st.write(df_abit)

if __name__ == '__main__':
    run()
