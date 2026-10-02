from autotwin.core.enums import ObjectType
from autotwin.core.models import DetectedObject, SensorFrame
from autotwin.perception.fusion import SensorFusion

def test_sensor_fusion_combines_same_object():
    frames = [
        SensorFrame(1.0, "radar", [
            DetectedObject("car", ObjectType.VEHICLE, 20, -5, 0.1, 0.9, "radar")
        ]),
        SensorFrame(1.0, "camera", [
            DetectedObject("car", ObjectType.VEHICLE, 22, -4.5, 0.2, 0.8, "camera")
        ])
    ]
    fused = SensorFusion().fuse(frames)
    assert len(fused) == 1
    assert set(fused[0].sources) == {"radar", "camera"}
    assert 20 <= fused[0].distance_m <= 22
