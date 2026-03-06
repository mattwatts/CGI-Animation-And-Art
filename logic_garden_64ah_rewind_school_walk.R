
inDir <- "/home/mwatts/Artifacts/The Logic Garden 2026-02-27/frames_64ae_school/"
outDir <- "/home/mwatts/Artifacts/The Logic Garden 2026-02-27/frames_64ah_home_time/"

for (i in 1:185)
{
  file.copy(paste0(inDir,"frame_",sprintf("%04d", i),".png"),
            paste0(outDir,"frame_",sprintf("%04d", 186-i),".png"),
            overwrite=T)
}

