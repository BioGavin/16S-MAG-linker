# 16S_MAG_linker

In this study, we used Python to create a linkage analysis program (16S-MAG-linker) between amplicon sequences and assembled genomes of macrogenomes for in-depth analysis of microbial diversity and function.



## Install using conda

```
conda create -n linker python=3.8
conda activate linker
pip install tqdm xlsxwriter
conda install blast fastan
```

### Inbuilt database

- `reference`: 16S blast database
- `dataset.json`: RefSeq genome and Relative path linkage
- `map.json`: Reference 16S and RefSeq genome linkage

- `RefGenome`: RefSeq genome, download from ...



## Usage

Download the repository, replace the contents of the `16s` and `mag` folders with your own data, and then run:

```bash
python3 16S_MAG_linker.py -r 16s/ -g mag/
```



### Output

#### intermediate files

- `blastResult.txt`: Blast results of input 16S against Inbuilt reference 16S blast database
- `matchdic.json`: Input 16S matched to candidate reference genomes with blast similarity
- `resultData`: Folder, FastANI result 
- `matchData`: Folder, Associated genomes corresponding to best match results in Blast results of input 16S
- `magspath`: Path to input MAG
- `16s.json`: Link results of the input 16S with the input MAG
- `mag.json`: Link results of the input MAG with the input 16S

#### result files

- `16s.xlsx`: 16S link to candidate MAG
- `mag.xlsx`: MAG link to candidate 16S

