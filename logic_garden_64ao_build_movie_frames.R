library(grid)
library(png)
library(magick)

# parameters
workingDir <- "/home/mwatts/Artifacts/The Logic Garden 2026-02-27/"
outDirName <- "frames_64ao_movie"
titleFrames <- 30
sceneTitleFrames <- 15
endFrames <- 15
titleMessage <- "C-64 Movie Scenes"
endMessage <- "The End"
frameFontSize <- 100

# FORMAT: YouTube Shorts (1080x1920)
movieWidth <- 1080
movieHeight <- 1920

###############Commodore C-64 Movie Tie-Ins (13)
#Logic Garden 64k: Terminator Intercept 64
#Logic Garden 64l: Signin' in the Rain 64
#Logic Garden 64m: The Wizard of Oz 64
#Logic Garden 64n: Ride of the Valkyries 64
#Logic Garden 64o: Time of my Life 64
#Logic Garden 64p: Battle of Helm's Deep 64
#Logic Garden 64q: Robocop 64
#Logic Garden 64r: You talkin to me 64
#Logic Garden 64s: Titanic 64
#Logic Garden 64t: Sad Hill Standoff 64
#Logic Garden 64u: T3 Hive 64
#Logic Garden 64v: Judgement Day 64
#Logic Garden 64z: Ludicrous Speed 64

gameNames <-
  c("Terminator Intercept 64",
    "Signin' in the Rain 64",
    "The Wizard of Oz 64",
    "Ride of the Valkyries 64",
    "Time of my Life 64",
    "Battle of Helm's Deep 64",
    "Robocop 64",
    "You talkin to me 64",
    "Titanic 64",
    "Sad Hill Standoff 64",
    "T3 Hive 64",
    "Judgement Day 64",
    "Ludicrous Speed 64")
gameFrameNames <-
  c("terminator","frame","frame","frame",
    "frame","frame","frame","frame",
    "frame","frame","frame","frame",
    "frame")

gameDirs <- 
c("logic_garden_terminator_frames",
  "frames_64l_rain",
  "frames_64m_oz",
  "frames_64n_apocalypse",
  "frames_64o_dancing",
  "frames_64p_helmsdeep",
  "frames_64q_robocop",
  "frames_64r_taxi",
  "frames_64s_titanic",
  "frames_64t_goodbadugly",
  "frames_64u_t3",
  "frames_64v_skynet",
  "frames_64z_ludicrous")

gameCounts <-
c(750,300,225,300,
  300,300,300,300,
  300,300,300,200,
  600)

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
