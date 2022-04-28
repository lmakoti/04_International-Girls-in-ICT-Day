#01 import the relevant libraries
import luigi #01a. scheduler package for running batch processes (simple test implementation, full capabilities not explored)
import requests #01b. sends HTTP requests to obtain response object data (usually loaded as a json response)
import pandas as pd #01c. manages the data manipulation (transformation)
import json #01d. json encoder for python data structures (dataframes)

#02a. luigi_pandas(), define the luigi task, by adding `luigi.task`
class luigi_pandas(luigi.Task):
    #02b. output(), define the target output produced by the task, `Luigi.LocalTarget` produces a local file `output_dataframe.txt` which contains the output dataframe
    def output(self):
        return luigi.LocalTarget('data/output_dataframe.csv')

    #02c. run(), define the code to execute for the pipeline stage
    def run(self):
        with self.output().open("w") as outfile:
            #03a. number of subscriptions for the mobile phone service, expressed per 100 people (SDG9.c : https://unstats.un.org/sdgs/metadata/?Text=&Goal=9&Target=9.c)
            url = 'http://ec2-54-174-131-205.compute-1.amazonaws.com/API/HDRO_API.php/country_code=AGO,BWA,COM,COD,SWZ,LSO,MDG,MWI,MUS,MOZ,NAM,SYC,ZAF,TZA,ZMB,ZWE/indicator_id=46006'

            #03b. encode the incoming object into a json object
            response = requests.get(url).json()

            #03c. obtain the data string/"column" from the json object through the `indicator_value` index
            df_response = response['indicator_value']

            #03d. flatten the data to the maximum number of levels i.e. {`key`:`value`}, the key-value pairs will be coverted to headers and get delimited by `.` "key.value"
            df_response = pd.json_normalize(df_response, max_level=3)

            #03e. unpivot the structure to combine all atributes into a single column (convert rows to colums, generating a key-value pair match in two columns)
            df_unpivotted = pd.DataFrame(df_response.melt())

            #03f. split the column using `.` (period) as the delimiter
            df_unpivotted['variable'].str.split('.', 3, expand=True)

            #03g. define the data columns
            df_unpivotted[['country', 'indicator', 'year']] = df_unpivotted['variable'].str.split('.', 2, expand=True)
            #03h. remove the `variable` column
            df_unpivotted.drop('variable', axis=1, inplace=True)
            #03i. remove empty rows
            df_unpivotted.dropna(inplace=True)

            #04 produce a csv file from the dataframe
            outfile.write(f'{df_unpivotted.to_csv(index=False)}')