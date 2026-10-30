
H.264/H.265 Video Encoder, Decoder and Streaming
================================================

*Application Development on Linux-Based Embedded Systems*

Introduction
============

Video encoding and decoding are important functions in modern multimedia applications. Digital cameras, surveillance systems, video conferencing devices, industrial monitoring equipment, and embedded multimedia platforms generate video data that must be compressed, stored, transmitted, and displayed efficiently.

Raw video contains a large amount of image data. Transmitting or storing uncompressed video requires significant memory capacity, processing resources, and network bandwidth. Video compression technologies reduce the amount of data while maintaining acceptable visual quality.

H.264 and H.265 are widely used video compression standards.

- **H.264**, also known as Advanced Video Coding (AVC), is commonly used in video streaming, surveillance, video conferencing, and digital video recording.
- **H.265**, also known as High Efficiency Video Coding (HEVC), is a newer video coding standard designed to provide improved compression efficiency compared with H.264 under suitable encoding conditions.

A video encoder converts raw video frames into a compressed bitstream. A video decoder receives the compressed bitstream and reconstructs video frames for display or further processing.

In Linux-based embedded systems, encoding and decoding can be performed using software libraries, hardware codec engines, and multimedia frameworks such as GStreamer and FFmpeg.

This document explains H.264/H.265 encoding and decoding, their architecture, compression methods, streaming workflow, Linux integration, practical commands, performance considerations, and troubleshooting.

Objectives
==========

The main objectives of this document are:

1. Understand video compression and its importance in multimedia applications.
2. Understand H.264 and H.265 video coding standards.
3. Understand the architecture of video encoders and decoders.
4. Understand intra-frame and inter-frame compression.
5. Identify the differences between H.264 and H.265.
6. Understand video resolution, frame rate, bitrate, and quality.
7. Understand software and hardware video encoding and decoding.
8. Understand the role of GStreamer and FFmpeg in multimedia applications.
9. Perform basic H.264/H.265 encoding and decoding tests.
10. Understand video streaming over an IP network.
11. Identify common video-processing and streaming problems.
12. Establish a practical validation procedure for embedded video applications.

Scope
=====

This document focuses on application-side video encoding, decoding, and streaming using H.264 and H.265 on Linux-based systems.

The scope includes:

- Video compression fundamentals.
- H.264 and H.265 standards.
- Encoder and decoder architecture.
- Intra-frame and inter-frame compression.
- I-frames, P-frames, and B-frames.
- Bitrate and rate-control methods.
- Video resolution and frame rate.
- Software and hardware codec processing.
- GStreamer multimedia pipelines.
- FFmpeg encoding and decoding.
- MP4 video storage.
- RTP/UDP video streaming.
- Linux application integration.
- Performance testing and troubleshooting.

The examples use generic Linux systems and commonly available multimedia tools.

Hardware codec elements, supported resolutions, encoder controls, and decoder capabilities vary by processor and multimedia driver. Platform-specific hardware acceleration must be verified using the target system's documentation.

Video Encoding and Decoding Overview
====================================

Video encoding and decoding are complementary operations.

Video Encoding
--------------

Video encoding converts raw image frames into a compressed video bitstream.

The main purpose is to reduce the amount of data required to store or transmit video.

A typical encoding process is:

.. code-block:: text

           Camera / Video Source
                    |
                    v
              Raw Video Frames
                    |
                    v
             Format Conversion
                    |
                    v
              Video Encoder
              (H.264 / H.265)
                    |
                    v
            Compressed Bitstream
                    |
              +-----+------+
              |            |
              v            v
            Storage     Network
           (MP4 File)  (Video Stream)

The encoder analyzes video frames and applies compression techniques to reduce redundant image information.

Video Decoding
--------------

Video decoding reconstructs video frames from a compressed bitstream.

The decoder receives encoded video data, processes the compressed information, and generates raw frames.

A typical decoding process is:

.. code-block:: text

           Compressed Video
              (H.264/H.265)
                    |
                    v
              Video Decoder
                    |
                    v
              Raw Video Frames
                    |
                    v
             Format Conversion
                    |
              +-----+------+
              |            |
              v            v
           Display      Processing

The decoded frames can be displayed, stored, analyzed, or passed to another multimedia application.

Complete Video Communication Flow
---------------------------------

In a video communication system, encoding and decoding work together.

.. code-block:: text

           TRANSMITTER
       +--------------------+
       | Camera / Video     |
       | Source             |
       +--------------------+
                 |
                 v
           Raw Video Frames
                 |
                 v
           H.264 / H.265
              Encoder
                 |
                 v
          Compressed Video
                 |
                 v
            IP Network
                 |
                 v
       +--------------------+
       |     RECEIVER       |
       +--------------------+
                 |
                 v
           H.264 / H.265
              Decoder
                 |
                 v
           Raw Video Frames
                 |
                 v
           Display / Output

This architecture is used in surveillance, video conferencing, remote monitoring, and network camera applications.

Video Compression Fundamentals
==============================

Video compression reduces the size of video data by removing redundant information.

A video consists of a sequence of image frames. Consecutive frames often contain similar visual information because most objects do not change significantly between frames.

Video codecs use this similarity to reduce the amount of information that must be stored or transmitted.

There are two major categories of compression:

1. Spatial compression.
2. Temporal compression.

Spatial Compression
-------------------

Spatial compression reduces redundant information within a single frame.

For example, a frame may contain a large region with a similar background color.

Instead of storing every pixel independently, the encoder uses transform, prediction, and quantization techniques to represent the image more efficiently.

This process is also called intra-frame compression.

Temporal Compression
--------------------

Temporal compression reduces redundant information between multiple frames.

For example, consider a video of a person standing in front of a stationary wall.

Most of the background remains unchanged between frames. The encoder can reuse information from previously encoded frames and represent only the changes where possible.

This reduces the amount of data required for the video.

Temporal compression is also called inter-frame compression.

Why Video Compression Is Required
---------------------------------

Consider an uncompressed video stream with the following configuration:

- Resolution: 1920 × 1080.
- Pixel format: YUV 4:2:0, 8-bit.
- Frame rate: 30 FPS.

The approximate data size per frame is:

.. code-block:: text

    1920 × 1080 × 1.5

    = 3,110,400 bytes per frame

The approximate data rate is:

.. code-block:: text

    3,110,400 × 30

    = 93,312,000 bytes per second

    = Approximately 93.3 MB/s

This is approximately 746.5 Mbps before additional overhead.

An uncompressed stream of this size requires significant bandwidth.

H.264 and H.265 reduce the amount of data required for storage and network transmission.

The final compressed bitrate depends on the encoder, image content, resolution, frame rate, quality settings, and rate-control method.

H.264 Video Compression
=======================

H.264 is also known as Advanced Video Coding (AVC).

It is standardized as ITU-T Recommendation H.264 and ISO/IEC 14496-10.

H.264 is widely used because of its broad compatibility with video players, browsers, cameras, media servers, and embedded multimedia systems.

