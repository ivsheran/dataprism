from langchain_ollama import ChatOllama
from langchain.agents import create_agent
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
        return create_agent(
            model=self.llm,
            tools=tools,
            system_prompt = self.prompt_text
        )
    
    def run(self, question: str, session_id: str):
        print(f"\n=== Session: {session_id} ===")
        print(f"History length: {len(self.history_store.get(session_id, []))}")
        print(f"History: {self.history_store.get(session_id, [])}")

        dataset_summary = self.data_loader.get_summary()
        print(f"\n=== Dataset Summary ===\n{dataset_summary}\n=== End Summary ===")
        
        system_with_data = self.prompt_text.replace("{dataset_summary}", dataset_summary)

        self.agent_executor = create_agent(
            model=self.llm,
            tools=self.chart_tools.get_tools(),
            system_prompt=system_with_data
            )

        if session_id not in self.history_store:
            self.history_store[session_id] = []
            
        last_tool_result = self.history_store.get(f"{session_id}_last_tool_result")
        print(f"DEBUG: last_tool_result being injected = {last_tool_result}")
        if last_tool_result:
            question_with_context = (
                 f"(Reminder: this exact data was already computed in a previous step "
                 f"and should be reused if relevant, without calling any tool:\n{last_tool_result}\n)\n\n"
                 f"{question}")
        else:
            question_with_context = question

        self.history_store[session_id].append({"role": "user", "content": question_with_context})

        inputs = {"messages": self.history_store[session_id]}
        result = self.agent_executor.invoke(inputs)

        messages = result["messages"]
        for msg in messages:
            print(f"Message type: {type(msg).__name__}, content: {msg.content[:100] if msg.content else 'None'}")
        response = messages[-1].content

        self.history_store[session_id].append({"role": "assistant", "content": response})
        
        chart_path = None
        for msg in messages:
            if hasattr(msg, 'content') and msg.content:
                content = msg.content

                if isinstance(content, str) and content.startswith(("Chart saved to ", "Aggregated data:")):
                    self.history_store[f"{session_id}_last_tool_result"] = content

                if isinstance(content, str) and content.startswith("Chart saved to "): 
                    chart_path = content.split("Chart saved to ", 1)[1].splitlines()[0].strip()

        last_chart = self.history_store.get(f"{session_id}_last_chart")
        print(f"DEBUG: chart_path={chart_path}, last_chart={last_chart}")
        if chart_path == last_chart:
            chart_path = None
        else:
            if chart_path:
                self.history_store[f"{session_id}_last_chart"] = chart_path
            
        return response, chart_path
    