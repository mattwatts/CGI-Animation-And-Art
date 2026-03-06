outDir <- "/home/mwatts/Artifacts/The Logic Garden 2026-02-27/frames_64ai_movie/"

inDirs <- c("frames_64a_bicycle_v2",
            "frames_64ab_fetch",
            "frames_64ac_car",
            "frames_64ad_airplane",
            "frames_64ae_school",
            "frames_64af_baseball",
            "frames_64ag_picnic",
            "frames_64ah_home_time")
inCount <- c(300,180,300,300,186,300,300,186)

frameIndex <- 0
for (dirIndex in 1:length(inDirs))
{
  theInDir <- paste0('/home/mwatts/Artifacts/The Logic Garden 2026-02-27/',
                     inDirs[dirIndex],"/")
  theInCount <- inCount[dirIndex]
  
  for (i in 0:(theInCount-1))
  {
    file.copy(paste0(theInDir,"frame_",sprintf("%04d", i),".png"),
              paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"),
              overwrite=T)
    frameIndex <- frameIndex + 1
  }
  
}
