from pathlib import Path, PureWindowsPath
import pandas as pd

from .data_cleaning_functions import *

def main():
    main_folder = PureWindowsPath("c:\\Users\\gilnr\\OneDrive - NOVASBE\\Work Project\\Code")
    MAIN_FOLDER = Path(main_folder)
    DATA_FOLDER = MAIN_FOLDER / "Data"

    bons_empregos = pd.read_json(DATA_FOLDER / 'bons_empregos_jobs.json')
    career_jet = pd.read_json(DATA_FOLDER / 'career_jet_api.json', lines=True)
    carga_de_trabalhos = pd.read_json(DATA_FOLDER / 'CargaDeTrabalhos.json', lines=True)
    emprego_xl = pd.read_json(DATA_FOLDER / 'EmpregoXl.json', lines=True)
    emprego_org = pd.read_json(DATA_FOLDER / 'EmpregoOrg.json')
    itjobs = pd.read_json(DATA_FOLDER / 'itjobs_api.json', lines=True)
    jooble = pd.read_json(DATA_FOLDER / 'jooble_api.json', lines=True)
    landing_jobs = pd.read_json(DATA_FOLDER / 'landingjobs_api.json', lines=True)
    net_empregos = pd.read_json(DATA_FOLDER / 'NetEmpregos.json', lines=True)

    # Bons Empregos
    def getPortugalLocation(dataframe):
        # Get only job offers in Portugal
        dataframe = dataframe.loc[dataframe['job_location'] != 'Estrangeiro'].copy()
        return dataframe

    bons_empregos_clean = (bons_empregos.
                        pipe(copy_df).
                        pipe(replacenan).
                        pipe(postDateFillNa).
                        pipe(dropNullJobs).
                        pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                        pipe(toDatetime, ['scrape_date']).
                        pipe(getPortugalLocation).
                        pipe(convertToDatetime, longToShortDate).
                        pipe(removeDupes)
    )

    # Career Jet
    # convert job location to list
    career_jet['job_location'] = career_jet['job_location'].apply(lambda x: x.split(','))

    career_jet_clean = (career_jet.
                        pipe(copy_df).
                        pipe(replacenan).
                        pipe(postDateFillNa).
                        pipe(dropNullJobs).
                        pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                        pipe(toDatetime, ['scrape_date', 'post_date']).
                        pipe(listToRows, 'job_location').
                        pipe(removeDupes)
    )

    # Carga de Trabalhos
    carga_de_trabalhos_clean = (carga_de_trabalhos.
                        pipe(copy_df).
                        pipe(replacenan).
                        pipe(postDateFillNa).
                        pipe(dropNullJobs).
                        pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                        pipe(toDatetime, ['scrape_date']).
                        pipe(convertToDatetime, longToShortDate, '/').
                        pipe(removeDupes)
    )

    # Emprego XL
    emprego_xl_clean = (emprego_xl.
                        pipe(copy_df).
                        pipe(replacenan).
                        pipe(postDateFillNa).
                        pipe(applyFuncToColumn).
                        pipe(pipeInvertDate).
                        pipe(dropNullJobs).
                        pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                        pipe(toDatetime, ['scrape_date', 'post_date']).
                        # # pipe(convertToDatetime, longToShortDate, '/').
                        pipe(removeDupes)
    )

    # Emprego Org
    emprego_org_clean = (emprego_org.
                        pipe(copy_df).
                        pipe(replacenan).
                        pipe(postDateFillNa).
                        pipe(dropNullJobs).
                        pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                        pipe(postDatePreprocess, '/').
                        pipe(toDatetime, ['scrape_date', 'post_date']).
                        pipe(removeDupes)
    )

    # ITJobs
    def simplifyDate(x):
        return dt.datetime.strptime(x.split(' ')[0], '%Y-%m-%d')

    itjobs_clean = (itjobs.
                        pipe(copy_df).
                        pipe(listToRows, 'job_location').
                        pipe(replacenan).
                        pipe(postDateFillNa).
                        pipe(dropNullJobs).
                        pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                        pipe(applyFuncToColumn, function=simplifyDate, columns_list=['post_date']).
                        pipe(toDatetime, ['scrape_date', 'post_date']).
                        # pipe(.apply(lambda x: dt.datetime.strftime('%Y-%m-%d'))).
                        pipe(removeDupes)
    )

    # Jooble
    jooble_clean = (jooble.
                        pipe(copy_df).
                        pipe(replacenan).
                        pipe(postDateFillNa).
                        pipe(dropNullJobs).
                        pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                        pipe(toDatetime, ['scrape_date', 'post_date']).
                        pipe(removeTags, ['job_title']).
                        pipe(removeDupes)
    )

    # Landing Jobs IT
    landing_jobs_clean = (landing_jobs.
                        pipe(copy_df).
                        pipe(replacenan).
                        pipe(postDateFillNa).
                        pipe(dropNullJobs).
                        pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                        pipe(postDatePreprocess, 'T').
                        pipe(toDatetime, ['scrape_date', 'post_date']).
                        # pipe(removeTags, 'job_title').
                        pipe(removeDupes)
    )

    # Net Empregos
    net_empregos_clean = (net_empregos.
                        pipe(copy_df).
                        pipe(replacenan).
                        pipe(pipeInvertDate).
                        pipe(postDateFillNa).
                        pipe(dropNullJobs).
                        # two pipes are needed beacause - for some reason, the function was not replacing some words it should
                        pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                        pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                        pipe(cleanDescription, ['job_title']).
                        pipe(toDatetime, ['scrape_date', 'post_date']).
                        pipe(removeDupes)
    )

    # Add Website Identifier before concating all dataframes into a single one
    jobs_dfs = [bons_empregos_clean, career_jet_clean, carga_de_trabalhos_clean, emprego_xl_clean, emprego_org_clean, itjobs_clean, jooble_clean, landing_jobs_clean, net_empregos_clean]
    websites = ['Bons empregos', 'Career Jet', 'Carga de Trabalhos', 'Emprego XL', 'Emprego.org','ITjobs','Jooble','Landing Jobs','Net-empregos']

    # Add column with website name
    for idx, value in enumerate(jobs_dfs):
        value['website'] = websites[idx]

    # CONCAT DATAFRAMES AND DEFINE COLUMN ORDER
    neworder = ['job_title','job_description','company','job_location','job_category','salary', 'post_date', 'scrape_date','job_href', 'website']

    df = pd.concat([i.reindex(columns=neworder) for i in jobs_dfs])

    # Validate that the concatenation is happening properly
    assert len(df) == sum(len(i) for i in jobs_dfs)

    #######################################################
    ############# Clean the Main Dataframe ################
    #######################################################
    df_clean = (df.
                pipe(copy_df).
                pipe(replacenan).sort_values(by='post_date').
                pipe(postDateFillNa).
                pipe(dropNullJobs).
                pipe(applyFuncToColumn, function=cleanJobTitle, columns_list=['job_title']).
                pipe(cleanCompany).
                pipe(cleanDescription, ['job_title', 'job_description']).
                pipe(removeDupes, ['job_title', 'job_description','company', 'job_location'])
    )

    df_clean.reset_index(drop=True, inplace=True)


    #######################################################
    ############# Pass the Data Into JSON #################
    #######################################################

    with open(DATA_FOLDER / 'full_data_clean.json', 'w', encoding='utf-8') as file:
        df_clean.to_json(file, force_ascii=False, orient='records', date_format='iso', date_unit='s')


if __name__ == '__main__':
    main()