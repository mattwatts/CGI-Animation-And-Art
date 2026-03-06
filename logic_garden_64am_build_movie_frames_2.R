library(grid)

workingDir <- "/home/mwatts/Artifacts/The Logic Garden 2026-02-27/"

outDir <- paste0(workingDir,"frames_64am_movie/")

inDirs <- c("frames_64a_bicycle_v2",
            "frames_64ab_fetch",
            "frames_64ac_car",
            "frames_64ad_airplane",
            "frames_64ae_school",
            "frames_64af_baseball",
            "frames_64ag_picnic",
            "frames_64ah_home_time",
            "frames_64aj_truck",
            "frames_64ak_beach",
            "frames_64al_forest")
inCount <- c(300,180,300,300,186,300,300,186,300,300,300)

beforeSceneMessage <- c("Bicycle","Fetch",
                        "Car","Airplane",
                        "School","Baseball",
                        "Picnic","Home Time",
                        "Truck","Beach",
                        "Forest")

frameIndex <- 0

theMessage <- "A Day In The Life"
for (i in 1:60)
{
  # Insert message frames. 30 frames = 2 seconds at 15 frames per second
  png(paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"), width=1080, height=1920)
  # FORMAT: YouTube Shorts (1080x1920)
  grid.rect(gp=gpar(fill="white",col="white"))
  grid.text(theMessage,x=0.5,y=0.5,gp=gpar(fontsize=120,col="black"))
  dev.off()
  frameIndex <- frameIndex + 1
}


for (dirIndex in 1:length(inDirs))
{
  theInDir <- paste0('/home/mwatts/Artifacts/The Logic Garden 2026-02-27/',
                     inDirs[dirIndex],"/")
  theInCount <- inCount[dirIndex]
  theMessage <- beforeSceneMessage[dirIndex]
  
  if (theMessage!="")
  {
    for (i in 1:30)
    {
      # Insert message frames. 30 frames = 2 seconds at 15 frames per second
      png(paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"), width=1080, height=1920)
      # FORMAT: YouTube Shorts (1080x1920)
      grid.rect(gp=gpar(fill="white",col="white"))
      grid.text(theMessage,x=0.5,y=0.5,gp=gpar(fontsize=120,col="black"))
      dev.off()
      frameIndex <- frameIndex + 1
    }
  }
  
  for (i in 0:(theInCount-1))
  {
    file.copy(paste0(theInDir,"frame_",sprintf("%04d", i),".png"),
              paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"),
              overwrite=T)
    frameIndex <- frameIndex + 1
  }
  
}

theMessage <- "The End"
for (i in 1:30)
{
  # Insert message frames. 30 frames = 2 seconds at 15 frames per second
  png(paste0(outDir,"frame_",sprintf("%04d",frameIndex),".png"), width=1080, height=1920)
  # FORMAT: YouTube Shorts (1080x1920)
  grid.rect(gp=gpar(fill="white",col="white"))
  grid.text(theMessage,x=0.5,y=0.5,gp=gpar(fontsize=120,col="black"))
  dev.off()
  frameIndex <- frameIndex + 1
}
