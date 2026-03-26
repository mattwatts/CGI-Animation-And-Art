library(grid)
library(png)
library(magick)
library(data.table)

# parameters
inputFrames1 <- "/home/mwatts/Artifacts/Logic Garden 2/frames_143_zen_1501_1559/"
workingDir <- "/home/mwatts/Artifacts/Logic Garden 2/"
outDirName1 <- "frames_144_movie"
outDir <- paste0(workingDir,outDirName1,"/")
dir.create(outDir)

# extract 143
frameIndex <- 0
for (i in 1501:1599)
{
  # i <- 1501
  file.copy(paste0(inputFrames1,"frame_",i,".png"),
            paste0(outDir,"frame_",frameIndex,".png"),
            overwrite=T)
  frameIndex <- frameIndex + 1
}

