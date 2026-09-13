#!/bin/bash
# PROJECT: Logic Garden 422 (The Automaton Grid Tensor)
# FORMAT: YouTube Shorts (1080x1920) COMBINATORIAL CASCADE

echo "LG-422: INITIATING 3X3 AUTOMATON MATRIX..."

ffmpeg \
-i logic_garden_276b_handstand_daylight.mp4 \
-i logic_garden_293_p1940_automaton.mp4 \
-i logic_garden_289_b1930_automaton.mp4 \
-i logic_garden_300_t850_automaton.mp4 \
-i logic_garden_276c_acrobatic_daylight.mp4 \
-i logic_garden_294_b1942_automaton.mp4 \
-i logic_garden_288_m1928_automaton.mp4 \
-i logic_garden_276_sovereign_walk_centered.mp4 \
-i logic_garden_303b_blue_bouncer.mp4 \
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
logic_garden_422_nine_robots.mp4

echo "COMPILATION COMPLETE. O(1) ROSTER LOCKED."
