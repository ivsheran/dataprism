from langchain_ollama import ChatOllama
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from core.config_loader import ConfigLoader
from core.chart_tools import ChartTools
from core.data_loader import DataLoader


class VisualizationAgent:
    def __init__(self, config: ConfigLoader, chart_tools: ChartTools, data_loader: DataLoader):
        self.config = config
        self.chart_tools = chart_tools
        self.data_loader = data_loader
        self.history_store = {}

        self.prompt_text = self._load_prompt_template(prompt_path='prompts/visualization_agent_system_prompt.txt')
        self.prompt = self._build_prompt()
        self.llm = self._build_llm()
        self.agent_executor = self._build_agent_executor()
    
    def _load_prompt_template(self, prompt_path):
        """Load the prompt template from a file."""
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt template file '{prompt_path}' not found.")
        
    def _build_prompt(self):
        """Build the prompt template for the agent."""
        return ChatPromptTemplate.from_messages([
            ("system", self.prompt_text),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
            ("placeholder", "{agent_scratchpad}")])
    
    def _build_llm(self):
        """Create ChatOllama from config."""
        return ChatOllama(
            model=self.config.default_model,
            base_url=self.config.ollama_base_url,
            temperature=self.config.temperature
        )
    
    def _build_agent_executor(self):
        """Create an agent executor with the prompt and llm."""
        tools = self.chart_tools.get_tools()
        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=tools,
            prompt=self.prompt
        )
        return AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    def run(self, question: str, session_id: str):
        dataset_summary = self.data_loader.get_summary()

        agent_with_history = RunnableWithMessageHistory(
            runnable=self.agent_executor,
            get_session_history=lambda sid: self.history_store.setdefault(sid, InMemoryChatMessageHistory()),
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        response = agent_with_history.invoke(
            {"input": question, 
             "dataset_summary": dataset_summary}, 
             config ={"configurable": {"session_id": session_id}}
        )

        steps = response.get("intermediate_steps", [])
        chart_path = steps[-1][1] if steps else None 
        return response["output"], chart_path


