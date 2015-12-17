
import logging
import subprocess
import time
import os
import steering_api

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('RECAST')

def recast(ctx):
  log.info('running CAP analysis')
  workdir = 'workdirs/{}'.format(ctx['jobguid'])
  analysis = 'dilepton_analysis'

  
  subprocess.check_call('cp {workdir}/inputs/* {workdir}'.format(workdir = workdir), shell = True)

  proc = subprocess.Popen('recastworkflow-capsteer {} {}'.format(workdir,analysis), shell = True, stderr = subprocess.STDOUT, stdout = subprocess.PIPE)
  while proc.poll() is None:
    s = proc.stdout.readline()
    try:
      splitup = s.strip().split(':',1)
      if len(splitup)==2:
        for line in splitup[1].splitlines():
          if 'adage' in line:
            log.log(getattr(logging,splitup[0]),line)
    except AttributeError:
      pass
    time.sleep(0.01)

  log.info('finished')
  if proc.returncode:
    log.error('workflow failed, raising error')
    raise RuntimeError
    
