#!/usr/bin/env python3
"""
SynToMid + FL Studio to unified JSON MIDI converter.
Converts YouTube Synthesia videos and FL Studio piano roll exports to DAW-agnostic JSON.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Note:
    """MIDI note in unified format."""
    start: float
    duration: float
    pitch: int
    velocity: float
    channel: int = 0
    channel_name: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if not d["channel_name"]:
            del d["channel_name"]
        return d


@dataclass
class NoteCollection:
    """Unified note collection matching SCHEMA.md."""
    version: str = "1.0"
    source: str = "manual"
    metadata: Dict[str, Any] = None
    notes: List[Note] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {
                "title": "",
                "bpm": 120,
                "time_signature": "4/4",
                "duration_seconds": 0.0
            }
        if self.notes is None:
            self.notes = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "source": self.source,
            "metadata": self.metadata,
            "notes": [n.to_dict() for n in self.notes]
        }

    def save(self, path: Path) -> None:
        """Save to JSON file."""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"Saved {len(self.notes)} notes to {path}")

    @classmethod
    def load(cls, path: Path) -> 'NoteCollection':
        """Load from JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        collection = cls(
            version=data.get("version", "1.0"),
            source=data.get("source", "manual"),
            metadata=data.get("metadata", {})
        )
        
        for note_data in data.get("notes", []):
            collection.notes.append(Note(**note_data))
        
        return collection


class SynToMidConverter:
    """Convert SynToMid (piano video) MIDI to unified JSON."""
    
    @staticmethod
    def from_midi_file(midi_path: Path, metadata: Dict[str, Any] = None) -> NoteCollection:
        """Convert MIDI file (from SynToMid) to unified JSON."""
        try:
            import mido
        except ImportError:
            print("Error: mido library required for MIDI conversion")
            print("Install: pip install mido")
            return None
        
        collection = NoteCollection(
            source="syntomid",
            metadata=metadata or {"title": midi_path.stem, "bpm": 120}
        )
        
        mid = mido.MidiFile(str(midi_path))
        
        # Extract notes from all tracks
        for track in mid.tracks:
            current_time = 0.0
            tempo = 500000  # Default microseconds per beat
            
            for msg in track:
                current_time += msg.time
                
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                elif msg.type == 'note_on' and msg.velocity > 0:
                    # Find corresponding note_off
                    duration = 0.0
                    # Simplified: just use a default duration
                    duration = 0.25
                    
                    time_seconds = current_time * (tempo / 1_000_000) / mid.ticks_per_beat
                    velocity_norm = msg.velocity / 127.0
                    
                    note = Note(
                        start=time_seconds,
                        duration=duration,
                        pitch=msg.note,
                        velocity=velocity_norm,
                        channel=msg.channel
                    )
                    collection.notes.append(note)
        
        # Sort by start time
        collection.notes.sort(key=lambda n: n.start)
        return collection


class FLStudioConverter:
    """Convert FL Studio piano roll exports to unified JSON."""
    
    @staticmethod
    def from_json(json_path: Path) -> NoteCollection:
        """Convert FL Studio exported JSON piano roll to unified format."""
        with open(json_path, 'r') as f:
            fl_data = json.load(f)
        
        collection = NoteCollection(
            source="fl_studio",
            metadata={
                "title": json_path.stem,
                "bpm": fl_data.get("bpm", 120),
                "time_signature": fl_data.get("time_signature", "4/4"),
                "duration_seconds": fl_data.get("duration_seconds", 0.0)
            }
        )
        
        for note_data in fl_data.get("notes", []):
            note = Note(
                start=note_data["start"],
                duration=note_data["duration"],
                pitch=note_data["pitch"],
                velocity=note_data["velocity"],
                channel=note_data.get("channel", 0),
                channel_name=note_data.get("channel_name", "")
            )
            collection.notes.append(note)
        
        return collection


def main():
    parser = argparse.ArgumentParser(
        description="Convert SynToMid/FL Studio MIDI to unified JSON format"
    )
    
    parser.add_argument(
        "input",
        help="Input file (MIDI or JSON)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output JSON file (default: input_name.json)"
    )
    parser.add_argument(
        "-s", "--source",
        choices=["syntomid", "fl_studio", "auto"],
        default="auto",
        help="Source format (auto-detect from extension)"
    )
    parser.add_argument(
        "--title",
        help="Set metadata title"
    )
    parser.add_argument(
        "--bpm",
        type=int,
        default=120,
        help="Set BPM metadata"
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1
    
    # Auto-detect source
    source = args.source
    if source == "auto":
        if input_path.suffix.lower() == ".mid":
            source = "syntomid"
        elif input_path.suffix.lower() == ".json":
            source = "fl_studio"
        else:
            print(f"Error: Cannot auto-detect format for {input_path.suffix}")
            return 1
    
    # Convert
    if source == "syntomid":
        collection = SynToMidConverter.from_midi_file(
            input_path,
            metadata={
                "title": args.title or input_path.stem,
                "bpm": args.bpm
            }
        )
    elif source == "fl_studio":
        collection = FLStudioConverter.from_json(input_path)
    
    if collection is None:
        return 1
    
    # Save output
    output_path = Path(args.output or f"{input_path.stem}.json")
    collection.save(output_path)
    
    print(f"\nConversion complete:")
    print(f"  Source: {source}")
    print(f"  Notes: {len(collection.notes)}")
    print(f"  Output: {output_path}")
    
    return 0


if __name__ == "__main__":
    exit(main())