Common applications include:

- IP camera streaming.
- Video surveillance.
- Video conferencing.
- Digital video recording.
- Online video streaming.
- Remote monitoring.
- Multimedia playback.

H.264 Encoder Operation
-----------------------

The H.264 encoder receives raw video frames and compresses them into an H.264 bitstream.

A simplified encoder pipeline is:

.. code-block:: text

               Raw Video Frame
                      |
                      v
               Frame Partitioning
                      |
                      v
                 Prediction
                      |
                      v
                  Transform
                      |
                      v
                 Quantization
                      |
                      v
                Entropy Coding
                      |
                      v
              H.264 Compressed
                   Bitstream

The actual encoder includes additional operations such as motion estimation, motion compensation, filtering, and rate control.

H.264 Prediction
----------------

H.264 uses prediction to reduce redundant image information.

Two main prediction methods are used:

**Intra prediction**

Intra prediction estimates image blocks using neighboring information from the same frame.

It is useful when a frame must be encoded without relying on other frames.

**Inter prediction**

Inter prediction uses information from previously decoded or reference frames.

It estimates how image regions have moved and encodes the differences.

H.264 Transform and Quantization
--------------------------------

The encoder transforms image residual data into frequency-related coefficients.

Quantization reduces the precision of these coefficients to achieve compression.

Higher quantization generally reduces bitrate but can introduce more visible distortion.

The decoder reverses the corresponding operations to reconstruct the image.

H.264 Entropy Coding
--------------------

Entropy coding converts symbols and coefficient information into a compact bitstream.

H.264 supports coding methods such as:

- CAVLC (Context-Adaptive Variable-Length Coding).
- CABAC (Context-Adaptive Binary Arithmetic Coding).

The available coding method depends on the selected H.264 profile and encoder configuration.

H.264 Frame Types
=================

H.264 uses different frame and picture types to improve compression efficiency.

The commonly discussed types are I, P, and B frames.

I-Frame
-------

An I-frame is an intra-coded picture.

It can be decoded without requiring another picture for its image prediction.

Characteristics:

- Contains independently coded picture information.
- Provides a reference point for decoding.
- Commonly used at the beginning of a stream or GOP.
- Usually requires more data than a similar P-frame.

P-Frame
-------

A P-frame uses prediction from previously decoded reference pictures.

It stores information about changes relative to reference data.

Characteristics:

- Uses inter-frame prediction.
- Generally requires fewer bits than an I-frame.
- Depends on reference-picture information for reconstruction.

B-Frame
-------

A B-frame can use prediction from reference pictures before and after the current picture in display order.

Characteristics:

- Uses bidirectional prediction.
- Can improve compression efficiency.
- May require additional buffering and processing.
- Can introduce additional latency depending on the encoder configuration.

Frame Comparison
----------------

Frame TypeDescriptionReference RequirementI-frameIntra-coded pictureDoes not require another picture for its image predictionP-framePredictive pictureUses previously decoded reference picturesB-frameBidirectionally predictive pictureCan use reference pictures from both directionsA sequence of pictures is commonly organized into a Group of Pictures (GOP).

The GOP structure affects compression efficiency, seeking, error recovery, and streaming latency.

H.265 Video Compression
=======================

H.265 is also known as High Efficiency Video Coding (HEVC).

It is standardized as ITU-T Recommendation H.265 and ISO/IEC 23008-2.

H.265 was developed to improve video compression efficiency and support applications requiring high-resolution video.

Common applications include:

- 4K video streaming.
- High-resolution surveillance.
- Digital video recording.
- Video distribution.
- Professional multimedia applications.
- Embedded video systems.

H.265 Encoder Operation
-----------------------

H.265 uses more advanced coding tools than H.264.

A simplified encoding pipeline is:

.. code-block:: text

                Raw Video Frame
                       |
                       v
              Coding Tree Partition
                       |
                       v
                 Prediction
                       |
                       v
                   Transform
                       |
                       v
                 Quantization
                       |
                       v
                 Entropy Coding
                       |
                       v
              H.265 Compressed
                    Bitstream

The actual encoder also performs motion estimation, motion compensation, filtering, and rate control.

Coding Tree Units
-----------------

H.264 uses macroblock-based coding, commonly with a maximum macroblock size of 16 × 16 luma samples.

H.265 introduces Coding Tree Units (CTUs), which can be larger and are organized using flexible coding structures.

A CTU can have a maximum size of 64 × 64 luma samples in the standard.

Larger coding structures can improve compression efficiency, particularly for high-resolution video.

H.265 Compression Features
--------------------------

H.265 includes several improvements, such as:

- Larger coding structures.
- More flexible prediction.
- Improved motion compensation.
- More flexible transform processing.
- Improved entropy coding.
- Additional in-loop filtering tools.

These techniques can reduce the bitrate required for comparable visual quality under suitable encoding conditions.

H.265 Video Decoding
--------------------

The H.265 decoder receives the compressed bitstream and reconstructs the video frames.

The decoder performs operations corresponding to the encoder's coding tools, including:

1. Bitstream parsing.
2. Entropy decoding.
3. Inverse quantization.
4. Inverse transform.
5. Prediction reconstruction.
6. Motion compensation.
7. In-loop filtering.
8. Reference-picture management.
9. Output frame generation.

The resulting frames can be displayed or passed to another processing stage.

H.264 vs. H.265 Comparison
==========================

H.264 and H.265 are both widely used video compression standards, but they differ in coding tools, complexity, and ecosystem support.

ParameterH.264 (AVC)H.265 (HEVC)Full nameAdvanced Video CodingHigh Efficiency Video CodingStandardITU-T H.264ITU-T H.265Coding structureMacroblock-basedCoding Tree Unit-basedMaximum luma coding unit16 × 16 macroblock64 × 64 CTUCompression efficiencyEstablished and widely supportedGenerally improved at comparable qualityEncoding complexityGenerally lowerGenerally higherDecoding complexityGenerally lowerGenerally higherHardware supportVery widely availableDepends more on platform generationCompatibilityBroad device supportRequires HEVC-compatible decoderTypical applicationsGeneral video streaming and recordingHigh-resolution and bandwidth-sensitive video

Compression Efficiency
----------------------

H.265 is designed to achieve better compression efficiency than H.264.

In suitable comparisons, H.265 can deliver similar visual quality at a lower bitrate.

However, the actual improvement is not a fixed percentage. It depends on:

- Encoder implementation.
- Encoding preset.
- Video content.
- Resolution.
- Frame rate.
- Quality target.
- Rate-control configuration.

Processing Requirements
-----------------------

H.265 can require more processing resources than H.264, particularly during software encoding.

Hardware acceleration can reduce CPU load when the processor includes a compatible H.265 codec engine and Linux driver.

Compatibility
-------------

H.264 generally has broader compatibility across older devices and software.

H.265 requires a compatible decoder and suitable playback support.

The choice should consider both the sending and receiving systems.

