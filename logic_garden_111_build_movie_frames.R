library(grid)
library(png)
library(magick)
library(data.table)

# parameters
workingDir <- "/home/mwatts/Artifacts/The Logic Garden 2026-02-27/"
outDirName1 <- "frames_111_movie"

titleFrames <- 30
sceneTitleFrames <- 15
endFrames <- 15
titleMessage1 <- "Odyssey Of Little Tank"

endMessage <- "The End"
frameFontSize <- 100

# FORMAT: YouTube Shorts (1080x1920)
movieWidth <- 1080
movieHeight <- 1920

############### Weapon Sims
inputParams1 <- data.table(
rbind(
cbind("Odyssey Of Little Tank",600,"frames_68a","turret","Logic Garden 68a: The Little Tank"),
cbind("Drive",600,"frames_68b","turn","Logic Garden 68b: Drive"),
cbind("Burnout",600,"frames_68c","drift","Logic Garden 68c: Burnout"),
cbind("Tokyo Drift",600,"frames_68d","race","Logic Garden 68d: Tokyo Drift"),
cbind("Gladiator",900,"frames_68e","battle","Logic Garden 68e: Gladiator"),
cbind("Melee",900,"frames_68f","war","Logic Garden 68f: Melee"),
cbind("Boss Battle",1200,"frames_68g","titan","Logic Garden 68g: Boss Battle")
))
colnames(inputParams1) <- c("sceneLabel","frameCount","folderName","fileName","sceneName")
sum(as.numeric(inputParams1$frameCount))/30/60 # 3 minutes... need to trim a bit

#
inputParams <- inputParams1
outDir <- paste0(workingDir,outDirName1,"/")
titleMessage <- titleMessage1

dir.create(outDir)
frameIndex <- 0

# Include the title frames
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

# Traverse the input scenes, including their frames
for (rowIndex in 1:nrow(inputParams))
{
  # rowIndex <- 1
  theInDir <- paste0('/home/mwatts/Artifacts/The Logic Garden 2026-02-27/',
                     inputParams$folderName[rowIndex],"/")
  theInCount <- as.numeric(inputParams$frameCount[rowIndex])
  theMessage <- inputParams$sceneLabel[rowIndex]
  
  cat(rowIndex," ",theMessage,"  ")
  
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
  
  cat("Frames ")
  gameFrameName <- inputParams$fileName[rowIndex]
  for (i in 0:(theInCount-1))
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
