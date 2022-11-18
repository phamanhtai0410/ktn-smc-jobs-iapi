# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import os
import subprocess

from pydash import get

from logger import debug
from worker import worker
from bson import json_util
from enums.background_jobs import BackgroundJobsType
from web3 import Web3

_dict = os.getcwd()


@worker.task(name='worker.run_background_jobs', rate_limit='100/s')
def run_background_job(background_job):
    background_job = json_util.loads(background_job) if isinstance(background_job, str) else background_job
    _bg_id = get(background_job, '_id')
    debug(f"Start bg: {get(background_job, 'contract')} with event {get(background_job, 'events')}")

    debug(f"_dict {_dict}")
    _program = f'TASK_ID_{_bg_id}'
    _command = None

    _from_block = get(background_job, 'from_block')
    _contract = get(background_job, 'contract')
    _abi_path = get(background_job, 'abi_path')

    _contract = Web3.toChecksumAddress(_contract)
    if BackgroundJobsType.NFT == get(background_job, 'type'):
        debug("Run handle_logs NFT Transfer,TokenCreated")
        _command = f'python3 scripts/handle_logs.py contract={_contract} from_block={_from_block} abi_path={_dict}/{_abi_path} event=Transfer,TokenCreated handle_path=tasks handle_func=send_task_events event_type={BackgroundJobsType.NFT} extra_data=nft_type#NFT'

    if BackgroundJobsType.REFERRAL_COMMISSION == get(background_job, 'type'):
        debug("Run handle_logs NFT MintOrderForDev,MintOrderFromDaapCreator")
        _command = f'python3 scripts/handle_logs.py contract={_contract} from_block={_from_block} abi_path={_dict}/{_abi_path}  event=MintOrderForDev,MintOrderFromDaapCreator handle_path=tasks handle_func=send_task_events event_type={BackgroundJobsType.REFERRAL_COMMISSION} parse_event=1 args_fields=returnMintingOrder dict_fields=returnMintingOrder#tokenId-rarity-cid-nftType'

    if BackgroundJobsType.BOX == get(background_job, 'type'):
        debug("Run handle_logs BOX")
        _command = f'python3 scripts/handle_logs.py contract={_contract} from_block={_from_block} abi_path=abis/katana_box.json  event=SendNft,TokenCreated,OpenBox handle_path=tasks handle_func=send_task_events event_type={BackgroundJobsType.BOX} extra_data=nft_type#BOX'

    if BackgroundJobsType.BOX_REFERRAL_COMMISSION == get(background_job, 'type'):
        debug("Run handle_logs BOX COMMISSION")
        _command = f'python3 scripts/handle_logs.py contract={_contract} from_block={_from_block} abi_path=abis/katana_box.json  event=MintOrderForDev,MintOrderFromDaapCreator handle_path=tasks handle_func=send_task_events event_type={BackgroundJobsType.BOX_REFERRAL_COMMISSION} parse_event=1 args_fields=returnMintingOrder dict_fields=returnMintingOrder#id-index-price-is_opened-owner_by'

    if not _command:
        raise Exception("Not found command")

    config_txt = f"""
    [program:{_program}]
    command={_command}
    directory=/webapps
    autostart=true
    autorestart=false
    redirect_stderr=true
    stdout_logfile=/dev/stdout
    stderr_logfile=/dev/stderr
    stdout_logfile_maxbytes=0
    stderr_logfile_maxbytes=0
    """
    _config_file_path = f"/subprocess/{_bg_id}.conf"
    debug(f"_config_file_path {_config_file_path}")

    with open(_config_file_path, 'w') as f:
        f.write(config_txt)

    subprocess.run(
        ["supervisorctl", "reread"], timeout=10)

    subprocess.run(
        ["supervisorctl", "update"], timeout=10)
    debug(f"run subprocess {_config_file_path}")

    return "Job running"