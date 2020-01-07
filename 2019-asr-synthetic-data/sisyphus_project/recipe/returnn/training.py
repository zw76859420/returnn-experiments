__all__ = ['RETURNNModel', 'RETURNNTrainingFromFile']

from sisyphus import *
Path = setup_path(__package__)

import os
import stat
import subprocess as sp

from recipe.default_values import RETURNN_PYTHON_EXE, RETURNN_SRC_ROOT

from recipe.returnn.job_template import RETURNNJob

class RETURNNModel:
  def __init__(self, crnn_config_file, model, epoch):
    self.crnn_config_file = crnn_config_file
    self.model = model
    self.epoch = epoch


class RETURNNTrainingFromFile(RETURNNJob):
  """
  The Job allows to directly execute returnn config files. The config files have to have the line
  ext_model = config.value("ext_model", None) and set model = ext_model to correctly set the model path

  If the learning rate file should be available, add
  ext_learning_rate_file = config.value("ext_learning_rate_file", None) and
  set learning_rate_file = ext_learning_rate_file

  Other externally controllable parameters may also defined in the same way, and can be set by providing the parameter
  value in the parameter_dict. The "ext_" prefix is used for naming convention only, and is not mandatory.

  Also make sure that task="train" is set.
  """

  def __init__(self, returnn_config_file, parameter_dict,
               time_rqmt=72, mem_rqmt=8,
               returnn_python_exe=RETURNN_PYTHON_EXE, returnn_root=RETURNN_SRC_ROOT):
    """

    :param tk.Path|str returnn_config_file: a returnn training config file
    :param dict parameter_dict: provide external parameters to the rnn.py call
    :param int|str time_rqmt:
    :param int|str mem_rqmt:
    :param tk.Path|str returnn_python_exe: the executable for running returnn
    :param tk.Path |str returnn_root: the path to the returnn source folder
    """
    super().__init__(parameter_dict,
                     returnn_config_file,
                     returnn_python_exe,
                     returnn_root)

    self.rqmt = { 'gpu' : 1, 'cpu' : 2, 'mem' : mem_rqmt, 'time' : time_rqmt }


    self.learning_rates   = self.output_path('learning_rates')
    self.model_dir        = self.output_path('models', directory=True)

    self.models = None
    if 'ext_num_epochs' in parameter_dict:
      self.models           = { k : RETURNNModel(self.returnn_config_file,
                                                 self.output_path('models/epoch.%.3d.meta' % k), k)
                                for k in range(1, parameter_dict['ext_num_epochs'] +1)}

    self.parameter_dict['ext_model'] = tk.uncached_path(self.model_dir) + "/epoch"
    self.parameter_dict['ext_learning_rate_file'] = tk.uncached_path(self.learning_rates)

  def tasks(self):
    yield Task('create_files', mini_task=True)
    yield Task('run', resume='run', rqmt=self.rqmt)

  def path_available(self, path):
    # if job is finised the path is available
    res = super().path_available(path)
    if res:
      return res

    # learning rate files are only available at the end
    if path == self.learning_rates:
      return super().path_available(path)

    # maybe the file already exists
    res = os.path.exists(path.get_path())
    if res:
      return res

    # maybe the model is just a pretrain model
    file = os.path.basename(path.get_path())
    directory = os.path.dirname(path.get_path())
    if file.startswith('epoch.'):
      segments      = file.split('.')
      pretrain_file = '.'.join([segments[0], 'pretrain', segments[1]])
      pretrain_path = os.path.join(directory, pretrain_file)
      return os.path.exists(pretrain_path)

    return False

  @classmethod
  def hash(cls, kwargs):

    d = { 'returnn_config_file'     : kwargs['returnn_config_file'],
          'parameter_dict'     : kwargs['parameter_dict'],
          'returnn_python_exe' : kwargs['returnn_python_exe'],
          'returnn_root'       : kwargs['returnn_root']}

    return super().hash(d)
