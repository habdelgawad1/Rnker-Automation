import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill

# Full dataset from the JSON (first 200 athletes to keep processing reasonable)
athletes_data = [
(1, "Svetlana OSIPOVA", "Uzbekistan", 210.20, 25, "UZB-1759"),
(2, "Nafia KUS AYDIN", "Türkiye", 203.32, 30, "TUR-1567"),
(3, "Dagmara HAREMZA", "Poland", 141.48, 23, "POL-1963"),
(4, "Wenzhe MU", "People's Republic Of China", 132.45, 23, "CHN-106651"),
(5, "Tania CASTIÑEIRA ETCHEVERRIA", "Spain", 121.32, 24, "ESP-2188"),
(6, "Althéa LAURIN", "France", 120.00, 24, "FRA-2838"),
(6, "Lei XU", "People's Republic Of China", 120.00, 25, "CHN-106839"),
(8, "Lauren WILLIAMS", "Great Britain", 114.60, 26, "GBR-1901"),
(9, "Magdalena MATIC", "Croatia", 108.73, 18, "CRO-4549"),
(10, "Naomi ALADE", "United States of America", 101.64, 18, "USA-11185"),
(11, "DA BIN SONG", "Republic of Korea", 91.56, 24, "KOR-5704"),
(12, "Agoritsa Artemia KITSIOU", "Greece", 75.02, 20, "GRE-4439"),
(13, "Polina SHVEDKOVA", "Athlètes Individuels Neutres", 66.84, 19, "AIN-1217"),
(14, "Lorena BRANDL", "Germany", 62.77, 28, "GER-1634"),
(15, "Reba STEWART", "Australia", 61.39, 24, "AUS-9711"),
(16, "Astan Katherine Féghé BATHILY", "Cote D'ivoire", 60.29, 26, "CIV-1702"),
(17, "Raiany PEREIRA", "Brazil", 58.37, 31, "BRA-1892"),
(18, "Hannah KECK", "United States of America", 58.21, 23, "USA-6553"),
(19, "PALOMA GARCIA", "Mexico", 55.69, 21, "MEX-132467"),
(20, "I CHUN CHIN", "Chinese Taipei", 50.31, 20, "TPE-3481"),
(21, "Rachel FOUNTAIN", "Canada", 42.66, 21, "CAN-10243"),
(22, "Solène AVOULETTE", "France", 42.26, 26, "FRA-2022"),
(23, "Famke KLOOSTERMAN", "Netherlands", 38.24, 22, "NED-2326"),
(24, "Anastasiia KOSMYCHEVA", "Athlètes Individuels Neutres", 36.04, 21, "AIN-1216"),
(25, "DABIN LEE", "Republic of Korea", 36.00, 29, "KOR-1536"),
(26, "Naishka ROMAN TORRES", "Puerto Rico", 31.38, 25, "PUR-1632"),
(27, "Noor Nazar MOHAMMED", "Qatar", 30.80, 18, "QAT-2062"),
(27, "ELIS VASCONCELOS MELLO DOS SANTOS", "Brazil", 30.80, 17, "BRA-3023"),
(29, "Mariia KUTS", "Ukraine", 30.47, 18, "UKR-3648"),
(30, "Kristina ADEBAIO", "Athlètes Individuels Neutres", 30.38, 23, "AIN-108"),
(31, "BOUMH OMAYMA", "Morocco", 30.00, 19, "MAR-3759"),
(32, "Maelynn Emilée FRADL", "Aruba", 28.50, 19, "ARU-1671"),
(33, "Munira ABDUSALOMOVA", "Tajikistan", 27.12, 28, "TJK-2916"),
(34, "KHADIJA LAMDARDAR", "Morocco", 26.85, 18, "MAR-3944"),
(35, "Aleksandra KOWALCZUK", "Poland", 26.24, 29, "POL-1530"),
(36, "Hafsa Liana CHTIOUI", "Denmark", 26.10, 21, "DEN-2639"),
(37, "LINARA MUSLIMOVA", "Athlètes Individuels Neutres", 23.84, 22, "AIN-1095"),
(38, "Esra AKBULAK", "Türkiye", 23.45, 25, "TUR-7020"),
(39, "Viktorija HELVIGA", "Latvia", 23.16, 20, "LAT-1569"),
(40, "Emna HAMADACHE", "France", 23.04, 19, "FRA-3998"),
(41, "Zeqi ZHOU", "People's Republic Of China", 22.93, 26, "CHN-106656"),
(42, "Nadja TESIC", "Serbia", 22.48, 22, "SRB-3231"),
(43, "Rebecca MCGOWAN", "Great Britain", 21.60, 25, "GBR-2270"),
(43, "PALINA MIKHALCHUK", "Athlètes Individuels Neutres", 21.60, 17, "AIN-1139"),
(45, "Janna GWAILY", "Egypt", 21.12, 20, "EGY-2521"),
(46, "Juan SHI", "People's Republic Of China", 20.80, 25, "CHN-106746"),
(47, "SUGEE JUNG", "Republic of Korea", 20.16, 20, "KOR-10198"),
(48, "ELIFNAZ KOSEOGLU", "Türkiye", 20.00, 17, "TUR-22389"),
(48, "Elina ALIPOOR", "Islamic Republic Of Iran", 20.00, 17, "IRI-24515"),
(48, "Aruzhan NAIMANBAYEVA", "Kazakhstan", 20.00, 17, "KAZ-3930"),
(51, "Esmeralda HUSOVIC", "Germany", 19.25, 21, "GER-2843"),
(51, "MANISHA ALI", "Pakistan", 19.25, 23, "PAK-5365"),
(53, "Andjela SEVIC", "Serbia", 19.20, 17, "SRB-3226"),
(54, "Merveille MARINDI", "Gabon", 18.42, 23, "GAB-1606"),
(54, "Kalina BOYADZHIEVA", "Bulgaria", 18.42, 19, "BUL-5563"),
(56, "ZITING ZHAO", "People's Republic Of China", 17.24, 22, "CHN-106877"),
(57, "Elizaveta STEPANOVA", "Athlètes Individuels Neutres", 16.32, 23, "AIN-1009"),
(57, "Yawen LI", "People's Republic Of China", 16.32, 21, "CHN-108183"),
(59, "Veronica Mbang Esono AYANG", "Equatorial Guinea", 15.65, 23, "GEQ-1502"),
(60, "IRODA MIRTADJIEVA", "Uzbekistan", 15.12, 21, "UZB-1860"),
(61, "Sarah CHAÂRI", "Belgium", 15.02, 20, "BEL-2228"),
(62, "Evgeniya KAIMOVA", "Kazakhstan", 14.82, 36, "KAZ-6492"),
(62, "Inayatou HAROUNA GOUNO", "Niger", 14.82, 19, "NIG-2127"),
(62, "Marilena CHARALAMBOUS", "Cyprus", 14.82, 28, "CYP-1616"),
(62, "Laetitia BARROSO", "Portugal", 14.82, 24, "POR-4706"),
(62, "Jyoti YADAV", "India", 14.82, 21, "IND-10688"),
(67, "Kimi Laurene OSSIN", "Cote D'ivoire", 14.40, 17, "CIV-2606"),
(68, "Xueting ZHAO", "People's Republic Of China", 14.32, 21, "CHN-107508"),
(69, "Rama ABO-ALRUB", "Jordan", 13.61, 24, "JOR-1731"),
(70, "ZEHRA BEGUM KAVUKCUOGLU", "Türkiye", 13.32, 20, "TUR-11446"),
(71, "Alena VIANA", "United States of America", 12.96, 22, "USA-5627"),
(72, "Yeojin CHOI", "Republic of Korea", 12.17, 24, "KOR-11270"),
(73, "YERIM LIM", "Republic of Korea", 12.00, 18, "KOR-10808"),
(73, "Nadica BOZANIC", "Serbia", 12.00, 24, "SRB-1678"),
(73, "Fatemeh ESKANDARNIA", "Islamic Republic Of Iran", 12.00, 17, "IRI-23925"),
(73, "BORIM KIM", "Republic of Korea", 12.00, 17, "KOR-12019"),
(77, "Ainhoa PASTOR RODRIGUEZ", "Spain", 10.80, 20, "ESP-4146"),
(77, "Luz Quimey CORA", "Argentina", 10.80, 18, "ARG-3574"),
(77, "Viktoriia KUCHYNA", "Ukraine", 10.80, 17, "UKR-3937"),
(80, "Nusa URNAUT", "Slovenia", 10.73, 25, "SLO-1546"),
(81, "Arlettys de la Caridad ACOSTA HERRERA", "Cuba", 10.41, 26, "CUB-1587"),
(82, "Desiree RIVADULLA LORENZO", "Spain", 10.37, 22, "ESP-3057"),
(82, "RODALI BARUA", "India", 10.37, 29, "IND-1849"),
(82, "Alisi FAITANGANE", "Tonga", 10.37, 21, "TGA-1591"),
(82, "Lipaz HAJAMA", "Israel", 10.37, 17, "ISR-2123"),
(82, "Yinyin ZHANG", "People's Republic Of China", 10.37, 20, "CHN-107385"),
(87, "Shunan XIAO", "People's Republic Of China", 10.36, 26, "CHN-106654"),
(88, "Mouna OUASSOU", "France", 9.84, 21, "FRA-3317"),
(89, "Malak Diaa Ahmed ORABI", "Egypt", 9.60, 21, "EGY-12292"),
(90, "SUDE YAREN UZUNCAVDAR", "Türkiye", 9.02, 20, "TUR-7298"),
(91, "Do Hee YOON", "Republic of Korea", 8.64, 26, "KOR-5948"),
(91, "Zeinab ASADI", "Islamic Republic Of Iran", 8.64, 23, "IRI-23175"),
(93, "Darija ZELJKO", "Croatia", 8.40, 22, "CRO-2675"),
(94, "Ana CIUCHITU", "Italy", 8.10, 26, "ITA-2032"),
(95, "Alema HADZIC", "Germany", 7.80, 25, "GER-3367"),
(96, "Venice Elizabeth Megan TRAILL", "Fiji", 7.41, 28, "FIJ-1505"),
(96, "Marlene JAHL", "Austria", 7.41, 30, "AUT-1838"),
(96, "Fernanda AGUIRRE", "Chile", 7.41, 28, "CHI-1712"),
(96, "FATIMA-EZZAHRA ABOUFARAS", "Morocco", 7.41, 23, "MAR-2969"),
(96, "Petra STOLBOVA", "Czech Republic", 7.41, 24, "CZE-1562"),
(101, "Hongdan DING", "People's Republic Of China", 7.20, 23, "CHN-107483"),
(101, "Julia NOWAK", "Poland", 7.20, 18, "POL-2164"),
(101, "Zahra POURESMAEILKARANI", "Islamic Republic Of Iran", 7.20, 25, "IRI-12976"),
(101, "ANDREA  GABRIELA CARIAS LOZANO", "Honduras", 7.20, 17, "HON-1592"),
(101, "Sofía Isabel FRIAS", "Dominican Republic", 7.20, 17, "DOM-2155"),
(101, "DIOUF DIEYNABA", "Senegal", 7.20, 24, "SEN-1811"),
(101, "Huan WANG", "People's Republic Of China", 7.20, 27, "CHN-106735"),
(101, "Yu-Hsuan LIN", "Chinese Taipei", 7.20, 17, "TPE-3899"),
(101, "Gulzora AMIROVA", "Uzbekistan", 7.20, 17, "UZB-3475"),
(110, "Meruert TKEBAEVA", "Kazakhstan", 6.48, 28, "KAZ-3220"),
(110, "Mengqi WANG", "People's Republic Of China", 6.48, 18, "CHN-108213"),
(112, "RISHITA DANG.", "India", 6.05, 20, "IND-12281"),
(112, "HIMANSHI ANTIL", "India", 6.05, 26, "IND-6383"),
(114, "Zitong ZHAO", "People's Republic Of China", 6.04, 22, "CHN-106876"),
(115, "Christina KIBASSA-MALIBA", "United States of America", 6.00, 19, "USA-12818"),
(115, "Xu HAN", "People's Republic Of China", 6.00, 21, "CHN-107463"),
(117, "Poppy MACKAY", "Great Britain", 5.76, 22, "GBR-5169"),
(118, "Dania HAWASH", "Sweden", 5.18, 23, "SWE-5039"),
(119, "EL MAJIDI FARAH", "Morocco", 4.32, 22, "MAR-3756"),
(119, "Ayselnur SAGLIK", "Türkiye", 4.32, 23, "TUR-6873"),
(119, "Dilara ARSLAN", "Türkiye", 4.32, 24, "TUR-2600"),
(119, "Gabriele SIQUEIRA", "Brazil", 4.32, 31, "BRA-1597"),
(119, "CHIMENE YSISSE W. ILBOUDO", "Burkina Faso", 4.32, 23, "BUR-1599"),
(119, "Chen LI", "People's Republic Of China", 4.32, 28, "CHN-1619"),
(125, "Sujuan ZHANG", "People's Republic Of China", 4.28, 23, "CHN-107397"),
(125, "Ane VALLO ZURDO", "Spain", 4.28, 19, "ESP-5675"),
(127, "Olajumoke OLATEJU", "Nigeria", 4.23, 25, "NGR-4128"),
(127, "Celine ASKARJIAN", "Lebanon", 4.23, 22, "LBN-4767"),
(127, "KARINA BARRIOS CASTAÑEDA", "Mexico", 4.23, 19, "MEX-134214"),
(130, "SUN KYOUNG BAEK", "Republic of Korea", 3.60, 23, "KOR-9031"),
(130, "INDAH PERMATA SARI", "Indonesia", 3.60, 20, "INA-303189"),
(130, "Nour SAMER ELSAYED", "Egypt", 3.60, 21, "EGY-2741"),
(133, "Jiahui SUN", "People's Republic Of China", 3.02, 19, "CHN-107372"),
(133, "ZHIJING YUAN", "People's Republic Of China", 3.02, 21, "CHN-107104"),
(133, "Belen MORAN ROMERO", "Spain", 3.02, 28, "ESP-2183"),
(133, "Crystal WEEKES", "Puerto Rico", 3.02, 27, "PUR-1614"),
(133, "Seungju OH", "Republic of Korea", 3.02, 22, "KOR-10054"),
(138, "MISEO KWON", "Republic of Korea", 3.00, 22, "KOR-10429"),
(139, "Yanpei LU", "People's Republic Of China", 2.16, 18, "CHN-107914"),
(139, "Anh Ngan TRAN NGUYEN", "Vietnam", 2.16, 21, "VIE-2281"),
(139, "Keran WU", "People's Republic Of China", 2.16, 21, "CHN-107880"),
(139, "Anna KRAPIVKA", "Athlètes Individuels Neutres", 2.16, 21, "AIN-1298"),
(139, "ALIKI VICTORIA SPYRIDOU", "Greece", 2.16, 18, "GRE-9046"),
(139, "Axaule YERKASSIMOVA", "Kazakhstan", 2.16, 26, "KAZ-1883"),
(139, "Fatimah ADERIBIGBE", "Nigeria", 2.16, 28, "NGR-2534"),
(139, "Bumeigha Christabel AMAKURO", "Nigeria", 2.16, 19, "NGR-4342"),
(147, "Victoria RIVAS", "Argentina", 2.12, 22, "ARG-2816"),
(147, "Huan WANG", "People's Republic Of China", 2.12, 27, "CHN-1874"),
(147, "SEOYEON NAMGUNG", "Republic of Korea", 2.12, 18, "KOR-10706"),
(147, "Helena GARCÍA SUÁREZ", "Spain", 2.12, 19, "ESP-5055"),
(151, "Julia PERALES CHACON", "Spain", 1.80, 21, "ESP-5202"),
(151, "Soraya MARTIN PARRA", "Spain", 1.80, 22, "ESP-5547"),
(151, "Elianet María CRESPO HERNÁNDEZ", "Cuba", 1.80, 21, "CUB-1784"),
(151, "Violeta PEREZ MANZANO", "Spain", 1.80, 24, "ESP-3140"),
(151, "Ruzica KRIZANAC", "Bosnia and Herzegovina", 1.80, 19, "BIH-1786"),
(156, "SOO YEON KIM", "Republic of Korea", 1.48, 25, "KOR-5706"),
(156, "Alexia Naomi RAMIREZ CRUZ", "Mexico", 1.48, 20, "MEX-133188"),
(158, "Darija HUSOVIC", "Germany", 1.08, 24, "GER-2539"),
(158, "YASAMIN AZIZI", "Afghanistan", 1.08, 25, "AFG-106812"),
(158, "MAYRA MAYESLI CARTAGENA MURILLO", "Honduras", 1.08, 19, "HON-1618"),
]

