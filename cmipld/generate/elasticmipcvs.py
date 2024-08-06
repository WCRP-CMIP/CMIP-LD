
from cmipld import Frame
from cmipld.graph import JSONLDGraphProcessor
import asyncio

from elasticsearch import Elasticsearch
import os 
from dotenv import load_dotenv
load_dotenv()

es = Elasticsearch(
        ['https://127.0.0.1:9200'],  
        basic_auth=('elastic', os.getenv('ELASTIC_PASSWORD')),
    )

async def main():
    files = ['cmip6plus_ld', 'mip_cmor_tabes_ld']

    # # Process input files
    # ldcontent = await CMIPFileUtils().load(files)
    # print("Graph processing completed.")
    graph = JSONLDGraphProcessor()

    await graph.make_graph(files)
    
    print("Graph processing completed.")
    ldcontent = graph.lddata
    core_frame = graph.generate_frames
    linked_frame = graph.link_frames

    # Initialize the Elasticsearch client with correct parameters


    indexes = []


    for fname,fvalue in linked_frame.items():
        print("Linked Frame: ", fname)
        print('--',fvalue)
        if '@context' in fvalue:
            del fvalue['@context']
    
        data = Frame(ldcontent, fvalue)
        
        index,doc = fvalue.split(':') 
        indexes.append(index)
        
        # add to 
        es.index(index=index, doc_type=doc, id=fvalue["@id"], body=fvalue)
        
    for index in indexes:
        es.indices.refresh(index=index)
        print(f'Index {index} has been refreshed')



def run():
    asyncio.run(main())
    
    
if __name__ == "__main__":
    run()
