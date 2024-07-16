

from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

from autogen import oai
from autogen.agentchat.agent import Agent
from autogen.agentchat.assistant_agent import ConversableAgent

system_message = """You are an expert in excel or csv Customer Requirements Analysis.
The user will give you excel or .xlsx to analyze(always a path).
The user will give you analysis INSTRUCTIONS copied twice, at both the beginning and the end.
You will follow these INSTRUCTIONS in analyzing the TEXT, then give the results of your expert analysis in the format requested."""


class DavidRetrieveUserProxyAgent(RetrieveUserProxyAgent):
    """(Experimental) Text Analysis agent, a subclass of ConversableAgent designed to analyze text as instructed."""

    def __init__(
        self,
        name="david-RetrieveChatAgent",  # default set to RetrieveChatAgent
        human_input_mode: Literal["ALWAYS", "NEVER", "TERMINATE"] = "ALWAYS",
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        retrieve_config: Optional[Dict] = None,  # config for the retrieve agent
        **kwargs,
    ):
        super().__init__(
            name=name,
            human_input_mode=human_input_mode,
            is_termination_msg=is_termination_msg,
            retrieve_config=retrieve_config,
            **kwargs,
        )

    def receive(
        self,
        message: Union[Dict, str],
        sender: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False,
    ):
        super().receive(message, sender, request_reply, silent)
        pass
        
    def retrieve_docs(self, problem: str, n_results: int = 20, search_string: str = ""):
        super().retrieve_docs(problem, n_results, search_string) 