Video Profiles and Levels
=========================

Video codecs define profiles and levels to describe supported coding features and operating limits.

H.264 Profiles
--------------

Common H.264 profiles include:

ProfileDescriptionBaselineDesigned for simpler decoding and compatibility-oriented applicationsMainSupports additional coding tools, including B-frame-related featuresHighSupports additional compression tools and is widely used for HD videoOther profiles are also defined by the standard.

The selected profile must be supported by the decoder.

H.265 Profiles
--------------

H.265 includes profiles such as:

- Main.
- Main 10.
- Main Still Picture.

Main 10 supports up to 10-bit sample representation in the relevant profile configuration.

The actual supported profile and bit depth depend on the codec implementation.

Levels
------

A codec level specifies constraints related to video processing, including parameters such as:

- Maximum picture size.
- Maximum processing rate.
- Bitrate limits.
- Decoded-picture buffer requirements.

The profile and level must be selected according to the intended resolution, frame rate, bitrate, and decoder capabilities.

Important Video Encoding Parameters
===================================

Video quality and performance depend on several encoder parameters.

Resolution
----------

Resolution represents the number of pixels in each video frame.

Common examples include:

ResolutionTotal PixelsTypical Description640 × 480307,200VGA1280 × 720921,600HD1920 × 10802,073,600Full HD2560 × 14403,686,400QHD3840 × 21608,294,4004K UHDHigher resolutions provide more image detail but require more processing and bandwidth.

Frame Rate
----------

Frame rate is the number of video frames processed per second.

It is measured in FPS.

Common frame rates include:

- 15 FPS.
- 24 FPS.
- 25 FPS.
- 30 FPS.
- 50 FPS.
- 60 FPS.

A higher frame rate can improve motion representation, but it increases encoding, decoding, and network requirements.

Bitrate
-------

Bitrate describes the amount of compressed video data produced or transmitted per second.

It is usually measured in:

- Kbps: kilobits per second.
- Mbps: megabits per second.

For example, an encoder configured for a target bitrate of 4 Mbps aims to produce an average data rate around that target, depending on its rate-control mode.

Bitrate affects:

- Network bandwidth.
- Storage capacity.
- Compression quality.
- Buffering requirements.

The required bitrate depends on video complexity, resolution, frame rate, and quality expectations.

Quantization Parameter
----------------------

The Quantization Parameter (QP) controls quantization strength in many codec implementations.

In general:

- Lower QP preserves more image detail and produces a larger bitstream.
- Higher QP produces stronger compression and may reduce visual quality.

The exact relationship between QP and bitrate depends on the encoder and video content.

GOP Size
--------

GOP size represents the interval or structure between key reference pictures, depending on the encoder's configuration.

A shorter GOP can improve recovery after packet loss and make seeking easier.

A longer GOP may improve compression efficiency but can increase the time required to recover from errors or join a stream.

Rate Control
------------

Rate control manages the amount of data generated by the encoder.

Common methods include:

**Constant Bitrate (CBR)**

The encoder attempts to maintain a relatively stable target bitrate.

Useful for systems with predictable network bandwidth.

**Variable Bitrate (VBR)**

The encoder adjusts the bitrate according to scene complexity.

More complex scenes may use more bits, while simpler scenes may use fewer bits.

**Constant Rate Factor (CRF) / Constant Quality**

The encoder attempts to maintain a selected quality level, allowing the bitrate to vary.

The exact mode and options depend on the encoder implementation.

Software and Hardware Video Encoding
====================================

Video encoding can be implemented using software or dedicated hardware.

Software Encoding
-----------------

Software encoding uses the host CPU to perform compression.

Examples include:

- x264 for H.264.
- x265 for H.265.
- FFmpeg codec integrations.
- GStreamer software encoder elements.

Advantages:

- Flexible configuration.
- Broad availability on supported systems.
- Easier experimentation with encoding parameters.
- No dedicated codec engine required.

Limitations:

- Higher CPU utilization.
- Greater power consumption under heavy workloads.
- Performance may be limited at high resolutions or frame rates.

Hardware Encoding
-----------------

Hardware encoding uses a dedicated video codec engine integrated into the processor or multimedia subsystem.

The hardware encoder receives raw frames and generates a compressed bitstream.

Typical architecture:

.. code-block:: text

              Raw Video Frames
                      |
                      v
                Host Processor
                      |
                      v
              Hardware Encoder
                      |
                      v
              H.264 / H.265
              Compressed Stream
                      |
                      v
               Storage / Network

Advantages:

- Reduced CPU workload.
- Improved performance per watt.
- Suitable for continuous video processing.
- Can support high-resolution video efficiently.

Limitations:

- Supported codecs depend on the processor.
- Available profiles and levels may be restricted.
- Hardware-specific drivers and libraries may be required.
- Some controls may not be exposed through standard applications.

Software vs. Hardware Encoding
------------------------------

ParameterSoftware EncodingHardware EncodingProcessing unitCPUDedicated codec hardwareCPU utilizationUsually higherUsually lowerPower efficiencyDepends on CPU and workloadOften better for supported workloadsConfigurationOften highly flexibleDepends on hardware and driverPlatform supportDepends on software librariesRequires compatible codec hardwarePerformanceLimited by CPU resourcesDepends on codec engine capability

Hardware Decoding
-----------------

Hardware decoding uses a dedicated decoder engine to reconstruct video frames.

This can reduce CPU utilization and improve playback performance.

However, the decoded frames may need to be transferred between memory domains or converted into formats suitable for the display or application.

Zero-copy or DMA-BUF-based processing may reduce unnecessary copies when supported by the complete pipeline.

Linux Multimedia Frameworks
===========================

Linux provides several tools and frameworks for video encoding, decoding, and streaming.

The two commonly used tools are GStreamer and FFmpeg.

GStreamer
---------

GStreamer is a multimedia framework used to construct audio and video processing pipelines.

A pipeline consists of connected elements that process data.

Common element categories include:

Element TypePurposeSourceProvides video inputConverterConverts video formatsEncoderCompresses raw videoParserProcesses encoded bitstream structureMuxerCombines encoded streams into a containerDemuxerSeparates streams from a containerDecoderReconstructs raw videoSinkDisplays, stores, or transmits outputExamples of GStreamer elements include:

- ``v4l2src``
- ``videoconvert``
- ``x264enc``
- ``x265enc``
- ``h264parse``
- ``h265parse``
- ``avdec_h264``
- ``avdec_h265``
- ``mp4mux``
- ``filesink``
- ``udpsink``
- ``udpsrc``
- ``rtph264pay``
- ``rtph264depay``
- ``rtph265pay``
- ``rtph265depay``

Element availability depends on the installed GStreamer version and plugins.

FFmpeg
------

FFmpeg is a multimedia framework and command-line toolset used for:

- Video encoding.
- Video decoding.
- Audio processing.
- Format conversion.
- Container processing.
- Streaming.
- Multimedia inspection.

