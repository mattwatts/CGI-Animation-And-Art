library(grid)
library(png)
library(magick)
library(data.table)

# parameters
workingDir <- "/home/mwatts/Artifacts/The Logic Garden 2026-02-27/"
outDirName1 <- "frames_109_movie"
outDirName2 <- "frames_110_movie"
titleFrames <- 30
sceneTitleFrames <- 15
endFrames <- 15
titleMessage1 <- "Weapon Sims 1"
titleMessage2 <- "Weapon Sims 2"
endMessage <- "The End"
frameFontSize <- 100

# FORMAT: YouTube Shorts (1080x1920)
movieWidth <- 1080
movieHeight <- 1920

############### Weapon Sims
inputParams1 <- data.table(
rbind(
cbind("Hive Mind",300,"frames_99","frame","Logic Garden 99: Hive Mind"),
cbind("Star Wars - SDI",450,"frames_106a","frame","Logic Garden 106a: Star Wars (SDI)"),
cbind("Iron Dome - Saturation",500,"frames_98","frame","Logic Garden 98: Iron Dome (Saturation Defense)"),
cbind("Lead Computing",600,"frames_108a","frame","Logic Garden 108a: Lead Computing"),
cbind("Disney Bomb",300,"frames_47","disney","Logic Garden 47: The Disney Bomb"),
cbind("Lead Dynamics",600,"frames_108b","frame","Logic Garden 108b: Lead Dynamics"),
cbind("Variable Time Fuse",950,"frames_48","vt_final","Logic Garden 48: The Variable Time (VT) Fuse"),
cbind("H-K Aerial Swarm",600,"frames_107","frame","Logic Garden 107: H-K Aerial Swarm")
))
inputParams2 <- data.table(
  rbind(
cbind("Implosion Lens",1200,"frames_58","implosion","Logic Garden 58: The Implosion Lens"),
cbind("Steel Rain - ICBM",960,"frames_96","frame","Logic Garden 96: Steel Rain (ICBM)"),
cbind("Star Wars - Threat Cloud",330,"frames_106b","frame","Logic Garden 106b: Star Wars (Threat Cloud)"),
cbind("Star Maker",600,"frames_20b","frame","Logic Garden 20b Star Maker"),
cbind("AEGIS Weapon System",1200,"frames_50","aegis","Logic Garden 50: The Phased Array"),
cbind("Star Maker",600,"frames_20a","star","Logic Garden 20a: The Star Maker")
))
colnames(inputParams1) <- c("sceneLabel","frameCount","folderName","fileName","sceneName")
colnames(inputParams2) <- c("sceneLabel","frameCount","folderName","fileName","sceneName")

#inputParams1$sceneLabel
#inputParams2$sceneLabel

#sum(as.numeric(inputParams1$frameCount)) # 4300
#sum(as.numeric(inputParams2$frameCount)) # 4890
# 300 + 450 + 500 + 600 + 300 + 600 + 950 + 600 + 1200 +  960 +  330 + 600+ 1200+  600
# 300 + 450 + 500 + 600 + 300 + 600 + 950 # 3700
# 9190 / 2 # 4595
# 300 + 450 + 500 + 600 + 300 + 600 + 950 + 600 # 

#
inputParams <- inputParams1
outDir <- paste0(workingDir,outDirName1,"/")
titleMessage <- titleMessage1
#
inputParams <- inputParams2
outDir <- paste0(workingDir,outDirName2,"/")
titleMessage <- titleMessage2

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
#cat(titleMessage2,"  ")
#if (titleFrames>0)
#{
#  for (i in 1:titleFrames)
#  {
#    png(paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"),width=movieWidth,height=movieHeight)
#    grid.rect(gp=gpar(fill="white",col="white"))
#    grid.text(titleMessage2,x=0.5,y=0.5,gp=gpar(fontsize=frameFontSize,col="black"))
#    dev.off()
#    frameIndex <- frameIndex + 1
#  }
#}

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
