import json

from fastapi import APIRouter

from app.schemas.sche_base import DataResponse, ResponseSchemaBase
from app.schemas.sche_player import GameResp, GameStatusResp, GameActionsResp, GameActionsReq

router = APIRouter()

action_lists = []
current_turn = 0
count_post_request = 0


@router.get('/{game_id}')
def get_detail_game(game_id: int):
    raw_data = open("mock/map_mock.json")
    response: dict = json.load(raw_data)
    game_resp = GameResp(**response)
    return DataResponse().data_response(game_resp)


@router.get('/{game_id}/status')
def get_game_status(game_id: int):
    global current_turn
    current_turn += 1
    response = {
        "cur_turn": current_turn,
        "max_turn": 100,
        "remaining": 10
    }
    return DataResponse().data_response(GameStatusResp(**response))


@router.get('/{game_id}/actions')
def get_game_actions(game_id: int):
    global action_lists
    list_resp = []
    if type(action_lists) is list:
        for actions in action_lists:
            list_resp.append(GameActionsResp(**actions))
    return DataResponse().data_response(list_resp)


@router.post('/{game_id}/actions')
def get_game_actions(game_id: int, game_actions_req: GameActionsReq):
    data = game_actions_req.dict()
    data["team_id"] = 1
    global action_lists
    action_lists.append(data)
    return ResponseSchemaBase().success_response()

