import pandas as pd, json, re, math, os
from pathlib import Path
ROOT=Path(__file__).parent
SOURCE=Path(os.environ.get('RTU_PUB_CSV', ROOT/'source'/'RTU Scopus Publications 2019-2026.csv'))
AUTH=Path(os.environ.get('RTU_AUTH_CSV', ROOT/'source'/'RTU Scopus Authors.csv'))
# The temporary sandbox fallback is for initial artifact creation only.
if not SOURCE.exists() and Path('/mnt/data/RTU Scopus Publications 2019-2026.csv').exists():
    SOURCE=Path('/mnt/data/RTU Scopus Publications 2019-2026.csv')
if not AUTH.exists() and Path('/mnt/data/RTU Scopus Authors.csv').exists():
    AUTH=Path('/mnt/data/RTU Scopus Authors.csv')
if not SOURCE.exists() or not AUTH.exists():
    raise FileNotFoundError('Place the source CSVs in source/ or set RTU_PUB_CSV and RTU_AUTH_CSV')
raw=pd.read_csv(SOURCE, dtype=str, keep_default_na=False)
auth=pd.read_csv(AUTH,skiprows=5,dtype=str,keep_default_na=False)
auth=auth[auth['Auth-ID'].str.match(r'^\d{8,15}$',na=False)].copy()
# Curated publication-title patterns (SDG number lists; first entry is the primary topical alignment).
# Conservative multi-label thematic classification; zero-assignment explicitly permitted.
# IMPORTANT: This is analyst-defined, not Scopus/SciVal/UN validated SDG attribution.
CURATED = [
# 2021
('factors that influence students', [4]),
('integration of learning management system', [4]),
('ionospheric precursor associated to', [11]),
('ionospheric storm caused in', []),
('satellite navigation effects', [9]),
('cold-point tropopause temperature', [13]),
('recovering communities from typhoon', [11,13]),
('potential astronomical optical observatory sites', [11]),
# 2022
('heavy metal levels in an urban river', [6,3,14]),
('burstt:', []),
('business technology and innovation research', [9,8]),
('hubble constant and its lower limit', []),
('radiation risks and resource opportunities', [3,12]),
('experiential learning and job satisfaction', [4,8]),
('spratly islands in using viirs', [14,16]),
('physics and astronomy education teaching', [4]),
('total solar irradiance on philippine precipitation', [13]),
('mabel cook cole', [11]),
('membership and age determination of m67', []),
('night-time human mobility during pandemic', [11,3]),
('rare earths in philippine phosphogypsum', [12,9]),
('research productivity as performance dynamics of pisa', [4]),
('traditional and flipped learning', [4]),
('transport of toxic metals in the bottom', [3,6,14]),
('washington accord', [4,9]),
# 2023
('frequently repeating fast radio burst', []),
('distance pattern and spacing of the multiplanet', []),
('ecological and health risks from heavy metal', [3,12,15]),
('gamification of statistics and probability', [4]),
('gamified mobile apps', [4]),
('heavy metal pollution in soil and surface', [6,15]),
('cluster members of ngc 869', []),
('open cluster ngc 7789', []),
('classification of repeating frbs', []),
('rare earths leaching from philippine', [12,9]),
('re-emergence of parang sabil', [16]),
('abrupt shift to online learning', [4]),
# 2024
('integrating multimodality in science', [4]),
('chasing the break:', []),
('precipitable water vapor and sea surface', [13]),
('vlafc model', [4]),
('publication of sdg6 research', [6]),
('civil engineering research in the philippines', [9]),
('electrical and electronics engineering research', [9]),
('thermal unrest in taal volcano', [11]),
('modis- and gnss-based precipitable', [13]),
('rice paddy areas in nueva ecija', [2]),
('research performance of philippine sdg4', [4]),
("n'synk:", [11,3]),
('polycyclic aromatic hydrocarbon luminous', []),
('biotechnology research in the philippines', [9]),
('severe weather archive', [13,11]),
('remote assessment of learning', [4]),
('mangrove ecosystem in calatagan', [14,15]),
('rainfall and temperature on sugarcane', [2,13]),
# 2025
('#edutok:', [4]),
('organizational behavior and human resource', [8]),
('ai chatbot misuse in education', [4]),
('philippine materials science research', [9]),
('physics mastery of first-year engineering', [4]),
('astronomy and astrophysics publication research metrics', []),
('base isolation system in essential facilities', [11,9]),
('darkest nights of the marawi siege', [16,11]),
('green wall system beside roadways', [11,12]),
('grit and academic engagement in combat', [4,3]),
('inspired by curiosity: enhancing students', [4]),
('faculty modeling system', [4]),
('engineering education in the philippines', [4,9]),
('technical vocational teacher education', [4,8]),
('pre-service teacher transitions', [4]),
('lp 890-9 planetary system', []),
('how passion fuels student athletes', [3]),
('instructors’ emotional support and students', [4,3]),
('light pollution mapping and its implications', [11]),
('sustainable business and industry practices:', [12,8]),
('next-generation hemostasis:', [3,9]),
('orbital evolution of r aquarii', []),
('perspective of science educators and students', [4]),
('promoting analog space mission through students', [4]),
('research trends of biophysics', []),
('sustainable cities and communities:', [11]),
('seven years of space weather research', []),
('smart human resource development', [8,4]),
('school climate shapes academic resilience', [4]),
('urban heat island trends in makati', [11,13]),
('digital review material utilizing mobile', [4]),
('plyometric training exercise', [3]),
('black hole transient maxi', []),
('sustainable business and industry practice:', [12,8]),
# 2026
('management information system services', [9]),
('culturally sensitive physical education', [4,5,10]),
('h5p-based material', [4,9]),
('preservice mathematics teachers', [4]),
('hybrid pre-processing strategies', []),
('next-gen finance:', [8,9,10]),
('nutrient management strategy', [2,12,14]),
('nutritional profiling of 30 tropical marine', [2,14]),
('profiling sdg 4 research', [4]),
('native-speakerism in world englishes', [4,10]),
('sacred burnout:', [3,8]),
('safeguarding faculty retention through mentoring', [4,8]),
('social and cultural competencies of sikaran', [11]),
('betaphycus gelatinus', [2,14]),
('teacher emotional support and student well-being', [4,3]),
('culture in oral corrective feedback', [4]),
('academic motivation in the relationship between', [4]),
('tracing obscured agn', []),
('virtual patients from the learner', [3,4]),
]
def normalize(s):
    s=s.casefold().replace('’',"'").replace('‐','-').replace('–','-')
    return re.sub(r'\s+',' ',s.strip())
