import os,glob
import importlib.util

def run():
    import cmipld.tests.elements as el
    
    for element in dir(el):
         if '__' not in element[:2]:
            try:
                module = getattr(el,element)
                template = module.get_template()
                
                print(template)

            # except ModuleNotFoundError:
            #     pass
            except AttributeError:
                pass
            except Exception as e:
                print(e)
                continue
        
    
    # print(__file__)
    # files = glob.glob(__file__.replace('generate/issue_template','tests/elements/*'))
    # print(files)
    
    
    


# module_name = os.path.splitext(os.path.basename(file_path))[0]
#     spec = importlib.util.spec_from_file_location(module_name, file_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
    