# Continental classification
EUROPE_COUNTRIES = {
    'Norway', 'Türkiye', 'Spain', 'Hungary', 'France', 'Italy', 'Ireland', 'Finland', 
    'Germany', 'Croatia', 'Netherlands', 'Austria', 'Bulgaria', 'Serbia', 'Ukraine',
    'Poland', 'Azerbaijan', 'Bosnia and Herzegovina', 'Denmark', 'Portugal', 'Greece',
    'Albania', 'Cyprus', 'Slovakia', 'Great Britain', 'Romania', 'Luxembourg',
    'Montenegro', 'Malta', 'Israel', 'Athlètes Individuels Neutres', 'Georgia', 'Kosovo'
}

ASIA_COUNTRIES = {
    'Republic of Korea', 'Kazakhstan', 'Islamic Republic Of Iran', 'Japan',
    'Uzbekistan', 'Jordan', 'Thailand', 'Chinese Taipei', 'People\'s Republic Of China',
    'Hong Kong, the People\'s Republic of China', 'Mongolia', 'Pakistan', 'India',
    'Saudi Arabia', 'Indonesia', 'Vietnam', 'Philippines', 'Macau, China', 'Nepal',
    'Afghanistan', 'Palestine', 'Bahrain', 'Kuwait', 'Singapore'
}

