import os
import numpy as np
from tqdm import tqdm
import soundfile as sf
import h5py

def VAD(x, sr=44100, win=441, session_length=6):
    # x shape: (T, 2)
    # VAD
    x_len = x.shape[0] // sr * sr
    x = x[:x_len]
    x_p = x.reshape(-1, win, 2)
    x_pow = np.sum(np.power(x_p, 2), (1, 2)).reshape(-1,)
    # skip all silent segments when calculating threshold
    x_valid_pow = x_pow[x_pow > 1e-3]
    if len(x_valid_pow) > 0:
        threshold = np.quantile(x_valid_pow, 0.15)
        valid_segment = []

        num_session = (x_len - sr * session_length) // (sr * session_length // 2)

        for s in range(num_session):
            this_segment = x[s * sr * session_length // 2:s * sr * session_length // 2 + sr * session_length,:]
            this_segment_pow = this_segment.reshape(-1, win, 2)
            this_segment_pow = np.sum(np.power(this_segment_pow, 2), (1,2)).reshape(-1,)
            pow_ratio = np.sum(this_segment_pow > threshold) / len(this_segment_pow)
            if pow_ratio > 0.5:
                valid_segment.append(this_segment)

        return valid_segment
    else:
        return []
    
def musdb_preprocess(root_dir, output_dir, sr=44100, session_length=6):
    all_data_dir = {}
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".wav"):
                track = root.split("/")[-1]
                if track not in all_data_dir.keys():
                    all_data_dir[track] = [os.path.join(root, file)]
                else:
                    all_data_dir[track].append(os.path.join(root, file))
    
    for _, track in enumerate(all_data_dir.keys()):
        os.makedirs(os.path.join(output_dir, track), exist_ok=True)
        cnt = len(os.listdir(os.path.join(output_dir, track))) + 1
        print(f"Processing {track}, starting from sample {cnt}")
        for file in tqdm(all_data_dir[track], dynamic_ncols=True):
            x, sr = sf.read(file)
            x = VAD(x, sr=sr, session_length=session_length)
            if len(x) > 0:
                dataset_name = os.path.join(output_dir, track, 'sample'+str(cnt)+'.hdf5')
                dataset = h5py.File(dataset_name, 'a')
                dataset.create_dataset('data', shape=(len(x), 2, sr * session_length), dtype=float)

                for s in range(len(x)):
                    dataset['data'][s,:] = np.asarray(x[s].T)
                dataset.close()
                cnt += 1

if __name__ == "__main__":
    root_dir = "moisesdb/moisesdb_v0.1"
    output_dir = "musdb18hq-moises-hdf5"
    musdb_preprocess(root_dir, output_dir, sr=44100, session_length=6)