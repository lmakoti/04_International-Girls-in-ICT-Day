<h1 align="center">United Nations International Girls in ICT Day , 28 April 2022</a></h1>



## Python ETL Libraries
- **Requests**: Extraction
- **Pandas**: Transformation (Initial, faster than PowerBI direct data load)
- **Luigi**: Scheduler
- **PowerBI**: Transformation, Load and Visualisation

## Data Source

**UNDP Human Development Reports**: https://hdr.undp.org/en/data (identify relevant indicators)

**UNDP API:** http://ec2-54-174-131-205.compute-1.amazonaws.com/API/Information.php (API Documentation Link/URL) - get indicator ids

**Base URL:** http://ec2-54-174-131-205.compute-1.amazonaws.com/API/HDRO_API.php/

**Parameters:**

1. `country_code` e.g. country_code = 'LSO, ZAF, GBR'
2. `indicator_id` e.g.  indicator_code='690706'
   - 69706-Expected years of schooling (years)
3. `year` e.g. year = '2020, 2019, 2017,2018'


```python
http://ec2-54-174-131-205.compute-1.amazonaws.com/API/HDRO_API.php/country_code=LSO/indicator_code=690706/year=2019
```

****

### Solution Architecture

1. Create environment : `python -m venv luigi-venv`

2. Activate environment: `.luigi-venv/Scripts/activate`

3. Create Luigi task:  `nano main` or `touch main`

   ```python
   import luigi
   
   #mixin:In object-oriented programming languages, a mixin (or mix-in)is a class that contains methods for use by other classes without having to be the parent class of those other classes.
   
   class HelloLuigi(luigi.Task):
       def output(self):
           return luigi.LocalTarget('hello-luigi.txt')
   
       def run(self):
           with self.output().open("w") as outfile:
               outfile.write("Hello Luigi!")
   ```

4. Running a Luigi task: `python -m luigi --module ScriptFileName className --local-scheduler`

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
    
  - Education index
    **Dimension**: Education
    **Definition**: Education index is an average of mean years of schooling (of adults) and expected years of schooling (of children), both expressed as an index obtained by scaling with the corresponding maxima.
    **Source**: HDRO calculations based on expected years of schooling and mean years of schooling from UNESCO Institute for Statistics (2020) and other sources. Accessed on 21 July 2020.

    - https://hdr.undp.org/en/indicators/103706

    ​	

- **Create your analysis plan**

  1. Find out if there is progress in the participation of females in STEM programmes at tertiary level and countries' inclusive education index

  2. Check for the yearly data completeness

  3. Evaluate the trends in the identified indicators

     

- **Develop your ETL Pipeline**

  - **Extraction**

    **Installation libraries:** 

    - `requests` -  is a simple, yet elegant, HTTP library, used to get API data from source (**UNDP** - Human Development Report Office Statistical Data API).
    - `bs4 or beautifulsoup4` - Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree. - *not used but in original algorithm*
    - `html5lib` - html5lib is a pure-python library for parsing HTML. It is designed to conform to the WHATWG HTML specification, as is implemented by all major web browsers. - *not used but in original algorithm*

  - **Transformation**

    **Use Pandas to perform the transformation**

    ```python
    import requests
    import pandas as pd
    
    baseurl = 'http://ec2-54-174-131-205.compute-1.amazonaws.com/API/HDRO_API.php/country_code=ATG,AUS,BGD,BHS,BLZ,BRB,BRN,BWA,CAN,CMR,CYP,DMA,FJI,GBR,GHA,GMB,GRD,GUY,IND,JAM,KEN,KIR,KNA,LCA,LKA,LSO,MDV,MLT,MOZ,MUS,MWI,MYS,NAM,NGA,NRU,NZL,PAK,PNG,RWA,SGP,SLB,SLE,SWZ,SYC,TON,TTO,TUV,TZA,UGA,VCT,VUT,WSM,ZAF,ZMB/indicator_id=103706,183506,175906'
    
    #01 get the data
    req = requests.get(baseurl)
    data = req.json()
    
    #02 flatten the data inside of a dataframe
    data_df_flat = pd.json_normalize(data, max_level=3)
    
    #03 unpivot data frame
    data_unpivot = pd.melt(data_df_flat)
    
    #data_unpivot = pd.melt(pd.json_normalize(data, max_level=3))
    
    #04 split variable column by delimiter
    data_unpivot[['placeholder','iso3', 'indicator_code', 'year']] = data_unpivot['variable'].str.split('.', expand=True)
    
    #05 remove unnecessary columns
    data_unpivot.pop('variable')
    data_unpivot.pop('placeholder')
    
    #06 see how the data looks like printed
    #print(type(data_unpivot))
    #print(data_unpivot)
    
    # Steps 02,03 can be combined: data_unpivot = pd.melt(pd.json_normalize(data, max_level=3))
    # Step 06 can be removed, just a check step
    
    ```
  
    
  
  - **Transform + Load (PowerBI)**
  
    - Use the above script to load the data into a single data frame (data_unpivot), which gets loaded as a query/table in PowerBI
    
    - Perform the following transformation steps using M-query language
    
      ```python
      #01 expand the value column from the loaded data frame to pull in the data table 
      = Source{[Name="data_unpivot"]}[Value] 
      
      #02 remove the last 3 columns containing the indicator meta descriptions
      = Table.RemoveLastN(data_unpivot1,3)
      
      #03 reordered columns
      = Table.ReorderColumns(#"Changed Type",{"iso3", "indicator_code", "value", "year"})
      
      #04 replaced comma, with period to accomodate the locale region setup for text to number conversion
      = Table.ReplaceValue(#"Reordered Columns",".",",",Replacer.ReplaceText,{"value"})
      = Table.TransformColumnTypes(#"Replaced Value",{{"value", type number}})
      
      #05 remove every null data point using the year column
      = Table.SelectRows(#"Changed Type1", each ([year] <> null))
      ```
      
      
  
## Reference 

- **Highly Recommended** - https://pandas.pydata.org/pandas-docs/stable/getting_started/index.html
- https://www.integrate.io/blog/comparison-of-the-top-python-etl-tools/
- https://www.makeuseof.com/best-python-etl-tools/
- https://content.techgig.com/technology/top-5-python-based-etl-tools-to-learn-in-2020/articleshow/74489069.cms
- https://hevodata.com/learn/python-etl-tools/
- https://www.digitalocean.com/community/tutorials/how-to-build-a-data-processing-pipeline-using-luigi-in-python-on-ubuntu-20-04



****
