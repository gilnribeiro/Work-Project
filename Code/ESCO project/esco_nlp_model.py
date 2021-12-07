import numpy as np
import pandas as pd
from tqdm import tqdm
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct


def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    try:
        ct.sparse_dot_topn(
            M, N, np.asarray(A.indptr, dtype=idx_dtype),
            np.asarray(A.indices, dtype=idx_dtype),
            A.data,
            np.asarray(B.indptr, dtype=idx_dtype),
            np.asarray(B.indices, dtype=idx_dtype),
            B.data,
            ntop,
            lower_bound,
            indptr, indices, data)
    except IndexError:
        return "NOT FOUND"

    return csr_matrix((data,indices,indptr),shape=(M,N))


def nlpModel(esco_dict):
    # Get the list of all job known job titles in the ESCO database
    known_job_titles = [i for i in esco_dict]
    vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 3))
    tf_idf_matrix = vectorizer.fit_transform(known_job_titles)
    return vectorizer, tf_idf_matrix, known_job_titles


def getMatches(vectorizer, tf_idf_matrix, known_job_titles, esco_dict, text, ret_score=False, threshold=0.6):    
    m = vectorizer.transform([text])
    matches = awesome_cossim_top(m, tf_idf_matrix.transpose(), 1, 0)
    try:
        best_match, score = known_job_titles[matches.nonzero()[1][0]], matches[0,matches.nonzero()[1][0]]
    except:
        return 'NOT FOUND', 'NOT FOUND', 'NOT FOUND', 'NOT FOUND' 
    if score >= threshold:
        return best_match, esco_dict[best_match]['skills'], esco_dict[best_match]['iscoGroup'], score
    return 'NOT FOUND', 'NOT FOUND', 'NOT FOUND', 'NOT FOUND'

if __name__ == '__main__':
    
    FOLDER_PATH = "/Users/gilnr/OneDrive - NOVASBE/Work Project/Code/ESCO project/"
    
    data = pd.read_json(FOLDER_PATH + 'esco_project_data.json')
    with open("esco_dictionary.json", 'r', encoding='utf-8') as file:
        esco_dict = json.load(file)
    
    vectorizer, tf_idf_matrix, known_job_titles = nlpModel(esco_dict)

    best_matches = []
    skills_list = []
    scores = []
    isco_groups = []

    for text in tqdm(data['job_title']):
        best_match, skills, isco_group, score = getMatches(vectorizer, tf_idf_matrix, known_job_titles, 
                                esco_dict, text, ret_score=True, threshold=0.6)
        best_matches.append(best_match)
        skills_list.append(skills)
        scores.append(score)
        isco_groups.append(isco_group)
        
    data['similarity_titles'] = best_matches
    data['similarity_scores'] = scores
    data['skills'] = skills_list
    data['iscoGroup'] = isco_groups
    
    count = len(data.loc[data['similarity_titles'] != 'NOT FOUND'])
    print('There are ', count, ' similar ESCO matches at a 60% threshold from a total of ', len(data), 
      'jobs. This is approximatly', round(count/len(data),4)*100,'% of jobs')
    
    with open(FOLDER_PATH + 'esco_project_data_with_similarity.json', 'w', encoding='utf-8') as file:
        data.to_json(file, force_ascii=False, orient='records', date_format='iso', date_unit='s')