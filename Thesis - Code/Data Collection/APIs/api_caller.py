from Career_jet_api.career_jet_jobs import main as career_jet_api
from Itjobs_api.itjobs_api import main as itjobs_api
from Jooble_api.jooble_api import handleResults as jooble_api
from LandingJobsIT_api.landingJobs_api import main as landingjobs_api


from tqdm import tqdm

apis = [career_jet_api, itjobs_api, jooble_api, landingjobs_api]
api_names = ['Career Jet API', 'ITjobs API', 'Jooble API', 'Landing Jobs API']
filenames = ['career_jet_api', 'itjobs_api', 'jooble_api', 'landingjobs_api']

for index, api in tqdm(enumerate(apis)):
    print(f'\nRunning {api_names[index]}...')
    api(filenames[index])
    print(f'{api_names[index]} - SUCCESS')

