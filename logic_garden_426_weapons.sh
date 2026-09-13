





ffmpeg \
-i logic_garden_20a_star_maker.mp4 \
-i logic_garden_20b_starmaker_shorts_fixed.mp4 \
-i logic_garden_106a_star_wars_v2.mp4 \
-i logic_garden_106b_star_wars_v3.mp4 \
-i logic_garden_107_hk_swarm_v2.mp4 \
-i logic_garden_108a_metal_storm.mp4 \
-i logic_garden_108b_lead_computing.mp4 \
-i logic_garden_137_aegis_kill_web.mp4 \
-i logic_garden_337b_fleet_air_defense.mp4 \
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
logic_garden_426_weapons.mp4