FFmpeg supports multiple codecs and hardware acceleration backends, depending on how it was built and which libraries are installed.

It can be used for quick video conversion and codec validation.

Installing Required Software
============================

The following examples use Ubuntu or Debian-based Linux distributions.

Install GStreamer
-----------------

Run:

.. code-block:: text

    sudo apt update
    sudo apt install gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav

Package availability and plugin contents vary by distribution.

Install FFmpeg
--------------

Run:

.. code-block:: text

    sudo apt install ffmpeg

Check the version:

.. code-block:: text

    ffmpeg -version

Verify GStreamer
----------------

Run:

.. code-block:: text

    gst-launch-1.0 --version

Check whether the H.264 encoder is available:

.. code-block:: text

    gst-inspect-1.0 x264enc

Check whether the H.265 encoder is available:

.. code-block:: text

    gst-inspect-1.0 x265enc

Check H.264 decoding:

.. code-block:: text

    gst-inspect-1.0 avdec_h264

Check H.265 decoding:

.. code-block:: text

    gst-inspect-1.0 avdec_h265

If an element is unavailable, the required plugin may not be installed or may not have been included in the GStreamer build.

H.264 Encoding Using GStreamer
==============================

This section demonstrates how to encode video into H.264 using GStreamer.

The examples use the ``videotestsrc`` element, which generates test video without requiring a physical camera.

This is useful for validating the encoder and pipeline independently of camera hardware.

Generate an H.264 Video File
----------------------------

Run:

.. code-block:: text

    gst-launch-1.0 -e \
    videotestsrc num-buffers=300 ! \
    video/x-raw,width=1280,height=720,framerate=30/1 ! \
    videoconvert ! \
    x264enc bitrate=4000 speed-preset=ultrafast ! \
    h264parse ! \
    mp4mux ! \
    filesink location=output_h264.mp4

Explanation:

- ``videotestsrc``: Generates test video frames.
- ``num-buffers=300``: Generates 300 frames.
- ``video/x-raw``: Defines raw video dimensions and frame rate.
- ``videoconvert``: Converts the input into a format accepted by the encoder.
- ``x264enc``: Encodes the raw video into H.264.
- ``bitrate=4000``: Requests a target bitrate of approximately 4000 kbit/s.
- ``speed-preset=ultrafast``: Selects a faster encoding preset.
- ``h264parse``: Parses the H.264 bitstream.
- ``mp4mux``: Packages the video into an MP4 container.
- ``filesink``: Writes the output to a file.

The ``-e`` option requests an orderly pipeline shutdown so that the MP4 container can be finalized.

Check the output file:

.. code-block:: text

    ls -lh output_h264.mp4

Inspect the H.264 File
----------------------

Run:

.. code-block:: text

    ffprobe -v error \
    -select_streams v:0 \
    -show_entries stream=codec_name,width,height,r_frame_rate,bit_rate \
    -of default=noprint_wrappers=1 \
    output_h264.mp4

The output should identify the H.264 video stream and its available properties.

The reported bitrate may differ from the configured target.

H.265 Encoding Using GStreamer
==============================

H.265 encoding can be performed using the ``x265enc`` software encoder when the required plugin and library are available.

Generate an H.265 Video File
----------------------------

Run:

.. code-block:: text

    gst-launch-1.0 -e \
    videotestsrc num-buffers=300 ! \
    video/x-raw,width=1280,height=720,framerate=30/1 ! \
    videoconvert ! \
    x265enc bitrate=3000 ! \
    h265parse ! \
    mp4mux ! \
    filesink location=output_h265.mp4

Explanation:

- ``videotestsrc``: Generates test frames.
- ``video/x-raw``: Defines the video dimensions and frame rate.
- ``videoconvert``: Converts the raw video format.
- ``x265enc``: Encodes video into H.265.
- ``bitrate=3000``: Requests a target bitrate of approximately 3000 kbit/s.
- ``h265parse``: Parses the encoded H.265 bitstream.
- ``mp4mux``: Packages the stream into an MP4 container.
- ``filesink``: Saves the output.

The selected bitrate is an example. It does not guarantee that H.265 will always produce the same quality as H.264 at a lower bitrate.

Inspect the H.265 File
----------------------

Run:

.. code-block:: text

    ffprobe -v error \
    -select_streams v:0 \
    -show_entries stream=codec_name,width,height,r_frame_rate,bit_rate \
    -of default=noprint_wrappers=1 \
    output_h265.mp4

Check that the video stream is identified as HEVC.

Compare Output Files
--------------------

Run:

.. code-block:: text

    ls -lh output_h264.mp4 output_h265.mp4

File size can provide a basic comparison, but it does not independently measure visual quality.

For a meaningful comparison, use the same source video, resolution, frame rate, and a defined quality target.

Video Decoding Using GStreamer
==============================

Decoding converts a compressed video stream into raw video frames.

Decode H.264 Video
------------------

Run:

.. code-block:: text

    gst-launch-1.0 -v \
    filesrc location=output_h264.mp4 ! \
    qtdemux ! \
    h264parse ! \
    avdec_h264 ! \
    videoconvert ! \
    autovideosink

Explanation:

- ``filesrc``: Reads the MP4 file.
- ``qtdemux``: Extracts the video stream from the MP4 container.
- ``h264parse``: Parses H.264 data.
- ``avdec_h264``: Decodes the H.264 bitstream using the GStreamer libav plugin.
- ``videoconvert``: Converts the decoded frames into a suitable display format.
- ``autovideosink``: Selects an available video output sink.

The system must have a suitable graphical display or video output environment.

Decode H.265 Video
------------------

Run:

.. code-block:: text

    gst-launch-1.0 -v \
    filesrc location=output_h265.mp4 ! \
    qtdemux ! \
    h265parse ! \
    avdec_h265 ! \
    videoconvert ! \
    autovideosink

This pipeline extracts and decodes the H.265 stream and displays the resulting frames.

Decode Without Display
----------------------

For a headless embedded system, video can be decoded without opening a graphical window.

For example:

.. code-block:: text

    gst-launch-1.0 -v \
    filesrc location=output_h264.mp4 ! \
    qtdemux ! \
    h264parse ! \
    avdec_h264 ! \
    fakesink

This is useful for checking whether the decoder can process the stream.

A successful pipeline indicates that decoding completed, but it does not verify display output or image quality.

Encoding and Decoding Using FFmpeg
==================================

FFmpeg provides convenient commands for video conversion and codec validation.

Encode H.264
------------

Run:

.. code-block:: text

    ffmpeg -i input.mp4 \
    -c:v libx264 \
    -preset veryfast \
    -crf 23 \
    -pix_fmt yuv420p \
    output_h264.mp4

Explanation:

- ``-i input.mp4``: Specifies the input video.
- ``-c:v libx264``: Selects the H.264 software encoder.
- ``-preset veryfast``: Selects the encoding-speed preset.
- ``-crf 23``: Selects a constant-quality encoding value.
- ``-pix_fmt yuv420p``: Requests 8-bit YUV 4:2:0 pixel format.
- ``output_h264.mp4``: Specifies the output file.

