# extracted form merlin, program to generate wav from generated cmp data and norm file

# Move the generated cmp file to wav directory and norm file to norm_file directory, then run generate.py

import configuration
import sys
import numpy
from frontend.mean_variance_norm import MeanVarianceNorm
from frontend.parameter_generation import ParameterGeneration
from utils.generate import generate_wav
import os

cfg = configuration.cfg

config_file = sys.argv[1]
speaker = sys.argv[2]

cfg.configure(config_file, use_logging=False)

norm_info_file = 'norm_file_' + speaker + '/norm_info_file'

fid = open(norm_info_file, 'rb')
cmp_min_max = numpy.fromfile(fid, dtype=numpy.float32)
fid.close()
cmp_min_max = cmp_min_max.reshape((2, -1))
cmp_min_vector = cmp_min_max[0, ] 
cmp_max_vector = cmp_min_max[1, ]

var_file_dict = {}
cur_path = os.getcwd()
var_file_dict['bap'] = cur_path + '/var_' + speaker + '/bap_3'
var_file_dict['lf0'] = cur_path + '/var_' + speaker + '/lf0_3'
var_file_dict['mgc'] = cur_path + '/var_' + speaker + '/mgc_180'
var_file_dict['vuv'] = cur_path + '/var_' + speaker + '/vuv_1'

list_file = open('list', 'rb')
gen_dir = cfg.work_dir
gen_file_list = []
gen_file_id_list = []
for item in list_file.readlines():
    gen_file_id_list.append(item.split()[0])
    gen_file_list.append(gen_dir + '/' + item.split()[0] + cfg.cmp_ext)

list_file.close()

denormaliser = MeanVarianceNorm(feature_dimension = cfg.cmp_dim)
denormaliser.feature_denormalisation(gen_file_list, gen_file_list, cmp_min_vector, cmp_max_vector)

generator = ParameterGeneration(gen_wav_features = cfg.gen_wav_features, enforce_silence = cfg.enforce_silence)
generator.acoustic_decomposition(gen_file_list, cfg.cmp_dim, cfg.out_dimension_dict, cfg.file_extension_dict, var_file_dict, do_MLPG=cfg.do_MLPG, cfg=cfg) 

generate_wav(gen_dir, gen_file_id_list, cfg)
