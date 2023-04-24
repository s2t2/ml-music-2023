
# Notes



## GTZAN Dataset

## Provided Features

```

chroma_stft_mean, chroma_stft_var
rms_mean, rms_var
spectral_centroid_mean, spectral_centroid_var
spectral_bandwidth_mean, spectral_bandwidth_var
rolloff_mean, rolloff_var
zero_crossing_rate_mean, zero_crossing_rate_var
harmony_mean, harmony_var
perceptr_mean, perceptr_var
tempo
mfcc1_mean, mfcc1_var
mfcc2_mean, mfcc2_var
...
mfcc20_mean, mfcc20_var
```


### Audio Processing

#### Track Cutting

Some of the files are not exactly 30 seconds long (1292 length), so we are trimming the longer ones and discarding the shorter ones. We could alternatively consider to decrease the track length to 28 or 29 seconds to capture all tracks.

length | num tracks
--- | ---
1290      | 1
1292      | 9
1293      | 944
longer   | 45


Longer Tracks:
  + classical.00049.wav
  + classical.00051.wav
  + country.00003.wav
  + country.00004.wav
  + country.00007.wav
  + disco.00014.wav
  + jazz.00054.wav
  + rock.00027.wav
  + rock.00038.wav
  + hiphop.00031.wav
  + hiphop.00032.wav
