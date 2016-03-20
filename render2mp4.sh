#!/usr/bin/env bash
ffmpeg -framerate 10 -i render/linefollow-%09d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
