from datetime import datetime
import json
from fastapi import APIRouter

from app.schemas.sche_base import DataResponse, ResponseSchemaBase
from app.schemas.sche_player import GameResp, GameStatusResp, GameActionsResp, GameActionsReq

router = APIRouter()

start_time = datetime.now()
interval = 2
action_lists = []
current_turn = 0
count_post_request = 0

def calculate_current_turn():
    gap = (datetime.now() - start_time).seconds
    turn = gap // interval
    return turn


@router.get('/{game_id}')
def get_detail_game(game_id: int):
    raw_data = open("app/mock/map_mock.json")
    response: dict = json.load(raw_data)
    game_resp = GameResp(**response)
    return DataResponse().data_response(game_resp)


@router.get('/{game_id}/status')
def get_game_status(game_id: int):
    turn = calculate_current_turn()
    response = {
        "cur_turn": turn,
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
def post_game_actions(game_id: int, game_actions_req: GameActionsReq):
    data = game_actions_req.dict()
    turn = calculate_current_turn()
    print("------------------------")
    print(data)
    print("turn: ", turn)
    print("------------------------")
    check = True
    global action_lists

    if data['turn'] - turn > 2 or data['turn'] - turn <= 0:
        print("request turn: ", data['turn'])
        print("server turn: ", turn)
        return ResponseSchemaBase().success_response()
    
    team = None
    if len(data['actions']) > 0:
        if data['actions'][0]['craftsman_id'][0] == '1':
            team = 1
        elif data['actions'][0]['craftsman_id'][0] == '2':
            team = 2    
    data['team_id'] = team

    if check:
        print("Correct. Action: ", data)
        action_lists.append(data)

    return ResponseSchemaBase().success_response()

