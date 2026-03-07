library(grid)
library(png)
library(magick)

# parameters
workingDir <- "/home/mwatts/Artifacts/The Logic Garden 2026-02-27/"
outDirName <- "frames_64an_movie"
titleFrames <- 60
sceneTitleFrames <- 30
endFrames <- 30
titleMessage <- "C-64 Game Demos"
endMessage <- "The End"
frameFontSize <- 100

# FORMAT: YouTube Shorts (1080x1920)
movieWidth <- 1080
movieHeight <- 1920


##########Commodore C-64 Games (11)
#Logic Garden 64b: The 8-Bit War
#Logic Garden 64d: AEGIS Shield 64
#Logic Garden 64e: Tank Deathmatch 64
#Logic Garden 64f: Atomic Kettle 64
#Logic Garden 64g: Star Maker 64
#Logic Garden 64h: Moon Lander 64
#Logic Garden 64i: Melee 64
#Logic Garden 64j: Hive Mind 64
#Logic Garden 64w: Hunter Killer Swarm 64
#Logic Garden 64x: Metal Storm 64
#Logic Garden 64y: Wolf Pack 64

gameFrameNames <-
  c("c64_tank","aegis","madman","kettle","starmaker","eagle","totalwar","swarm","frame","frame","frame")

gameDirs <- 
c("logic_garden_8bit_frames",
  "logic_garden_aegis_frames",
  "logic_garden_madman_frames",
  "logic_garden_kettle_frames",
  "logic_garden_starmaker_frames",
  "logic_garden_eagle_frames",
  "logic_garden_totalwar_frames",
  "logic_garden_swarm_frames",
  "frames_64w_hk",
  "frames_64x_metal",
  "frames_64y_wolf")

gameCounts <-
c(900,
  900,
  900,
  600,
  750,
  750,
  900,
  750,
  250,
  300,
  300)

gameNames <-
c("The 8-Bit War",
  "AEGIS Shield 64",
  "Tank Deathmatch 64",
  "Atomic Kettle 64",
  "Star Maker 64",
  "Moon Lander 64",
  "Melee 64",
  "Hive Mind 64",
  "Hunter Killer Swarm 64",
  "Metal Storm 64",
  "Wolf Pack 64")

outDir <- paste0(workingDir,outDirName,"/")
dir.create(outDir)
inDirs <- gameDirs
inCount <- gameCounts
beforeSceneMessage <- gameNames
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
for (dirIndex in 1:length(inDirs))
{
  # dirIndex <- 1
  theInDir <- paste0('/home/mwatts/Artifacts/The Logic Garden 2026-02-27/',
                     inDirs[dirIndex],"/")
  theInCount <- inCount[dirIndex]
  theMessage <- beforeSceneMessage[dirIndex]
  
  cat(dirIndex," ",theMessage,"  ")
  
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
  gameFrameName <- gameFrameNames[dirIndex]
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
