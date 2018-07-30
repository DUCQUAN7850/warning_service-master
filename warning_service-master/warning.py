from anomaly_domain import AnomalyDomain

'''
This class control all anomaly warning class
create and remove an automation warning class
'''
class Warning :

    def __init__(self, host) :
        self.repo_list = {}
        self.host = host
        return 
    

    def add_repo (self, name) :
        if name in self.repo_list :
            return False
        else :
            new_process = AnomalyDomain(name=name, host=self.host)
            self.repo_list[name] = new_process
            new_process.run()

        return True
    

    def remove_repo (self, name) :
        self.repo_list[name].terminate()
        self.repo_list.pop(name, None)
        return 
        

    
    
    