keys=[(normalize(t),v) for t,v in CURATED]
records=[]; unmatched=[]
for _,r in raw.iterrows():
    title=r['Title']; nt=normalize(title)
    matched=[(k,v) for k,v in keys if k in nt]
    if len(matched)!=1:
        unmatched.append((title,[x[0] for x in matched])); goal=[]
    else: goal=matched[0][1]
    def num(s):
        try:return int(float(s))
        except:return 0
    eid=r['EID']
    aa=[i.strip() for i in r['Author(s) ID'].split(';') if i.strip()]
    names=[x.strip() for x in r['Authors'].split(';') if x.strip()]
    records.append(dict(id=eid,title=title,year=num(r['Year']),source=r['Source title'],type=r['Document Type'],citations=num(r['Cited by']),openAccess=bool(r['Open Access'].strip()),doi=r['DOI'],url=('https://doi.org/'+r['DOI']) if r['DOI'] else r['Link'],authorIds=aa,authors=names,sdgs=goal,sdgBasis='explicit' if re.search(r'\bsdgs?\s*[- ]?\s*(4|6|11)\b',nt) else ('indicative' if goal else 'unmapped')))
print('unmatched',unmatched)
assert not unmatched, 'Every publication title must be explicitly audited'
# Avoid mixing authors from the separate source into a unique-RTU-author KPI.
authors=[]
for _,r in auth.iterrows():
    authors.append(dict(id=r['Auth-ID'],name=r['Author Name'],documents=int(r['Number of Documents']) if r['Number of Documents'].isdigit() else 0,orcid=r['Orc_ID']))
