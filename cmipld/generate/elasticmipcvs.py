
from cmipld import Frame
from cmipld.graph import JSONLDGraphProcessor
import asyncio

from elasticsearch import Elasticsearch
import os 
from dotenv import load_dotenv
# load_dotenv()

home_dir = os.path.expanduser('~')
env_path = os.path.join(home_dir, '.env')
# Load environment variables from the .env file
load_dotenv(dotenv_path=env_path)



async def main():
    files = ['cmip6plus_ld', 'mip_cmor_tabes_ld']

    # Initialize the Elasticsearch client with correct parameters
    es = Elasticsearch(
            ['https://127.0.0.1:9200'],  
            basic_auth=('elastic', os.environ['ELASTIC_PASSWORD']),
            verify_certs=True,  # Enable certificate verification
            ca_certs=os.environ['ELASTIC_CERTS']  # Path to CA certificate
        )
    
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html

    # # Process input files
    # ldcontent = await CMIPFileUtils().load(files)
    # print("Graph processing completed.")
    graph = JSONLDGraphProcessor()

    await graph.make_graph(files)
    
    print("Graph processing completed.")
    ldcontent = graph.lddata
    core_frame = graph.generate_frames
    linked_frame = graph.link_frames



    indexes = []

   
    for fname,fvalue in linked_frame.items():
        print("Linked Frame: ", fname)
        # print('--',fvalue)
        if '@context' in fvalue:
            del fvalue['@context']

    
        data = Frame(ldcontent, fvalue).data
        
        index,doc = fname.split(':') 
        indexes.append(index)
        
        # add to 
        counter = 0
        
        for entry in data:
            if '@id' in entry:
                es.index(index=index, id=entry["@id"], body=entry)
                counter += 1
            else: 
                print(f'No @id in {fname}, {fvalue}')
            
        print(f'Added {counter} documents to index')
        
    for index in indexes:
        es.indices.refresh(index=index)
        print(f'Index {index} has been refreshed')



def run():
    asyncio.run(main())
    
    
if __name__ == "__main__":
    run()
