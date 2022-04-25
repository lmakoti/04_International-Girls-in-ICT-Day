<h1 align="center">United Nations International Girls in ICT Day , 28 April 2022</a></h1>



## Data Source

**UNDP Human Development Reports**: https://hdr.undp.org/en/data (identify relevant indicators)

**UNDP API: **http://ec2-54-174-131-205.compute-1.amazonaws.com/API/Information.php (API Documentation Link/URL) - get indicator ids

**Base URL: **http://ec2-54-174-131-205.compute-1.amazonaws.com/API/HDRO_API.php/[parameters]

**Parameter: **

1. `country_code` e.g. country_code = 'LSO, ZAF, GBR'
2. `indicator_id` e.g.  indicator_code='690706'
   - 69706-Expected years of schooling (years)
3. `year` e.g. year = '2020, 2019, 2017,2018'

*To view source-code press: ctrl+/*

```python
http://ec2-54-174-131-205.compute-1.amazonaws.com/API/HDRO_API.php/country_code=LSO/indicator_code=690706/year=2019
```



- Identify the relevant ***indicators***

  - Share of graduates from science, technology, engineering and mathematics programmes in tertiary education who are female (%)
    **Dimension**: Gender
    **Definition**: Share of female graduates among all graduates of tertiary programmes in science, technology, engineering and mathematics.
    **Source**: UNESCO (United Nations Educational, Scientific and Cultural Organization) Institute for Statistics (2020). Data Centre. http://data.uis.unesco.org. Accessed 21 July 2020.
    - https://hdr.undp.org/en/indicators/183506
  - Share of graduates in science, technology, engineering and mathematics programmes at tertiary level, female (%)
    **Dimension**: Gender
    **Definition**: Share of female tertiary graduates in science, technology, engineering and mathematics programmes among all female tertiary graduates.
    **Source**: UNESCO (United Nations Educational, Scientific and Cultural Organization) Institute for Statistics (2020). Data Centre. http://data.uis.unesco.org. Accessed 21 July 2020.
    - https://hdr.undp.org/en/indicators/175906
- **Create your analysis plan**

  - [provide]
- **Develop your ETL Pipeline**

- - ```python
  import requests
    import pandas as pd
  
    baseurl = 'http://ec2-54-174-131-205.compute-1.amazonaws.com/API/HDRO_API.php/country_code=ATG,AUS,BGD,BHS,BLZ,BRB,BRN,BWA,CAN,CMR,CYP,DMA,FJI,GBR,GHA,GMB,GRD,GUY,IND,JAM,KEN,KIR,KNA,LCA,LKA,LSO,MDV,MLT,MOZ,MUS,MWI,MYS,NAM,NGA,NRU,NZL,PAK,PNG,RWA,SGP,SLB,SLE,SWZ,SYC,TON,TTO,TUV,TZA,UGA,VCT,VUT,WSM,ZAF,ZMB/indicator_id=183506,175906'
  
    # [Your Algorithm]
    
    ```
  
    


****
