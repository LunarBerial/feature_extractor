from io_funcs.binary_io import  BinaryIOCollection
from frontend.label_normalisation import HTSLabelNormalisation, XMLLabelNormalisation
from frontend.silence_remover import SilenceRemover
from frontend.silence_remover import trim_silence
from frontend.min_max_norm import MinMaxNormalisation
from frontend.acoustic_composition import AcousticComposition
from frontend.parameter_generation import ParameterGeneration
from frontend.mean_variance_norm import MeanVarianceNorm
from frontend.label_composer import LabelComposer
from frontend.label_modifier import HTSLabelModification
from frontend.merge_features import MergeFeat
import os
import numpy as np

root = '/home/mdisk/data/'
datalist = [ 'lijiang/out_dio_16k_ns_1/']
def make_input_output_file_list (datapath):
    if not os.path.exists(datapath + 'cmp'):
        os.mkdir(datapath + 'cmp')
        os.mkdir(datapath + 'normed_cmp')
    file_ids = os.listdir (datapath + 'lf0')
    file_ids = [item.split ('.')[0] for item in file_ids]

    file_checked_ids = []

    for item in file_ids:
        try:
            lf0_length = np.fromfile (datapath + 'lf0/' + item + '.lf0', dtype=np.float32).reshape ((-1, 1)).shape[0]
            bap_length = np.fromfile ( datapath + 'bap/' + item + '.bap', dtype=np.float32).reshape ((-1, 1)).shape[0]
            mgc_length = np.fromfile (datapath + 'mgc/' + item + '.mgc', dtype=np.float32).reshape ((-1, 60)).shape[0]
        except:
            continue

        if lf0_length == 0 or bap_length == 0 or mgc_length == 0:
            continue
        else:
            file_checked_ids.append (item)

    input_dict = {}

    for name in ['lf0', 'bap', 'mgc']:

        value = [datapath  + name + '/' + item + '.' + name for item in file_checked_ids]
        input_dict.update ({name : value})

    output_list = [datapath + 'cmp/' + item + '.cmp' for item in file_checked_ids]

    output_norm_list = [datapath + 'normed_cmp/' + item + '.cmp' for item in file_checked_ids]
    return input_dict, output_list, output_norm_list
if __name__ == '__main__':

    delta_win = [-0.5, 0.0, 0.5]
    acc_win = [1.0, -2.0, 1.0]

    acoustic_worker = AcousticComposition(delta_win = delta_win, acc_win = acc_win)

    for data in datalist:
        datapath = root + data
        in_file_list_dict, nn_cmp_file_list, nn_cmp_norm_file_list = make_input_output_file_list (datapath)
        in_dimension_dict = {'mgc' : 60, 'lf0' : 1, 'bap' : 1}
        out_dimension_dict = {'mgc' : 180, 'vuv' : 1, 'lf0' : 3, 'bap' : 3}

        acoustic_worker.prepare_nn_data (in_file_list_dict, nn_cmp_file_list, in_dimension_dict, out_dimension_dict)

        var_dir = os.path.join (datapath, 'var')
        if not os.path.exists (var_dir):
            os.makedirs (var_dir)

        var_file_dict = {}
        for feature_name in out_dimension_dict.keys ():
            var_file_dict[feature_name] = os.path.join (var_dir, feature_name + '_' + str (out_dimension_dict[feature_name]))

        cmp_dim = 187

        normaliser = MeanVarianceNorm (feature_dimension=cmp_dim)
        global_mean_vector = normaliser.compute_mean(nn_cmp_file_list, 0, cmp_dim)
        global_std_vector = normaliser.compute_std(nn_cmp_file_list, global_mean_vector, 0, cmp_dim)
        normaliser.feature_normalisation(nn_cmp_file_list, nn_cmp_norm_file_list)
        cmp_norm_info = np.concatenate((global_mean_vector, global_std_vector), axis=0)

        norm_info_file =  datapath +'norm_info_file'

        cmp_norm_info = np.array(cmp_norm_info, 'float32')
        fid = open(norm_info_file, 'wb')
        cmp_norm_info.tofile(fid)
        fid.close()

        feature_index = 0
        for feature_name in out_dimension_dict.keys():
            feature_std_vector = np.array(global_std_vector[:,feature_index:feature_index+out_dimension_dict[feature_name]], 'float32')

            fid = open(var_file_dict[feature_name], 'w')
            feature_var_vector = feature_std_vector**2
            feature_var_vector.tofile(fid)
            fid.close()

            feature_index += out_dimension_dict[feature_name]