# An explicit 2026-October reporting snapshot, not directly reconciled to CSV.
presentation={
 'title':'State of University Address — Terminal Report on Research Accomplishments',
 'asOf':'6 October 2026',
 'period':'2019–October 2026',
 'publications':110,'citations':315,'authors':105,'partnerCountries':36,'openAccess':54,'fundedStudies':39,'rtuFundedStudies':12,'hIndex':8,
 'trend':{'years':[2019,2020,2021,2022,2023,2024,2025,2026],'publications':[2,0,9,16,8,20,38,17], 'citations':[51,0,26,96,44,50,42,6]},
 'targets2029':[
  {'indicator':'Annual Scopus-indexed publications','baseline':'38 (2025)','target':'≥ 50'},
  {'indicator':'Journal article share','baseline':'50%','target':'≥ 70%'},
  {'indicator':'International collaboration share','baseline':'18%','target':'≥ 30%'},
  {'indicator':'Open-access share','baseline':'49%','target':'≥ 65%'},
  {'indicator':'Annual active RTU authors','baseline':'56 (2025)','target':'≥ 80'},
  {'indicator':'Funded publication share','baseline':'35%','target':'≥ 50%'},
  {'indicator':'Publications naming an RTU unit','baseline':'74%','target':'100%'}
 ]
}
sdgs=[
 (1,'No Poverty','#E5243B'),(2,'Zero Hunger','#DDA63A'),(3,'Good Health and Well-being','#4C9F38'),
 (4,'Quality Education','#C5192D'),(5,'Gender Equality','#FF3A21'),(6,'Clean Water and Sanitation','#26BDE2'),
 (7,'Affordable and Clean Energy','#FCC30B'),(8,'Decent Work and Economic Growth','#A21942'),(9,'Industry, Innovation and Infrastructure','#FD6925'),
 (10,'Reduced Inequalities','#DD1367'),(11,'Sustainable Cities and Communities','#FD9D24'),(12,'Responsible Consumption and Production','#BF8B2E'),
 (13,'Climate Action','#3F7E44'),(14,'Life Below Water','#0A97D9'),(15,'Life on Land','#56C02B'),
 (16,'Peace, Justice and Strong Institutions','#00689D'),(17,'Partnerships for the Goals','#19486A')]
output={'metadata':{'export':'Uploaded RTU Scopus Publications 2019-2026.csv','publicationExportRange':'2021–2026','snapshot':'User-supplied Scopus exports, uploaded November 2026; export timestamp not independently provided','tagging':'Analyst-curated, indicative, primarily title-based multi-label SDG thematic mapping with selective abstract review; NOT official Scopus/SciVal/UN SDG attribution','scopusRecords':len(records),'authorRosterRows':len(authors),'dataMismatch':'CSV and presentation are distinct unreconciled snapshots. Figures are not interchangeable.'},'sdgs':[dict(id=i,name=n,color=c) for i,n,c in sdgs],'publications':records,'authors':authors,'presentation':presentation}
(ROOT/'data'/'data.js').write_text('window.RTU_DATA = '+json.dumps(output,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
(ROOT/'data'/'data.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
print('PUBLICATIONS',len(records),'CITATIONS',sum(x['citations'] for x in records),'MAPPED',sum(bool(x['sdgs']) for x in records))
from collections import Counter
print('GOAL COUNTS',Counter(j for x in records for j in x['sdgs']))
print('AUTHORS',len(authors))
