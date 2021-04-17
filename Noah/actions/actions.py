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

class QuestionAnsering(Action):
    def name(self) -> Text:
        return "action_cdqa"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        query = tracker.latest_message
        result = json.loads(requests.get(f"http://d972e4ae2d1e.ngrok.io/api?{query}").text)
        print("Read Sapiens")
        dispatcher.utter_message(result['answer'])
        dispatcher.utter_message("Call cdqa api")
        return []

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
        result = json.loads(requests.get(f"http://d972e4ae2d1e.ngrok.io/api?{query}").text)
        print("Read Sapiens")
        dispatcher.utter_message(result['answer'])
        return [{"event": "slot", "name": "read_sapiens", "value": "True"}]