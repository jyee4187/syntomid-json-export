# Unified Note JSON Schema

## Overview
Portable MIDI representation format for converting between SynToMid (YouTube Synthesia videos), FL Studio piano roll exports, and DAW-agnostic generative audio engines.

## Root Structure

```json
{
  "version": "1.0",
  "source": "syntomid" | "fl_studio" | "manual",
  "metadata": {
    "title": "string (optional)",
    "bpm": 120,
    "time_signature": "4/4",
    "duration_seconds": 60.0
  },
  "notes": []
}
```

## Note Object

Each note in the `notes` array:

```json
{
  "start": 0.0,           // float: time in seconds from song start
  "duration": 0.5,        // float: length in seconds
  "pitch": 60,            // int: MIDI note number (0-127, 60=middle C)
  "velocity": 0.8,        // float: 0.0-1.0, normalized velocity
  "channel": 0,           // int: MIDI channel (0-15)
  "channel_name": "Piano" // string: optional semantic label
}
```

## Field Details

### `start` (required)
- Time in seconds when note begins
- Must be >= 0
- Sorted ascending in array

### `duration` (required)
- Length in seconds
- Must be > 0

### `pitch` (required)
- MIDI note number
- 60 = middle C (C4)
- 0 = C-1, 127 = G9

### `velocity` (required)
- Normalized to 0.0-1.0 range
- Will be converted to MIDI 0-127 on export

### `channel` (optional, default 0)
- MIDI channel 0-15
- Useful for multi-track exports

### `channel_name` (optional)
- Human-readable track label
- "Piano", "Synth", "Bass", etc.

## Conversion Notes

### From SynToMid:
- Time extracted from waterfall video x-position
- Velocity estimated from pixel brightness/width
- All notes mapped to single channel unless multi-hand detection

### From FL Studio Piano Roll:
- Start/duration from FL time grid
- Pitch/velocity from FL note properties
- Channel from FL track assignment

## Example

```json
{
  "version": "1.0",
  "source": "fl_studio",
  "metadata": {
    "title": "Bach Prelude",
    "bpm": 120,
    "time_signature": "4/4",
    "duration_seconds": 30.0
  },
  "notes": [
    {
      "start": 0.0,
      "duration": 0.25,
      "pitch": 60,
      "velocity": 0.9,
      "channel": 0,
      "channel_name": "Piano"
    },
    {
      "start": 0.25,
      "duration": 0.25,
      "pitch": 64,
      "velocity": 0.85,
      "channel": 0,
      "channel_name": "Piano"
    }
  ]
}
```