The CRF value is an example. Lower CRF values generally produce higher quality and larger files with the x264 encoder.

Encode H.265
------------

Run:

.. code-block:: text

    ffmpeg -i input.mp4 \
    -c:v libx265 \
    -preset fast \
    -crf 28 \
    -pix_fmt yuv420p \
    output_h265.mp4

Explanation:

- ``-c:v libx265``: Selects the H.265 software encoder.
- ``-preset fast``: Selects an encoding-speed preset.
- ``-crf 28``: Selects the constant-quality setting.
- ``-pix_fmt yuv420p``: Requests 8-bit YUV 4:2:0 output.

The CRF values for x264 and x265 are not directly equivalent. A fair comparison requires quality evaluation rather than simply matching CRF numbers.

Decode H.264 to Raw Video
-------------------------

Run:

.. code-block:: text

    ffmpeg -i output_h264.mp4 \
    -an \
    -f null -

This decodes the video and discards the decoded output.

Decode H.265 to Raw Video
-------------------------

Run:

.. code-block:: text

    ffmpeg -i output_h265.mp4 \
    -an \
    -f null -

This provides a basic decoding test without saving another video file.

Real-Time Camera Encoding
=========================

A camera application can capture raw frames and pass them directly to a video encoder.

A typical pipeline is:

.. code-block:: text

              Camera Sensor
                    |
                    v
              Linux V4L2
                    |
                    v
              Raw Video Frames
                    |
                    v
              Video Converter
                    |
                    v
              H.264 / H.265
                 Encoder
                    |
                    v
              Compressed Video
                    |
              +-----+-----+
              |           |
              v           v
           Storage     Network

H.264 Encoding from a V4L2 Camera
---------------------------------

The following is an example for a camera that supports 1280 × 720 YUYV at 30 FPS and an available ``x264enc`` software encoder:

.. code-block:: text

    gst-launch-1.0 -e \
    v4l2src device=/dev/video0 ! \
    video/x-raw,format=YUY2,width=1280,height=720,framerate=30/1 ! \
    videoconvert ! \
    x264enc bitrate=4000 speed-preset=ultrafast ! \
    h264parse ! \
    mp4mux ! \
    filesink location=camera_h264.mp4

The pipeline reads frames from the V4L2 device and encodes them into an H.264 MP4 file.

The camera must support the requested format and resolution. GStreamer uses ``YUY2`` as its raw-video format name for the YUYV byte layout.

The pipeline runs until it is stopped. Use an orderly termination so the MP4 container can be finalized.

H.265 Encoding from a V4L2 Camera
---------------------------------

If the camera supports the selected raw format and the H.265 encoder is installed:

.. code-block:: text

    gst-launch-1.0 -e \
    v4l2src device=/dev/video0 ! \
    video/x-raw,format=YUY2,width=1280,height=720,framerate=30/1 ! \
    videoconvert ! \
    x265enc bitrate=3000 ! \
    h265parse ! \
    mp4mux ! \
    filesink location=camera_h265.mp4

This example uses software H.265 encoding.

On a constrained embedded processor, software encoding may not achieve the required frame rate. Hardware acceleration should be evaluated where available.

Video Streaming Over an IP Network
==================================

Video streaming transfers encoded video data from one device to another over a network.

The sender captures and encodes the video. The receiver obtains the compressed data, decodes it, and displays the video.

Common streaming technologies include:

- RTP over UDP.
- RTP over TCP.
- RTSP.
- HTTP-based video delivery.
- WebRTC.

The choice depends on latency, reliability, interoperability, and application requirements.

RTP and UDP
-----------

RTP (Real-time Transport Protocol) is commonly used to carry real-time audio and video.

UDP is often used with RTP because it avoids TCP retransmission delays.

However, UDP does not guarantee delivery. Packet loss can affect the decoded video.

RTP provides sequence numbers and timestamps that help receivers handle packet ordering and timing.

H.264 RTP Streaming Architecture
--------------------------------

.. code-block:: text

                  SENDER
            +------------------+
            | Camera / Source  |
            +------------------+
                     |
                     v
              Raw Video Frames
                     |
                     v
               H.264 Encoder
                     |
                     v
                H.264 Parser
                     |
                     v
              RTP Packetization
                     |
                     v
                 UDP Socket
                     |
                     v
                 IP Network
                     |
                     v
                  RECEIVER
                     |
                     v
               UDP Reception
                     |
                     v
              RTP Depacketization
                     |
                     v
                H.264 Parser
                     |
                     v
               H.264 Decoder
                     |
                     v
               Video Display

H.264 Streaming Using GStreamer
===============================

The following example demonstrates basic H.264 streaming between two Linux systems on the same network.

Assumptions:

- Sender IP address: ``192.168.1.10``.
- Receiver IP address: ``192.168.1.20``.
- UDP port: ``5000``.
- Resolution: 1280 × 720.
- Frame rate: 30 FPS.

Replace the IP addresses with the actual addresses of the systems.

Sender Command
--------------

Run on the sender:

.. code-block:: text

    gst-launch-1.0 -v \
    videotestsrc is-live=true ! \
    video/x-raw,width=1280,height=720,framerate=30/1 ! \
    videoconvert ! \
    x264enc tune=zerolatency speed-preset=ultrafast bitrate=2000 key-int-max=30 ! \
    h264parse ! \
    rtph264pay pt=96 config-interval=1 ! \
    udpsink host=192.168.1.20 port=5000

Explanation:

- ``videotestsrc is-live=true``: Generates a live test stream.
- ``videoconvert``: Converts the raw video format.
- ``x264enc``: Encodes the video into H.264.
- ``tune=zerolatency``: Selects a low-latency tuning mode.
- ``speed-preset=ultrafast``: Prioritizes encoding speed.
- ``bitrate=2000``: Requests approximately 2000 kbit/s.
- ``key-int-max=30``: Sets the maximum keyframe interval in frames.
- ``h264parse``: Parses the encoded stream.
- ``rtph264pay``: Packetizes H.264 data into RTP packets.
- ``config-interval=1``: Sends codec configuration information periodically.
- ``udpsink``: Sends the packets to the receiver.

Receiver Command
----------------

Run on the receiver:

.. code-block:: text

    gst-launch-1.0 -v \
    udpsrc port=5000 \
    caps="application/x-rtp,media=video,encoding-name=H264,payload=96,clock-rate=90000" ! \
    rtpjitterbuffer latency=100 ! \
    rtph264depay ! \
    h264parse ! \
    avdec_h264 ! \
    videoconvert ! \
    autovideosink

Explanation:

- ``udpsrc``: Receives UDP packets.
- RTP caps: Describe the incoming H.264 RTP stream.
- ``rtpjitterbuffer``: Handles packet arrival timing and reordering within its configured buffering limits.
- ``rtph264depay``: Extracts H.264 data from RTP packets.
- ``h264parse``: Parses the H.264 stream.
- ``avdec_h264``: Decodes the video.
- ``videoconvert``: Converts the decoded format.
- ``autovideosink``: Displays the video.

