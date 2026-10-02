from collections import defaultdict
from ..core.models import DetectedObject, FusedObject

class SensorFusion:
    """Simple deterministic association and confidence-weighted fusion."""

    def __init__(self, distance_gate_m=6.0):
        self.distance_gate_m = distance_gate_m

    def fuse(self, frames) -> list[FusedObject]:
        detections = [d for frame in frames for d in frame.objects]
        groups: dict[str, list[DetectedObject]] = defaultdict(list)

        for detection in detections:
            groups[detection.object_id].append(detection)

        fused = []
        for object_id, items in groups.items():
            total_weight = sum(max(i.confidence, 0.01) for i in items)
            distance = sum(i.distance_m * i.confidence for i in items) / total_weight
            relative_speed = sum(i.relative_speed_ms * i.confidence for i in items) / total_weight
            lateral = sum(i.lateral_offset_m * i.confidence for i in items) / total_weight
            confidence = min(
                0.99,
                sum(i.confidence for i in items) / max(1, len(items)) + 0.05 * (len(items)-1)
            )
            fused.append(FusedObject(
                object_id=object_id,
                object_type=items[0].object_type,
                distance_m=distance,
                relative_speed_ms=relative_speed,
                lateral_offset_m=lateral,
                confidence=confidence,
                sources=sorted({i.source for i in items}),
            ))
        return fused

    def lane_offset(self, frames):
        values = [f.lane_offset_m for f in frames if f.lane_offset_m is not None]
        return sum(values) / len(values) if values else None
