# Apollo Training Data Preprocessing

<p align="center">
  <img src="https://visitor-badge.laobi.icu/badge?page_id=JusperLee.Apollo-data-preprocess" alt="访客统计" />
  <img src="https://img.shields.io/github/stars/JusperLee/Apollo-data-preprocess?style=social" alt="GitHub stars" />
  <img alt="Static Badge" src="https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey">
</p>

This repository contains code for preprocessing training data for the Apollo audio processing model. It includes two scripts for handling different datasets: `moisesdb_preprocess.py` and `musdb_preprocess.py`.

## Overview

The preprocessing code performs the following steps:
1. Loads audio files
2. Applies Voice Activity Detection (VAD) to filter out silent segments
3. Splits the audio into fixed-length sessions
4. Stores the processed data in HDF5 format for efficient training

## Usage

### MoisesDB Preprocessing

To preprocess the MoisesDB dataset:

```bash
python moisesdb_preprocess.py
```

By default, this will:
- Read data from `moisesdb/moisesdb_v0.1`
- Output processed data to `musdb18hq-moises-hdf5`
- Sample rate is set to 44.1kHz
- Session length is 6 seconds

You can modify the default paths and parameters in the script as needed.

### MUSDB Preprocessing

To preprocess the MUSDB18-HQ dataset:

```bash
python musdb_preprocess.py
```

By default, this will:
- Read training data from `musdb18hq/train`
- Read test data from `musdb18hq/test`
- Output processed data to `musdb18hq-moises-hdf5`
- Sample rate is set to 44.1kHz
- Session length is 6 seconds

You can modify the default paths and parameters in the script as needed.

## Implementation Details

Both scripts implement a VAD (Voice Activity Detection) function that:
- Takes in audio data
- Calculates power thresholds
- Identifies segments where audio is present (not silent)
- Extracts valid audio segments
- Returns segments that have significant audio content

The processed data is stored in an HDF5 format, with each track organized in a separate directory.

## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

## Contact

If you have any questions or suggestions, please feel free to contact me at
- Email: tsinghua.kaili@gmail.com

## Citation

If you find this code useful, please consider citing the following paper:

```
@inproceedings{li2025apollo,
  title={Apollo: Band-sequence Modeling for High-Quality Music Restoration in Compressed Audio},
  author={Li, Kai and Luo, Yi},
  booktitle={IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  year={2025},
  organization={IEEE}
}
```