Both systems must have the necessary GStreamer plugins installed.

The receiver must be running before or while the sender starts transmitting.

This is a basic demonstration, not a production-ready streaming configuration. It does not provide authentication or encryption.

H.265 Streaming Using GStreamer
===============================

H.265 can also be transmitted using RTP.

The RTP payload format for H.265 is defined by RFC 7798.

Sender Command
--------------

Run on the sender:

.. code-block:: text

    gst-launch-1.0 -v \
    videotestsrc is-live=true ! \
    video/x-raw,width=1280,height=720,framerate=30/1 ! \
    videoconvert ! \
    x265enc bitrate=2000 ! \
    h265parse ! \
    rtph265pay pt=96 ! \
    udpsink host=192.168.1.20 port=5000

This generates test video, encodes it into H.265, packetizes the stream using RTP, and transmits it over UDP.

Receiver Command
----------------

Run on the receiver:

.. code-block:: text

    gst-launch-1.0 -v \
    udpsrc port=5000 \
    caps="application/x-rtp,media=video,encoding-name=H265,payload=96,clock-rate=90000" ! \
    rtpjitterbuffer latency=100 ! \
    rtph265depay ! \
    h265parse ! \
    avdec_h265 ! \
    videoconvert ! \
    autovideosink

The receiver depacketizes and decodes the incoming H.265 stream.

The sender and receiver must agree on the codec, RTP payload type, and stream configuration.

Some systems require additional parameter-set handling or pipeline configuration. Validate the stream with the installed GStreamer version and target decoder.

Hardware Codec Integration on Embedded Linux
============================================

Many embedded processors include dedicated hardware for video encoding and decoding.

The codec hardware may be integrated into the multimedia subsystem or implemented as a separate processing engine.

A typical embedded video architecture is:

.. code-block:: text

               Camera / Video Input
                        |
                        v
                   V4L2 Source
                        |
                        v
                  Raw Video Data
                        |
                        v
                 Hardware Encoder
                   (If Supported)
                        |
                        v
                  H.264 / H.265
                    Bitstream
                        |
                   +----+----+
                   |         |
                   v         v
                Storage   Network

Hardware Encoder
----------------

A hardware encoder receives raw video frames and generates a compressed bitstream.

The application interacts with it through a driver or multimedia framework.

Possible Linux interfaces include:

- V4L2 memory-to-memory encoder interface.
- Platform-specific codec APIs.
- GStreamer hardware encoder plugins.
- Vendor multimedia libraries.

Hardware Decoder
----------------

A hardware decoder receives compressed H.264/H.265 data and generates decoded frames.

The output may be stored in system memory or in hardware-accessible buffers.

Applications may use DMA-BUF or other supported buffer-sharing mechanisms to reduce copying between components.

Verify Hardware Codec Support
-----------------------------

Do not assume that every embedded processor supports both H.264 and H.265 encoding and decoding.

Check:

1. Processor datasheet.
2. Multimedia subsystem documentation.
3. Linux kernel driver documentation.
4. Vendor SDK documentation.
5. Installed GStreamer elements.
6. FFmpeg hardware acceleration support.

For GStreamer, list available encoder and decoder elements:

.. code-block:: text

    gst-inspect-1.0 | grep -Ei '264|265|hevc|h264'

Inspect a candidate element:

.. code-block:: text

    gst-inspect-1.0 ELEMENT_NAME

Replace ``ELEMENT_NAME`` with the actual element discovered on the target system.

For example, a platform may expose a V4L2-based hardware encoder, but its element name and supported controls are implementation-dependent.

Software and Hardware Performance Testing
-----------------------------------------

Compare software and hardware implementations using the same:

- Input video.
- Resolution.
- Frame rate.
- Codec.
- Quality target.
- Test duration.

Measure:

- CPU utilization.
- Memory usage.
- Power consumption, where measurable.
- Encoding or decoding frame rate.
- End-to-end latency.
- Output bitrate.
- Image quality.

Hardware acceleration should be confirmed through driver and pipeline information rather than inferred only from successful video playback.

Video Container and Bitstream Formats
=====================================

A video codec and a video container are different concepts.

A codec defines how the video is compressed. A container stores one or more encoded streams and related metadata.

H.264 and H.265 Bitstreams
--------------------------

H.264 and H.265 encoded data can be represented in different stream formats.

For example:

- Annex B byte-stream format.
- Length-prefixed formats used in certain containers.

The required format depends on the application and transport.

MP4 Container
-------------

MP4 is a container format commonly used for storing encoded video and audio.

It can contain H.264 or H.265 video, provided the application supports the selected codec and container configuration.

MKV Container
-------------

Matroska (MKV) is another container format that supports multiple video and audio codecs.

Container Comparison
--------------------

ContainerDescriptionTypical UseMP4Widely supported multimedia containerVideo storage and playbackMKVFlexible multimedia containerGeneral multimedia storageMPEG-TSTransport stream containerBroadcasting and some streaming applicationsRaw H.264H.264 elementary streamCodec testing and transportRaw H.265H.265 elementary streamCodec testing and transportThe selected container should be compatible with the intended playback and streaming software.

Performance and Latency Considerations
======================================

Video encoding and decoding performance depend on the complete multimedia pipeline.

CPU Utilization
---------------

Software encoding and decoding can consume significant CPU resources.

High CPU usage may affect other applications running on the embedded system.

Hardware acceleration can reduce this load when the codec engine is supported and correctly integrated.

Memory Bandwidth
----------------

Raw video frames require significant memory bandwidth.

Higher resolutions and frame rates increase the amount of data transferred between the camera, processor, encoder, decoder, and display.

Buffer allocation and unnecessary frame copies can affect performance.

Encoding Latency
----------------

Encoding latency is the time required to convert raw frames into compressed data.

It can be affected by:

- Encoder preset.
- B-frame configuration.
- Rate control.
- Lookahead.
- Frame buffering.
- Processing resources.

Low-latency applications may use settings that reduce buffering and disable features that introduce additional delay.

Network Latency
---------------

Network latency depends on:

- Encoding delay.
- Packetization.
- Network transmission.
- Jitter buffering.
- Packet loss.
- Decoding delay.
- Display synchronization.

A low-latency system must optimize the complete pipeline rather than only the encoder.

Packet Loss
-----------

UDP-based streaming does not guarantee delivery of every packet.

Packet loss can damage portions of the compressed stream, especially when lost data is required to reconstruct later frames.

Recovery mechanisms can include:

- Periodic keyframes.
- Requesting a new keyframe.
- Forward error correction.
- Appropriate buffering.
- Reliable network design.

The exact recovery strategy depends on the streaming protocol and application.

Troubleshooting
===============

