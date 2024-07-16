
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.agentchat.conversable_agent import ConversableAgent
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

from autogen import oai
from autogen.agentchat.agent import Agent
from autogen.agentchat.assistant_agent import ConversableAgent

system_message = """You are an expert in excel or csv Customer Requirements Analysis.
The user will give you excel or .xlsx to analyze(always a path).
The user will give you analysis INSTRUCTIONS copied twice, at both the beginning and the end.
You will follow these INSTRUCTIONS in analyzing the TEXT, then give the results of your expert analysis in the format requested."""


class DavidRetrieveAsistantAgent(RetrieveAssistantAgent):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.replace_reply_func(RetrieveAssistantAgent._generate_retrieve_assistant_reply, DavidRetrieveAsistantAgent._generate_retrieve_assistant_reply)


    def _generate_retrieve_assistant_reply(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[Any] = None,
    ) -> Tuple[bool, Union[str, Dict, None]]:
        if config is None:
            config = self
        if messages is None:
            messages = self._oai_messages[sender]
        if len(messages) <= 1:
             return False, None
        message = messages[-1]
        if "exitcode: 0 (execution succeeded)" in message.get("content", ""):
            # Terminate the conversation when the code execution succeeds. Although sometimes even when the
            # code execution succeeds, the task is not solved, but it's hard to tell. If the human_input_mode
            # of RetrieveUserProxyAgent is "TERMINATE" or "ALWAYS", user can still continue the conversation.
            return True, "TERMINATE"
        elif (
            "UPDATE CONTEXT" in message.get("content", "")[-20:].upper()
            or "UPDATE CONTEXT" in message.get("content", "")[:20].upper()
        ):
            return True, "UPDATE CONTEXT"
        else:
            return False, None
