import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests


class Layer3Task(object):

    def __init__(
        self, 
        id: int,
        title: str,
        taskType: str,
        rewardType: str,
        missionDoc: Dict[str, Any],
        createdAt: str,
        expirationDate: str,
        numberOfWinners: int,
        numberOfSubTasks: int = 1,
        xp: Optional[str] = None,
        namespace: Optional[str] = None,
        **kwargs) -> None:
        self.id = id
        self.title = title
        self.task_type = taskType
        self.reward_type = rewardType

        self.infos = []
        for _content in missionDoc.get("content", {}):
            for text_item in _content.get("content", []):
                text = text_item.get("text")
                text_type = text_item.get("type")
                text_marks = [_item.get("type", None) for _item in text_item.get("marks", [])]

                self.infos.append({"text": text, "type": text_type, "marks": text_marks})

        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.created_at = datetime.strptime(createdAt, date_format) if createdAt is not None else None
        self.expiration_date = datetime.strptime(expirationDate, date_format) if expirationDate is not None else None

        self.number_of_winners = numberOfWinners
        self.number_of_subtasks = numberOfSubTasks
        self.xp = xp
        self.namespace = namespace

        self.url = f"https://beta.layer3.xyz/quests/{namespace}" if namespace is not None else None

    def to_string(self, markdown: bool = True) -> str:
        template = f"**{self.title}**" if markdown else self.title
        if self.url is not None:
            template += f"\nURL: {self.url}"
        template += f"\n\nCreated at:\t{self.created_at}"
        template += f"\nExpiration Date:\t{self.expiration_date}"

        info = re.sub(r" +", " ", " ".join([_t["text"] for _t in self.infos]))
        template += f"\n\n{info}"
        return template


class Layer3API():

    def __init__(self) -> None:
        self.base_url = f"https://beta.layer3.xyz/api/"

    def get_tasks(
        self, 
        include_featured: bool = False, 
        include_claimed: bool = False, 
        include_expired: bool = False,
    ) -> List[Layer3Task]:
        api_url = os.path.join(self.base_url, "trpc/task.getTasks")
        params = {
            "input": json.dumps({
                "json": {
                    "taskType": ["BOUNTY","QUEST"],
                    "onlyUnavailable": None,
                    "onlyClaimed": None,
                    "onlyInProgressQuests": None,
                    "includeFeatured": include_featured,
                    "includeClaimed": include_claimed,
                    "includeExpired": include_expired,
                    "cursor": None},
                "meta": {
                    "values": {
                        "onlyUnavailable": ["undefined"],
                        "onlyClaimed":["undefined"],
                        "onlyInProgressQuests": ["undefined"],
                        "cursor": ["undefined"]
                    }
                }
            })
        }

        response = requests.get(api_url, params=params)

        if response.status_code != 200:
            raise ConnectionError(response.status_code, response.text)

        item = response.json()
        tasks = item.get("result", {}).get("data", {}).get("json", {}).get("items", [])

        tasks = [
            Layer3Task(**_task)
            for _task in tasks
        ]

        return tasks
