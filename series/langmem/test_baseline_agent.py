"""Real framework tests with explicitly scripted model responses; no network calls."""
import unittest
import json
import httpx
from pydantic import ValidationError
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from baseline_agent import (
    EmailInput, Router, OfflineFixtureModel, normalize_email, email, spam_email,
    tools, TOOL_AUDIT, write_email, schedule_meeting, check_calendar_availability,
    make_models, build_email_agent, create_prompt,
)

class BaselineTests(unittest.TestCase):
    def setUp(self):
        TOOL_AUDIT.clear()
        router, model = make_models(hosted=False)
        self.graph = build_email_agent(router, create_agent(model, tools=tools, system_prompt=create_prompt()))

    def test_input_aliases_and_missing_fields(self):
        data = normalize_email(email)
        self.assertEqual(data["author"], email["from"])
        self.assertEqual(normalize_email(data), data)
        with self.assertRaises(ValidationError): normalize_email({"subject":"Incomplete"})
        with self.assertRaises(ValidationError): normalize_email({**email,"unexpected":"bad"})

    def test_invalid_classification_rejected(self):
        with self.assertRaises(ValidationError): Router(reasoning="fixture", classification="delete")
        bad_router = RunnableLambda(lambda _: {"reasoning":"fixture", "classification":"delete"})
        broken = build_email_agent(bad_router)
        with self.assertRaises(ValidationError): broken.invoke({"email_input":email, "messages":[]})
        self.assertEqual(TOOL_AUDIT, [])

    def test_ignore_does_not_call_response_tools(self):
        result = self.graph.invoke({"email_input":spam_email,"messages":[]})
        self.assertEqual(result["classification"], "ignore")
        self.assertEqual(result.get("messages",[]), [])
        self.assertEqual(TOOL_AUDIT, [])

    def test_notify_exposes_notification_without_tool_calls(self):
        notice={**spam_email,"subject":"Build system notification", "email_thread":"Build system completed successfully."}
        result=self.graph.invoke({"email_input":notice,"messages":[]})
        self.assertEqual(result["classification"],"notify")
        self.assertIn("Build system",result["notification"])
        self.assertEqual(TOOL_AUDIT,[])

    def test_respond_executes_real_tool_and_correct_recipient(self):
        result=self.graph.invoke({"email_input":email,"messages":[]})
        self.assertEqual(result["classification"],"respond")
        self.assertEqual([x["tool"] for x in TOOL_AUDIT],["write_email"])
        self.assertEqual(TOOL_AUDIT[0]["to"],"Oliver.Jack@ToDataBeyond.com")
        self.assertTrue(any(isinstance(m,ToolMessage) for m in result["messages"]))
        self.assertIn("not sent",result["messages"][-1].content)

    def test_stateless_second_invocation(self):
        self.graph.invoke({"email_input":email,"messages":[]})
        TOOL_AUDIT.clear()
        result=self.graph.invoke({"email_input":spam_email,"messages":[]})
        self.assertEqual(result["messages"],[])
        self.assertEqual(TOOL_AUDIT,[])

    def test_calendar_tool_and_validation(self):
        self.assertIn("9:00 AM",check_calendar_availability.invoke({"day":"Tuesday"}))
        proposal={"attendees":["oliver@example.com"],"subject":"Project sync","duration_minutes":30,"preferred_day":"Tuesday"}
        self.assertIn("not booked",schedule_meeting.invoke(proposal))
        with self.assertRaises(ValidationError): schedule_meeting.invoke({**proposal,"duration_minutes":0})
        with self.assertRaises(ValueError): schedule_meeting.invoke({**proposal,"attendees":[]})
        with self.assertRaises(ValueError): check_calendar_availability.invoke({"day":""})
        with self.assertRaises(ValueError): write_email.invoke({"to":"invalid","subject":"Hi","content":"Test"})

    def test_actual_agent_calendar_and_meeting_tool_loop(self):
        class MeetingFixture(OfflineFixtureModel):
            def _generate(self,messages,stop=None,run_manager=None,**kwargs):
                observed=[m.name for m in messages if isinstance(m,ToolMessage)]
                if not observed:
                    msg=AIMessage(content="",tool_calls=[{"name":"check_calendar_availability","args":{"day":"Tuesday"},"id":"calendar-test"}])
                elif "schedule_meeting" not in observed:
                    msg=AIMessage(content="",tool_calls=[{"name":"schedule_meeting","args":{"attendees":["oliver@example.com"],"subject":"Project sync","duration_minutes":30,"preferred_day":"Tuesday"},"id":"meeting-test"}])
                else: msg=AIMessage(content="Sandbox proposal complete, not booked.")
                return ChatResult(generations=[ChatGeneration(message=msg)])
        main=create_agent(MeetingFixture(purpose="agent"),tools=tools,system_prompt=create_prompt())
        main.invoke({"messages":[{"role":"user","content":"Propose a Tuesday meeting."}]},{"recursion_limit":20})
        self.assertEqual([x["tool"] for x in TOOL_AUDIT],["check_calendar_availability","schedule_meeting"])

    def test_actual_openai_sdk_transport_without_network(self):
        requests=[]
        def transport(request):
            payload=json.loads(request.content);requests.append(payload)
            names=[t["function"]["name"] for t in payload.get("tools",[])]
            if "Router" in names:
                call={"id":"mock-router","type":"function","function":{"name":"Router","arguments":json.dumps({"reasoning":"Explicit mocked HTTP response","classification":"respond"})}}
                msg={"role":"assistant","content":None,"tool_calls":[call]}
            elif payload["messages"][-1]["role"]=="tool":msg={"role":"assistant","content":"Sandbox draft recorded, not sent."}
            else:
                call={"id":"mock-draft","type":"function","function":{"name":"write_email","arguments":json.dumps({"to":"Oliver.Jack@ToDataBeyond.com","subject":"Re: API documentation","content":"Thanks; I will verify before confirming."})}}
                msg={"role":"assistant","content":None,"tool_calls":[call]}
            return httpx.Response(200,json={"id":"offline-fixture","object":"chat.completion","created":0,"model":"fixture-model","choices":[{"index":0,"message":msg,"finish_reason":"tool_calls" if "tool_calls" in msg else "stop"}],"usage":{"prompt_tokens":0,"completion_tokens":0,"total_tokens":0}})
        with httpx.Client(transport=httpx.MockTransport(transport)) as client:
            model=ChatOpenAI(model="fixture-model",api_key="offline-fixture-not-a-secret",http_client=client,max_retries=0)
            router=model.with_structured_output(Router,method="function_calling")
            graph=build_email_agent(router,create_agent(model,tools=tools,system_prompt=create_prompt()))
            result=graph.invoke({"email_input":email,"messages":[]},{"recursion_limit":20})
        self.assertEqual(len(requests),3)
        self.assertEqual(result["classification"],"respond")
        self.assertEqual(TOOL_AUDIT[0]["to"],"Oliver.Jack@ToDataBeyond.com")

if __name__=="__main__":
    unittest.main()
