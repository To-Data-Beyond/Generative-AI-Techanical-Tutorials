"""Actual LangMem/store/vector execution with explicitly scripted agent decisions."""
import json
import unittest
from pydantic import ValidationError
from semantic_memory_agent import (
    make_store, build_response_agent, build_email_graph, MemoryFixtureModel,
    NAMESPACE, user_config, require_user, create_manage_memory_tool,
    create_search_memory_tool, ToolMessage, TOOL_AUDIT, email_input, followup_email,
    normalize_email, EMBEDDING_DIMS, embed_texts,
)

class SemanticMemoryTests(unittest.TestCase):
    def setUp(self):
        self.store=make_store()
        self.agent=build_response_agent(self.store,MemoryFixtureModel(purpose="agent"))
        self.manage=create_manage_memory_tool(NAMESPACE,store=self.store)
        self.search=create_search_memory_tool(NAMESPACE,store=self.store)
        self.config=user_config("user-a")
        self.namespace=("email_assistant","user-a","collection")
        TOOL_AUDIT.clear()

    def invoke(self,text,config=None):
        return self.agent.invoke({"messages":[{"role":"user","content":text}]},config=config or self.config)

    def test_actual_embeddings_and_paraphrase_ranking(self):
        vectors=embed_texts(["A meeting on Tuesday","An appointment on Tuesday"])
        self.assertEqual(len(vectors[0]),EMBEDDING_DIMS)
        self.assertNotEqual(vectors[0],vectors[1])
        for key,fact in [("schedule","The user prefers meetings on Tuesday afternoons."),("family","Jim is Youssef's friend."),("api","Oliver asked about missing authentication endpoint documentation.")]:
            self.store.put(self.namespace,key,{"content":fact})
        hits=json.loads(self.search.invoke({"query":"Preferred weekday for appointments","limit":3},config=self.config))
        self.assertEqual(hits[0]["key"],"schedule")
        self.assertTrue(all(-1.01<=x["score"]<=1.01 for x in hits))
        print("Actual MiniLM paraphrase top match:",hits[0]["value"]["content"])

    def test_create_and_recall_across_independent_invocations(self):
        first=self.invoke("Jim is my friend")
        second=self.invoke("who is jim?")
        self.assertEqual([m.name for m in first["messages"] if isinstance(m,ToolMessage)],["manage_memory"])
        self.assertEqual([m.name for m in second["messages"] if isinstance(m,ToolMessage)],["search_memory"])
        self.assertIn("Jim is Youssef's friend",second["messages"][-1].content)
        self.assertEqual(len([m for m in second["messages"] if m.type=="human"]),1)

    def test_user_namespace_isolation(self):
        self.invoke("Jim is my friend")
        other=self.invoke("who is jim?",user_config("user-b"))
        self.assertIn("No matching notes",other["messages"][-1].content)
        self.assertEqual(self.store.search(("email_assistant","user-b","collection")),[])

    def test_update_real_memory_in_place(self):
        self.manage.invoke({"content":"Jim is a friend"},config=self.config)
        key=self.store.search(self.namespace)[0].key
        self.manage.invoke({"id":key,"action":"update","content":"Jim is Youssef's brother"},config=self.config)
        self.assertEqual(len(self.store.search(self.namespace)),1)
        self.assertEqual(self.store.get(self.namespace,key).value["content"],"Jim is Youssef's brother")

    def test_delete_removes_value_and_search_result(self):
        self.manage.invoke({"content":"Jim is a friend"},config=self.config)
        key=self.store.search(self.namespace)[0].key
        self.manage.invoke({"id":key,"action":"delete"},config=self.config)
        self.assertIsNone(self.store.get(self.namespace,key))
        self.assertEqual(json.loads(self.search.invoke({"query":"Jim","limit":3},config=self.config)),[])

    def test_wrong_namespace_cannot_delete_other_users_fact(self):
        self.manage.invoke({"content":"Private demo fact for user A"},config=self.config)
        key=self.store.search(self.namespace)[0].key
        self.manage.invoke({"id":key,"action":"delete"},config=user_config("user-b"))
        self.assertIsNotNone(self.store.get(self.namespace,key))

    def test_invalid_memory_operations_fail(self):
        with self.assertRaises(ValueError):self.manage.invoke({"action":"update","content":"No ID"},config=self.config)
        with self.assertRaises(ValueError):self.manage.invoke({"action":"delete"},config=self.config)
        with self.assertRaises(ValidationError):self.manage.invoke({"action":"erase"},config=self.config)
        with self.assertRaises(ValidationError):self.manage.invoke({"action":"update","id":"not-a-uuid","content":"invalid"},config=self.config)

    def test_explicit_identity_required(self):
        for bad in [None,"",123]:
            with self.assertRaises(ValueError):user_config(bad)
        with self.assertRaises(ValueError):require_user({})
        graph=build_email_graph(self.store,MemoryFixtureModel(purpose="agent"))
        with self.assertRaises(ValueError):graph.invoke({"email_input":email_input,"messages":[]})
        self.assertEqual(self.store.search(self.namespace),[])

    def test_new_store_does_not_survive_restart(self):
        self.invoke("Jim is my friend")
        fresh=make_store()
        self.assertEqual(fresh.search(self.namespace),[])
        self.assertEqual(len(self.store.search(self.namespace)),1)

    def test_repeated_creates_are_not_automatic_deduplication(self):
        self.manage.invoke({"content":"Jim is a friend"},config=self.config)
        self.manage.invoke({"content":"Jim is a friend"},config=self.config)
        self.assertEqual(len(self.store.search(self.namespace)),2)

    def test_complete_email_memory_and_followup(self):
        graph=build_email_graph(self.store,MemoryFixtureModel(purpose="agent"))
        initial=graph.invoke({"email_input":email_input,"messages":[]},config=self.config)
        followup=graph.invoke({"email_input":followup_email,"messages":[]},config=self.config)
        self.assertEqual(initial["classification"],"respond")
        self.assertEqual([m.name for m in initial["messages"] if isinstance(m,ToolMessage)],["write_email","manage_memory"])
        self.assertEqual([m.name for m in followup["messages"] if isinstance(m,ToolMessage)],["search_memory","write_email"])
        self.assertEqual(TOOL_AUDIT[-1]["to"],"Oliver.Jack@ToDataBeyond.com")
        self.assertIn("authentication API documentation",TOOL_AUDIT[-1]["content"])
        self.assertIn("no verified status",TOOL_AUDIT[-1]["content"])
        self.assertEqual(len([m for m in followup["messages"] if m.type=="human"]),1)
        print("Actual graph tool sequences: write_email → manage_memory; search_memory → write_email")

    def test_followup_without_memory_requests_clarification(self):
        graph=build_email_graph(self.store,MemoryFixtureModel(purpose="agent"))
        graph.invoke({"email_input":followup_email,"messages":[]},config=self.config)
        self.assertEqual(TOOL_AUDIT[-1]["content"],"Could you clarify your previous request?")

    def test_ignore_and_notify_skip_memory_and_email_tools(self):
        graph=build_email_graph(self.store,MemoryFixtureModel(purpose="agent"))
        for subject,label in [("Discount on tools","ignore"),("Build system notification","notify")]:
            sample={**email_input,"subject":subject,"email_thread":subject}
            output=graph.invoke({"email_input":sample,"messages":[]},config=self.config)
            self.assertEqual(output["classification"],label)
            if label=="notify":self.assertIn(subject,output["notification"])
        self.assertEqual(TOOL_AUDIT,[])
        self.assertEqual(self.store.search(self.namespace),[])

if __name__=="__main__":
    unittest.main()
