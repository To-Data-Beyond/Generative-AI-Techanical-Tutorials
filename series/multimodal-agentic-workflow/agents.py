from crewai import Agent

def router_agent(llm):
    return Agent(role='Task Router', goal='Select exactly one supported capability.',
        backstory='You classify requests; you never perform the requested action.',
        llm=llm, tools=[], allow_delegation=False, verbose=False, max_iter=2,
        max_retry_limit=0)

def executor_agent(llm, executor_tool):
    return Agent(role='Task Executor', goal='Call execute_selected_tool exactly once.',
        backstory='The controller has already fixed the route and original request. '
                  'Call your tool with no arguments. Never invent an artifact or result.',
        llm=llm, tools=[executor_tool], allow_delegation=False, verbose=False,
        max_iter=2, max_retry_limit=0)
