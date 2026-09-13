```bash
#!/bin/bash

ffmpeg \
-i logic_garden_279_diesel_daylight.mp4 \
-i logic_garden_27b_ramjet_daylight.mp4 \
-i logic_garden_184d_wankel_daylight.mp4 \
-i logic_garden_184c_2stroke_daylight.mp4 \
-i logic_garden_184b_otto_daylight.mp4 \
-i logic_garden_191d_behemoth_daylight.mp4 \
-i logic_garden_191c_macro_daylight.mp4 \
-i logic_garden_278_supercritical_hcci_daylight.mp4 \
-i logic_garden_285_iowa_kinematics_daylight.mp4 \
-filter_complex "\
[0:v]scale=360:640:flags=lanczos[v0];\
[1:v]scale=360:640:flags=lanczos[v1];\
[2:v]scale=360:640:flags=lanczos[v2];\
[3:v]scale=360:640:flags=lanczos[v3];\
[4:v]scale=360:640:flags=lanczos[v4];\
[5:v]scale=360:640:flags=lanczos[v5];\
[6:v]scale=360:640:flags=lanczos[v6];\
[7:v]scale=360:640:flags=lanczos[v7];\
[8:v]scale=360:640:flags=lanczos[v8];\
[v0][v1][v2][v3][v4][v5][v6][v7][v8]xstack=inputs=9:layout=0_0|360_0|720_0|0_640|360_640|720_640|0_1280|360_1280|720_1280[out]" \
-map "[out]" \
-c:v libx264 -pix_fmt yuv420p -crf 14 \
-preset slow -tune animation \
-color_primaries bt709 -color_trc bt709 -colorspace bt709 \
logic_garden_423_nine_engines.mp4

echo "COMPILATION COMPLETE. O(1) ROSTER LOCKED."
```

