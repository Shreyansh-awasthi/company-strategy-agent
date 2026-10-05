import os
import time
import json
import random
import logging
import warnings
from urllib.parse import urlparse
from typing import TypedDict, Optional, Dict, Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from firecrawl import FirecrawlApp

warnings.filterwarnings("ignore")
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("CompetitorIntel")

llm = ChatGroq(
    model="qwen/qwen3.8-27b", 
    temperature=0.2,
    api_key=os.getenv('GROQ_API_KEY'),
    max_tokens=2000
)

MAX_MARKDOWN_CHARS = 5500
MAX_RETRIES = 4
BASE_DELAY = 5


class AgentState(TypedDict):
    competitor_url: str
    raw_markdown: Optional[str]
    analysis_report: Optional[Dict[str, Any]]
    error: Optional[str]


class StrategyAnalysis(BaseModel):
    pricing_changes: str = Field(description="Updates to tiers, scaling units, billing frequencies or access caps.")
    feature_additions: str = Field(description="Newly added tools, ecosystem tools, engines or workflows.")
    messaging_shift: str = Field(description="Modifications to positioning, value props, structural target audiencing.")
    strategic_intent: str = Field(description="The underlying commercial strategy or target vector.")


def scrape_competitor_node(state: AgentState) -> Dict[str, Any]:
    url = state["competitor_url"].strip()
    if not urlparse(url).scheme:
        url = "https://" + url
        
    logger.info(f"Fetching data from target: {url}")
    try:
        app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
        scrape_result = app.scrape_url(url, formats=["markdown"])
        extracted_markdown = getattr(scrape_result, "markdown", "") if scrape_result else ""

        if not extracted_markdown:
            return {"raw_markdown": None, "error": "Scraping succeeded but returned empty content strings."}

        return {"raw_markdown": extracted_markdown, "error": None}
    except Exception as e:
        return {"raw_markdown": None, "error": f"Scraping interface error: {str(e)}"}


def analyze_data(state: AgentState) -> Dict[str, Any]:
    logger.info("Processing raw data matrices with Groq Qwen infrastructure...")
    if state.get("error") or not state.get("raw_markdown"):
        return {"analysis_report": None, "error": state.get("error") or "Context array missing."}

    trimmed_markdown = state["raw_markdown"][:MAX_MARKDOWN_CHARS]
    structured_llm = llm.with_structured_output(StrategyAnalysis)

    system_prompt = (
        "You are an elite corporate strategy analyst. Review the provided raw markdown "
        "scraped from a competitor's website. Strip out all marketing fluff, adjectives, "
        "and buzzwords. Identify concrete, structural changes or feature offerings."
    )
    user_prompt = f"Target Website Data:\n\n{trimmed_markdown}"

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            validated_report = structured_llm.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ])

            return {"analysis_report": validated_report.model_dump(), "error": None}

        except ValidationError as e:
            last_error = e
            logger.error(f"Schema validation error on operational attempt {attempt}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(BASE_DELAY)
                continue
            break

        except Exception as e:
            last_error = e
            is_rate_limit = "429" in str(e) or "rate_limit_exceeded" in str(e)
            if is_rate_limit and attempt < MAX_RETRIES:
                delay = BASE_DELAY * (2 ** (attempt - 1)) + random.uniform(0, 2)
                logger.warning(f"Rate limit hit. Retrying execution context block in {delay:.1f}s. Error: {e}")
                time.sleep(delay)
                continue
            break

    return {"analysis_report": None, "error": f"Groq gateway pipeline termination: {str(last_error)}"}


workflow = StateGraph(AgentState)
workflow.add_node("scraper", scrape_competitor_node)
workflow.add_node("analyst", analyze_data)
workflow.set_entry_point("scraper")
workflow.add_edge("scraper", "analyst")
workflow.add_edge("analyst", END)

competitor_agent = workflow.compile()


def run_single_url(url: str) -> Dict[str, Any]:
    initial_input = {
        "competitor_url": url,
        "raw_markdown": None,
        "analysis_report": None,
        "error": None,
    }
    final_state = competitor_agent.invoke(initial_input)
    
    if not final_state.get("error"):
        try:
            domain = urlparse(url).netloc.replace(".", "_")
            if not domain:
                domain = "competitor"
            filename = f"intel_{domain}_{time.strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(os.path.dirname(__file__), filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(final_state["analysis_report"], f, indent=4, ensure_ascii=False)
            logger.info(f"Successfully generated structured asset file mapping to disk: {filepath}")
        except Exception as export_error:
            logger.error(f"Asset serialization error frame: {export_error}")
            
    return final_state


if __name__ == "__main__":
    logger.info("Initializing Competitor Intelligence Graph Processing Execution Frame")
    final_state = run_single_url("https://nvidia.com")

    if final_state.get("error"):
        logger.error(f"Workflow execution halted: {final_state['error']}")
    else:
        report = final_state["analysis_report"]
        print("\nSTRATEGIC INTELLIGENCE REPORT:")
        print(f"Pricing: {report['pricing_changes']}\n")
        print(f"Features: {report['feature_additions']}\n")
        print(f"Messaging: {report['messaging_shift']}\n")
        print(f"Expected Strategic Intent: {report['strategic_intent']}\n")
