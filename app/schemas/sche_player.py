import json
from datetime import datetime
from enum import Enum
from typing import Optional, List, Union, Any

from pydantic import BaseModel, root_validator


class ActionType(str, Enum):
    STAY = "STAY"
    MOVE = "MOVE"
    BUILD = "BUILD"
    DESTROY = "DESTROY"


class MoveType(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UPPER_LEFT = "UPPER_LEFT"
    UPPER_RIGHT = "UPPER_RIGHT"
    LOWER_LEFT = "LOWER_LEFT"
    LOWER_RIGHT = "LOWER_RIGHT"


class BuildAndDestroyType(str, Enum):
    ABOVE = "ABOVE"
    BELOW = "BELOW"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class SideEnum(str, Enum):
    A = "A"
    B = "B"


class GameActionsReq(BaseModel):

    class ChildAction(BaseModel):
        action: Optional[ActionType]
        action_param: Optional[Union[MoveType, BuildAndDestroyType]]
        craftsman_id: Optional[str]

    turn: Optional[int]
    actions: Optional[List[ChildAction]]


class GameActionsResp(BaseModel):

    class ChildAction(BaseModel):
        action: Optional[ActionType]
        action_param: Optional[Union[MoveType, BuildAndDestroyType]]
        craftsman_id: Optional[str]
        id: Optional[int]
        action_id: Optional[int]

    turn: Optional[int]
    actions: Optional[List[ChildAction]]
    team_id: Optional[int]
    game_id: Optional[int]
    id: Optional[int]
    created_time: Optional[datetime]


class GameResp(BaseModel):

    class Side(BaseModel):
        side: Optional[SideEnum]
        team_name: Optional[str]
        team_id: Optional[int]
        game_id: Optional[int]
        id: Optional[int]

    class Field(BaseModel):

        class CastleResp(BaseModel):
            x: Optional[int]
            y: Optional[int]

        class CraftsMenResp(BaseModel):
            x: Optional[int]
            y: Optional[int]
            side: Optional[SideEnum]
            id: Optional[str]

        class PondResp(BaseModel):
            x: Optional[int]
            y: Optional[int]

        name: Optional[str]
        castle_coeff: Optional[int]
        wall_coeff: Optional[int]
        territory_coeff: Optional[int]
        id: Optional[int]
        width: Optional[int]
        height: Optional[int]
        ponds: Optional[Union[List[PondResp], str]]
        castles: Optional[Union[List[CastleResp], str]]
        craftsmen: Optional[Union[List[CraftsMenResp], str]]
        match_id: Optional[int]

        @root_validator(pre=True)
        def validate_data(cls, data: Any) -> Any:
            castles_str = str(data.get("castles"))
            castles_str = castles_str.replace("'", '"')
            data["castles"] = castles_str

            ponds_str = str(data.get("ponds"))
            ponds_str = ponds_str.replace("'", '"')
            data["ponds"] = ponds_str

            craftsmen_str = str(data.get("craftsmen"))
            craftsmen_str = craftsmen_str.replace("'", '"')
            data["craftsmen"] = craftsmen_str

            return data

    name: Optional[str]
    num_of_turns: Optional[int]
    time_per_turn: Optional[int]
    start_time: Optional[datetime]
    id: Optional[int]
    field_id: Optional[int]
    sides: Optional[List[Side]]
    field: Optional[Field]


class GameStatusResp(BaseModel):
    cur_turn: Optional[int]
    max_turn: Optional[int]
    remaining: Optional[int]


class GameActionsStatusResp(BaseModel):
    data: Optional[List[GameActionsResp]]
    status: Optional[GameStatusResp]