The following table describes common problems encountered during H.264/H.265 encoding, decoding, and streaming.

ProblemPossible CauseRecommended Action``x264enc`` not foundRequired GStreamer plugin is missingCheck the installed GStreamer plugins and install the required package``x265enc`` not foundH.265 encoder plugin is missingCheck the GStreamer build and plugin availability``avdec_h264`` not foundGStreamer libav decoder plugin is missingInstall or enable the appropriate libav plugin``avdec_h265`` not foundH.265 decoder support is unavailableCheck the installed decoder pluginsUnsupported formatInput pixel format is not accepted by the encoderUse a supported format and ``videoconvert`` where appropriateEncoder fails to initializeUnsupported resolution, format, or encoder configurationInspect encoder properties and input capsDecoder cannot play the fileUnsupported codec profile, bit depth, or malformed streamInspect the stream using ``ffprobe`` and verify decoder supportOutput file is empty or incompletePipeline stopped before the container was finalizedStop the pipeline cleanly and check the output againHigh CPU utilizationSoftware codec processing is demandingReduce resolution or frame rate, or evaluate hardware accelerationVideo is delayedExcessive buffering or encoding latencyReview encoder settings, jitter buffer, and pipeline queuesVideo is freezingNetwork packet loss, insufficient bandwidth, or decoder overloadCheck network statistics and decoder performanceNo video at receiverIncorrect destination IP, port, RTP caps, or codecVerify sender and receiver configurationVideo has artifactsPacket loss, corrupted bitstream, or decoding issuesInspect network conditions and encoder/decoder logsAudio and video are not synchronizedTimestamp or synchronization problemCheck the media pipeline and stream timestampsHardware encoder unavailableDriver, plugin, or codec hardware is missingCheck processor capabilities and platform multimedia documentation

Inspect Video Information
-------------------------

Use FFprobe:

.. code-block:: text

    ffprobe -hide_banner output_h264.mp4

This displays information about the video streams, codec, resolution, frame rate, and container.

Check GStreamer Element Availability
------------------------------------

Run:

.. code-block:: text

    gst-inspect-1.0 x264enc
    gst-inspect-1.0 x265enc
    gst-inspect-1.0 avdec_h264
    gst-inspect-1.0 avdec_h265

This identifies whether the required elements are installed and available.

Enable GStreamer Debug Logs
---------------------------

Run:

.. code-block:: text

    GST_DEBUG=3 gst-launch-1.0 ...

Replace ``...`` with the pipeline being tested.

For more detailed logs:

.. code-block:: text

    GST_DEBUG=5 gst-launch-1.0 ...

Higher debug levels generate more output and may affect performance.

Check Network Connectivity
--------------------------

Check the receiver:

.. code-block:: text

    ip addr

Test connectivity from the sender:

.. code-block:: text

    ping 192.168.1.20

Check whether the receiving UDP port is active:

.. code-block:: text

    ss -lunp

UDP applications do not establish a TCP-style connection, so a successful ping alone does not prove that video packets are reaching the receiver.

Practical Validation Procedure
==============================

The following sequence can be used to validate H.264/H.265 support on a Linux system.

Step 1: Check Installed Tools
-----------------------------

.. code-block:: text

    gst-launch-1.0 --version
    ffmpeg -version

Step 2: Check H.264 Encoder Availability
----------------------------------------

.. code-block:: text

    gst-inspect-1.0 x264enc

Expected result: GStreamer displays the H.264 encoder element information.

Step 3: Check H.265 Encoder Availability
----------------------------------------

.. code-block:: text

    gst-inspect-1.0 x265enc

Expected result: GStreamer displays the H.265 encoder element information if the required plugin is available.

Step 4: Generate H.264 Output
-----------------------------

Run the H.264 test pipeline described in Section 15.

Expected result: An H.264 MP4 file is created.

Step 5: Generate H.265 Output
-----------------------------

Run the H.265 test pipeline described in Section 16.

Expected result: An H.265 MP4 file is created.

Step 6: Verify the Encoded Files
--------------------------------

.. code-block:: text

    ffprobe output_h264.mp4
    ffprobe output_h265.mp4

Expected result: The video codec, resolution, and frame rate are displayed.

Step 7: Test H.264 Decoding
---------------------------

Run the H.264 decoding pipeline described in Section 17.

Expected result: The video is decoded successfully.

Step 8: Test H.265 Decoding
---------------------------

Run the H.265 decoding pipeline described in Section 17.

Expected result: The video is decoded successfully.

Step 9: Test Network Streaming
------------------------------

Run the H.264 or H.265 sender and receiver pipelines from Sections 21 and 22 on two systems.

Expected result: The receiver displays the incoming test video.

Step 10: Evaluate Performance
-----------------------------

Record the following information:

- Codec used.
- Resolution.
- Frame rate.
- Target bitrate.
- Actual output bitrate.
- CPU utilization.
- Memory usage.
- Streaming latency.
- Playback stability.

The final test results should be compared against the application's requirements.

Security and Deployment Considerations
======================================

Video streaming applications may transmit sensitive image information.

A production deployment should consider the following points.

Network Security
----------------

Basic RTP/UDP streaming does not automatically provide encryption or authentication.

For sensitive video applications, use an appropriate secure transport architecture, such as:

- SRTP with suitable key management.
- Secure RTSP configurations.
- WebRTC with its security mechanisms.
- Encrypted network tunnels where appropriate.

Access Control
--------------

Restrict access to camera devices, video files, and streaming services.

Only authorized applications and users should be able to capture or access sensitive video data.

Resource Management
-------------------

Video applications should manage:

- Encoder and decoder buffers.
- Memory allocation.
- CPU usage.
- Network bandwidth.
- Storage capacity.
- Application shutdown.

Error Handling
--------------

Applications should detect:

- Encoder initialization failures.
- Decoder errors.
- Camera disconnections.
- Network interruptions.
- Incomplete streams.
- Buffer allocation failures.

A production application should recover gracefully where possible.

Codec and Patent Licensing
--------------------------

H.264 and H.265 are standardized technologies with associated patent and licensing considerations.

For commercial products, the software libraries, codec implementations, and intended distribution or usage model should be reviewed for applicable licensing requirements.

Conclusion
==========

H.264 and H.265 are important video compression standards used in modern multimedia and embedded applications.

H.264 provides broad compatibility and is widely used in video recording, surveillance, and streaming applications. H.265 provides improved compression tools and can reduce bitrate requirements for comparable visual quality under suitable conditions.

Video encoding converts raw frames into compressed data, while decoding reconstructs the frames for display or further processing.

In Linux-based systems, multimedia frameworks such as GStreamer and FFmpeg provide practical interfaces for encoding, decoding, storing, and streaming video.

Embedded processors may also provide dedicated hardware codec engines that improve performance and reduce CPU utilization. Their availability and supported features must be verified using processor documentation, drivers, and multimedia software.

A reliable video application should validate codec support, input formats, resolution, frame rate, bitrate, encoder and decoder performance, network behavior, and output quality.

