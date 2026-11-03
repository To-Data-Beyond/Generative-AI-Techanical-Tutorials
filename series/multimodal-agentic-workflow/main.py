from config import make_llm
from crewai import Crew, Process
from agents import router_agent, executor_agent
from agentic_tools import ExecutionState, TaskExecutorTool
from helper_tools import Helpers
from tasks import router_task, executor_task

def run_workflow(question, image_path='', *, llm=None, helpers=None):
    if not isinstance(question, str) or not question.strip() or len(question) > 400:
        raise ValueError('Provide a request of 1–400 characters.')
    state = ExecutionState(question, str(image_path))
    llm = llm or make_llm()
    tool = TaskExecutorTool(state, helpers or Helpers())
    router, executor = router_agent(llm), executor_agent(llm, tool)
    route_task = router_task(router, state)
    execute_task = executor_task(executor, route_task)
    Crew(agents=[router, executor], tasks=[route_task, execute_task],
         process=Process.sequential, memory=False, cache=False, verbose=False,
         tracing=False).kickoff(inputs={'question': question, 'has_image': bool(image_path)})
    if state.error:
        raise RuntimeError('The selected helper failed; no successful result is available.') from state.error
    if not state.attempted or state.result is None:
        raise RuntimeError('The executor did not produce a real helper result.')
    return state.result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('question')
    parser.add_argument('--image', default='')
    args = parser.parse_args()
    print(run_workflow(args.question, args.image).model_dump_json(indent=2))