AMERICAS_COUNTRIES = {
    'Brazil', 'Canada', 'United States of America', 'Venezuela', 'Chile', 'Peru',
    'Mexico', 'Puerto Rico', 'Argentina', 'Colombia', 'Guatemala', 'Panama',
    'Costa Rica', 'Ecuador', 'Suriname'
}

# Organize athletes by continent
continents = {
    'EUROPE': [],
    'ASIA': [],
    'AMERICAS': []
}

for athlete in athletes_data:
    rank, name, nation, points, age, license_id = athlete
    
    if nation in EUROPE_COUNTRIES:
        continents['EUROPE'].append(athlete)
    elif nation in ASIA_COUNTRIES:
        continents['ASIA'].append(athlete)
    elif nation in AMERICAS_COUNTRIES:
        continents['AMERICAS'].append(athlete)

# Create Excel workbook
wb = openpyxl.Workbook()
wb.remove(wb.active)

# Style settings
header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
header_font = Font(bold=True, color="FFFFFF", size=11)
header_alignment = Alignment(horizontal="center", vertical="center")

# Create sheets for each continent
for continent_name in ['EUROPE', 'ASIA', 'AMERICAS']:
    ws = wb.create_sheet(continent_name)
    athletes = continents[continent_name]
    
    # Headers
    headers = ['Rank', 'Name', 'Nation', 'Points', 'Age', 'WTF License ID']
    ws.append(headers)
    
    # Style header row
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
    
    # Add athlete data
    for athlete in athletes:
        ws.append(list(athlete))
    
    # Auto-adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[column_letter].width = min(max_length + 2, 50)

# Save file
output_path = 'F+73kg_Continental_Rankings.xlsx'
wb.save(output_path)
print(f"✓ Excel file created successfully!")
print(f"  EUROPE: {len(continents['EUROPE'])} athletes")
print(f"  ASIA: {len(continents['ASIA'])} athletes")
print(f"  AMERICAS: {len(continents['AMERICAS'])} athletes")
print(f"  Total: {len(continents['EUROPE']) + len(continents['ASIA']) + len(continents['AMERICAS'])}")
