"""
Wood 2

Startegy:
1. Select the furthest type at the bottom (2, 1, 0) to scan other fishes while going down
2. Get every fish from that type
3. Once all fishes of that type are scanned, go validate to the surface
4. Repeat for all types
"""



from typing import List, NamedTuple, Dict

# Define the data structures as namedtuples
class Vector(NamedTuple):
    x: int
    y: int

dir2vec = {
    "TL" : Vector(-600,-600),
    "TR" : Vector(600,-600),
    "BL" : Vector(-600,600),
    "BR" : Vector(600,600)
}

class FishDetail(NamedTuple):
    color: int
    type: int

class Fish(NamedTuple):
    fish_id: int
    pos: Vector
    speed: Vector
    detail: FishDetail

class RadarBlip(NamedTuple):
    fish_id: int
    dir: str

class Drone(NamedTuple):
    drone_id: int
    pos: Vector
    dead: bool
    battery: int
    scans: List[int]

fish_details: Dict[int, FishDetail] = {}

def distance_between(pos1,pos2):
    return ((pos1.x - pos2.x)**2+(pos1.y - pos2.y)**2)**(1/2)



fish_count = int(input())
fish_types = set()
for _ in range(fish_count):
    fish_id, color, _type = map(int, input().split())
    fish_details[fish_id] = FishDetail(color, _type)
    fish_types.add(_type)
fish_types = list(fish_types)

go_up = False

# game loop
while True:
    my_scans: List[int] = []
    foe_scans: List[int] = []
    drone_by_id: Dict[int, Drone] = {}
    my_drones: List[Drone] = []
    foe_drones: List[Drone] = []
    visible_fish: List[Fish] = []
    my_radar_blips: Dict[int, List[RadarBlip]] = {}

    my_score = int(input())
    foe_score = int(input())

    my_scan_count = int(input())
    for _ in range(my_scan_count):
        fish_id = int(input())
        my_scans.append(fish_id)

    foe_scan_count = int(input())
    for _ in range(foe_scan_count):
        fish_id = int(input())
        foe_scans.append(fish_id)

    my_drone_count = int(input())
    for _ in range(my_drone_count):
        drone_id, drone_x, drone_y, dead, battery = map(int, input().split())
        pos = Vector(drone_x, drone_y)
        drone = Drone(drone_id, pos, dead == '1', battery, [])
        drone_by_id[drone_id] = drone
        my_drones.append(drone)
        my_radar_blips[drone_id] = []

    foe_drone_count = int(input())
    for _ in range(foe_drone_count):
        drone_id, drone_x, drone_y, dead, battery = map(int, input().split())
        pos = Vector(drone_x, drone_y)
        drone = Drone(drone_id, pos, dead == '1', battery, [])
        drone_by_id[drone_id] = drone
        foe_drones.append(drone)
    
    drone_scan_count = int(input())
    for _ in range(drone_scan_count):
        drone_id, fish_id = map(int, input().split())
        drone_by_id[drone_id].scans.append(fish_id)

    visible_fish_count = int(input())
    for _ in range(visible_fish_count):
        fish_id, fish_x, fish_y, fish_vx, fish_vy = map(int, input().split())
        pos = Vector(fish_x, fish_y)
        speed = Vector(fish_vx, fish_vy)
        visible_fish.append(Fish(fish_id, pos, speed, fish_details[fish_id]))

    my_radar_blip_count = int(input())
    for _ in range(my_radar_blip_count):
        drone_id, fish_id, dir = input().split()
        drone_id = int(drone_id)
        fish_id = int(fish_id)
        my_radar_blips[drone_id].append(RadarBlip(fish_id, dir))

    for drone in my_drones:
        x = drone.pos.x
        y = drone.pos.y
        
        closest = None
        target = None
        for blip in my_radar_blips[drone.drone_id]:
            detail = fish_details[blip.fish_id]
            if detail.type == fish_types[0] and blip.fish_id not in drone.scans and blip.fish_id not in my_scans:
                target = Vector(x + dir2vec[blip.dir].x, y + dir2vec[blip.dir].y)

        if target is None:
                go_up = True
        
        light = 1

        if go_up and y <= 500:
            go_up = False
            fish_types.pop(-1)
            print(f"WAIT 0")
        elif go_up:
            print(f"MOVE {x} 0 {light}")
        else:
            print(f"MOVE {target.x} {target.y} {light}")