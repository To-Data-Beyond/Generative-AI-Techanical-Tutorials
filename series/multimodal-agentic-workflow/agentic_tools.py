"""Validate a route, then execute once using controller-owned request state."""
from dataclasses import dataclass
from typing import Literal
from crewai.tools import BaseTool
from pydantic import BaseModel, ConfigDict, PrivateAttr
from helper_tools import Helpers, ToolResult, image_bytes

class Route(BaseModel):
    model_config = ConfigDict(extra='forbid')
    tool: Literal['text2image', 'text2speech', 'image2text', 'web_search', 'unsupported']

class RouteInput(BaseModel):
    route_json: str

class EmptyInput(BaseModel):
    model_config = ConfigDict(extra='forbid')

class RouterTool(BaseTool):
    name: str = 'validate_route'
    description: str = 'Validate a structured route without running any helper.'
    args_schema: type[BaseModel] = RouteInput

    def _run(self, route_json: str) -> str:
        route = Route.model_validate_json(route_json)
        if route.tool == 'unsupported':
            raise ValueError('Request is outside the four supported capabilities.')
        return route.model_dump_json()

@dataclass
class ExecutionState:
    question: str
    image_path: str = ''
    route: Route | None = None
    attempted: bool = False
    result: ToolResult | None = None
    error: Exception | None = None

class TaskExecutorTool(BaseTool):
    name: str = 'execute_selected_tool'
    description: str = 'Execute the already validated route exactly once. No arguments.'
    args_schema: type[BaseModel] = EmptyInput
    result_as_answer: bool = True
    _state: ExecutionState = PrivateAttr()
    _helpers: Helpers = PrivateAttr()

    def __init__(self, state, helpers):
        super().__init__()
        self._state, self._helpers = state, helpers

    def _run(self) -> str:
        s = self._state
        if s.attempted or s.route is None:
            raise RuntimeError('Execution is missing a route or was already attempted.')
        s.attempted = True
        try:
            s.result = self._helpers.execute(s.route.tool, s.question, s.image_path)
            if s.result.tool != s.route.tool:
                raise RuntimeError('Helper returned the wrong tool identity.')
            return s.result.model_dump_json()
        except Exception as exc:
            s.result = None
            s.error = exc
            # Do not expose provider credentials, response bodies or user input.
            return '{"ok":false,"error":"Selected tool failed."}'

def accept_route(output, state):
    route_json = output.pydantic.model_dump_json() if output.pydantic else output.raw
    route = Route.model_validate_json(RouterTool()._run(route_json))
    if route.tool == 'image2text':
        image_bytes(state.image_path)
    state.route = route
