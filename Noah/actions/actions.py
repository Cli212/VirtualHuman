# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import requests
import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []



URL="http://ca4ad9a68498.ngrok.io/api"

class QuestionAnsering(Action):
    def name(self) -> Text:
        return "action_cdqa"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        try:
            query = tracker.latest_message
            result = json.loads(requests.get(f"{URL}?query={query}").text)
            last_paragraph = result['paragraph']
            score = result['score']
            title = result['title']
            print("Read Sapiens")
            dispatcher.utter_message(result['answer'])
            return [{"event": "slot", "name": "last_paragraph", "value": last_paragraph}]
        except:
            dispatcher.utter_message("Error occurs when call the api")
            return []
        # dispatcher.utter_message("Call cdqa api")



class HaveReadSapiens(Action):
    def name(self) -> Text:
        return "action_read_sapiens"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        query = tracker.latest_message
        result = json.loads(requests.get(f"{URL}?query={query}").text)
        print("Read Sapiens")
        dispatcher.utter_message(result['answer'])
        return [{"event": "slot", "name": "read_sapiens", "value": "True"}]


class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="my_custom_fallback_template")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]