Following a structured testing process helps developers identify multimedia issues early and build stable video recording and streaming applications.

References
==========

The following official standards and technical documentation provide additional information about H.264/H.265 encoding, decoding, multimedia frameworks, and Linux video integration.

International Video Coding Standards
------------------------------------

**1. ITU-T H.264 – Advanced Video Coding for Generic Audiovisual Services**

International Telecommunication Union (ITU-T).

Defines the H.264/AVC video coding standard, including coding tools, profiles, levels, and bitstream structure.

`https://www.itu.int/ITU-T/recommendations/rec.aspx?rec=H.264 <https://www.itu.int/ITU-T/recommendations/rec.aspx?rec=H.264>`_

**2. ITU-T H.265 – High Efficiency Video Coding**

International Telecommunication Union (ITU-T).

Defines the H.265/HEVC video coding standard and its compression tools, coding structures, and bitstream requirements.

`https://www.itu.int/ITU-T/recommendations/rec.aspx?rec=H.265 <https://www.itu.int/ITU-T/recommendations/rec.aspx?rec=H.265>`_

GStreamer Documentation
-----------------------

**3. GStreamer Official Documentation**

GStreamer Project.

Provides information about multimedia pipelines, elements, encoding, decoding, and streaming.

`https://gstreamer.freedesktop.org/documentation/ <https://gstreamer.freedesktop.org/documentation/>`_

**4. GStreamer H.264 Encoder – x264enc**

Documents the software H.264 encoder, its supported input formats, bitrate configuration, and encoding properties.

`https://gstreamer.freedesktop.org/documentation/x264/index.html <https://gstreamer.freedesktop.org/documentation/x264/index.html>`_

**5. GStreamer H.265 Encoder – x265enc**

Documents the software H.265 encoder and its supported configuration options.

`https://gstreamer.freedesktop.org/documentation/x265/index.html <https://gstreamer.freedesktop.org/documentation/x265/index.html>`_

**6. GStreamer RTP H.264 Payloader**

Explains how H.264 video is packetized into RTP packets for network streaming.

`https://gstreamer.freedesktop.org/documentation/rtp/rtph264pay.html <https://gstreamer.freedesktop.org/documentation/rtp/rtph264pay.html>`_

**7. GStreamer RTP H.265 Payloader**

Explains how H.265 video is packetized into RTP packets.

`https://gstreamer.freedesktop.org/documentation/rtp/rtph265pay.html <https://gstreamer.freedesktop.org/documentation/rtp/rtph265pay.html>`_

**8. GStreamer Plugin Reference**

Provides a searchable reference for available encoders, decoders, parsers, muxers, and streaming elements.

`https://gstreamer.freedesktop.org/documentation/plugins_doc.html <https://gstreamer.freedesktop.org/documentation/plugins_doc.html>`_

FFmpeg Documentation
--------------------

**9. FFmpeg Official Documentation**

Provides information about video conversion, encoding, decoding, streaming, and multimedia processing.

`https://ffmpeg.org/documentation.html <https://ffmpeg.org/documentation.html>`_

**10. FFmpeg Codec Documentation**

Documents supported encoders, decoders, codec options, and encoding parameters.

`https://ffmpeg.org/ffmpeg-codecs.html <https://ffmpeg.org/ffmpeg-codecs.html>`_

**11. FFprobe Documentation**

Explains how to inspect multimedia files, video streams, codecs, and media properties.

`https://ffmpeg.org/ffprobe.html <https://ffmpeg.org/ffprobe.html>`_

Linux Kernel Documentation
--------------------------

**12. V4L2 Video Encoder Interface**

Linux Kernel Documentation.

Describes the Linux V4L2 memory-to-memory video encoder interface and its operation.

`https://docs.kernel.org/userspace-api/media/v4l/dev-encoder.html <https://docs.kernel.org/userspace-api/media/v4l/dev-encoder.html>`_

**13. V4L2 Video Decoder Interface**

Linux Kernel Documentation.

Describes the V4L2 memory-to-memory video decoder interface and its operation.

`https://docs.kernel.org/userspace-api/media/v4l/dev-decoder.html <https://docs.kernel.org/userspace-api/media/v4l/dev-decoder.html>`_

**14. Video4Linux2 API Documentation**

Linux Kernel Documentation.

Provides information about the V4L2 userspace API, video device capabilities, and video processing interfaces.

`https://docs.kernel.org/userspace-api/media/v4l/v4l2.html <https://docs.kernel.org/userspace-api/media/v4l/v4l2.html>`_

Network Streaming Standards
---------------------------

**15. RFC 3984 – RTP Payload Format for H.264 Video**

Internet Engineering Task Force (IETF).

Defines the RTP payload format used for H.264 video transmission.

`https://www.rfc-editor.org/rfc/rfc3984 <https://www.rfc-editor.org/rfc/rfc3984>`_

**16. RFC 7798 – RTP Payload Format for High Efficiency Video Coding (HEVC)**

Internet Engineering Task Force (IETF).

Defines the RTP payload format used for H.265/HEVC video transmission.

`https://www.rfc-editor.org/rfc/rfc7798 <https://www.rfc-editor.org/rfc/rfc7798>`_

**17. RFC 3550 – RTP: A Transport Protocol for Real-Time Applications**

Internet Engineering Task Force (IETF).

Defines the Real-time Transport Protocol and its use in multimedia communication.

`https://www.rfc-editor.org/rfc/rfc3550 <https://www.rfc-editor.org/rfc/rfc3550>`_

Additional Embedded Multimedia References
-----------------------------------------

**18. Linux Media Subsystem Documentation**

Linux Kernel Documentation.

Provides information about video devices, media pipelines, and userspace multimedia interfaces.

`https://docs.kernel.org/userspace-api/media/index.html <https://docs.kernel.org/userspace-api/media/index.html>`_

**NXP i.MX Software and Development Tools**

NXP Semiconductors.

Provides processor-specific software resources and documentation for supported i.MX multimedia platforms.

`https://www.nxp.com/design/design-center/software/embedded-software/i-mx-software-and-development-tools:IMX-SW <https://www.nxp.com/design/design-center/software/embedded-software/i-mx-software-and-development-tools:IMX-SW>`_

**NVIDIA Video Codec SDK Documentation**

NVIDIA.

Provides information about hardware-accelerated video encoding and decoding on supported NVIDIA platforms.

`https://developer.nvidia.com/video-codec-sdk <https://developer.nvidia.com/video-codec-sdk>`_

Reference Usage Note
--------------------

The ITU-T recommendations should be treated as the primary references for the H.264 and H.265 coding standards.

GStreamer and FFmpeg documentation should be used for application-level encoding, decoding, and streaming implementation.

Linux kernel documentation describes the standard V4L2 interfaces used by supported video codec drivers.

For hardware acceleration, always refer to the target processor's datasheet, multimedia SDK, codec driver documentation, and supported GStreamer or FFmpeg implementation.
