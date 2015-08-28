import fireworks
from fireworks.queue import queue_launcher
from fireworks.core import rocket_launcher
from fireworks.utilities.fw_serializers import load_object_from_file
from pymongo import MongoClient
import getpass, os, sys
FW_LPAD_CONFIG_LOC = "/opt/common/CentOS_6-dev/cmo/fireworks_config_files"
FW_WFLOW_LAUNCH_LOC = "/opt/common/CentOS_6-dev/fireworks_workflows"
class Job(fireworks.Firework):
    #FIXME inherit from Firework?
    #TODO type checking
    #if not isinstance(command, string):
    def __new__(cls, command, **kwargs):
        bsub_options_dict={}
        spec = None
        name = None
        for key in['queue', 'resources', 'walltime']:
            if key in kwargs:
                bsub_options_dict[key]=kwargs[key]
        if len(bsub_options_dict.keys()) > 0:
            spec = {}
            spec['_queueadapter']=bsub_options_dict
        if name in kwargs:
            name=name
        return fireworks.Firework(fireworks.ScriptTask.from_str(command), name=name, spec=spec)
    def __init__(self, command, rusage=None, name=None, queue=None, walltime=None):
        self.rusage = rusage
        self.queue= queue
        self.walltime=walltime
        if name:
            self.name=name
       
class Workflow():
    def __init__(self, jobs_list, job_dependencies, name=None):
        self.jobs_list = jobs_list
        self.job_dependencies = job_dependencies
        self.workflow = fireworks.Workflow(jobs_list, job_dependencies)
        db = DatabaseManager()
        self.launchpad = fireworks.LaunchPad.from_file(db.find_lpad_config())
    def run(self, processing_mode):
        if processing_mode=='serial':
            #load user launchpad
            #create user collection if necessary
            #init if necessary
            rocket_launcher.rapidfire(self.launchpad, fireworks.FWorker())
        elif processing_mode=='LSF':
            self.launchpad.add_wf(self.workflow)

class DatabaseManager():
    def __init__(self, host="plvcbiocmo2.mskcc.org", port="27017", user=getpass.getuser()):
        self.host=host
        self.port=port
        self.client=MongoClient(host+":"+port)
        self.user = user
    def lpad_cfg_filename(self):
        return self.user+".yaml"
    def find_lpad_config(self):
        lpad_file = os.path.join(FW_LPAD_CONFIG_LOC, self.lpad_cfg_filename())
        if not os.path.exists(lpad_file):
            self.create_lpad_config()
        return lpad_file
    def create_lpad_config(self):
        if os.path.exists(find_lpad_config):
            print >>sys.stderr, "Config already exists: %s" % self.find_lpad_config
        else:
            fh.open(self.find_lpad_config(),"w")
            yaml_dict =  { "username" : self.user,
                    "name" : self.user,
                    "strm_lvl": "INFO",
                    "host" : self.host,
                    "logdir" : "null",
                    "password" : "speakfriendandenter",
                    "port" : self.port }
            for key, value in yaml_dict:
                fh.write(key + ": " + value + "\n")
            fh.close()
            client.admin.authenticate("fireworks", "speakfriendandenter")
            client.charris.add_user("charris","speakfriendandenter", roles=[{'role':'readWrite', 'db':'testdb'}])
            lpad = fireworks.LaunchPad.from_file(self.find_lpad_config())
            lpad.reset()
        return self.find_lpad_config()
        



