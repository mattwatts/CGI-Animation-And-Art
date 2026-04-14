library(grid)
library(png)
library(magick)
library(data.table)

# parameters
"/home/mwatts/Artifacts/Logic Garden 2/frames_170_enfilade/"
workingDir <- "/home/mwatts/Artifacts/Logic Garden 2/"
inDirName <- "frames_173_obsolescence"
outDirName1 <- "frames_173_movie"
inDir <- paste0(workingDir,inDirName,"/")
outDir <- paste0(workingDir,outDirName1,"/")

dir.create(outDir)

# FORMAT: YouTube Shorts (1080x1920)
movieWidth <- 1080
movieHeight <- 1920

# map video frames from enfilade to movie. we are removing 5 seconds (fast) of dead space near the end of the video.
# map video frames from enfilade to movie. we are removing 10 seconds (slow) of dead space near the end of the video.
frameIndex <- 0
for (i in 0:1199)
{
  # i <- 0
  inFileName <- paste0(inDir,"frame_",sprintf("%04d", i),".png")
  
  if (file.exists(inFileName))
  {
    if (file.copy(inFileName,
                  paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"),
                  overwrite=T))
    { frameIndex <- frameIndex + 1 } else { cat("Error not copy ",frameIndex," ",i," ",inFileName," ") }
  } else { cat("Error not exist ",frameIndex," ",i," ",inFileName," ") }
}
for (i in 1919:2099)
{
  # i <- 1919
  inFileName <- paste0(inDir,"frame_",sprintf("%04d", i),".png")
  
  if (file.exists(inFileName))
  {
    if (file.copy(inFileName,
                  paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"),
                  overwrite=T))
    { frameIndex <- frameIndex + 1 } else { cat("Error not copy ",frameIndex," ",i," ",inFileName," ") }
  } else { cat("Error not exist ",frameIndex," ",i," ",inFileName," ") }
}
# rewind 117
#inputDir <- paste0(workingDir,"frames_117_turnaround/")
#rewindDir <- paste0(workingDir,"frames_117b_rewind/")
#dir.create(rewindDir)
#for (i in 0:199)
#{
#  # i <- 0
#  file.copy(paste0(inputDir,"frame_",i),
#            paste0(rewindDir,"frame_",(199-i)),
#            overwrite=T)
#}

############### The Walker
inputParams1 <- data.table(
rbind(
cbind("Turnaround RHS",150,299,"frames_117_turnaround","frame"),
cbind("Walker",0,199,"frames_113_walker","frame"),

cbind("Walker Back",0,299,"frames_118_refusal","frame"),

# out of order
cbind("Return",0,199,"frames_116_walker_return","frame"),

cbind("Turnaround LHS",0,149,"frames_117_turnaround","frame")
))
colnames(inputParams1) <- c("sceneLabel","frameStart","frameEnd","folderName","fileName")

#
inputParams <- inputParams1
outDir <- paste0(workingDir,outDirName1,"/")
titleMessage <- titleMessage1

dir.create(outDir)
frameIndex <- 0

fDisplayMessage <- F

# Include the title frames
if (fDisplayMessage)
{
  cat(titleMessage,"  ")
  if (titleFrames>0)
  {
    for (i in 1:titleFrames)
    {
      png(paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"),width=movieWidth,height=movieHeight)
      grid.rect(gp=gpar(fill="white",col="white"))
      grid.text(titleMessage,x=0.5,y=0.5,gp=gpar(fontsize=frameFontSize,col="black"))
      dev.off()
      frameIndex <- frameIndex + 1
    }
  }
}

# Traverse the input scenes, including their frames
for (rowIndex in 1:nrow(inputParams))
{
  # rowIndex <- 1
  theInDir <- paste0('/home/mwatts/Artifacts/The Logic Garden 2026-02-27/',
                     inputParams$folderName[rowIndex],"/")
  theInCount <- as.numeric(inputParams$frameCount[rowIndex])
  theMessage <- inputParams$sceneLabel[rowIndex]
  
  cat(rowIndex," ",theMessage,"  ")
  
  if (fDisplayMessage)
  {
    if (theMessage!="")
    {
      if (sceneTitleFrames>0)
      {
        for (i in 1:sceneTitleFrames)
        {
          png(paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"),width=movieWidth,height=movieHeight)
          grid.rect(gp=gpar(fill="white",col="white"))
          grid.text(theMessage,x=0.5,y=0.5,gp=gpar(fontsize=frameFontSize,col="black"))
          dev.off()
          frameIndex <- frameIndex + 1
        }
      }
    }
  }
  
  cat("Frames ")
  gameFrameName <- inputParams$fileName[rowIndex]
  frameStart <- inputParams$frameStart[rowIndex]
  frameEnd <- inputParams$frameEnd[rowIndex]
  
  for (i in frameStart:frameEnd)
  {
    # i <- 0
    inFileName <- paste0(theInDir,gameFrameName,"_",sprintf("%04d", i),".png")
    
    if (file.exists(inFileName))
    {
      if (file.copy(inFileName,
                    paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"),
                    overwrite=T))
      { frameIndex <- frameIndex + 1 } else { cat("Error not copy ",frameIndex," ",i," ",inFileName," ") }
    } else { cat("Error not exist ",frameIndex," ",i," ",inFileName," ") }
  }
}

# Include the end title frames
if (fDisplayMessage)
{
  cat(endMessage,"\n")
  if (endFrames>0)
  {
    for (i in 1:endFrames)
    {
      png(paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"),width=movieWidth,height=movieHeight)
      grid.rect(gp=gpar(fill="white",col="white"))
      grid.text(endMessage,x=0.5,y=0.5,gp=gpar(fontsize=frameFontSize,col="black"))
      dev.off()
      frameIndex <- frameIndex + 1
    }
  }
}
