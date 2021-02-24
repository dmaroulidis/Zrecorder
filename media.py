#!/usr/bin/env python

# Module media contains helper functions, relating to screen recording and
# encoding.

from subprocess import Popen, PIPE, STDOUT, SubprocessError
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FfmpegExecutorParams():
    """Class for storing ffmpeg execution parameters"""
    resolution: str = '1280x720'
    framerate: int = 30
    video_encode_preset: str = 'veryfast'
    queue_size: int = 4096
    h264_constant_rate_factor: int = 28
    gop_size: int = framerate * 2


@dataclass
class Sink():
    """Class for storing format and path of recorded video"""
    path: str
    format: str = 'matroska'


def get_ffmpeg_command(ffmpeg_params, sink):
    return ['ffmpeg', '-y', '-v', 'info', '-f', 'x11grab', '-draw_mouse', '0',
            '-r', str(ffmpeg_params.framerate),
            '-s', str(ffmpeg_params.resolution),
            '-thread_queue_size', str(ffmpeg_params.queue_size),
            '-i', ':0.0+0,0',
            '-f', 'alsa',
            '-thread_queue_size', str(ffmpeg_params.queue_size),
            '-i', 'hw:Loopback,1,0',
            '-channels', '2',
            '-acodec', 'aac',
            '-strict', '2',
            '-ar', '44100',
            '-b:a', '128k',
            '-af', 'aresample=async=1',
            '-c:v', 'libx264',
            '-preset', str(ffmpeg_params.video_encode_preset),
            '-pix_fmt', 'yuv420p',
            '-r', str(ffmpeg_params.framerate),
            '-crf', str(ffmpeg_params.h264_constant_rate_factor),
            '-g', str(ffmpeg_params.gop_size), '-tune', 'zerolatency',
            '-f', sink.format, sink.path]

def get_ffmpeg_command_lossless(ffmpeg_params, sink):
    return ['ffmpeg', '-y', '-v', 'info', '-f', 'x11grab', '-draw_mouse', '0',
            '-r', str(ffmpeg_params.framerate),
            '-s', str(ffmpeg_params.resolution),
            '-thread_queue_size', str(ffmpeg_params.queue_size),
            '-i', ':0.0+0,0',
            '-f', 'alsa',
            '-thread_queue_size', str(ffmpeg_params.queue_size),
            '-i', 'hw:Loopback,1,0',
            '-channels', '2',
            '-acodec', 'pcm_s16le',
            '-strict', '2',
            '-ar', '44100',
            '-c:v', 'libx264',
            '-preset', str(ffmpeg_params.video_encode_preset),
            '-pix_fmt', 'yuv420p',
            '-r', str(ffmpeg_params.framerate),
            '-crf', '0',
            '-tune', 'zerolatency',
            '-f', sink.format, sink.path]


def record(ffmpeg_command):
    """TODO"""
    try:
        ffmpeg_proc = Popen(ffmpeg_command, stdin=PIPE, stdout=PIPE,
                            stderr=STDOUT, text=True, shell=True)
        print('record(): Started ffmpeg process')
        return ffmpeg_proc
    except (SubprocessError, OSError) as e:
        print('ERROR: ffmpeg command failed')
        return 'ERROR: ffmpeg command failed'


def get_recording_filename(course_name, output_dir):
    """
    Return a Sink() object complete with the recording's path for the
    current lecture.
    """
    now = datetime.now()
    extension = now.strftime('%d-%m-%Y_%H-%M-%S.mkv')
    name = course_name.replace(' ', '_')  + '_' + extension
    path = output_dir / name
    return Sink(path=str(path.resolve()))
