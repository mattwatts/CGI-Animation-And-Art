library(grid)
library(png)
library(magick)
library(data.table)

# parameters
"/home/mwatts/Artifacts/Logic Garden 3/frames_170_enfilade/"
"/home/mwatts/Artifacts/Logic Garden 3/frames_258_relativistic/"
workingDir <- "/home/mwatts/Artifacts/Logic Garden 3/"

inDirName <- "frames_258_relativistic"
outDirName1 <- "frames_258b_relativistic"
inDir <- paste0(workingDir,inDirName,"/")
outDir <- paste0(workingDir,outDirName1,"/")

dir.create(outDir)

# FORMAT: YouTube Shorts (1080x1920)
movieWidth <- 1080
movieHeight <- 1920

# map video frames from inDir to outDir.
# map video frames from enfilade to movie. we are removing 10 seconds (slow) of dead space near the end of the video.
frameIndex <- 0
for (i in 0:1079)
{
  # i <- 0
  inFile1 <- paste0(inDir,"frame_",sprintf("%04d", i),".png")
  inFile2 <- paste0(inDir,"frame_",sprintf("%04d", (1079-i)),".png")
  
  #if (file.exists(inFileName))
  #{
    outFile1 <- paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png")
    outFile2 <- paste0(outDir,"frame_",sprintf("%04d",(frameIndex+1080)),".png")
    
    didCopy1 <- file.copy(inFile1,
                          outFile1,
                          overwrite=T)
    didCopy2 <- file.copy(inFile2,
                          outFile2,
                          overwrite=T)
    
    if (didCopy1&didCopy2)
    { frameIndex <- frameIndex + 1 } else { cat("Error not copy ",frameIndex," ",i," ") }
  #} else { cat("Error not exist ",frameIndex," ",i," ") }
}
