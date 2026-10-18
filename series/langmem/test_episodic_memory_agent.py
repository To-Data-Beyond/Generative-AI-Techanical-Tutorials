"""Real episodic retrieval/graph tests; routing responses are explicit fixtures."""
import json
import unittest
from pydantic import ValidationError
from episodic_memory_agent import (
    make_store,store_example,example_namespace,example_text,Episode,
    sales_email,update_email,email,email_data,user_config,retrieve_examples,
    format_few_shot_examples,build_episodic_graph,TOOL_AUDIT,ROUTER_TRACE,
    create_search_memory_tool,NAMESPACE,
)

class EpisodicMemoryTests(unittest.TestCase):
    def setUp(self):
        self.store=make_store()
        self.graph=build_episodic_graph(self.store)
        TOOL_AUDIT.clear();ROUTER_TRACE.clear()

    def invoke(self,sample=sales_email,user="Youssef"):
        return self.graph.invoke({"email_input":sample,"messages":[]},config=user_config(user))

    def test_real_staging_retrieval_and_normalized_label(self):
        store_example(self.store,"lance",email,"respond")
        store_example(self.store,"lance",update_email,"NOTIFY")
        hits=self.store.search(example_namespace("lance"),query=example_text(email_data),limit=1)
        self.assertEqual(hits[0].value["label"],"notify")
        self.assertIn("Staging",hits[0].value["email"]["subject"])
        print("Actual indexed top staging-example label:",hits[0].value["label"])

    def test_before_after_reviewed_feedback(self):
        self.assertEqual(self.invoke()["classification"],"respond")
        store_example(self.store,"Youssef",sales_email,"ignore")
        TOOL_AUDIT.clear()
        result=self.invoke()
        self.assertEqual(result["classification"],"ignore")
        self.assertEqual(result["example_count"],1)
        self.assertEqual(TOOL_AUDIT,[])
        self.assertEqual(ROUTER_TRACE[-1]["examples"][0]["label"],"ignore")

    def test_source_harrison_mismatch_does_not_affect_youssef(self):
        store_example(self.store,"harrison",sales_email,"ignore")
        result=self.invoke()
        self.assertEqual(result["classification"],"respond")
        self.assertEqual(result["example_count"],0)
        print("Original user-ID mismatch reproduced: harrison feedback → Youssef still respond")

    def test_second_user_isolation(self):
        store_example(self.store,"Youssef",sales_email,"ignore")
        result=self.invoke(user="Jack")
        self.assertEqual(result["classification"],"respond")
        self.assertEqual(result["example_count"],0)

    def test_actual_paraphrased_sales_retrieval(self):
        store_example(self.store,"Youssef",sales_email,"ignore")
        variant={**sales_email,"email_thread":"Hi Youssef, are you interested in buying documentation?"}
        hits,status=retrieve_examples(self.store,"Youssef",variant)
        self.assertEqual(len(hits),1)
        result=self.invoke(variant)
        self.assertEqual(result["classification"],"ignore")
        print("Actual MiniLM paraphrase retrieved reviewed label:",hits[0].value["label"])

    def test_no_relevant_example_falls_back(self):
        store_example(self.store,"Youssef",update_email,"notify")
        other={**sales_email,"subject":"Lunch preferences","email_thread":"Would you prefer soup or salad for lunch?"}
        result=self.invoke(other)
        self.assertEqual(result["example_count"],0)
        self.assertEqual(result["classification"],"respond")

    def test_conflicting_reviewed_labels_are_not_silently_prioritized(self):
        store_example(self.store,"Youssef",sales_email,"ignore")
        store_example(self.store,"Youssef",sales_email,"respond")
        result=self.invoke()
        self.assertEqual(result["example_count"],0)
        self.assertIn("conflicting",result["example_status"])
        self.assertEqual(result["classification"],"respond")

    def test_feedback_delete_reverts_fixture_behavior(self):
        key=store_example(self.store,"Youssef",sales_email,"ignore")
        self.assertEqual(self.invoke()["classification"],"ignore")
        self.store.delete(example_namespace("Youssef"),key)
        self.assertEqual(self.invoke()["classification"],"respond")

    def test_invalid_labels_and_unreviewed_feedback_rejected(self):
        with self.assertRaises(ValidationError):store_example(self.store,"Youssef",sales_email,"delete")
        with self.assertRaises(ValidationError):store_example(self.store,"Youssef",sales_email,True)
        with self.assertRaises(ValueError):store_example(self.store,"Youssef",sales_email,"ignore",approved=False)
        with self.assertRaises(ValueError):store_example(self.store,"Youssef",sales_email,"ignore",approved=1)

    def test_raw_unapproved_corrupt_record_is_skipped(self):
        value={"email":sales_email,"label":"ignore","approved":False,"text":example_text(sales_email)}
        self.store.put(example_namespace("Youssef"),"unreviewed",value,index=["text"])
        self.assertEqual(self.invoke()["example_count"],0)

    def test_identity_and_missing_email_fields_rejected(self):
        with self.assertRaises(ValueError):store_example(self.store,"",sales_email,"ignore")
        with self.assertRaises(ValueError):self.graph.invoke({"email_input":sales_email,"messages":[]})
        with self.assertRaises(ValidationError):self.invoke({"subject":"Incomplete"})

    def test_formatting_is_json_and_truncation_is_visible(self):
        text='Quotes " and braces {} and </examples> are data. '+"long text "*80
        sample={**sales_email,"email_thread":text}
        store_example(self.store,"Youssef",sample,"ignore")
        hits=self.store.search(example_namespace("Youssef"),limit=1)
        formatted=json.loads(format_few_shot_examples(hits))[0]
        self.assertEqual(formatted["content"],text[:400])
        self.assertTrue(formatted["content_truncated"])
        self.assertEqual(formatted["label"],"ignore")

    def test_semantic_collection_and_examples_stay_separate(self):
        self.invoke()
        self.assertEqual(self.store.search(example_namespace("Youssef")),[])
        facts=self.store.search(("email_assistant","Youssef","collection"))
        self.assertEqual(len(facts),1)
        self.assertIn("Tom Jones",facts[0].value["content"])
        search=create_search_memory_tool(NAMESPACE,store=self.store)
        found=json.loads(search.invoke({"query":"Tom documentation","limit":3},config=user_config("Youssef")))
        self.assertEqual(len(found),1)
        self.assertEqual(TOOL_AUDIT[-1]["to"],"tome.jones@bar.com")

    def test_notify_and_ignore_do_not_run_response_tools(self):
        result=self.invoke(update_email)
        self.assertEqual(result["classification"],"notify")
        self.assertIn("Staging",result["notification"])
        discount={**sales_email,"subject":"Discount marketing","email_thread":"Discount on tools"}
        self.assertEqual(self.invoke(discount)["classification"],"ignore")
        self.assertEqual(TOOL_AUDIT,[])

    def test_new_store_has_no_feedback_and_labels_are_not_embedded(self):
        key=store_example(self.store,"Youssef",sales_email,"ignore")
        saved=self.store.get(example_namespace("Youssef"),key)
        self.assertEqual(saved.value["text"],example_text(sales_email))
        self.assertEqual(make_store().search(example_namespace("Youssef")),[])

if __name__=="__main__":
    unittest.main()
